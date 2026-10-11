# 第6章6.5節に掲載したテスト（本文と同一。生成された7件のうち掲載した3件）
import pytest
from stats import calculate_average


def test_average_normal():
    # normal case: average of three values
    assert calculate_average([1.0, 2.0, 3.0]) == 2.0


def test_average_single():
    # boundary case: a single value
    assert calculate_average([5.0]) == 5.0


def test_average_empty():
    # error case: empty list raises ValueError
    with pytest.raises(ValueError):
        calculate_average([])
