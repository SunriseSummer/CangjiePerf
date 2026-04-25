# Hand-written quicksort — micro-benchmark.
#
# This is a complement to the `sort` benchmark (which uses the language's
# stdlib sort): here we run an algorithmically identical Lomuto-partition
# quicksort in all three languages so that ALL cross-language work — pivot
# choice, partition step, recursion shape, and array indexing — is the same.
#
# The pivot is the middle element; recursion is on the smaller side first
# (with iterative tail-call on the larger side) so worst-case stack depth is
# O(log N) and the algorithm is deterministic given the input.
#
# Argument: N (default 1_500_000).

import sys
import time


def quicksort(a: list, lo: int, hi: int) -> None:
    while lo < hi:
        # Lomuto partition with middle-element pivot.
        mid = (lo + hi) >> 1
        pivot = a[mid]
        # Move pivot to the end.
        a[mid], a[hi] = a[hi], a[mid]
        i = lo - 1
        for j in range(lo, hi):
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        i += 1
        a[i], a[hi] = a[hi], a[i]
        # Recurse on the smaller side first; iterate on the other.
        if (i - lo) < (hi - i):
            quicksort(a, lo, i - 1)
            lo = i + 1
        else:
            quicksort(a, i + 1, hi)
            hi = i - 1


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1_500_000

    # Deterministic LCG (kept outside the timed region).
    a = [0] * n
    seed = 1234567
    mask = 0x7FFFFFFF
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & mask
        a[i] = seed

    sys.setrecursionlimit(max(1000, n))
    t0 = time.perf_counter_ns()
    quicksort(a, 0, n - 1)
    elapsed_ns = time.perf_counter_ns() - t0

    # Checksum: every 1024-th element XORed in.
    cs = 0
    k = 0
    while k < n:
        cs ^= a[k]
        k += 1024
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
