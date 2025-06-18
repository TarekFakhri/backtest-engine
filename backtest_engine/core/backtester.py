"""
@File: backtester.py

Simulates the execution of a trading strategy over historical data.

@Author: Tarek Fakhri
@Date: 2025-06-18
"""

from typing import List, Dict
import pandas as pd
from backtest_engine.strategies.base_strategy import BaseStrategy


class Backtester:
    """
    Core backtesting engine for single-asset, daily-resolution strategies.
    """

    def __init__(self, strategy: BaseStrategy, initial_cash: float = 10000.0) -> None:
        """
        Initialize the backtester.

        Parameters:
        - strategy (BaseStrategy): The trading strategy to run
        - initial_cash (float): Starting portfolio value in cash
        """
        self.strategy = strategy
        self.prices = strategy.prices
        self.cash = initial_cash
        self.position = 0.0  # number of shares
        self.entry_price = None
        self.trade_log: List[Dict] = []
        self.portfolio_value = []

    def run(self) -> pd.DataFrame:
        """
        Run the backtest over the price data and strategy signals.

        Returns:
        - pd.DataFrame: Portfolio value and trades indexed by date
        """
        signals = self.strategy.generate_signals()
        for date, signal in signals.items():
            close_price = self.prices.loc[date, "Close"]

            # Buy signal
            if signal == 1 and self.position == 0:
                self.position = self.cash / close_price
                self.cash = 0.0
                self.entry_price = close_price
                self.trade_log.append({
                    "date": date,
                    "type": "BUY",
                    "price": close_price,
                    "shares": self.position,
                })

            # Sell signal
            elif signal == -1 and self.position > 0:
                self.cash = self.position * close_price
                self.trade_log.append({
                    "date": date,
                    "type": "SELL",
                    "price": close_price,
                    "shares": self.position,
                    "pnl": (close_price - self.entry_price) * self.position
                })
                self.position = 0.0
                self.entry_price = None

            # Track portfolio value
            value = self.cash + self.position * close_price
            self.portfolio_value.append((date, value))

        return self._build_result_df()

    def _build_result_df(self) -> pd.DataFrame:
        """
        Build the final portfolio value DataFrame.
        """
        df = pd.DataFrame(self.portfolio_value, columns=["date", "portfolio_value"])
        df.set_index("date", inplace=True)
        return df
