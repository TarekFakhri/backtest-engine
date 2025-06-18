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

def test_moving_average_crossover_strategy_basic():
    """
    Ensure MovingAverageCrossoverStrategy returns valid signals.
    """
    from backtest_engine.strategies.moving_average_crossover import MovingAverageCrossoverStrategy

    # Create fake data with a known crossover pattern
    prices = pd.DataFrame({
        'Close': [10, 11, 12, 13, 14, 13, 12, 11, 10, 9, 10, 11, 12, 13, 14]
    }, index=pd.date_range("2024-01-01", periods=15))

    strategy = MovingAverageCrossoverStrategy(prices, short_window=3, long_window=5)
    signals = strategy.generate_signals()

    assert isinstance(signals, pd.Series)
    assert set(signals).issubset({-1, 0, 1})
    assert all(signals.index == prices.index)
    assert len(signals) == len(prices)

    # Spot-check that there is at least one buy and one sell
    assert (signals == 1).sum() > 0
    assert (signals == -1).sum() > 0

def test_moving_average_crossover_strategy_logic():
    """
    Validate that the strategy detects actual MA crossovers.
    """
    from backtest_engine.strategies.moving_average_crossover import MovingAverageCrossoverStrategy

    # Simple pattern: flat, rising, falling — will cause crossover events
    prices = pd.DataFrame({
        'Close': [10, 10, 10, 10, 10, 12, 14, 16, 18, 20, 19, 17, 15, 13, 11]
    }, index=pd.date_range("2024-01-01", periods=15))

    short_window = 3
    long_window = 5

    strategy = MovingAverageCrossoverStrategy(prices, short_window, long_window)
    signals = strategy.generate_signals()

    # Get MAs manually
    short_ma = prices['Close'].rolling(window=short_window, min_periods=1).mean()
    long_ma = prices['Close'].rolling(window=long_window, min_periods=1).mean()

    # Manually derive expected signals
    expected_signals = pd.Series(0, index=prices.index)
    expected_signals[short_ma > long_ma] = 1
    expected_signals[short_ma < long_ma] = -1
    expected_signals = expected_signals.where(expected_signals != expected_signals.shift(), 0)

    # Ensure exact match
    pd.testing.assert_series_equal(signals, expected_signals)
