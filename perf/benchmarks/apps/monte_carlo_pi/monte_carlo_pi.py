# monte_carlo_pi — integer-only Monte-Carlo PI count benchmark.
#
# For N pairs (x, y) drawn from a deterministic LCG modulo R, count how many
# satisfy x*x + y*y <= R*R. R is fixed at 65536. Argument: N (default 5_000_000).

import sys
import time

R = 65536


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    R2 = R * R
    t0 = time.perf_counter_ns()
    seed = 1
    inside = 0
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        x = seed % R
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        y = seed % R
        if x * x + y * y <= R2:
            inside += 1
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{inside}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
