"""
@File: base_strategy.py

Abstract base class for trading strategies.

Defines the interface that all user-defined strategies must implement
in order to be compatible with the backtesting engine.

@Author: Tarek Fakhri
@Date: 2025-06-17
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.

    Any subclass must implement the `generate_signals` method,
    which receives a DataFrame of historical price data and returns
    a Series of signals with values:
        1  -> Buy
        0  -> Hold
       -1  -> Sell
    """

    def __init__(self, prices: pd.DataFrame) -> None:
        """
        Initialize the strategy with historical price data.

        Parameters:
        - prices (pd.DataFrame): Historical OHLCV data indexed by date,
                                 with at least a 'Close' column.
        """
        self.prices = prices.copy()
        self._validate_prices()

    @abstractmethod
    def generate_signals(self) -> pd.Series:
        """
        Generate a time-indexed Series of trade signals.

        Returns:
        - pd.Series: Signal values (1, 0, -1) aligned with prices index.
        """
        pass

    def _validate_prices(self) -> None:
        """
        Validate that the price DataFrame contains required columns.
        Raises an exception if validation fails.
        """
        required_columns = {'Close'}
        missing = required_columns - set(self.prices.columns)
        if missing:
            raise ValueError(f"Missing required columns in price data: {missing}")

