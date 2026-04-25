# HashMap insert + lookup — stdlib hash-table micro-benchmark.
#
# Generates N synthetic string keys, inserts (key, i) pairs, then looks up
# each key once and accumulates a checksum from the values.
# Argument: N (default 500_000).

import sys
import time


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
    # Pre-build keys outside the timed region so we measure the hash-map work.
    keys = [f"key-{i}" for i in range(n)]

    t0 = time.perf_counter_ns()
    m: dict[str, int] = {}
    for i, k in enumerate(keys):
        m[k] = i
    cs = 0
    for k in keys:
        cs ^= m[k]
    elapsed_ns = time.perf_counter_ns() - t0

    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
