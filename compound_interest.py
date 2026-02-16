"""Compound interest: discrete and continuous compounding."""

from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True)
class CompoundResult:
    principal: float
    rate: float
    n: int          # compounding frequency per year
    years: float
    amount: float
    interest_earned: float
    effective_annual_rate: float


@dataclass(frozen=True)
class GrowthSeries:
    """Year-by-year breakdown of compound growth."""
    years: np.ndarray
    amounts: np.ndarray
    interest: np.ndarray     # cumulative interest at each year
    principal: float


class CompoundInterest:
    """A = P(1 + r/n)^(nt) for discrete, A = Pe^(rt) for continuous."""

    @staticmethod
    def calculate(principal: float, rate: float, n: int, years: float) -> CompoundResult:
        """Discrete compounding.

        Args:
            principal: initial investment [currency]
            rate: annual interest rate as decimal (0.08 = 8%)
            n: compounding periods per year (1=annual, 12=monthly, 365=daily)
            years: investment horizon
        """
        if principal <= 0:
            raise ValueError("Principal must be positive")
        if n < 1:
            raise ValueError("Compounding frequency must be >= 1")

        amount = principal * (1 + rate / n) ** (n * years)
        eff_rate = (1 + rate / n) ** n - 1

        return CompoundResult(
            principal=principal,
            rate=rate,
            n=n,
            years=years,
            amount=amount,
            interest_earned=amount - principal,
            effective_annual_rate=eff_rate,
        )

    @staticmethod
    def continuous(principal: float, rate: float, years: float) -> float:
        """Continuous compounding: A = Pe^(rt)."""
        return principal * math.exp(rate * years)

    @staticmethod
    def doubling_time(rate: float, n: int = 1) -> float:
        """Exact doubling time via ln(2) / [n * ln(1 + r/n)].
        Falls back to Rule of 72 approximation if rate is zero.
        """
        if rate <= 0:
            return float("inf")
        return math.log(2) / (n * math.log(1 + rate / n))

    @staticmethod
    def time_series(principal: float, rate: float, n: int, years: int) -> GrowthSeries:
        """Year-by-year growth curve."""
        yr = np.arange(0, years + 1, dtype=float)
        amounts = principal * (1 + rate / n) ** (n * yr)
        return GrowthSeries(
            years=yr,
            amounts=amounts,
            interest=amounts - principal,
            principal=principal,
        )

    @staticmethod
    def rate_sweep(principal: float, n: int, years: float,
                   rates: list[float]) -> list[CompoundResult]:
        """Compare final amounts across different rates."""
        return [CompoundInterest.calculate(principal, r, n, years) for r in rates]

    @staticmethod
    def frequency_sweep(principal: float, rate: float, years: float,
                        frequencies: list[int]) -> list[CompoundResult]:
        """Compare final amounts across compounding frequencies."""
        return [CompoundInterest.calculate(principal, rate, n, years) for n in frequencies]
