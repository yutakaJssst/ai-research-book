# 第6章6.5節で説明したAI生成テスト（7件のうち、正常、境界、異常を代表する3件）
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
