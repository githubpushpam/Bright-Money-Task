from django.db import models
import uuid
from decimal import Decimal
from django.utils import timezone

class User(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aadhar_id = models.CharField(max_length=12, unique=True, null=True, blank=True)  # Made optional
    name = models.CharField(max_length=100, default='Default Name')
    email = models.EmailField(unique=True, default='default@example.com')
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    credit_score = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.name} - {self.aadhar_id}"

class Loan(models.Model):
    LOAN_TYPES = [
        ('CREDIT_CARD', 'Credit Card Loan'),
    ]
    
    LOAN_STATUS = [
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES, default='CREDIT_CARD')
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    term_period = models.IntegerField(default=12)
    disbursement_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=LOAN_STATUS, default='ACTIVE')
    principal_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"Loan-{self.id} - {self.user.name}"

class EMI(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='emis')
    due_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    principal_component = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_component = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['due_date']

class Bill(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='bills')
    billing_date = models.DateField(default=timezone.now)
    due_date = models.DateField(default=timezone.now)
    min_due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_accrued = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['billing_date']

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)