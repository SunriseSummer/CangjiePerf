# deque_ops — dynamic-array push/pop micro-benchmark.
#
# Push N integers onto an array (computed via LCG), then pop them all and
# XOR-fold them into a checksum. Argument: N (default 2_000_000).

import sys
import time


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    t0 = time.perf_counter_ns()
    a: list[int] = []
    seed = 1
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        a.append(seed)
    cs = 0
    while a:
        cs ^= a.pop()
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
