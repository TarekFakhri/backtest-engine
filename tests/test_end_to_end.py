"""
@File: test_end_to_end.py

Integration test to validate end-to-end execution of strategy, backtester, and metrics.

@Author: Tarek Fakhri
@Date: 2025-06-18
"""

import pandas as pd
from backtest_engine.strategies.moving_average_crossover import MovingAverageCrossoverStrategy
from backtest_engine.core.backtester import Backtester
from backtest_engine.metrics.evaluator import calculate_metrics


def test_mac_strategy_end_to_end():
    """
    Run a complete backtest and evaluate metrics on synthetic price data.
    """
    prices = pd.DataFrame({
        "Close": [10, 11, 12, 13, 12, 11, 10, 11, 12, 13, 14, 13, 12]
    }, index=pd.date_range("2023-01-01", periods=13))

    strategy = MovingAverageCrossoverStrategy(prices, short_window=2, long_window=3)
    backtester = Backtester(strategy, initial_cash=1000.0)
    result = backtester.run()
    metrics = calculate_metrics(result["portfolio_value"])

    assert isinstance(result, pd.DataFrame)
    assert "portfolio_value" in result.columns
    assert result.shape[0] == len(prices)

    assert metrics["Final Value"] > 0
    assert "CAGR" in metrics
    assert "Sharpe Ratio" in metrics
    assert "Max Drawdown" in metrics
