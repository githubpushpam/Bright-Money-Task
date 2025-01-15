from celery import shared_task
import pandas as pd
from decimal import Decimal
from .models import User

@shared_task
def calculate_credit_score(user_id):
    user = User.objects.get(unique_id=user_id)
    
    # Read CSV file
    df = pd.read_csv('transactions.csv')
    
    # Filter transactions for the user
    user_transactions = df[df['AADHAR_ID'] == user.aadhar_id]
    
    # Calculate total balance
    credits = user_transactions[user_transactions['Transaction_type'] == 'CREDIT']['Amount'].sum()
    debits = user_transactions[user_transactions['Transaction_type'] == 'DEBIT']['Amount'].sum()
    balance = credits - debits
    
    # Calculate credit score
    if balance >= 1000000:
        credit_score = 900
    elif balance <= 10000:
        credit_score = 300
    else:
        # Calculate intermediate score
        excess_balance = balance - 10000
        additional_points = (excess_balance / 15000) * 10
        credit_score = min(900, max(300, 300 + int(additional_points)))
    
    user.credit_score = credit_score
    user.save()