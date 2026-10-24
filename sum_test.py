import pytest
from sum import sum

def test_sum():
    x = sum(5, 5)

    assert x == 10