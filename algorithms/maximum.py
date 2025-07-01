import math
import random
from typing import Any
from compare_aggregate import (
    compare_direct,
    compare_aggregate,
    complete_graph,
    CompareAggregateFn,
)


def max_two_iteration_valiant(x: list) -> Any:
    """
    Implementation of Algorithm 5: Two iteration maximum finding in Valiant's model.
    (from Agarwal et al. 2024, page 56)
    """
    n = len(x)
    if n == 0:
        return None
    if n == 1:
        return x[0]

    # Line 1: Let t = n^(2/3) / 2^(1/3)
    t = max(1, int(n ** (2 / 3) / (2 ** (1 / 3))))
    if t > n:  # Ensure t is not greater than n, especially for small n
        t = n

    # Iteration 1:
    # Line 2: Split [n] into t consecutive disjoint parts A1, . . . , At
    partitions_indices = []
    current_idx = 0
    for i in range(t):
        if i < t - 1:
            part_size = math.floor(n / t)
        else:
            part_size = n - current_idx
        partitions_indices.append(list(range(current_idx, current_idx + part_size)))
        current_idx += part_size

    # Line 3: Let H1 = (V1, E1) be an undirected graph where node set V1 = [n]
    # and E1 s.t. every Ai individually forms a clique.
    H1_edges = []
    for part_indices in partitions_indices:
        for i_idx in range(len(part_indices)):
            for j_idx in range(i_idx + 1, len(part_indices)):
                H1_edges.append((part_indices[i_idx], part_indices[j_idx]))

    # Line 4: Let xiter-1 := x.
    x_iter1 = x

    # Line 5: Let {Ce}e∈E1 := Compare(xiter-1, H1), be the comparison results.
    ce_iter1 = compare_direct(x_iter1, H1_edges)

    # Iteration 2:
    # Line 6: Based on {Ce}e∈E1, select the indices k1, . . . , kt s.t. for all j∈ [t],
    # xiter-1 is the maximum element among {xiter-1}i∈Aj.
    max_elements_from_partitions = []
    for part_indices in partitions_indices:
        if not part_indices:
            continue
        current_max_val = x_iter1[part_indices[0]]
        current_max_idx = part_indices[0]
        for i_idx in range(len(part_indices)):
            for j_idx in range(i_idx + 1, len(part_indices)):
                if (part_indices[i_idx], part_indices[j_idx]) in ce_iter1:
                    if (
                        ce_iter1[(part_indices[i_idx], part_indices[j_idx])] == 1
                    ):  # x[i] > x[j]
                        if x_iter1[part_indices[i_idx]] > current_max_val:
                            current_max_val = x_iter1[part_indices[i_idx]]
                            current_max_idx = part_indices[i_idx]
                    else:  # x[j] > x[i]
                        if x_iter1[part_indices[j_idx]] > current_max_val:
                            current_max_val = x_iter1[part_indices[j_idx]]
                            current_max_idx = part_indices[j_idx]
                # Handle cases where comparison might not be explicitly in H1_edges if part_size is 1
                elif x_iter1[part_indices[i_idx]] > current_max_val:
                    current_max_val = x_iter1[part_indices[i_idx]]
                    current_max_idx = part_indices[i_idx]
        max_elements_from_partitions.append(current_max_val)

    # Line 7: Let H2 = (V2, E2) be an undirected graph where node set V2 = [t]
    # and edge set E2 forms a clique over V2.
    H2_edges = complete_graph(len(max_elements_from_partitions))

    # Line 8: Let xiter-2 := (max_elements_from_partitions)
    x_iter2 = max_elements_from_partitions

    # Line 9: Let {Ce}e∈E2 := Compare(xiter-2, H2), be the comparison results.
    ce_iter2 = compare_direct(x_iter2, H2_edges)

    # Output computation:
    # Line 10: Based on {Ce}e∈E2, find the index i* ∈ [t] s.t. xiter-2 is the maximum element among xiter-2.
    if not x_iter2:
        return None  # Should not happen if n > 0

    max_val = x_iter2[0]
    for i in range(len(x_iter2)):
        is_max = True
        for j in range(len(x_iter2)):
            if i == j:
                continue
            if (i, j) in ce_iter2 and ce_iter2[(i, j)] == 0:  # x_iter2[i] <= x_iter2[j]
                is_max = False
                break
            elif (j, i) in ce_iter2 and ce_iter2[
                (j, i)
            ] == 1:  # x_iter2[j] > x_iter2[i]
                is_max = False
                break
        if is_max:
            max_val = x_iter2[i]
            break  # Found the maximum

    # Line 11: Output xiter-2[i*] (the maximum element)
    return max_val


