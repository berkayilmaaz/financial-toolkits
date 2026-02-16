"""Dark-theme matplotlib plots matching the brky.ai design system."""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from .compound_interest import CompoundInterest, GrowthSeries
from .loan import LoanAmortization, LoanResult
from .time_value import TimeValue

# brky.ai palette
COLORS = {
    "bg": "#0e1117",
    "grid": "#21262d",
    "zero": "#30363d",
    "text": "#c9d1d9",
    "secondary": "#8b949e",
    "blue": "#7EC8E3",
    "red": "#C2506A",
    "yellow": "#eab308",
    "green": "#22c55e",
    "purple": "#a855f7",
    "orange": "#f97316",
}

SERIES_COLORS = [
    COLORS["blue"], COLORS["red"], COLORS["yellow"],
    COLORS["green"], COLORS["purple"], COLORS["orange"],
]


def _apply_theme(ax: plt.Axes, fig: plt.Figure) -> None:
    """Apply the dark brky.ai theme to axes and figure."""
    fig.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])
    ax.tick_params(colors=COLORS["secondary"], labelsize=9)
    ax.xaxis.label.set_color(COLORS["secondary"])
    ax.yaxis.label.set_color(COLORS["secondary"])
    ax.title.set_color(COLORS["text"])
    ax.title.set_fontsize(12)
    ax.title.set_fontweight(600)
    for spine in ax.spines.values():
        spine.set_color(COLORS["grid"])
    ax.grid(True, color=COLORS["grid"], linewidth=0.5, alpha=0.6)
    ax.set_axisbelow(True)


def _currency_formatter(x, _):
    if abs(x) >= 1e6:
        return f"₺{x/1e6:.1f}M"
    if abs(x) >= 1e3:
        return f"₺{x/1e3:.0f}K"
    return f"₺{x:.0f}"


def plot_compound_growth(series: GrowthSeries, title: str = "Compound Interest Growth",
                         save_path: str | None = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    _apply_theme(ax, fig)

    ax.fill_between(series.years, series.amounts, alpha=0.08, color=COLORS["blue"])
    ax.plot(series.years, series.amounts, color=COLORS["blue"], lw=2.2, label="Balance")
    ax.axhline(series.principal, color=COLORS["red"], lw=1.2, ls="--", label="Principal")
    ax.plot(series.years, series.interest, color=COLORS["yellow"], lw=1.8, label="Interest Earned")

    ax.set_xlabel("Year")
    ax.set_ylabel("Amount")
    ax.set_title(title)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
    ax.legend(facecolor=COLORS["bg"], edgecolor=COLORS["grid"],
              labelcolor=COLORS["text"], fontsize=9)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_rate_sweep(principal: float, n: int, years: float,
                    rates: list[float], title: str = "Rate Sensitivity",
                    save_path: str | None = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    _apply_theme(ax, fig)

    for i, r in enumerate(rates):
        s = CompoundInterest.time_series(principal, r, n, int(years))
        c = SERIES_COLORS[i % len(SERIES_COLORS)]
        ax.plot(s.years, s.amounts, color=c, lw=2, label=f"{r*100:.0f}%")

    ax.set_xlabel("Year")
    ax.set_ylabel("Amount")
    ax.set_title(title)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
    ax.legend(facecolor=COLORS["bg"], edgecolor=COLORS["grid"],
              labelcolor=COLORS["text"], fontsize=9, ncol=2)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_loan_balance(result: LoanResult, title: str = "Loan Amortization",
                      save_path: str | None = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    _apply_theme(ax, fig)

    months = [0] + [r.month for r in result.schedule]
    balance = [result.principal] + [r.remaining_balance for r in result.schedule]
    cum_int = [0] + [r.cumulative_interest for r in result.schedule]
    cum_prn = [0] + [r.cumulative_principal for r in result.schedule]

    ax.fill_between(months, balance, alpha=0.06, color=COLORS["blue"])
    ax.plot(months, balance, color=COLORS["blue"], lw=2.2, label="Remaining Balance")
    ax.plot(months, cum_int, color=COLORS["red"], lw=1.8, label="Cumulative Interest")
    ax.plot(months, cum_prn, color=COLORS["green"], lw=1.8, label="Cumulative Principal")

    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")
    ax.set_title(title)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
    ax.legend(facecolor=COLORS["bg"], edgecolor=COLORS["grid"],
              labelcolor=COLORS["text"], fontsize=9)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_loan_breakdown(result: LoanResult, title: str = "Monthly Payment Breakdown",
                        save_path: str | None = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    _apply_theme(ax, fig)

    months = [r.month for r in result.schedule]
    princ = [r.principal_part for r in result.schedule]
    inter = [r.interest_part for r in result.schedule]

    ax.bar(months, princ, color=COLORS["green"], alpha=0.85, label="Principal", width=0.8)
    ax.bar(months, inter, bottom=princ, color=COLORS["red"], alpha=0.85, label="Interest", width=0.8)

    ax.set_xlabel("Month")
    ax.set_ylabel("Payment")
    ax.set_title(title)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
    ax.legend(facecolor=COLORS["bg"], edgecolor=COLORS["grid"],
              labelcolor=COLORS["text"], fontsize=9)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_time_value(amount: float, rate: float, max_years: int,
                    title: str = "Time Value of Money",
                    save_path: str | None = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    _apply_theme(ax, fig)

    yr, fv, pv = TimeValue.time_curve(amount, rate, max_years)

    ax.fill_between(yr, fv, alpha=0.06, color=COLORS["blue"])
    ax.fill_between(yr, pv, alpha=0.06, color=COLORS["red"])
    ax.plot(yr, fv, color=COLORS["blue"], lw=2.2, label="Future Value")
    ax.plot(yr, pv, color=COLORS["red"], lw=2.2, label="Present Value")
    ax.axhline(amount, color=COLORS["yellow"], lw=1.2, ls="--", label="Amount")

    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    ax.set_title(title)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(_currency_formatter))
    ax.legend(facecolor=COLORS["bg"], edgecolor=COLORS["grid"],
              labelcolor=COLORS["text"], fontsize=9)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_percentage_pie(part: float, total: float,
                        title: str = "Percentage Breakdown",
                        save_path: str | None = None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(5, 5))
    fig.set_facecolor(COLORS["bg"])
    ax.set_facecolor(COLORS["bg"])

    remaining = max(total - part, 0)
    sizes = [part, remaining]
    labels = [f"Part: {part:,.0f}", f"Remaining: {remaining:,.0f}"]
    colors = [COLORS["blue"], COLORS["red"]]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.1f%%",
        startangle=90, pctdistance=0.75,
        wedgeprops={"edgecolor": COLORS["bg"], "linewidth": 2},
    )
    for t in texts:
        t.set_color(COLORS["text"])
        t.set_fontsize(10)
    for t in autotexts:
        t.set_color("#fff")
        t.set_fontsize(10)
        t.set_fontweight(600)

    centre = plt.Circle((0, 0), 0.55, fc=COLORS["bg"])
    ax.add_artist(centre)
    ax.text(0, 0, f"{part/total*100:.1f}%", ha="center", va="center",
            fontsize=18, fontweight=700, color=COLORS["blue"])

    ax.set_title(title, color=COLORS["text"], fontsize=12, fontweight=600, pad=16)
    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig
