# string_split — repeated stdlib string-split micro-benchmark.
#
# Build a deterministic comma-separated string of K tokens once, then split
# it REPEATS times and accumulate (number of tokens) ^ (length of token 0).
# Argument: REPEATS (default 20_000).

import sys
import time


def main() -> None:
    repeats = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000
    # Build a fixed input string outside the timed region.
    parts = []
    seed = 1
    for _ in range(64):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        parts.append(f"tok{seed % 100000:05d}")
    s = ",".join(parts)

    t0 = time.perf_counter_ns()
    cs = 0
    for r in range(repeats):
        toks = s.split(",")
        idx = r % len(toks)
        cs ^= (r + 1) * 1000003 + len(toks) + len(toks[idx])
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
