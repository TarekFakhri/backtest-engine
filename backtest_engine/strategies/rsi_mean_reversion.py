"""
@File: rsi_mean_reversion.py

RSI-based mean reversion strategy:
Buy when RSI < 30, sell when RSI > 70

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

import pandas as pd
from backtest_engine.strategies.base_strategy import BaseStrategy


class RSIMeanReversionStrategy(BaseStrategy):
    def __init__(self, prices: pd.DataFrame, window: int = 14, low_threshold: float = 30, high_threshold: float = 70):
        super().__init__(prices)
        self.window = window
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.rsi = self._compute_rsi()
        self.indicators = {"RSI": self.rsi}

    def _compute_rsi(self) -> pd.Series:
        delta = self.prices["Close"].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(self.window).mean()
        avg_loss = loss.rolling(self.window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def generate_signals(self) -> pd.Series:
        signals = pd.Series(0, index=self.prices.index)

        signals[self.rsi < self.low_threshold] = 1  # BUY
        signals[self.rsi > self.high_threshold] = -1  # SELL

        return signals
