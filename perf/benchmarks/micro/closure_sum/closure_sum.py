# Closure / higher-order pipeline — micro-benchmark.
#
# Builds an array of N integers, then evaluates a map -> filter -> reduce
# pipeline using closures. Stresses higher-order functions, closure dispatch,
# and integer arithmetic.
#
# Argument: N (default 2_000_000).

import sys
import time
from functools import reduce


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    data = list(range(n))

    t0 = time.perf_counter_ns()
    cs = reduce(
        lambda acc, x: acc + x,
        filter(lambda x: x % 3 == 0, map(lambda x: x * x - 7, data)),
        0,
    )
    elapsed_ns = time.perf_counter_ns() - t0

    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
