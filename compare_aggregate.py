"""
This module implements secure sorting and selection algorithms based on the
Function Secret Sharing (FSS) paper, "Secure sorting and selection via function
secret sharing," by Agarwal et al. (2024).

The implementations include variants for both Valiant's model and the
Compare-Aggregate (CA) model. The CA model assumes the existence of a
`CompareAggregate` function with the following signature:

def CompareAggregate(x: List[Any], H: List[Tuple[int, int]]) -> List[int]

This module provides a trivial, cleartext version of this function,
`CompareAggregate_trivial`, for demonstration and testing purposes.
"""

from typing import Any, Callable, List, Tuple

# Type alias for the CompareAggregate function
CompareAggregateFn = Callable[[List[Any], List[Tuple[int, int]]], List[int]]


def compare_direct(x: list, H: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
    """
    Helper function to simulate the Compare operation for Valiant's model.
    Returns a dictionary of comparison results for each edge in H.
    Ce = 1 if x[i] > x[j], 0 otherwise.
    """
    results = {}
    for i, j in H:
        results[(i, j)] = 1 if x[i] > x[j] else 0
    return results


def compare_aggregate(x: List[Any], H: List[Tuple[int, int]]) -> List[int]:
    """
    A trivial, cleartext implementation of the CompareAggregate function.

    This function computes the rank of each element in `x` based on the
    comparisons defined by the graph `H`. The rank is the number of elements
    it is greater than. This is a "stable" ranking, meaning that ties are
    broken by the original index.

    Args:
        x: A list of elements to compare.
        H: A list of tuples representing the edges of the comparison graph.

    Returns:
        A list of integers representing the local rank of each element.
    """
    n = len(x)
    local_rank = [0] * n
    for i, j in H:
        if x[i] > x[j] or (x[i] == x[j] and i > j):
            local_rank[i] += 1
        else:
            local_rank[j] += 1
    return local_rank


def complete_graph(n: int) -> List[Tuple[int, int]]:
    """
    Generates a list of edges representing a complete graph on `n` vertices.

    Args:
        n: The number of vertices.

    Returns:
        A list of tuples, where each tuple is an edge (i, j) with i < j.
    """
    return [(i, j) for i in range(n) for j in range(i + 1, n)]
