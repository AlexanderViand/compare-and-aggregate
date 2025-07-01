"""Untested AI-generated code for CA-based algorithms that might or might not actually correspond to the algorithms in the paper."""

import random
from typing import Any, Callable, List, Tuple
from compare_aggregate import (
    compare_aggregate,
    complete_graph,
    CompareAggregateFn,
)


# --- 5. GENERIC COMPARE-AGGREGATE PARALLEL SELECTION ---


def parallel_selection_CA(
    x: List[Any],
    k: int,
    rounds: int,
    CompareAggregate: CompareAggregateFn = compare_aggregate,
) -> Any:
    """
    Generic parallel selection in `r` rounds (as in Table 3, using CA).

    In each round, it uses a CA comparison graph to partition and reduce the
    set of candidates. After `rounds-1` rounds, it selects the k-th element
    from the small remaining set.

    Args:
        x: A list of elements.
        k: The desired rank (0-based).
        rounds: The number of parallel rounds.
        CompareAggregate: The Compare-Aggregate function to use.

    Returns:
        The k-th smallest element.
    """
    S = x[:]
    for r in range(rounds - 1):
        if len(S) <= max(k, 2):
            break

        # Sample pivots to partition the current set S
        num_pivots = max(2, int(len(S) ** (1.0 / (rounds - r))))
        pivots = random.sample(S, min(num_pivots, len(S)))

        # Use CA to compare every element in S to every pivot
        H = [(i, j) for i in range(len(S)) for j in range(len(pivots))]
        # The ranks are computed on the combined list of S and pivots
        local_ranks = CompareAggregate(S + pivots, H)

        # Prune S based on the ranks. A naive approach is to keep the
        # candidates with the lowest ranks relative to the pivots.
        paired = sorted(zip(S, local_ranks[: len(S)]), key=lambda t: t[1])
        S = [xi for xi, rank in paired[: max(k, 2)]]

    # Final selection among the remaining candidates in S
    if not S:
        return None  # Should not happen with valid inputs
    if len(S) == 1:
        return S[0]

    H_final = complete_graph(len(S))
    ranks = CompareAggregate(S, H_final)
    # The desired element is the one with rank k-1 in the final set
    try:
        idx = ranks.index(k - 1)
        return S[idx]
    except (ValueError, IndexError):
        # Fallback for edge cases
        return sorted(S)[k - 1 if k > 0 else 0]


# --- 6. SORTED TOP-k VIA ROUNDS (Braverman et al.) ---


def sorted_top_k_parallel_CA(
    x: List[Any],
    k: int,
    rounds: int,
    CompareAggregate: CompareAggregateFn = compare_aggregate,
) -> List[Any]:
    """
    Computes sorted top-k in `r` rounds, inspired by Braverman et al. [21].

    Args:
        x: A list of elements.
        k: The number of top elements to find.
        rounds: The number of parallel rounds.
        CompareAggregate: The Compare-Aggregate function to use.

    Returns:
        A sorted list of the top `k` elements.
    """
    S = x[:]
    for r in range(rounds - 1):
        if len(S) <= k:
            break
        # Use random pivots to parallelize, similar to parallel sort
        num_pivots = max(2, int(len(S) ** (1.0 / (rounds - r))))
        pivots = random.sample(S, min(num_pivots, len(S)))

        # Partition S via CA by comparing every element to every pivot
        H = [(i, j) for i in range(len(S)) for j in range(len(pivots))]
        local_ranks = CompareAggregate(S + pivots, H)
        paired = sorted(zip(S, local_ranks[: len(S)]), key=lambda t: t[1])
        # Keep the top candidates
        S = [xi for xi, rank in paired[: max(k, 2)]]

    # Final CA-sort on the reduced set to get the sorted top-k
    if not S:
        return []
    H_final = complete_graph(len(S))
    ranks = CompareAggregate(S, H_final)
    result = [None] * min(k, len(S))
    for idx, r in enumerate(ranks):
        if r < k:
            result[r] = S[idx]
    return [item for item in result if item is not None]


def sorted_top_k_braverman_CA(
    x: List[Any],
    k: int,
    r: int,
    CompareAggregate: CompareAggregateFn = compare_aggregate,
) -> List[Any]:
    """
    Sorted top-k in `r` rounds (CA-model), following Braverman et al. [21].
    (See Table 3, App. B.4 of Agarwal et al. 2024)

    Args:
        x: A list of elements.
        k: The number of top elements to find.
        r: The number of rounds.
        CompareAggregate: The Compare-Aggregate function to use.

    Returns:
        A sorted list of the top `k` elements.
    """
    S = x[:]
    for _ in range(r):
        if len(S) <= k:
            break
        # Partition into O(k^0.5) buckets using random pivots
        num_pivots = min(int(k**0.5), len(S))
        if num_pivots == 0 and len(S) > 0:
            num_pivots = 1
        pivots = sorted(random.sample(S, num_pivots))

        # Partition S into blocks by pivots (use CA bipartite graph)
        biclique = [(i, j) for i in range(len(S)) for j in range(len(pivots))]
        ranks = CompareAggregate(S + pivots, biclique)

        # Filter to keep elements likely in top-k
        S = [xi for i, xi in enumerate(S) if ranks[i] < k]

    # Final CA-sort to get the precise top-k
    if not S:
        return []
    H_final = complete_graph(len(S))
    ranks = CompareAggregate(S, H_final)
    top_k_pairs = sorted(
        [(S[i], r) for i, r in enumerate(ranks) if r < k], key=lambda item: item[1]
    )
    return [item[0] for item in top_k_pairs]


