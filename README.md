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
