# String building — stdlib StringBuilder-style micro-benchmark.
#
# Build one large string by appending N small fragments using the language's
# recommended efficient builder (Python list + ''.join).
# Argument: N (default 500_000).

import sys
import time


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
    t0 = time.perf_counter_ns()
    parts: list[str] = []
    for i in range(n):
        parts.append("frag")
        parts.append(str(i))
        parts.append(";")
    s = "".join(parts)
    elapsed_ns = time.perf_counter_ns() - t0
    cs = len(s)
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
