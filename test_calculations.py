import pytest
from script import (
    calculate_monthly_payment,
    calculate_interest_payment,
    process_yearly_payments
)


@pytest.mark.parametrize("principal, rate, term, expected", [
    (100000, 0.05 / 12, 120, 1060.66),  # 5% godišnje, 10 godina
    (200000, 0.03 / 12, 240, 1109.20),  # 3% godišnje, 20 godina
    (50000, 0.0, 12, 4166.67),  # Beskamatni kredit
])
def test_monthly_payment(principal, rate, term, expected):
    """Testira izračun mesečne rate"""
    result = calculate_monthly_payment(principal, rate, term)
    assert round(result, 2) == expected


def test_interest_payment():
    """Testira izračun kamate za tekući mesec"""
    assert calculate_interest_payment(100000, 0.05 / 12) == pytest.approx(416.67, abs=0.01)
    assert calculate_interest_payment(50000, 0.03 / 12) == 125.0


@pytest.mark.parametrize("principal, rate, term, extra, expected_interest, tol", [
    # Podaci provereni sa https://www.calculator.net/loan-calculator.html
    (100000, 5.0, 12, 0, 2728.98, 5.0),  # 1 godina bez prevremenih otplata
    (100000, 5.0, 24, 10000, 5018.44, 5.0),  # 2 godine sa godišnjom otplatom od 10k
    (200000, 3.0, 60, 0, 15624.28, 5.0),  # 5 godina bez prevremenih otplata
])
def test_full_amortization(principal, rate, term, extra, expected_interest, tol):
    """Testira kompletan amortizacioni plan sa tolerancijom"""
    monthly_rate = rate / 100 / 12
    total_interest, _ = process_yearly_payments(principal, monthly_rate, term, extra)
    assert total_interest == pytest.approx(expected_interest, abs=tol)
    # assert abs(total_interest - expected_interest) <= tol


# Osetljivi testovi (tačniji proračuni)
@pytest.mark.sensitive
@pytest.mark.parametrize("principal, rate, expected", [
    (100000, 0.05 / 12, 416.67),
    (50000, 0.03 / 12, 125.00)
])
def test_interest_payment(principal, rate, expected):
    """Precizni testovi za izračun kamate"""
    result = calculate_interest_payment(principal, rate)
    assert abs(result - expected) < 0.01


# Golden testovi - provera protiv referentnih vrednosti
@pytest.mark.golden
def test_against_industry_standards():
    """Provera da rezultati padaju u industrijski prihvaćen raspon"""
    cases = [
        (200000, 3.0, 60, (15500, 15700)),
        (100000, 5.0, 12, (2700, 2750))
    ]

    for principal, rate, term, (min_exp, max_exp) in cases:
        monthly_rate = rate / 100 / 12
        total_interest, _ = process_yearly_payments(principal, monthly_rate, term, 0)
        assert min_exp <= total_interest <= max_exp


@pytest.mark.edge
def test_edge_cases():
    """Testira minimalne i maksimalne vrednosti"""
    assert calculate_monthly_payment(1, 0.05 / 12, 1) == pytest.approx(1.00, abs=0.01)
    _, total_principal = process_yearly_payments(1000, 0.05 / 12, 1, 0)
    assert total_principal == 1000
