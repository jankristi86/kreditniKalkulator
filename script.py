import sys
from typing import Tuple, Optional, Dict, Union

"""
Financial calculations for loan amortization.

"""


def calculate_monthly_payment(principal: float, monthly_rate: float, months: int) -> float:
    """Calculates the monthly payment using the annuity formula with precise rounding.

    Args:
        principal: The initial loan amount
        monthly_rate: Monthly interest rate (annual rate / 12)
        months: Total number of payment months

    Returns:
        float: Monthly payment amount rounded to 2 decimal places

    Note:
        For zero-interest loans, simply divides principal by months.
        Uses standard banking rounding (2 decimal places).
    """
    if monthly_rate == 0:
        return round(principal / months, 2)

    factor = (1 + monthly_rate) ** months
    payment = principal * monthly_rate * factor / (factor - 1)
    return round(payment, 2)  # Bankarski standard - 2 decimalna mesta


def calculate_interest_payment(remaining_principal: float, monthly_rate: float) -> float:
    """Calculates the interest portion of a monthly payment.

    Args:
        remaining_principal: Current loan balance before payment
        monthly_rate: Monthly interest rate

    Returns:
        float: Interest amount for the current period
    """
    return remaining_principal * monthly_rate


"""
Display and formatting functions.
"""


def print_monthly_payment_details(month_num: int, monthly_payment: float,
                                  interest: float, principal: float, remaining: float):
    """Prints formatted monthly payment details in a table row.

    Args:
        month_num: Current month number in the schedule
        monthly_payment: Total monthly payment amount
        interest: Interest portion of payment
        principal: Principal portion of payment
        remaining: Remaining loan balance after payment
    """
    print(
        f"{month_num:5} | {monthly_payment:12.2f} EUR | {interest:6.2f} EUR | {principal:15.2f} EUR | {remaining:12.2f} EUR")


def print_yearly_summary(year: int, year_interest: float, year_principal: float, remaining: float):
    """Prints a yearly summary of loan repayment progress.

    Args:
        year: Current year number
        year_interest: Total interest paid in the year
        year_principal: Total principal paid in the year
        remaining: Remaining loan balance
    """
    print("\nRezime za godinu:")
    print(f"Ukupno kamata: {year_interest:.2f} EUR")
    print(f"Ukupno glavnica: {year_principal:.2f} EUR")
    print(f"Preostali dug: {remaining:.2f} EUR")


def print_final_summary(initial_principal: float, total_interest: float, total_principal: float):
    """Prints the final loan repayment summary with totals.

    Args:
        initial_principal: Original loan amount
        total_interest: Total interest paid over loan term
        total_principal: Total principal paid over loan term
    """
    print("\n\nFINALNI REZIME:")
    print("=" * 40)
    print(f"Početni kredit: {initial_principal:,.2f} EUR")
    print(f"Ukupno plaćeno: {total_principal + total_interest:,.2f} EUR")
    print(f"Od toga kamata: {total_interest:,.2f} EUR")
    print(f"Od toga glavnica: {total_principal:,.2f} EUR")
    if initial_principal > 0:
        print(f"Efektivna kamatna stopa: {total_interest / initial_principal * 100:,.2f}%")
    print("=" * 40)


"""
Core repayment logic.
"""


