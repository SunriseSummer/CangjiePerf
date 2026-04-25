# Math-intensive loop — std.math micro-benchmark.
#
# Computes a sum of sin/cos/sqrt/exp values over N iterations.
# Stresses the math standard library and floating-point throughput.
#
# Argument: N (default 5_000_000).

import math
import sys
import time


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000

    t0 = time.perf_counter_ns()
    s = 0.0
    inv = 1.0 / n
    for i in range(n):
        x = i * inv
        s += math.sin(x) * math.cos(x) + math.sqrt(x + 1.0) - math.exp(-x)
    elapsed_ns = time.perf_counter_ns() - t0

    # Round to integer scale to keep the checksum stable across implementations
    # despite tiny floating-point reordering effects.
    cs = round(s * 1e6)
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