def max_two_iteration_ca(
    x: list, CompareAggregate: CompareAggregateFn = compare_aggregate
) -> Any:
    """
    Implementation of Algorithm 5: Two iteration maximum finding in the Compare-Aggregate model.
    (from Agarwal et al. 2024, page 56)
    """
    n = len(x)
    if n == 0:
        return None
    if n == 1:
        return x[0]

    # Line 1: Let t = n^(2/3) / 2^(1/3)
    t = max(1, int(n ** (2 / 3) / (2 ** (1 / 3))))
    if t > n:  # Ensure t is not greater than n, especially for small n
        t = n

    # Iteration 1:
    # Line 2: Split [n] into t consecutive disjoint parts A1, . . . , At
    partitions_indices = []
    current_idx = 0
    for i in range(t):
        if i < t - 1:
            part_size = math.floor(n / t)
        else:
            part_size = n - current_idx
        partitions_indices.append(list(range(current_idx, current_idx + part_size)))
        current_idx += part_size

    # Line 3: Let H1 = (V1, E1) be an undirected graph where node set V1 = [n]
    # and E1 s.t. every Ai individually forms a clique.
    H1_edges = []
    for part_indices in partitions_indices:
        for i_idx in range(len(part_indices)):
            for j_idx in range(i_idx + 1, len(part_indices)):
                H1_edges.append((part_indices[i_idx], part_indices[j_idx]))

    # Line 4: Let xiter-1 := x.
    x_iter1 = x

    # Line 5 (CA version): Let {Lrankv}v∈V1 := Compare-Aggregate(xiter-1, H1), be the local rank results.
    lrank_iter1 = CompareAggregate(x_iter1, H1_edges)

    # Iteration 2:
    # Line 6 (CA version): Based on {Lrankv}v∈V1, select the indices k1 ∈ A1, . . . , kt ∈ At
    # s.t. for all j ∈ [t], we have Lrankkj≥ Lranki for every i ∈ Aj.
    # This means finding the element with the highest local rank within each partition.
    max_elements_from_partitions = []
    for part_indices in partitions_indices:
        if not part_indices:
            continue
        # Find the index within the partition that has the maximum local rank
        max_lrank_in_part = -1
        max_lrank_idx_in_part = -1
        for original_idx in part_indices:
            if lrank_iter1[original_idx] > max_lrank_in_part:
                max_lrank_in_part = lrank_iter1[original_idx]
                max_lrank_idx_in_part = original_idx
        max_elements_from_partitions.append(x_iter1[max_lrank_idx_in_part])

    # Line 7: Let H2 = (V2, E2) be an undirected graph where node set V2 = [t]
    # and edge set E2 forms a clique over V2.
    H2_edges = complete_graph(len(max_elements_from_partitions))

    # Line 8: Let xiter-2 := (max_elements_from_partitions)
    x_iter2 = max_elements_from_partitions

    # Line 9 (CA version): Let {Lrankv}v∈V2 := Compare-Aggregate(xiter-2, H2), be the local rank results.
    lrank_iter2 = CompareAggregate(x_iter2, H2_edges)

    # Output computation:
    # Line 10 (CA version): Based on {Lrankv}v∈V2, find the index i* ∈ [t]
    # s.t. Lranki* > Lranki for all i ∈ [t].
    # This means finding the element with the highest local rank in the final set.
    if not x_iter2:
        return None  # Should not happen if n > 0

    max_lrank_final = -1
    max_lrank_idx_final = -1
    for i in range(len(lrank_iter2)):
        if lrank_iter2[i] > max_lrank_final:
            max_lrank_final = lrank_iter2[i]
            max_lrank_idx_final = i

    # Line 11: Output xiter-2[i*] (the maximum element)
    return x_iter2[max_lrank_idx_final]


if __name__ == "__main__":
    # Example usage for Two-Iteration Maximum Finding:
    data_for_max = [random.randint(0, 1000) for _ in range(50)]
    print(f"Data for Max (first 20 elements): {data_for_max[:20]}")

    max_valiant = max_two_iteration_valiant(data_for_max)
    max_ca = max_two_iteration_ca(data_for_max)
    expected_max = max(data_for_max)

    print(f"Max (Valiant): {max_valiant}")
    print(f"Max (CA): {max_ca}")
    print(f"Expected Max: {expected_max}")

    print(f"Verification against Python's built-in max()...")
    assert max_valiant == expected_max
    assert max_ca == expected_max
    print("Two-Iteration Maximum Finding is correct.")
