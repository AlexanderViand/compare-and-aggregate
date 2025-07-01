# Compare-and-Aggregate Algorithms

Reference Python implementations of Compare-and-Aggregate (CA) sorting, selection, and top-k algorithms, as described in [Secure Sorting and Selection via Function Secret Sharing](https://dl.acm.org/doi/10.1145/3658644.3690359).

Includes:
- Direct (Valiant's model) and Compare-Aggregate (CA model) implementations for selection, sorting, and top-k.
- A simple test suite for correctness on cleartext data.

## Usage

```python
from compare_aggregate import select_kth, select_kth_CA, sorted_top_k, sorted_top_k_CA

# Direct selection:
print(select_kth([3,1,2], 1))  # => 2
```
