Loan Management System
This project implements a Loan Management System with features such as user registration, loan application, EMI calculation, payment handling, and credit score management. The system is built using Django and Django REST Framework (DRF).

Features

User Registration:

Users can register with their Aadhar ID, name, email, and annual income.

Upon successful registration, the system calculates the user's credit score asynchronously.



Loan Application:

Users can apply for a loan by specifying the loan type, amount, interest rate, and term period.

The system validates the user's credit score and annual income before approving the loan.

The system calculates the EMI schedule and ensures it does not exceed 20% of the user's monthly income.



Payment Processing:

Users can make payments for their EMIs.

Payments are validated against the current outstanding EMI.



Loan Statement:

Users can view their loan statements, including past payments and upcoming EMIs.



Async Tasks:

Credit score calculation is performed asynchronously using Celery.



Tech Stack

Backend: Django, Django REST Framework

Database: SQLite 

Task Queue: Celery (with Redis as the message broker)

Python Libraries: Decimal, Django Transaction Management

Database Models

UserInformation:
name: name of the user
email: email of the user
annual_income: annual_income of the user
aadhar_id: aadhar_id of the user which is a unique field
credit_score: credit score of the user
user_uuid: unique uuid generated for each registered user

UserTransactionInformation:
aadhar_id: aadhar_id of the user
registration_date: transaction registration date
amount: transaction amount
transaction_type: type of transaction either DEBIT or CREDIT
credit_score: credit score of the user

LoanInfo:
loan_id: unique uuid generated to identify the loan
user_uuid: uuid field which is a foreign key to UserInformation's user_uuid field
loan_type: type of loan applied
loan_amount: loan amount in rupees
annual_interest_rate: annual rate of interest for the loan applied
term_period: term period of repayment of the loan in months
disbursement_date: date of disbursement of loan

EMIDetails:
loan_id: loan_id of the loan for which EMIs are generated which is a foreign key to LoanInfo loan_id field 
amount_due: EMI due each month in rupees
amount_paid: EMI paid each month in rupees
installment_date: date of installment of EMI


