# histogram — bucket-counts of LCG ints application benchmark.
#
# Generate N pseudo-random ints (LCG), bucket each into K buckets by modulo,
# and return XOR of all bucket counts as the checksum.
# Argument: N (default 5_000_000), with K fixed at 1024.

import sys
import time

K = 1024


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    t0 = time.perf_counter_ns()
    buckets = [0] * K
    seed = 1
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        buckets[(seed >> 8) & (K - 1)] += 1
    cs = 0
    for v in buckets:
        cs ^= v
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
