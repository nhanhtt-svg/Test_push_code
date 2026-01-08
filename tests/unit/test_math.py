import pytest

from apps.demo_yapf import add, moving_average, safe_divide, top_n, total_positive


def test_add():
    assert add(1, 2) == 3


def test_safe_divide_ok():
    assert safe_divide(10, 2) == 5


def test_safe_divide_zero_raises():
    with pytest.raises(ValueError):
        safe_divide(1, 0)


def test_total_positive():
    assert total_positive([1, -2, 3, 0, -5]) == 4


def test_moving_average():
    assert moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]


def test_top_n():
    assert top_n([5, 1, 9, 2], 2) == [9, 5]
