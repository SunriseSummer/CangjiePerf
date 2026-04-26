# levenshtein — edit-distance DP application benchmark.
#
# Build two deterministic strings A and B (length L each, characters drawn
# from 'a'..'h' via independent LCG streams) and compute their Levenshtein
# edit distance using a 1-D rolling DP. Argument: L (default 1500).

import sys
import time


def make_str(seed: int, n: int) -> str:
    out = []
    for _ in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        out.append(chr(ord('a') + ((seed >> 16) & 7)))
    return "".join(out)


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
    a = make_str(1, n)
    b = make_str(7, n)

    t0 = time.perf_counter_ns()
    prev = list(range(n + 1))
    cur = [0] * (n + 1)
    for i in range(1, n + 1):
        cur[0] = i
        ai = a[i - 1]
        for j in range(1, n + 1):
            cost = 0 if ai == b[j - 1] else 1
            v = prev[j - 1] + cost
            d = cur[j - 1] + 1
            if d < v:
                v = d
            d = prev[j] + 1
            if d < v:
                v = d
            cur[j] = v
        prev, cur = cur, prev
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{prev[n]}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
