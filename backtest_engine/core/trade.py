"""
@File: trade.py

Dataclass for standardized trade record-keeping.

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    """
    Represents a single executed trade.

    Attributes:
    - date (datetime): Date of the trade
    - type (str): 'BUY' or 'SELL'
    - price (float): Execution price
    - shares (float): Number of shares traded
    - pnl (float): Realized profit/loss (only for SELL trades)
    """
    date: datetime
    type: str
    price: float
    shares: float
    pnl: float = 0.0
