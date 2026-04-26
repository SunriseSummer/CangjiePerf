# set_ops — HashSet insert + membership micro-benchmark.
#
# Insert N pseudo-random integers (LCG) into a hash set, then test membership
# of N more pseudo-random integers from the same stream. CHECKSUM is the
# count of "found" lookups. Argument: N (default 500_000).

import sys
import time


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
    t0 = time.perf_counter_ns()
    s: set[int] = set()
    seed = 1
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        s.add(seed % (n * 2))
    found = 0
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        if (seed % (n * 2)) in s:
            found += 1
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{found}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
