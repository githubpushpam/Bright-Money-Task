# Loan Management System

A robust Django-based system for managing loans, including user registration, loan applications, EMI calculations, and payment processing. Built with Django REST Framework for API functionality and Celery for asynchronous task processing.

## Features

### User Registration
- Register users with Aadhar ID, name, email, and annual income
- Automatic asynchronous credit score calculation upon registration

### Loan Application
- Users can apply for a loan by specifying the loan type, amount, interest rate, and term period.
- The system validates the user's credit score and annual income before approving the loan.-
- The system calculates the EMI schedule and ensures it does not exceed 20% of the user's monthly income.



### Payment Processing
- Streamlined EMI payment handling
- Real-time payment validation against outstanding EMIs

### Loan Statement
- Comprehensive view of loan details
- Track payment history
- Monitor upcoming EMI schedule

## Technical Stack

- **Backend Framework**: Django & Django REST Framework
- **Database**: SQLite
- **Task Queue**: Celery with Redis message broker
- **Key Libraries**: 
  - Decimal (for precise financial calculations)
  - Django Transaction Management

## Database Schema

### UserInformation
```
- name: str
- email: str
- annual_income: decimal
- aadhar_id: str (unique)
- credit_score: int
- user_uuid: uuid (unique)
```

### UserTransactionInformation
```
- aadhar_id: str (foreign key)
- registration_date: datetime
- amount: decimal
- transaction_type: str (DEBIT/CREDIT)
- credit_score: int
```

### LoanInfo
```
- loan_id: uuid (primary key)
- user_uuid: uuid (foreign key to UserInformation)
- loan_type: str
- loan_amount: decimal
- annual_interest_rate: decimal
- term_period: int (months)
- disbursement_date: date
```

### EMIDetails
```
- loan_id: uuid (foreign key to LoanInfo)
- amount_due: decimal
- amount_paid: decimal
- installment_date: date
```


