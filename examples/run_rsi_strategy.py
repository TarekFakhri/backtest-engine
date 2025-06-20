"""
@File: run_rsi_strategy.py

Run a full backtest using the RSI Mean Reversion Strategy on real market data.

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

import pandas as pd
from backtest_engine.data.loader import load_yahoo_data
from backtest_engine.strategies.rsi_mean_reversion import RSIMeanReversionStrategy
from backtest_engine.core.backtester import Backtester
from backtest_engine.metrics.evaluator import calculate_metrics
from backtest_engine.visualization.plotter import plot_price_with_signals, plot_equity_curve


def main():
    ticker = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    prices = load_yahoo_data(ticker, start=start_date, end=end_date)

    strategy = RSIMeanReversionStrategy(prices, window=14, low_threshold=30, high_threshold=70)
    signals = strategy.generate_signals()

    backtester = Backtester(strategy, initial_cash=10000)
    result_df = backtester.run()

    metrics = calculate_metrics(result_df["portfolio_value"])
    print(f"\nRSI Backtest Results for {ticker} ({start_date} to {end_date}):")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    plot_price_with_signals(prices, signals, indicators=strategy.indicators)
    plot_equity_curve(result_df["portfolio_value"])


if __name__ == "__main__":
    main()
