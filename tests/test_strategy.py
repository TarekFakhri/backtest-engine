"""
@File: test_strategy.py

Unit tests for the BaseStrategy interface and its requirements.

@Author: Tarek Fakhri
@Date: 2025-06-17
"""

import pytest
import pandas as pd
from backtest_engine.strategies.base_strategy import BaseStrategy


def test_base_strategy_cannot_be_instantiated():
    """
    Ensure that BaseStrategy cannot be instantiated directly.
    """
    with pytest.raises(TypeError):
        BaseStrategy(pd.DataFrame({'Close': [1, 2, 3]}))


def test_missing_close_column_raises_error():
    """
    Ensure that price data missing required columns raises ValueError.
    """
    class DummyStrategy(BaseStrategy):
        def generate_signals(self) -> pd.Series:
            return pd.Series([0] * len(self.prices), index=self.prices.index)

    with pytest.raises(ValueError, match="Missing required columns"):
        DummyStrategy(pd.DataFrame({'Open': [1, 2, 3]}))


def test_generate_signals_returns_valid_series():
    """
    Ensure that a valid subclass returns a correctly shaped signal Series.
    """
    class DummyStrategy(BaseStrategy):
        def generate_signals(self) -> pd.Series:
            return pd.Series([1, 0, -1], index=self.prices.index)

    prices = pd.DataFrame({'Close': [100, 101, 102]}, index=pd.date_range("2024-01-01", periods=3))
    strategy = DummyStrategy(prices)
    signals = strategy.generate_signals()

    assert isinstance(signals, pd.Series)
    assert set(signals).issubset({-1, 0, 1})
    assert all(signals.index == prices.index)

