# gcd_loop — Euclidean GCD tight-loop micro-benchmark.
#
# For i in [1, N] compute gcd(i, b_i) where b_i comes from a deterministic
# LCG, and accumulate the sum modulo 2^31. Argument: N (default 2_000_000).

import sys
import time


def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    t0 = time.perf_counter_ns()
    cs = 0
    seed = 1
    for i in range(1, n + 1):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        cs = (cs + gcd(i, seed)) & 0x7FFFFFFF
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
