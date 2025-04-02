import sys
from typing import Tuple, Optional


def calculate_monthly_payment(P: float, r: float, n: int) -> float:
    """Izračunava mesečnu ratu koristeći formulu za anuitet."""
    if r == 0:
        return P / n
    return (P * r * (1 + r) ** n) / ((1 + r) ** n - 1)


def generate_amortization_schedule(P: float, r: float, n: int, yearly_extra: float) -> Tuple[float, float]:
    """Generiše kompletan amortizacioni plan sa mesečnim detaljima."""
    remaining = P
    total_int = 0.0
    total_prin = 0.0
    month_num = 1
    current_year = 2025

    while month_num <= n and remaining > 0:
        # Izračunaj mesečnu ratu za tekući period
        monthly_pmt = calculate_monthly_payment(remaining, r, n - month_num + 1)

        print(f"\n{current_year}. godina:")
        print("--------------------------------------------------")
        print("Mesec | Mesečna rata | Kamata | Otplata glavnice | Preostali dug")
        print("--------------------------------------------------")

        year_interest = 0.0
        year_principal = 0.0

        for month_in_year in range(1, 13):
            if month_num > n or remaining <= 0:
                break

            interest = remaining * r
            principal = min(monthly_pmt - interest, remaining)
            remaining -= principal

            total_int += interest
            total_prin += principal
            year_interest += interest
            year_principal += principal

            print(
                f"{month_num:5} | {monthly_pmt:12.2f} EUR | {interest:6.2f} EUR | {principal:15.2f} EUR | {remaining:12.2f} EUR")
            month_num += 1

        # Godišnja prevremena otplata
        if remaining > 0 and month_num <= n:
            extra = min(yearly_extra, remaining)
            remaining -= extra
            total_prin += extra
            year_principal += extra

            print("\nPrevremena otplata na kraju godine:", f"{extra:.2f} EUR")

        # Godišnji rezime
        print("\nRezime za godinu:")
        print(f"Ukupno kamata: {year_interest:.2f} EUR")
        print(f"Ukupno glavnica: {year_principal:.2f} EUR")
        print(f"Preostali dug: {remaining:.2f} EUR")

        current_year += 1

    return round(total_int, 2), round(total_prin, 2)


def get_input(prompt: str, input_type: type, default: Optional[float] = None) -> float:
    """Obrada korisničkog unosa sa podrazumevanim vrednostima."""
    while True:
        try:
            user_input = input(f"{prompt} [{default}]: " if default else f"{prompt}: ")
            if not user_input and default is not None:
                return default
            return input_type(user_input)
        except ValueError:
            print(f"Nevažeći unos. Unesite {input_type.__name__}.")


def main():
    print("\nKALKULATOR KREDITA\n" + "=" * 40)

    # Podrazumevane vrednosti
    defaults = {
        'amount': 76874,
        'rate': 5.0,
        'term': 317,
        'extra': 0
    }

    # Provera argumenata komandne linije
    if len(sys.argv) == 5:
        try:
            params = {
                'amount': float(sys.argv[1]),
                'rate': float(sys.argv[2]),
                'term': int(sys.argv[3]),
                'extra': float(sys.argv[4])
            }
        except ValueError:
            print("Greška u argumentima. Koristiću interaktivni unos.")
            params = {}
    else:
        params = {}

    # Unos parametara
    P = params.get('amount') or get_input("Unesite iznos kredita (EUR)", float, defaults['amount'])
    annual_rate = params.get('rate') or get_input("Unesite godišnju kamatnu stopu (%)", float, defaults['rate'])
    n = params.get('term') or get_input("Unesite broj rata", int, defaults['term'])
    yearly_extra = params.get('extra') or get_input("Unesite godišnju prevremenu otplatu (EUR)", float,
                                                    defaults['extra'])

    # Konverzija stope
    monthly_rate = annual_rate / 100 / 12

    # Generisanje i prikaz amortizacionog plana
    total_interest, total_principal = generate_amortization_schedule(P, monthly_rate, n, yearly_extra)

    # Finalni rezime
    print("\n\nFINALNI REZIME:")
    print("=" * 40)
    print(f"Početni kredit: {P:,.2f} EUR")
    print(f"Ukupno plaćeno: {total_principal + total_interest:,.2f} EUR")
    print(f"Od toga kamata: {total_interest:,.2f} EUR")
    print(f"Od toga glavnica: {total_principal:,.2f} EUR")
    print(f"Efektivna kamatna stopa: {total_interest / P * 100:,.2f}%")
    print("=" * 40)


if __name__ == "__main__":
    main()
