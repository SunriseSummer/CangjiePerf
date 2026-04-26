# string_search — substring-search tight-loop micro-benchmark.
#
# Build a deterministic ~10KB haystack and a small needle, then count
# occurrences of needle in haystack via str.find in a sliding loop, REPEATS
# times. Argument: REPEATS (default 50_000).

import sys
import time

NEEDLE = "abcde"


def main() -> None:
    repeats = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000
    # 10_000-character pseudo-random ASCII haystack (a..h).
    seed = 1
    chars = []
    for _ in range(10_000):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        chars.append(chr(ord('a') + (seed % 8)))
    hay = "".join(chars)

    t0 = time.perf_counter_ns()
    cs = 0
    for r in range(repeats):
        count = 0
        pos = 0
        while True:
            i = hay.find(NEEDLE, pos)
            if i < 0:
                break
            count += 1
            pos = i + 1
        cs ^= (r + 1) * 1000003 + count
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
