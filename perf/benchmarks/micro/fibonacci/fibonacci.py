# Fibonacci — recursive function-call micro-benchmark.
#
# Computes fib(N) recursively then prints CHECKSUM and ELAPSED_MS.
# Argument: N (default 32).

import sys
import time


def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    sys.setrecursionlimit(max(1000, n + 100))
    t0 = time.perf_counter_ns()
    result = fib(n)
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{result}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
