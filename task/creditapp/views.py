from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .tasks import calculate_credit_score
from decimal import Decimal
from datetime import timedelta
from .serializers import UserRegistrationSerializer,LoanApplicationSerializer,PaymentSerializer
from .models import User,Loan,Bill,Decimal,EMI,Payment
from django.utils import timezone

class UserRegistrationView(viewsets.ViewSet):
    @transaction.atomic
    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        
        # Trigger async credit score calculation
        calculate_credit_score.delay(str(user.unique_id))
        
        return Response({
            'error': None,
            'unique_user_id': user.unique_id
        }, status=status.HTTP_200_OK)

class LoanApplicationView(viewsets.ViewSet):
    @transaction.atomic
    def create(self, request):
        try:
            user = User.objects.get(unique_id=request.data.get('unique_user_id'))
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate credit score and income
        if not user.credit_score or user.credit_score < 450:
            return Response({'error': 'Credit score too low'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.annual_income < Decimal('150000'):
            return Response({'error': 'Annual income too low'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LoanApplicationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        loan_amount = Decimal(request.data.get('loan_amount'))
        if loan_amount > 5000:
            return Response({'error': 'Loan amount exceeds maximum limit'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate EMIs and validate
        monthly_income = user.annual_income / 12
        max_emi = monthly_income * Decimal('0.2')
        
        loan = serializer.save(user=user, principal_balance=loan_amount)
        
        # Generate EMI schedule
        emis = self.generate_emi_schedule(loan)
        
        if any(emi['amount'] > max_emi for emi in emis):
            loan.delete()
            return Response({'error': 'EMI exceeds 20% of monthly income'}, status=status.HTTP_400_BAD_REQUEST)

        # Create EMI records
        EMI.objects.bulk_create([
            EMI(
                loan=loan,
                due_date=emi['date'],
                amount=emi['amount'],
                principal_component=emi['principal'],
                interest_component=emi['interest']
            ) for emi in emis
        ])

        return Response({
            'error': None,
            'loan_id': loan.id,
            'due_dates': [{'date': emi['date'], 'amount_due': emi['amount']} for emi in emis]
        }, status=status.HTTP_200_OK)

    def generate_emi_schedule(self, loan):
        # EMI calculation logic here
        # This is a simplified version - you'll need to implement the full logic
        principal = loan.loan_amount
        rate = loan.interest_rate / 12 / 100  # Monthly rate
        tenure = loan.term_period
        
        emi_amount = principal * rate * (1 + rate)*tenure / ((1 + rate)*tenure - 1)
        
        emis = []
        current_date = loan.disbursement_date
        
        for month in range(tenure):
            interest = principal * rate
            principal_component = emi_amount - interest
            
            if month == tenure - 1:  # Last EMI
                emi_amount = principal + interest  # Adjust for any rounding differences
            
            emis.append({
                'date': current_date + timedelta(days=30 * (month + 1)),
                'amount': emi_amount,
                'principal': principal_component,
                'interest': interest
            })
            
            principal -= principal_component
        
        return emis

@api_view(['POST'])
@transaction.atomic
def make_payment(request):
    try:
        loan = Loan.objects.get(id=request.data.get('loan_id'))
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PaymentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    amount = Decimal(request.data.get('amount'))
    
    # Get unpaid EMIs
    unpaid_emis = loan.emis.filter(is_paid=False).order_by('due_date')
    
    if not unpaid_emis.exists():
        return Response({'error': 'No pending EMIs'}, status=status.HTTP_400_BAD_REQUEST)
    
    current_emi = unpaid_emis.first()
    
    if amount < current_emi.amount:
        return Response({'error': 'Payment amount less than EMI amount'}, status=status.HTTP_400_BAD_REQUEST)
    
    payment = Payment.objects.create(
        loan=loan,
        amount=amount,
        payment_date=timezone.now().date()
    )
    
    current_emi.is_paid = True
    current_emi.save()
    
    # Update loan principal balance
    loan.principal_balance -= current_emi.principal_component
    loan.save()
    
    if loan.principal_balance <= 0:
        loan.status = 'CLOSED'
        loan.save()

    return Response({'error': None}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_statement(request):
    try:
        loan = Loan.objects.get(id=request.GET.get('loan_id'))
    except Loan.DoesNotExist:
        return Response({'error': 'Loan not found'}, status=status.HTTP_400_BAD_REQUEST)

    if loan.status == 'CLOSED':
        return Response({'error': 'Loan is closed'}, status=status.HTTP_400_BAD_REQUEST)

    # Get past transactions
    past_transactions = []
    for payment in loan.payments.all():
        past_transactions.append({
            'date': payment.payment_date,
            'principal': payment.amount,
            'interest': 0,  # Calculate actual interest
            'amount_paid': payment.amount
        })

    # Get upcoming transactions
    upcoming_transactions = []
    for emi in loan.emis.filter(is_paid=False):
        upcoming_transactions.append({
            'date': emi.due_date,
            'amount_due': emi.amount
        })

    return Response({
        'error': None,
        'past_transactions': past_transactions,
        'upcoming_transactions': upcoming_transactions
    }, status=status.HTTP_200_OK)