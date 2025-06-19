"""
@File: run_mac_strategy.py

Run a full backtest using the Moving Average Crossover strategy.

@Author: Tarek Fakhri
@Created: 2025-06-18
"""

import pandas as pd
from backtest_engine.strategies.moving_average_crossover import MovingAverageCrossoverStrategy
from backtest_engine.core.backtester import Backtester
from backtest_engine.metrics.evaluator import calculate_metrics
from backtest_engine.visualization.plotter import plot_price_with_signals, plot_equity_curve


def main():
    # === 1. Create synthetic price data ===
    prices = pd.DataFrame({
        "Close": [10, 11, 12, 13, 12, 11, 10, 11, 12, 13, 14, 13, 12, 11, 12]
    }, index=pd.date_range("2023-01-01", periods=15))

    # === 2. Initialize and run strategy ===
    strategy = MovingAverageCrossoverStrategy(prices, short_window=3, long_window=5)
    signals = strategy.generate_signals()

    backtester = Backtester(strategy, initial_cash=1000)
    result_df = backtester.run()

    # === 3. Print metrics ===
    metrics = calculate_metrics(result_df["portfolio_value"])
    print("\nBacktest Performance Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # === 4. Plot results ===
    plot_price_with_signals(prices, signals)
    plot_equity_curve(result_df["portfolio_value"])


if __name__ == "__main__":
    main()
