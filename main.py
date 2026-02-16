#!/usr/bin/env python3
"""Financial Mathematics Toolkit — CLI entry point.

Usage:
    python main.py                  # full analysis with plots
    python main.py --no-plots       # numbers only
    python main.py --validate       # run validation checks
"""

from __future__ import annotations
import argparse
import math
import sys

import numpy as np

from financial_math import (
    CompoundInterest, LoanAmortization, TimeValue, Percentage,
)


def fmt(x: float) -> str:
    return f"₺{x:,.2f}"


def print_header(title: str) -> None:
    bar = "═" * 60
    print(f"\n{bar}")
    print(f"  {title}")
    print(bar)


def run_compound_interest() -> None:
    print_header("COMPOUND INTEREST")

    P, r, n, t = 10_000, 0.08, 12, 10
    result = CompoundInterest.calculate(P, r, n, t)

    print(f"  Principal:          {fmt(P)}")
    print(f"  Rate:               {r*100:.1f}% annual, compounded {n}×/yr")
    print(f"  Horizon:            {t} years")
    print(f"  ─────────────────────────────────")
    print(f"  Accumulated:        {fmt(result.amount)}")
    print(f"  Interest earned:    {fmt(result.interest_earned)}")
    print(f"  Effective rate:     {result.effective_annual_rate*100:.4f}%")
    print(f"  Continuous equiv:   {fmt(CompoundInterest.continuous(P, r, t))}")
    print(f"  Doubling time:      {CompoundInterest.doubling_time(r, n):.2f} years")

    print("\n  Rate comparison (₺10,000, 12×/yr, 20 years):")
    rates = [0.02, 0.05, 0.08, 0.10, 0.15]
    for res in CompoundInterest.rate_sweep(P, 12, 20, rates):
        print(f"    {res.rate*100:5.1f}%  →  {fmt(res.amount)}")

    print("\n  Frequency comparison (₺10,000, 10%, 20 years):")
    freqs = [(1, "Annual"), (4, "Quarterly"), (12, "Monthly"), (365, "Daily")]
    for n_val, label in freqs:
        res = CompoundInterest.calculate(10_000, 0.10, n_val, 20)
        print(f"    {label:<12s} (n={n_val:<3d})  →  {fmt(res.amount)}")
    print(f"    {'Continuous':<12s}          →  {fmt(CompoundInterest.continuous(10_000, 0.10, 20))}")


def run_loan() -> None:
    print_header("LOAN AMORTIZATION")

    P, r, N = 500_000, 0.24, 36
    result = LoanAmortization.schedule(P, r, N)

    print(f"  Loan:               {fmt(P)}")
    print(f"  Rate:               {r*100:.1f}% annual")
    print(f"  Term:               {N} months")
    print(f"  ─────────────────────────────────")
    print(f"  Monthly payment:    {fmt(result.monthly_payment)}")
    print(f"  Total paid:         {fmt(result.total_paid)}")
    print(f"  Total interest:     {fmt(result.total_interest)}")
    print(f"  Interest ratio:     {result.interest_ratio*100:.1f}%")

    print("\n  First 6 months:")
    print(f"    {'Mo':>4s}  {'Payment':>12s}  {'Principal':>12s}  {'Interest':>12s}  {'Balance':>14s}")
    for row in result.schedule[:6]:
        print(f"    {row.month:4d}  {fmt(row.payment):>12s}  {fmt(row.principal_part):>12s}  "
              f"{fmt(row.interest_part):>12s}  {fmt(row.remaining_balance):>14s}")

    budget = 20_000
    affordable = LoanAmortization.affordable_principal(budget, 0.24, 36)
    print(f"\n  Affordable principal at {fmt(budget)}/mo budget: {fmt(affordable)}")

    print("\n  Rate comparison (₺500K, 36 months):")
    for res in LoanAmortization.rate_comparison(500_000, 36, [0.12, 0.18, 0.24, 0.36, 0.48]):
        print(f"    {res.annual_rate*100:5.1f}%  →  {fmt(res.monthly_payment)}/mo  "
              f"total interest: {fmt(res.total_interest)}")


def run_time_value() -> None:
    print_header("TIME VALUE OF MONEY")

    amount, r, t = 100_000, 0.10, 15
    tv = TimeValue.analyze(amount, r, t)

    print(f"  Amount:             {fmt(amount)}")
    print(f"  Rate:               {r*100:.1f}%")
    print(f"  Horizon:            {t} years")
    print(f"  ─────────────────────────────────")
    print(f"  Future value:       {fmt(tv.future_value)}")
    print(f"  Present value:      {fmt(tv.present_value)}")
    print(f"  Growth factor:      {tv.growth_factor:.4f}×")
    print(f"  Discount factor:    {tv.discount_factor:.6f}")

    # annuity
    pmt = 5_000
    fv_ann = TimeValue.fv_annuity(pmt, 0.08 / 12, 12 * 10)
    pv_ann = TimeValue.pv_annuity(pmt, 0.08 / 12, 12 * 10)
    print(f"\n  Annuity ({fmt(pmt)}/mo, 8%, 10yr):")
    print(f"    FV of annuity:    {fmt(fv_ann)}")
    print(f"    PV of annuity:    {fmt(pv_ann)}")

    # IRR
    cashflows = [-100_000, 25_000, 30_000, 35_000, 40_000, 20_000]
    irr = TimeValue.irr_bisect(cashflows)
    print(f"\n  IRR for cashflows {cashflows}:")
    print(f"    IRR:              {irr*100:.2f}%" if irr else "    IRR:  not found")


