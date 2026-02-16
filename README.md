<p align="center">
  <img src="assets/brky-logo.png" alt="brky.ai" height="64" style="border-radius:8px">
</p>

<h3 align="center">Financial Mathematics Toolkit</h3>

<p align="center">
  <strong>brky.ai</strong> — Berkay Yılmaz<br>
  <a href="https://projects.brky.ai/finance/">🔗 Live Demo</a> · <a href="https://brky.ai">brky.ai</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/numpy-≥1.24-013243?logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/matplotlib-≥3.7-11557c?logo=plotly&logoColor=white" alt="Matplotlib">
  <img src="https://img.shields.io/badge/license-Unlicense-blue" alt="License">
</p>

---

## Overview

An object-oriented Python toolkit for core financial mathematics: compound interest, loan amortization, present & future value analysis, and percentage calculations. Includes a dark-themed matplotlib visualization module and a validation suite.

```
Principal → CompoundInterest → GrowthSeries  → plot_compound_growth()
Loan      → LoanAmortization → LoanResult    → plot_loan_balance()
Amount    → TimeValue        → FV / PV / IRR → plot_time_value()
Part      → Percentage       → Ratio / Change → plot_percentage_pie()
```

The companion web interface is live at **[projects.brky.ai/finance](https://projects.brky.ai/finance/)** — a single-page application that mirrors the Python engine with client-side JavaScript.

## Features

- **Compound Interest** — Discrete and continuous compounding, effective annual rate, doubling time. Rate sweep and frequency sweep comparisons.
- **Loan Amortization** — Fixed-rate annuity payment with full month-by-month schedule. Inverse problem: maximum affordable principal given a budget.
- **Time Value of Money** — FV/PV computation, ordinary annuity (FV & PV), internal rate of return via bisection.
- **Percentage Arithmetic** — Part-of-total, find-the-whole, percentage change, profit margin, and markup.
- **Dark-Theme Plots** — Matplotlib visualizations matching the brky.ai design system palette.
- **Validation Suite** — 17 automated checks against analytical solutions and edge cases.

## Project Structure

```
financial-mathematics-toolkit/
├── assets/
│   └── brky-logo.png              # brand logo
├── financial_math/
│   ├── __init__.py                 # package exports
│   ├── compound_interest.py        # A = P(1 + r/n)^(nt)
│   ├── loan.py                     # annuity formula, amortization schedule
│   ├── time_value.py               # FV, PV, annuities, IRR
│   ├── percentage.py               # percentage arithmetic
│   ├── plots.py                    # matplotlib dark-theme visualization
│   ├── main.py                     # CLI entry point
│   └── requirements.txt
├── Percentage_calculator.py        # original tkinter prototype
├── README.md
└── LICENSE
```

## Quick Start

```bash
git clone https://github.com/berkayilmaaz/Financial-Mathematics-Toolkit.git
cd Financial-Mathematics-Toolkit

pip install -r financial_math/requirements.txt

python -m financial_math.main                # full analysis + plots
python -m financial_math.main --no-plots     # numbers only
python -m financial_math.main --validate     # run validation suite
```

## Usage

### Compound Interest

```python
from financial_math import CompoundInterest

result = CompoundInterest.calculate(
    principal=10_000,   # ₺10,000
    rate=0.08,          # 8% annual
    n=12,               # monthly compounding
    years=10,
)

print(f"Accumulated: ₺{result.amount:,.2f}")
print(f"Interest:    ₺{result.interest_earned:,.2f}")
print(f"Eff. rate:   {result.effective_annual_rate*100:.4f}%")
print(f"Doubling:    {CompoundInterest.doubling_time(0.08, 12):.2f} years")
```

### Loan Amortization

```python
from financial_math import LoanAmortization

loan = LoanAmortization.schedule(
    principal=500_000,    # ₺500K
    annual_rate=0.24,     # 24%
    months=36,
)

print(f"Monthly: ₺{loan.monthly_payment:,.2f}")
print(f"Total interest: ₺{loan.total_interest:,.2f}")

for row in loan.schedule[:3]:
    print(f"  Mo {row.month}: principal=₺{row.principal_part:,.2f}  "
          f"interest=₺{row.interest_part:,.2f}  balance=₺{row.remaining_balance:,.2f}")
```

### Time Value of Money

```python
from financial_math import TimeValue

fv = TimeValue.future_value(pv=100_000, rate=0.10, years=15)
pv = TimeValue.present_value(fv=500_000, rate=0.10, years=15)

print(f"₺100K in 15yr at 10%: ₺{fv:,.2f}")
print(f"₺500K today is worth: ₺{pv:,.2f}")

irr = TimeValue.irr_bisect([-100_000, 25_000, 30_000, 35_000, 40_000, 20_000])
print(f"IRR: {irr*100:.2f}%")
```

### Percentage

```python
from financial_math import Percentage

result = Percentage.of(part=2500, total=10000)
print(f"Percentage: {result.percentage:.2f}%")
print(f"Change 80→120: {Percentage.change(80, 120):+.2f}%")
print(f"Margin: {Percentage.margin(revenue=1000, cost=600):.1f}%")
```

## Mathematics

| Module | Formula | Domain |
|--------|---------|--------|
| **Compound Interest** | $A = P(1 + r/n)^{nt}$ | Savings, investments |
| **Continuous** | $A = Pe^{rt}$ | Theoretical limit |
| **Loan Payment** | $M = P \cdot \frac{r_m(1+r_m)^N}{(1+r_m)^N - 1}$ | Mortgages, personal loans |
| **Future Value** | $FV = PV \cdot (1+r)^t$ | Projection |
| **Present Value** | $PV = FV / (1+r)^t$ | Discounting |
| **FV Annuity** | $FV = PMT \cdot \frac{(1+r)^n - 1}{r}$ | Regular contributions |
| **IRR** | $\sum_{t=0}^{N} \frac{CF_t}{(1+r)^t} = 0$ | Investment evaluation |

## Validation

```
$ python -m financial_math.main --validate

  ✓  CI: basic annual ........................ 1628.894627
  ✓  CI: continuous .......................... 1648.721271
  ✓  CI: effective rate ...................... 0.126825
  ✓  CI: doubling time ....................... 10.244768
  ✓  Loan: zero rate ......................... 1000.000000
  ✓  Loan: 12mo payment ...................... 8884.878856
  ✓  Loan: balance→0 ......................... 0.000000
  ✓  TV: FV→PV roundtrip .................... 5000.000000
  ...
  Result: 17/17 checks passed.
```

## Legacy

The original `Percentage_calculator.py` is a tkinter GUI for basic percentage calculations with pie chart visualization. This toolkit extends that idea into a full financial mathematics package with proper OOP architecture.

## Author

**Berkay Yılmaz** — [brky.ai](https://brky.ai) · [LinkedIn](https://linkedin.com/in/berkayilmaaz)

---

<p align="center">
  <sub>brky.ai — Berkay Yılmaz</sub>
</p>
