"""
@File: test_portfolio.py

Unit tests for the Portfolio class logic.

@Author: Tarek Fakhri
@Date: 2025-06-19
"""

from backtest_engine.core.portfolio import Portfolio


def test_portfolio_buy_and_value():
    """
    Buying a full position should zero out cash and set correct position.
    """
    p = Portfolio(initial_cash=1000.0)
    p.buy(price=100.0)

    assert p.position == 10.0
    assert p.cash == 0.0
    assert p.entry_price == 100.0
    assert p.value(price=100.0) == 1000.0


def test_portfolio_sell_and_pnl():
    """
    Selling a position should return correct PnL and reset state.
    """
    p = Portfolio(initial_cash=1000.0)
    p.buy(price=100.0)
    pnl = p.sell(price=110.0)

    assert pnl == 100.0
    assert p.position == 0.0
    assert p.cash == 1100.0
    assert p.entry_price is None
    assert p.value(price=110.0) == 1100.0


def test_sell_without_position_returns_zero():
    """
    Selling with no position should return zero PnL and not throw.
    """
    p = Portfolio(initial_cash=1000.0)
    pnl = p.sell(price=120.0)

    assert pnl == 0.0
    assert p.cash == 1000.0
    assert p.position == 0.0
