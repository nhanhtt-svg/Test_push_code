import pytest
from decimal import Decimal

from apps.demo_yapf import Calculator, OrderItem, order_total


def test_calculator_store_recall_clear():
    c = Calculator()
    c.store(12.5)
    assert c.recall() == 12.5
    c.clear()
    assert c.recall() == 0.0


def test_order_total_no_discount():
    items = [
        OrderItem(sku="A", qty=2, unit_price=Decimal("10.00")),
        OrderItem(sku="B", qty=1, unit_price=Decimal("5.50")),
    ]
    assert order_total(items) == Decimal("25.50")


def test_order_total_with_discount():
    items = [OrderItem(sku="A", qty=2, unit_price=Decimal("10.00"))]
    assert order_total(items, discount_rate=Decimal("0.1")) == Decimal("18.00")


def test_order_item_negative_qty_raises():
    it = OrderItem(sku="X", qty=-1, unit_price=Decimal("1.00"))
    with pytest.raises(ValueError):
        it.line_total()
