
# 🏦 Loan Amortization Calculator

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-passing-brightgreen)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive loan amortization calculator with detailed payment schedule, extra payment support, and complete test coverage.

## 📜 Content

- [✨ Features](#-features)
- [⚙️ Installation](#-installation)
- [🚀 Usage](#-usage)
- [🧮 Examples](#-example-output)
- [📁 Project Structure](#-project-structure)
- [🧪 Testing](#-testing)
- [🤝 Contributing](#-contributing)
- [📄 Licence](#-license)

## ✨ Features


✅ **Accurate Calculations**
- Monthly payment computation using annuity formula
- Interest and principal breakdown for each payment
- Support for annual extra payments
- Zero-interest loan handling

✅ **Detailed Reporting**
- Monthly payment schedule
- Yearly summaries
- Final loan summary with effective interest rate

✅ **Robust Testing**
- Unit tests for all calculation functions
- Golden tests against industry standards
- Edge case testing
- 100% test coverage

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/jankristi86/kreditniKalkulator.git
cd kreditniKalkulator
```
2. Set up a virtual environment (recommended):
```bash
python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage
### Command Line Interface
Run the calculator interactively:
```bash
python script.py
```
Or provide parameters directly:

```bash
python script.py 100000 5.0 120 5000
# Parameters: principal, annual_rate%, term_months, yearly_extra_payment(optional)
```

Import as Module:
```bash
from script import calculate_monthly_payment, process_yearly_payments

# Calculate monthly payment
monthly_payment = calculate_monthly_payment(100000, 0.05/12, 120)

# Generate full amortization schedule
total_interest, total_principal = process_yearly_payments(
    principal=100000,
    monthly_rate=0.05/12,
    months=120,
    yearly_extra=5000
)
```

## 📂 Project Structure
```bash
        .
        ├── script.py               # main logic
        ├── test_smoke.py           # Unit tests
        ├── conftest.py             # Pytest conf 
        ├── requirements.txt        # Dependencies
        └── README.md               # Documentation
```

## 🧪 Testing
The project uses Pytest for testing with multiple test categories:


```bash
# Run all tests
pytest -v

# Run specific test types
pytest -m sensitive -v    # High-precision calculation tests
pytest -m golden -v       # Industry standard comparison tests
pytest -m edge -v         # Edge case tests

# Run with coverage report
pytest --cov=.
pytest --cov=script --cov-report=html

# Check all markers
pytest --markers
```
Test markers (defined in conftest.py):

- sensitive: Tests requiring high precision
- golden: Tests against industry reference values
- edge: Boundary case tests

## 📊 Example Output
```bash
MONTHLY PAYMENT SCHEDULE
--------------------------------------------------
Month | Payment     | Interest | Principal Paid  | Remaining
--------------------------------------------------
    1 |  1060.66 EUR | 416.67 EUR |      644.00 EUR |  99356.00 EUR
    2 |  1060.66 EUR | 413.98 EUR |      646.68 EUR |  98709.32 EUR
...

YEARLY SUMMARY
Total interest: 4852.23 EUR
Total principal: 7847.77 EUR
Remaining balance: 92152.23 EUR

FINAL SUMMARY:
========================================
Initial loan: 100,000.00 EUR
Total paid: 112,745.55 EUR
Interest paid: 27,745.55 EUR
Principal paid: 85,000.00 EUR
Effective interest rate: 27.75%
========================================
```
## 🤝 Contributing
### Contributions are welcome! Please follow these steps:

```textmate
1. Fork the repository
2. Create a feature branch (git checkout -b feature/your-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Open a Pull Request
```

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

> ⚠️ **Important**: This software is intended for educational purposes only. Loan calculations should be verified with a qualified financial advisor.


<div align="center"> <sub>Made with ❤️ for financial literacy</sub> </div>
