from math import log2, ceil


def _compare_swap(a, i, j, direction=True):
    """Swap a[i] and a[j] if they are out of order with respect to *direction*.
    direction=True  ⇒   ascending
    direction=False ⇒   descending
    """
    if (a[i] > a[j]) == direction:
        a[i], a[j] = a[j], a[i]


def _bitonic_merge(a, lo, length, direction):
    """Merge the two halves of a bitonic sequence in *a[lo : lo+length]*."""
    if length > 1:
        k = length // 2
        for i in range(lo, lo + k):
            _compare_swap(a, i, i + k, direction)
        _bitonic_merge(a, lo, k, direction)
        _bitonic_merge(a, lo + k, k, direction)


def _bitonic_sort(a, lo, length, direction):
    """Recursively build a bitonic sequence, then sort it with _bitonic_merge."""
    if length > 1:
        k = length // 2
        _bitonic_sort(a, lo, k, True)  # first half  ascending
        _bitonic_sort(a, lo + k, k, False)  # second half descending
        _bitonic_merge(a, lo, length, direction)


def bitonic_sort(arr):
    """
    Sort *arr* in place using a fixed bitonic sorting network.
    Length need not be a power of two; we pad with +∞ sentinels.
    """
    n = len(arr)
    if n == 0 or n == 1:
        return arr  # nothing to sort

    p = 1 << ceil(log2(n))  # next power of two
    padded = arr + [float("inf")] * (p - n)

    _bitonic_sort(padded, 0, p, True)

    # remove sentinels and copy back
    del padded[n:]  # drop the padding
    arr[:] = padded  # write result back into original list
    return arr