def median_BB90_4iter_CA(
    x: List[Any], CompareAggregate: CompareAggregateFn = compare_aggregate
) -> Any:
    """
    4-iteration BB90 median algorithm (CA version).
    (App. B.2, Alg. 8, p. 64 of Agarwal et al. 2024)

    Args:
        x: A list of elements.
        CompareAggregate: The Compare-Aggregate function to use.

    Returns:
        The median of the list `x`.
    """
    n = len(x)
    if n <= 5:
        return select_kth_CA(x, n // 2, CompareAggregate)

    # 1. Sample S (size sqrt(n)) and T (size n^(2/3))
    s_size = int(n**0.5)
    t_size = int(n ** (2 / 3))
    all_indices = list(range(n))
    random.shuffle(all_indices)
    S_indices = all_indices[:s_size]
    T_indices = all_indices[s_size : s_size + t_size]
    S = [x[i] for i in S_indices]
    T = [x[i] for i in T_indices]

    # 2. CA-sort S to find markers x1 and x2
    S_sorted = sorted_top_k_CA(S, len(S), CompareAggregate)
    x1 = S_sorted[len(S) // 2 - int(len(S) ** 0.5)]
    x2 = S_sorted[len(S) // 2 + int(len(S) ** 0.5)]

    # 3. Filter X to get elements U between markers x1 and x2
    U = [xi for xi in x if x1 <= xi <= x2]
    if len(U) > 4 * n**0.75:
        # Fallback to full CA-selection if U is too large
        return select_kth_CA(x, n // 2, CompareAggregate)

    # 4. CA-sort T to find markers y1 and y2
    T_sorted = sorted_top_k_CA(T, len(T), CompareAggregate)
    y1 = T_sorted[len(T) // 2 - int(len(T) ** 0.5)]
    y2 = T_sorted[len(T) // 2 + int(len(T) ** 0.5)]

    # 5. Partition T to get V between markers y1 and y2
    V = [ti for ti in T if y1 <= ti <= y2]

    # 6. Take m markers Z from V and compare U with them
    m = int(n**0.25)
    if m < 2:
        m = 2
    if len(V) < m:
        Z = V
    else:
        Z = [V[int(i * len(V) / m)] for i in range(m)]

    if not Z:  # If V was empty, Z will be empty.
        # Fallback to sorting U if there are no markers in Z.
        return select_kth_CA(U, len(U) // 2, CompareAggregate)

    # Compare U with markers Z. This step is simplified in the paper.
    # A full implementation would use the ranks to find a smaller window for the median.
    # For this implementation, we proceed to sort the filtered set U.
    if len(U) > 4 * n**0.75:
        return select_kth_CA(U, len(U) // 2, CompareAggregate)

    # 7. Final CA-clique on U to find the median
    return select_kth_CA(U, len(U) // 2, CompareAggregate)


def max_four_iteration_CA(
    x: List[Any], CompareAggregate: CompareAggregateFn = compare_aggregate
) -> Any:
    """
    4-iteration maximum finding algorithm (CA model, Algorithm 7, p. 60).

    Args:
        x: A list of elements.
        CompareAggregate: The Compare-Aggregate function to use.

    Returns:
        The maximum element in the list `x`.
    """
    n = len(x)
    p_size = int(n ** (1 / 3))
    if n <= 1 or p_size < 2:
        return max(x) if x else None

    # 1. Sample p pivots and find their maximum using a CA clique.
    pivot_indices = random.sample(range(n), p_size)
    pivots = [x[i] for i in pivot_indices]
    H_piv = complete_graph(len(pivots))
    ranks_piv = CompareAggregate(pivots, H_piv)
    max_rank = max(ranks_piv)
    max_idx_in_pivots = ranks_piv.index(max_rank)
    pivot_max = pivots[max_idx_in_pivots]

    # 2. Filter elements greater than the pivot_max.
    survivors = [xi for xi in x if xi > pivot_max]
    if not survivors:
        return pivot_max

    # 3. Apply a 2-iteration max algorithm on the survivors.
    m = len(survivors)
    t = max(2, int(m**0.5))
    group_size = (m + t - 1) // t
    groups = [
        survivors[i * group_size : min(m, (i + 1) * group_size)] for i in range(t)
    ]

    maxima = []
    for g in groups:
        if not g:
            continue
        H = complete_graph(len(g))
        ranks = CompareAggregate(g, H)
        max_rank_in_group = max(ranks)
        idx = ranks.index(max_rank_in_group)
        maxima.append(g[idx])

    if not maxima:
        return pivot_max  # Should not be reached if survivors is not empty

    # Final round: find the maximum of the group maxima.
    H2 = complete_graph(len(maxima))
    ranks2 = CompareAggregate(maxima, H2)
    max_rank_final = max(ranks2)
    idx2 = ranks2.index(max_rank_final)
    return maxima[idx2]
