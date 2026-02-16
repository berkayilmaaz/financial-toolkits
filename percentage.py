"""Percentage arithmetic: part-of-total, change, margin."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class PercentageResult:
    part: float
    total: float
    percentage: float      # (part/total) * 100
    remaining: float
    ratio: float           # part / total (raw)


class Percentage:
    """Three fundamental percentage operations plus margin/markup."""

    @staticmethod
    def of(part: float, total: float) -> PercentageResult:
        """What percent is `part` of `total`?"""
        if total == 0:
            raise ValueError("Total cannot be zero")
        pct = (part / total) * 100
        return PercentageResult(
            part=part,
            total=total,
            percentage=pct,
            remaining=total - part,
            ratio=part / total,
        )

    @staticmethod
    def value(percent: float, total: float) -> float:
        """What is P% of total?"""
        return (percent / 100) * total

    @staticmethod
    def find_total(part: float, percent: float) -> float:
        """If `part` is P% of the total, what is the total?"""
        if percent == 0:
            raise ValueError("Percent cannot be zero")
        return (part * 100) / percent

    @staticmethod
    def change(old: float, new: float) -> float:
        """Percentage change from old to new: ((new - old) / |old|) * 100."""
        if old == 0:
            raise ValueError("Old value cannot be zero for percentage change")
        return ((new - old) / abs(old)) * 100

    @staticmethod
    def margin(revenue: float, cost: float) -> float:
        """Profit margin: (revenue - cost) / revenue * 100."""
        if revenue == 0:
            raise ValueError("Revenue cannot be zero")
        return ((revenue - cost) / revenue) * 100

    @staticmethod
    def markup(cost: float, selling_price: float) -> float:
        """Markup: (selling_price - cost) / cost * 100."""
        if cost == 0:
            raise ValueError("Cost cannot be zero")
        return ((selling_price - cost) / cost) * 100
