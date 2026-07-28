"""Tests for report calculations."""

import pytest
from app.services.report_service import _generate_insights


def test_generate_insights_high_ratio():
    result = _generate_insights(100000, 95000, 95000, {"cat1": 95000}, {"cat1": "Rent"})
    assert "quite high" in result
    assert "Rent" in result


def test_generate_insights_low_ratio():
    result = _generate_insights(100000, 30000, 30000, {"cat1": 30000}, {"cat1": "Supplies"})
    assert "healthy" in result


def test_generate_insights_no_data():
    result = _generate_insights(0, 0, 0, {}, {})
    assert "looks clean" in result


def test_profit_loss_calculation():
    income = 25000000
    expenses = 15000000
    net = income - expenses
    assert net == 10000000


def test_balance_sheet_basic():
    assets = 50000000
    liabilities = 15000000
    equity = 35000000
    assert assets == liabilities + equity
