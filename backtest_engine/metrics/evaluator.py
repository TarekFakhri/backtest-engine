"""
@File: evaluator.py

Computes key performance metrics from portfolio equity curve.

@Author: Tarek Fakhri
@Date: 2025-06-18
"""

import numpy as np
import pandas as pd


def calculate_metrics(equity_curve: pd.Series) -> dict:
    """
    Compute common backtest metrics from a portfolio equity curve.

    Parameters:
    - equity_curve (pd.Series): Portfolio value indexed by date

    Returns:
    - dict: Metrics including CAGR, Sharpe, Max Drawdown
    """
    returns = equity_curve.pct_change().dropna()
    total_periods = (equity_curve.index[-1] - equity_curve.index[0]).days / 365.25

    cagr = (equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1 / total_periods) - 1

    sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) != 0 else np.nan

    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    return {
        "CAGR": round(cagr, 4),
        "Sharpe Ratio": round(sharpe, 4),
        "Max Drawdown": round(max_drawdown, 4),
        "Final Value": round(equity_curve.iloc[-1], 2),
        "Start Value": round(equity_curve.iloc[0], 2),
    }
