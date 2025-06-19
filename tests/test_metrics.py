"""
@File: test_metrics.py

Unit tests for the metrics evaluator.

@Author: Tarek Fakhri
@Date: 2025-06-18
"""

import pandas as pd
import numpy as np
from backtest_engine.metrics.evaluator import calculate_metrics


def test_metrics_on_rising_equity_curve():
    """
    Metrics for a perfectly rising portfolio (no drawdown, infinite Sharpe).
    """
    index = pd.date_range("2020-01-01", periods=252)
    values = pd.Series(np.linspace(1000, 2000, 252), index=index)
    
    metrics = calculate_metrics(values)

    assert metrics["Start Value"] == 1000
    assert metrics["Final Value"] == 2000
    assert metrics["Max Drawdown"] == 0.0
    assert metrics["CAGR"] > 0.0
    assert np.isnan(metrics["Sharpe Ratio"]) is False or isinstance(metrics["Sharpe Ratio"], float)


def test_metrics_on_flat_equity_curve():
    """
    Metrics for a flat portfolio (CAGR = 0, Sharpe undefined, no drawdown).
    """
    index = pd.date_range("2020-01-01", periods=252)
    values = pd.Series([1000.0] * 252, index=index)
    
    metrics = calculate_metrics(values)

    assert metrics["CAGR"] == 0.0
    assert np.isnan(metrics["Sharpe Ratio"]) or metrics["Sharpe Ratio"] == 0.0
    assert metrics["Max Drawdown"] == 0.0
    assert metrics["Final Value"] == 1000.0
