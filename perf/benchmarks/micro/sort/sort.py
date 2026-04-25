# Sort N integers — stdlib-sort micro-benchmark.
#
# We generate a deterministic LCG sequence, then time only the sort step.
# Argument: N (default 2_000_000).

import sys
import time


def gen_data(n: int) -> list[int]:
    seed = 12345
    arr = [0] * n
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        arr[i] = seed
    return arr


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    arr = gen_data(n)
    t0 = time.perf_counter_ns()
    arr.sort()
    elapsed_ns = time.perf_counter_ns() - t0
    checksum = arr[0] ^ arr[n // 2] ^ arr[-1]
    print(f"CHECKSUM:{checksum}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
