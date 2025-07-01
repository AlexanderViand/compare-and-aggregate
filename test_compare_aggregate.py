import pytest

from algorithms.aav86 import aav86_sort, aav86_sort_ca
from algorithms.maximum import max_two_iteration_valiant, max_two_iteration_ca
from algorithms.bitonic_sort import bitonic_sort
import random


# --- Test Data (Not yet currently used by tests) ---

UNIQUE_ITEMS = [3, 1, 4, 1, 5, 9, 2, 6]
REPEATED_ITEMS = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]


class StableItem:
    def __init__(self, value, id):
        self.value = value
        self.id = id

    def __repr__(self):
        return f"({self.value}, {self.id})"

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __rlt__(self, other):
        return other < self.value

    def __rle__(self, other):
        return other <= self.value

    def __req__(self, other):
        return other == self.value

    def __rne__(self, other):
        return other != self.value

    def __rgt__(self, other):
        return other > self.value

    def __rge__(self, other):
        return other >= self.value


STABLE_ITEMS = [
    StableItem(3, 0),
    StableItem(1, 1),
    StableItem(4, 2),
    StableItem(1, 3),
    StableItem(5, 4),
]

# --- Test Cases ---


@pytest.mark.parametrize(
    "input_list",
    [
        [],
        [5],
        [3, 1, 4, 1, 5, 9, 2, 6],
        REPEATED_ITEMS,
        [random.randint(0, 1000) for _ in range(100)],
    ],
)
def test_aav86_sort(input_list):
    k = 4  # AAV86 parameter, k > 1
    expected = sorted(input_list)
    actual = aav86_sort(input_list, k)
    assert actual == expected


@pytest.mark.parametrize(
    "input_list",
    [
        [],
        [5],
        [3, 1, 4, 1, 5, 9, 2, 6],
        REPEATED_ITEMS,
        [random.randint(0, 1000) for _ in range(100)],
    ],
)
def test_aav86_sort_ca(input_list):
    k = 4  # AAV86 parameter, k > 1
    expected = sorted(input_list)
    actual = aav86_sort_ca(input_list, k)
    assert actual == expected


def test_aav86_sort_stability():
    input_list = list(STABLE_ITEMS)
    k = 4
    sorted_list = aav86_sort(input_list, k)

    # Expected stable sort order: (1,1), (1,3), (3,0), (4,2), (5,4)
    expected_order = [
        StableItem(1, 1),
        StableItem(1, 3),
        StableItem(3, 0),
        StableItem(4, 2),
        StableItem(5, 4),
    ]
    assert sorted_list == expected_order


@pytest.mark.parametrize(
    "input_list",
    [
        [],
        [5],
        [3, 1, 4, 1, 5, 9, 2, 6],
        REPEATED_ITEMS,
        [random.randint(0, 1000) for _ in range(100)],
    ],
)
def test_max_two_iteration_valiant(input_list):
    expected = max(input_list) if input_list else None
    actual = max_two_iteration_valiant(input_list)
    assert actual == expected


@pytest.mark.parametrize(
    "input_list",
    [
        [],
        [5],
        [3, 1, 4, 1, 5, 9, 2, 6],
        REPEATED_ITEMS,
        [random.randint(0, 1000) for _ in range(100)],
    ],
)
def test_max_two_iteration_ca(input_list):
    expected = max(input_list) if input_list else None
    actual = max_two_iteration_ca(input_list)
    assert actual == expected


@pytest.mark.parametrize(
    "input_list",
    [
        [],
        [5],
        [3, 1, 4, 1, 5, 9, 2, 6],
        REPEATED_ITEMS,
        [random.randint(0, 1000) for _ in range(100)],
    ],
)
def test_bitonic_sort(input_list):
    # bitonic_sort sorts in-place, so make a copy
    list_copy = list(input_list)
    bitonic_sort(list_copy)
    assert list_copy == sorted(input_list)


def test_bitonic_sort_stability():
    input_list = list(STABLE_ITEMS)
    bitonic_sort(input_list)

    # Expected stable sort order: (1,1), (1,3), (3,0), (4,2), (5,4)
    expected_order = [
        StableItem(1, 1),
        StableItem(1, 3),
        StableItem(3, 0),
        StableItem(4, 2),
        StableItem(5, 4),
    ]
    assert input_list == expected_order
