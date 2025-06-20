"""
@File: plotter.py

Visualization utilities for backtest results.

@Author: Tarek Fakhri
@Date: 2025-06-18
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_price_with_signals(prices: pd.DataFrame, signals: pd.Series, indicators: dict = None) -> None:
    """
    Plot stock prices with buy/sell signals.

    Parameters:
    - prices (pd.DataFrame): Must contain 'Close', indexed by date
    - signals (pd.Series): Values {-1, 0, 1}, aligned with prices index
    """
    plt.figure(figsize=(12, 5))
    plt.plot(prices.index, prices["Close"], label="Close Price", linewidth=1.5)

    buy_signals = prices["Close"][signals == 1]
    sell_signals = prices["Close"][signals == -1]

    plt.scatter(buy_signals.index, buy_signals, label="Buy", marker="^", color="green", s=80)
    plt.scatter(sell_signals.index, sell_signals, label="Sell", marker="v", color="red", s=80)
    if indicators:
            for label, series in indicators.items():
                plt.plot(series.index, series, label=label, linestyle='--')

    plt.title("Price with Buy/Sell Signals")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_equity_curve(equity_curve: pd.Series) -> None:
    """
    Plot the portfolio equity curve over time.

    Parameters:
    - equity_curve (pd.Series): Indexed by date
    """
    plt.figure(figsize=(12, 4))
    plt.plot(equity_curve.index, equity_curve.values, label="Portfolio Value", color="blue", linewidth=1.5)

    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
