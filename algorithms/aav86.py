import math
import random
from algorithms.bitonic_sort import bitonic_sort
from compare_aggregate import (
    compare_aggregate,
    complete_graph,
    CompareAggregateFn,
)


def aav86_sort(x, k):
    """
    Implementation of Algorithm 1: AAV86 sorting from "Secure Sorting and
    Selection via Function Secret Sharing" by Agarwal et al. (2024), page 34.

    This algorithm is a variant of quicksort that uses multiple pivots.

    Args:
        x: A list of items to sort.
        k: The number of iterations parameter. The paper specifies k > 1 for the recursive step.
    """
    n = len(x)

    if n <= 1:
        return x

    # Line 1-5: Base case
    if k <= 1:
        # This part of the algorithm sorts using all pairwise comparisons.
        return bitonic_sort(x)

    # Line 6: Recursive case for k > 1

    # Line 7: Let p = floor(n^(1/k))
    p = math.floor(n ** (1 / k))

    # If p < 2, we cannot select p-1 pivots (if p=1, 0 pivots).
    # The list is not partitioned and we recurse with k-1, eventually hitting k=1.
    num_pivots = p - 1
    if num_pivots <= 0:
        return aav86_sort(x, k - 1)

    # Line 8: Sample uniformly (without replacement) a set P of indices for pivots.
    all_indices = list(range(n))
    P_indices = random.sample(all_indices, num_pivots)

    # Line 9: A = [n] \ P (non-pivots), B = P (pivots)
    xB = [x[i] for i in P_indices]
    A_indices = [i for i in all_indices if i not in P_indices]
    xA = [x[i] for i in A_indices]

    # Line 12: Reorder pivot elements to obtain u.
    u = bitonic_sort(xB)

    # Line 11: Partition non-pivot elements (xA) into p disjoint blocks.
    xA_partitions = [[] for _ in range(p)]
    for item_a in xA:
        # The rank of item_a is the number of pivots in u smaller than it.
        rank = 0
        for pivot_val in u:
            if item_a > pivot_val:
                rank += 1
        xA_partitions[rank].append(item_a)

    # Line 13: Recursively sort each partition.
    yA_partitions = []
    for i in range(p):
        yA_partitions.append(aav86_sort(xA_partitions[i], k - 1))

    # Line 14: Assemble the final sorted list.
    y = []
    for i in range(p):
        y.extend(yA_partitions[i])
        if i < len(u):
            y.append(u[i])

    # Line 15: Return y
    return y


def aav86_sort_ca(x, k, CompareAggregate: CompareAggregateFn = compare_aggregate):
    """
    Implementation of Algorithm 2: AAV86 sorting in the Compare-Aggregate model.
    (from Agarwal et al. 2024, page 35)
    """
    n = len(x)
    if n <= 1:
        return x

    # Line 1-5: Base case for k=1
    if k <= 1:
        # Line 2: Let H be a clique over V.
        H = complete_graph(n)
        # Line 3: Get local rank results from CompareAggregate.
        ranks = CompareAggregate(x, H)
        # Line 4: Reorder x based on the ranks to get the sorted list y.
        y = [None] * n
        for i, rank in enumerate(ranks):
            if rank < n:
                y[rank] = x[i]
        # Line 5: Return y
        return [item for item in y if item is not None]

    # Line 6: Recursive case for k > 1
    # Line 7: Let p = floor(n^(1/k))
    p = math.floor(n ** (1 / k))
    num_pivots = p - 1
    if num_pivots <= 0:
        return aav86_sort_ca(x, k - 1, CompareAggregate)

    # Line 8: Sample a set P of pivot indices.
    all_indices = list(range(n))
    P_indices = random.sample(all_indices, num_pivots)
    A_indices = [i for i in all_indices if i not in P_indices]

    # Line 9: Define the comparison graph H.
    # H is a complete bipartite graph between non-pivots (A) and pivots (B=P),
    # plus a clique on the pivots (B).
    H = []
    for i_a in A_indices:
        for i_p in P_indices:
            H.append(tuple(sorted((i_a, i_p))))
    for i in range(len(P_indices)):
        for j in range(i + 1, len(P_indices)):
            H.append(tuple(sorted((P_indices[i], P_indices[j]))))
    H = sorted(list(set(H)))

    # Line 10: Get local rank results from CompareAggregate.
    local_ranks = CompareAggregate(x, H)

    # Line 11: Partition non-pivot elements (xA) into p disjoint blocks.
    xA_partitions_by_idx = [[] for _ in range(p)]
    for idx in A_indices:
        rank = local_ranks[idx]
        if rank < p:
            xA_partitions_by_idx[rank].append(idx)

    # Line 12: Reorder pivot elements (xB) to obtain u.
    # This requires getting the ranks of pivots *among themselves*.
    # The local_ranks from the main CA call include comparisons with non-pivots,
    # so we run a smaller, separate CA call on just the pivots.
    pivots_only_graph = [e for e in H if e[0] in P_indices and e[1] in P_indices]
    pivot_items = [x[i] for i in P_indices]
    # The graph for the sub-call needs indices relative to the `pivot_items` list.
    pivots_relative_graph = [
        (P_indices.index(i), P_indices.index(j)) for i, j in pivots_only_graph
    ]
    pivot_ranks_within_pivots = CompareAggregate(pivot_items, pivots_relative_graph)

    sorted_pivots_indices_in_pivots_list = sorted(
        range(len(pivot_items)), key=lambda i: pivot_ranks_within_pivots[i]
    )
    u = [pivot_items[j] for j in sorted_pivots_indices_in_pivots_list]

    # Line 13: Recursively sort each partition of non-pivot elements.
    yA_partitions = []
    for i in range(p):
        partition_items = [x[j] for j in xA_partitions_by_idx[i]]
        yA_partitions.append(aav86_sort_ca(partition_items, k - 1, CompareAggregate))

    # Line 14: Assemble the final sorted list.
    y = []
    for i in range(p):
        y.extend(yA_partitions[i])
        if i < len(u):
            y.append(u[i])

    # Line 15: Return y
    return y


if __name__ == "__main__":
    # Example usage:
    data_to_sort = [random.randint(0, 1000) for _ in range(100)]
    print(f"Unsorted data (first 20 elements): {data_to_sort[:20]}")

    # The choice of k affects performance. The paper analyzes it as a parameter.
    # For n=100, let's try k=4. n^(1/4) is about 3.16, so p=3, and 2 pivots are chosen.
    k_parameter = 4
    print(f"Sorting with k={k_parameter}")
    sorted_data = aav86_sort(data_to_sort, k=k_parameter)
    sorted_data_ca = aav86_sort_ca(data_to_sort, k=k_parameter)

    print(f"Sorted data (first 20 elements): {sorted_data[:20]}")
    print(f"Sorted data CA (first 20 elements): {sorted_data_ca[:20]}")

    # Verification
    print(f"Verification against Python's built-in sorted()...")
    assert sorted_data == sorted(data_to_sort)
    assert sorted_data_ca == sorted(data_to_sort)
    print("Sort is correct.")
