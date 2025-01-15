from rest_framework import serializers
from .models import User, Loan, Payment  # Import the models

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['aadhar_id', 'name', 'email', 'annual_income']

class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['loan_type', 'loan_amount', 'interest_rate', 'term_period', 'disbursement_date']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount']