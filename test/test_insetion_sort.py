import pytest
from insertion_sort import insertion_sort

def test_insertion_sort():
    data = [3, 2, 1, 5]
    sorted_data = insertion_sort(data.copy())
    assert sorted_data == [1, 2, 3, 5]

def test_insertion_sort_empty():
    assert insertion_sort([]) == []

def test_insertion_sort_sorted():
    data = [1, 2, 3]
    assert insertion_sort(data.copy()) == [1, 2, 3]
