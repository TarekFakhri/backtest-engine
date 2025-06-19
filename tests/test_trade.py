"""
@File: test_trade.py

Unit tests for the Trade dataclass and its integration with Backtester.

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

import pandas as pd
from datetime import datetime
from backtest_engine.core.trade import Trade
from backtest_engine.core.backtester import Backtester
from backtest_engine.strategies.base_strategy import BaseStrategy


def test_trade_dataclass_instantiation():
    """
    Confirm that Trade objects are created with correct attributes.
    """
    t = Trade(date=datetime(2024, 1, 1), type="BUY", price=100.0, shares=10)
    assert t.type == "BUY"
    assert t.price == 100.0
    assert t.shares == 10
    assert t.pnl == 0.0


def test_backtester_trade_log_uses_trade_objects():
    """
    Confirm that Backtester appends Trade objects to trade_log.
    """
    class DummyStrategy(BaseStrategy):
        def generate_signals(self) -> pd.Series:
            s = pd.Series(0, index=self.prices.index)
            s.iloc[1] = 1   # BUY
            s.iloc[3] = -1  # SELL
            return s

    prices = pd.DataFrame({
        "Close": [100, 105, 110, 120, 115]
    }, index=pd.date_range("2024-01-01", periods=5))

    strategy = DummyStrategy(prices)
    backtester = Backtester(strategy, initial_cash=1000)
    result = backtester.run()

    trade_log = backtester.trade_log
    assert len(trade_log) == 2
    assert isinstance(trade_log[0], Trade)
    assert trade_log[0].type == "BUY"
    assert trade_log[1].type == "SELL"
    assert trade_log[1].pnl > 0
