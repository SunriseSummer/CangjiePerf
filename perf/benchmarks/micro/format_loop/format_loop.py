# format_loop — integer-formatting tight-loop micro-benchmark.
#
# Build a single large string by formatting N integers (with zero-padding)
# into a builder, separated by ';'. Returns the total length as checksum.
# Argument: N (default 500_000).

import sys
import time
import io


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
    t0 = time.perf_counter_ns()
    sb = io.StringIO()
    for i in range(n):
        sb.write(f"{i:08d};")
    s = sb.getvalue()
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{len(s)}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