def run_percentage() -> None:
    print_header("PERCENTAGE CALCULATIONS")

    res = Percentage.of(2500, 10000)
    print(f"  2,500 of 10,000:    {res.percentage:.2f}%")
    print(f"  15% of 8,000:       {Percentage.value(15, 8000):,.2f}")
    print(f"  What is 100% if 750 is 30%?  {Percentage.find_total(750, 30):,.2f}")
    print(f"  Change 80 → 120:   {Percentage.change(80, 120):+.2f}%")
    print(f"  Change 120 → 80:   {Percentage.change(120, 80):+.2f}%")
    print(f"  Margin (rev=1000, cost=600):   {Percentage.margin(1000, 600):.1f}%")
    print(f"  Markup (cost=600, sell=1000):   {Percentage.markup(600, 1000):.1f}%")


def run_validation() -> None:
    print_header("VALIDATION SUITE")

    checks = 0
    passed = 0

    def check(name: str, got: float, expected: float, tol: float = 1e-6):
        nonlocal checks, passed
        checks += 1
        ok = abs(got - expected) < tol
        if ok:
            passed += 1
        mark = "✓" if ok else "✗"
        dots = "." * (40 - len(name))
        print(f"  {mark}  {name} {dots} {got:.6f}  (exp: {expected:.6f})")

    # compound interest: ₺1000, 5%, annual, 10 years → 1000*(1.05)^10
    check("CI: basic annual", CompoundInterest.calculate(1000, 0.05, 1, 10).amount, 1000 * 1.05**10)

    # continuous: ₺1000, 5%, 10 years → 1000*e^(0.5)
    check("CI: continuous", CompoundInterest.continuous(1000, 0.05, 10), 1000 * math.exp(0.5))

    # effective rate: 12% monthly → (1+0.01)^12 - 1
    res = CompoundInterest.calculate(1000, 0.12, 12, 1)
    check("CI: effective rate", res.effective_annual_rate, (1.01)**12 - 1)

    # doubling time at 7% annual: ln2/ln(1.07)
    check("CI: doubling time", CompoundInterest.doubling_time(0.07, 1), math.log(2) / math.log(1.07))

    # loan: zero-rate → P/N
    check("Loan: zero rate", LoanAmortization.monthly_payment(12000, 0, 12), 1000.0)

    # loan: known case — ₺100,000 at 12%/yr for 12 months
    # M = 100000 * 0.01*(1.01)^12 / ((1.01)^12 - 1)
    rm = 0.01
    expected_m = 100_000 * rm * (1 + rm)**12 / ((1 + rm)**12 - 1)
    check("Loan: 12mo payment", LoanAmortization.monthly_payment(100_000, 0.12, 12), expected_m)

    # loan: total paid should exceed principal
    loan_res = LoanAmortization.schedule(100_000, 0.12, 12)
    check("Loan: balance→0", loan_res.schedule[-1].remaining_balance, 0.0, tol=0.01)

    # time value: FV then PV should round-trip
    fv = TimeValue.future_value(5000, 0.08, 10)
    pv = TimeValue.present_value(fv, 0.08, 10)
    check("TV: FV→PV roundtrip", pv, 5000.0, tol=1e-4)

    # FV annuity: 100/mo at 0% for 12 months = 1200
    check("TV: annuity zero-rate", TimeValue.fv_annuity(100, 0, 12), 1200.0)

    # PV annuity at r=0
    check("TV: PV annuity r=0", TimeValue.pv_annuity(100, 0, 12), 1200.0)

    # IRR: simple case [-1000, 1100] → 10%
    irr = TimeValue.irr_bisect([-1000, 1100])
    check("TV: IRR simple", irr, 0.10, tol=1e-4)

    # percentage basics
    check("Pct: of", Percentage.of(25, 200).percentage, 12.5)
    check("Pct: value", Percentage.value(15, 200), 30.0)
    check("Pct: find_total", Percentage.find_total(30, 15), 200.0)
    check("Pct: change", Percentage.change(80, 100), 25.0)
    check("Pct: margin", Percentage.margin(1000, 600), 40.0)
    check("Pct: markup", Percentage.markup(600, 1000), 66.666667, tol=1e-4)

    print(f"\n  Result: {passed}/{checks} checks passed.")
    if passed < checks:
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Financial Mathematics Toolkit")
    parser.add_argument("--no-plots", action="store_true", help="Skip plot generation")
    parser.add_argument("--validate", action="store_true", help="Run validation suite")
    args = parser.parse_args()

    if args.validate:
        run_validation()
        return

    run_compound_interest()
    run_loan()
    run_time_value()
    run_percentage()

    if not args.no_plots:
        from financial_math.plots import (
            plot_compound_growth, plot_rate_sweep,
            plot_loan_balance, plot_loan_breakdown,
            plot_time_value, plot_percentage_pie,
        )

        print_header("GENERATING PLOTS")

        series = CompoundInterest.time_series(10_000, 0.08, 12, 20)
        plot_compound_growth(series, save_path="compound_growth.png")
        print("  → compound_growth.png")

        plot_rate_sweep(10_000, 12, 20, [0.02, 0.05, 0.08, 0.10, 0.15],
                        save_path="rate_sweep.png")
        print("  → rate_sweep.png")

        loan = LoanAmortization.schedule(500_000, 0.24, 36)
        plot_loan_balance(loan, save_path="loan_balance.png")
        print("  → loan_balance.png")

        plot_loan_breakdown(loan, save_path="loan_breakdown.png")
        print("  → loan_breakdown.png")

        plot_time_value(100_000, 0.10, 15, save_path="time_value.png")
        print("  → time_value.png")

        plot_percentage_pie(2500, 10000, save_path="percentage.png")
        print("  → percentage.png")

        print("\n  All plots saved. Use --no-plots to skip.")
        plt.show()


if __name__ == "__main__":
    main()
