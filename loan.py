"""Fixed-rate loan amortization via annuity formula."""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class AmortizationRow:
    month: int
    payment: float
    principal_part: float
    interest_part: float
    remaining_balance: float
    cumulative_interest: float
    cumulative_principal: float


@dataclass(frozen=True)
class LoanResult:
    principal: float
    annual_rate: float
    months: int
    monthly_payment: float
    total_paid: float
    total_interest: float
    interest_ratio: float       # total_interest / principal
    schedule: list[AmortizationRow]


class LoanAmortization:
    """M = P * r_m(1+r_m)^N / [(1+r_m)^N - 1]

    Handles the edge case r=0 (interest-free loan) where M = P/N.
    """

    @staticmethod
    def monthly_payment(principal: float, annual_rate: float, months: int) -> float:
        """Fixed monthly payment for a fully amortizing loan."""
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if months < 1:
            raise ValueError("Term must be at least 1 month")

        rm = annual_rate / 12.0
        if rm == 0:
            return principal / months
        return principal * (rm * (1 + rm) ** months) / ((1 + rm) ** months - 1)

    @staticmethod
    def schedule(principal: float, annual_rate: float, months: int) -> LoanResult:
        """Full amortization table, month by month."""
        rm = annual_rate / 12.0
        payment = LoanAmortization.monthly_payment(principal, annual_rate, months)
        balance = principal

        rows: list[AmortizationRow] = []
        cum_interest = 0.0
        cum_principal = 0.0

        for k in range(1, months + 1):
            interest = balance * rm
            princ = payment - interest

            # guard against floating-point overshoot on the last payment
            if princ > balance:
                princ = balance
                payment = princ + interest

            balance -= princ
            if balance < 0:
                balance = 0.0

            cum_interest += interest
            cum_principal += princ

            rows.append(AmortizationRow(
                month=k,
                payment=payment,
                principal_part=princ,
                interest_part=interest,
                remaining_balance=balance,
                cumulative_interest=cum_interest,
                cumulative_principal=cum_principal,
            ))

        total_paid = sum(r.payment for r in rows)
        return LoanResult(
            principal=principal,
            annual_rate=annual_rate,
            months=months,
            monthly_payment=rows[0].payment if rows else 0,
            total_paid=total_paid,
            total_interest=cum_interest,
            interest_ratio=cum_interest / principal if principal > 0 else 0,
            schedule=rows,
        )

    @staticmethod
    def affordable_principal(monthly_budget: float, annual_rate: float,
                             months: int) -> float:
        """Inverse problem: max loan you can take given a monthly budget.

        P = M * [(1+r_m)^N - 1] / [r_m * (1+r_m)^N]
        """
        rm = annual_rate / 12.0
        if rm == 0:
            return monthly_budget * months
        factor = ((1 + rm) ** months - 1) / (rm * (1 + rm) ** months)
        return monthly_budget * factor

    @staticmethod
    def rate_comparison(principal: float, months: int,
                        rates: list[float]) -> list[LoanResult]:
        """Compare total cost across different annual rates."""
        return [LoanAmortization.schedule(principal, r, months) for r in rates]
