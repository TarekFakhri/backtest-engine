"""
@File: backtester.py

Simulates the execution of a trading strategy over historical data.

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

from typing import List
import pandas as pd
from backtest_engine.strategies.base_strategy import BaseStrategy
from backtest_engine.core.trade import Trade
from backtest_engine.core.portfolio import Portfolio


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
        self.portfolio = Portfolio(initial_cash)
        self.trade_log: List[Trade] = []
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

            if signal == 1:
                if self.portfolio.position == 0:
                    self.portfolio.buy(close_price)
                    self.trade_log.append(Trade(
                        date=date,
                        type="BUY",
                        price=close_price,
                        shares=self.portfolio.position
                    ))

            elif signal == -1:
                if self.portfolio.position > 0:
                    pnl = self.portfolio.sell(close_price)
                    self.trade_log.append(Trade(
                        date=date,
                        type="SELL",
                        price=close_price,
                        shares=0.0,  # After sell, no position held
                        pnl=pnl
                    ))

            # Track value every day
            self.portfolio_value.append((date, self.portfolio.value(close_price)))

        return self._build_result_df()

    def _build_result_df(self) -> pd.DataFrame:
        """
        Build the final portfolio value DataFrame.
        """
        df = pd.DataFrame(self.portfolio_value, columns=["date", "portfolio_value"])
        df.set_index("date", inplace=True)
        return df
