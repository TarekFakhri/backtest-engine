"""
@File: moving_average_crossover.py

A simple moving average crossover strategy.

Buys when the short-term moving average crosses above the long-term moving average,
and sells when it crosses below.

@Author: Tarek Fakhri
@Created: 2025-06-17
"""

import pandas as pd
from backtest_engine.strategies.base_strategy import BaseStrategy


class MovingAverageCrossoverStrategy(BaseStrategy):
    """
    Moving Average Crossover Strategy.

    Buy Signal: Short MA crosses above Long MA
    Sell Signal: Short MA crosses below Long MA
    Hold: Otherwise
    """

    def __init__(self, prices: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> None:
        """
        Initialize strategy with price data and window lengths.

        Parameters:
        - prices (pd.DataFrame): OHLCV price data with 'Close' column
        - short_window (int): Lookback for short-term moving average
        - long_window (int): Lookback for long-term moving average
        """
        super().__init__(prices)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self) -> pd.Series:
        """
        Generate a Series of trading signals based on MA crossovers.

        Returns:
        - pd.Series of signals: 1 for buy, -1 for sell, 0 for hold
        """
        short_ma = self.prices['Close'].rolling(window=self.short_window, min_periods=1).mean()
        long_ma = self.prices['Close'].rolling(window=self.long_window, min_periods=1).mean()

        signal = pd.Series(0, index=self.prices.index)

        signal[short_ma > long_ma] = 1
        signal[short_ma < long_ma] = -1

        # Optional: Avoid redundant signals (i.e., hold if signal hasn't changed)
        signal = signal.where(signal != signal.shift(), 0)

        return signal