def process_yearly_payments(principal: float, monthly_rate: float, months: int,
                            yearly_extra: float, start_year: int = 2025) -> Tuple[float, float]:
    """Processes loan payments year by year with optional extra payments.

    Args:
        principal: Initial loan amount
        monthly_rate: Monthly interest rate
        months: Total number of payment months
        yearly_extra: Additional annual principal payment
        start_year: First year of repayment (default: 2025)

    Returns:
        Tuple[float, float]: (total_interest_paid, total_principal_paid)

    Note:
        Prints detailed amortization schedule and yearly summaries.
        Handles early loan payoff if extra payments are sufficient.
    """
    remaining = principal
    total_interest = 0.0
    total_principal = 0.0
    month_num = 1
    current_year = start_year

    while month_num <= months and remaining > 0:
        monthly_payment = calculate_monthly_payment(remaining, monthly_rate, months - month_num + 1)

        print(f"\n{current_year}. godina:")
        print("--------------------------------------------------")
        print("Mesec | Mesečna rata | Kamata | Otplata glavnice | Preostali dug")
        print("--------------------------------------------------")

        year_interest = 0.0
        year_principal = 0.0

        for _ in range(12):
            if month_num > months or remaining <= 0:
                break

            interest = calculate_interest_payment(remaining, monthly_rate)
            principal_payment = min(monthly_payment - interest, remaining)
            remaining -= principal_payment

            total_interest += interest
            total_principal += principal_payment
            year_interest += interest
            year_principal += principal_payment

            print_monthly_payment_details(month_num, monthly_payment, interest,
                                          principal_payment, remaining)
            month_num += 1

        # Obrada prevremene otplate
        if remaining > 0 and month_num <= months:
            extra_payment = process_extra_payment(remaining, yearly_extra)
            remaining -= extra_payment
            total_principal += extra_payment
            year_principal += extra_payment

        print_yearly_summary(current_year, year_interest, year_principal, remaining)
        current_year += 1

    return round(total_interest, 2), round(total_principal, 2)


def process_extra_payment(remaining: float, yearly_extra: float) -> float:
    """Processes an additional principal payment at year-end.

    Args:
        remaining: Current loan balance
        yearly_extra: Requested extra payment amount

    Returns:
        float: Actual extra payment applied (may be less than requested if loan balance is lower)
    """
    if yearly_extra > 0 and remaining > 0:
        extra = min(yearly_extra, remaining)
        print("\nPrevremena otplata na kraju godine:", f"{extra:.2f} EUR")
        return extra
    return 0.0


"""
Input handling and validation.
"""


def get_user_input(prompt: str, input_type: type, default: Optional[float] = None) -> float:
    """Gets and validates user input with optional default value.

    Args:
        prompt: Text prompt to display
        input_type: Expected data type (float/int)
        default: Default value if user enters nothing

    Returns:
        Validated user input

    Raises:
        ValueError: If input cannot be converted or is negative
    """
    while True:
        try:
            user_input = input(f"{prompt} [{default}]: " if default else f"{prompt}: ")
            if not user_input and default is not None:
                return default
            value = input_type(user_input)
            if value < 0:
                raise ValueError("Vrednost ne može biti negativna")
            return value
        except ValueError:
            print(f"Nevažeći unos. Unesite {input_type.__name__}.")


def parse_command_line_args() -> Dict[str, Union[float, int]]:
    """Parses command line arguments for non-interactive mode.

    Returns:
        Dict: Parsed arguments as {'amount': float, 'rate': float, 'term': int, 'extra': float}
        or empty dict if arguments are invalid/missing.
    """
    if len(sys.argv) == 5:
        try:
            return {
                'amount': float(sys.argv[1]),
                'rate': float(sys.argv[2]),
                'term': int(sys.argv[3]),
                'extra': float(sys.argv[4])
            }
        except ValueError:
            print("Greška u argumentima. Koristiću interaktivni unos.")
    return {}


"""
Main program execution.
"""


def main():
    """Main entry point for the loan calculator application."""
    print("\nKALKULATOR KREDITA\n" + "=" * 40)

    # Default values
    defaults = {
        'amount': 50000,
        'rate': 4.75,
        'term': 240,
        'extra': 0
    }

    # Get parameters
    params = parse_command_line_args()
    principal = params.get('amount') or get_user_input("Unesite iznos kredita (EUR)", float, defaults['amount'])
    annual_rate = params.get('rate') or get_user_input("Unesite godišnju kamatnu stopu (%)", float, defaults['rate'])
    term = params.get('term') or get_user_input("Unesite broj rata", int, defaults['term'])
    yearly_extra = params.get('extra') or get_user_input("Unesite godišnju prevremenu otplatu (EUR)", float,
                                                         defaults['extra'])

    # Convert and calculate
    monthly_rate = annual_rate / 100 / 12
    total_interest, total_principal = process_yearly_payments(principal, monthly_rate, term, yearly_extra)

    # Show results
    print_final_summary(principal, total_interest, total_principal)


if __name__ == "__main__":
    main()
