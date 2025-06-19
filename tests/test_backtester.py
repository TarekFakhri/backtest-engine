"""
@File: test_backtester.py

Unit tests for the Backtester core engine.

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

import pandas as pd
from backtest_engine.core.backtester import Backtester
from backtest_engine.strategies.base_strategy import BaseStrategy


class DummyStrategy(BaseStrategy):
    """
    A minimal strategy that buys on day 2 and sells on day 4.
    """
    def generate_signals(self) -> pd.Series:
        signals = pd.Series(0, index=self.prices.index)
        signals.iloc[1] = 1   # Buy
        signals.iloc[3] = -1  # Sell
        return signals


def test_backtester_executes_trades_correctly():
    """
    Run the backtester on a controlled price + signal pattern.
    """
    prices = pd.DataFrame({
        'Close': [100, 105, 110, 120, 115]
    }, index=pd.date_range("2024-01-01", periods=5))

    strategy = DummyStrategy(prices)
    backtester = Backtester(strategy, initial_cash=1000)
    result = backtester.run()

    # Assert correct shape of result
    assert isinstance(result, pd.DataFrame)
    assert "portfolio_value" in result.columns
    assert len(result) == 5

    # Validate expected trade outcomes
    trade_log = backtester.trade_log
    assert len(trade_log) == 2
    assert trade_log[0].type == "BUY"
    assert trade_log[0].price == 105
    assert trade_log[1].type == "SELL"
    assert trade_log[1].price == 120

    # Check portfolio value at final step (should be fully in cash after sell)
    final_value = result["portfolio_value"].iloc[-1]
    expected_cash = 1000 / 105 * 120
    assert abs(final_value - expected_cash) < 1e-6
