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
    - pd.DataFrame with OHLCV columns including 'Close', indexed by date
    """
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)

    # If MultiIndex columns, flatten them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Now standard processing
    if "Adj Close" in df.columns and "Close" not in df.columns:
        df.rename(columns={"Adj Close": "Close"}, inplace=True)

    if df.empty:
        raise ValueError(f"No data returned for {ticker} between {start} and {end}.")

    if "Close" not in df.columns:
        raise ValueError("No 'Close' column found in data.")

    expected_cols = ["Open", "High", "Low", "Close", "Volume"]
    df = df[[col for col in expected_cols if col in df.columns]]
    df.dropna(inplace=True)

    return df