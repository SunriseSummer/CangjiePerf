# bit_count — popcount tight-loop micro-benchmark.
#
# For i in [0, N) compute popcount(i * 2654435761 & 0xFFFFFFFF) and sum.
# Pure integer / bitwise work. Argument: N (default 5_000_000).

import sys
import time


def popcount(x: int) -> int:
    c = 0
    while x:
        x &= x - 1
        c += 1
    return c


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    t0 = time.perf_counter_ns()
    cs = 0
    for i in range(n):
        v = (i * 2654435761) & 0xFFFFFFFF
        cs += popcount(v)
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
