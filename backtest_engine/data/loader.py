"""
@File: loader.py

Utilities for loading historical price data from Yahoo Finance.

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

import pandas as pd
import yfinance as yf


def load_yahoo_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Download historical daily price data from Yahoo Finance.

    Parameters:
    - ticker (str): e.g., 'AAPL', 'TSLA', 'BTC-USD'
    - start (str): 'YYYY-MM-DD'
    - end (str): 'YYYY-MM-DD'

    Returns:
    - pd.DataFrame with OHLCV columns, indexed by date
    """
    df = yf.download(ticker, start=start, end=end)
    df = df[["Open", "High", "Low", "Close", "Volume"]]
    df.dropna(inplace=True)
    return df
