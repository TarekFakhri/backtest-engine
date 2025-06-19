"""
@File: portfolio.py

Encapsulates portfolio state and logic for managing cash, positions, and valuation.

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

from typing import Optional


class Portfolio:
    """
    Represents a simple long-only portfolio of a single asset.

    Tracks cash, share count, and entry price.
    """

    def __init__(self, initial_cash: float = 10000.0):
        self.cash = initial_cash
        self.position = 0.0  # number of shares
        self.entry_price: Optional[float] = None

    def buy(self, price: float) -> None:
        """
        Executes a full allocation BUY at the given price.
        """
        if self.position == 0:
            self.position = self.cash / price
            self.entry_price = price
            self.cash = 0.0

    def sell(self, price: float) -> float:
        """
        Executes a full liquidation SELL at the given price.

        Returns:
        - Realized profit/loss
        """
        if self.position > 0:
            pnl = (price - self.entry_price) * self.position
            self.cash = self.position * price
            self.position = 0.0
            self.entry_price = None
            return pnl
        return 0.0

    def value(self, price: float) -> float:
        """
        Computes total portfolio value given the current price.

        Returns:
        - float: cash + position * price
        """
        return self.cash + self.position * price
