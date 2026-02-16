"""Present value, future value, and annuity calculations."""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class TimeValueResult:
    present_value: float
    future_value: float
    rate: float
    years: float
    growth_factor: float       # (1+r)^t
    discount_factor: float     # 1 / (1+r)^t


class TimeValue:
    """FV = PV(1+r)^t  ⟺  PV = FV/(1+r)^t"""

    @staticmethod
    def future_value(pv: float, rate: float, years: float) -> float:
        return pv * (1 + rate) ** years

    @staticmethod
    def present_value(fv: float, rate: float, years: float) -> float:
        return fv / (1 + rate) ** years

    @staticmethod
    def analyze(amount: float, rate: float, years: float) -> TimeValueResult:
        """Given an amount today, compute both FV and PV interpretations."""
        gf = (1 + rate) ** years
        return TimeValueResult(
            present_value=amount / gf,
            future_value=amount * gf,
            rate=rate,
            years=years,
            growth_factor=gf,
            discount_factor=1.0 / gf,
        )

    @staticmethod
    def fv_annuity(payment: float, rate: float, periods: int) -> float:
        """Future value of an ordinary annuity (equal payments at end of each period).

        FV = PMT * [(1+r)^n - 1] / r
        """
        if rate == 0:
            return payment * periods
        return payment * ((1 + rate) ** periods - 1) / rate

    @staticmethod
    def pv_annuity(payment: float, rate: float, periods: int) -> float:
        """Present value of an ordinary annuity.

        PV = PMT * [1 - (1+r)^(-n)] / r
        """
        if rate == 0:
            return payment * periods
        return payment * (1 - (1 + rate) ** (-periods)) / rate

    @staticmethod
    def irr_bisect(cashflows: list[float], tol: float = 1e-8,
                   max_iter: int = 200) -> float | None:
        """Internal rate of return via bisection on NPV(r) = 0.

        cashflows[0] is typically negative (initial investment).
        Returns None if no root found in (-0.99, 10.0).
        """
        def npv(r):
            return sum(cf / (1 + r) ** t for t, cf in enumerate(cashflows))

        lo, hi = -0.99, 10.0
        if npv(lo) * npv(hi) > 0:
            return None

        for _ in range(max_iter):
            mid = (lo + hi) / 2
            val = npv(mid)
            if abs(val) < tol:
                return mid
            if npv(lo) * val < 0:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2

    @staticmethod
    def rate_sweep(pv: float, years: float,
                   rates: np.ndarray | list[float]) -> list[TimeValueResult]:
        """Compare FV/PV across multiple discount rates."""
        return [TimeValue.analyze(pv, r, years) for r in rates]

    @staticmethod
    def time_curve(amount: float, rate: float,
                   max_years: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Year-by-year FV and PV curves. Returns (years, fv_array, pv_array)."""
        yr = np.arange(0, max_years + 1, dtype=float)
        fv = amount * (1 + rate) ** yr
        pv = amount / (1 + rate) ** yr
        return yr, fv, pv
