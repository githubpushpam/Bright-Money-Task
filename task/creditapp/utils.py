from decimal import Decimal


# Utility function to calculate the minimum due amount for a billing cycle
def calculate_min_due(principal_balance, apr):
    """
    Calculates the minimum due for a billing cycle based on:
    - Principal Balance
    - Annual Percentage Rate (APR)

    Formula:
    - Daily APR = apr / 365
    - Accrued Interest = Principal Balance * Daily APR
    - Minimum Due = (Principal Balance * 3%) + Accrued Interest

    :param principal_balance: Decimal, the outstanding principal amount.
    :param apr: Decimal, the annual percentage rate.
    :return: Decimal, the calculated minimum due.
    """
    daily_apr = round(apr / Decimal('365'), 3)
    accrued_interest = principal_balance * daily_apr
    return (principal_balance * Decimal('0.03')) + accrued_interest
