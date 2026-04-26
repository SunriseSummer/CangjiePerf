# knapsack_dp — 0/1 knapsack DP application benchmark.
#
# Generate N items (deterministic LCG) with weight in [1..MAXW] and value
# in [1..MAXV], then solve 0/1 knapsack with capacity C using a 1-D DP array.
# Argument: N (default 1500), capacity C is fixed at 4000.

import sys
import time

C = 4000
MAXW = 200
MAXV = 1000


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    seed = 1
    weights = [0] * n
    values = [0] * n
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        weights[i] = 1 + (seed % MAXW)
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        values[i] = 1 + (seed % MAXV)

    t0 = time.perf_counter_ns()
    dp = [0] * (C + 1)
    for i in range(n):
        wi = weights[i]
        vi = values[i]
        for c in range(C, wi - 1, -1):
            v = dp[c - wi] + vi
            if v > dp[c]:
                dp[c] = v
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{dp[C]}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
