# Matrix multiplication — naive O(N^3) double-precision matmul.
#
# Computes C = A * B for two NxN matrices and reports a deterministic
# checksum over the result.
#
# Argument: N (default 250). Total ops ~ 2*N^3.

import sys
import time


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 250

    # Deterministic fill (kept outside the timed region).
    a = [[((i * 7 + j * 13) % 100) * 0.01 for j in range(n)] for i in range(n)]
    b = [[((i * 11 + j * 17) % 100) * 0.01 for j in range(n)] for i in range(n)]
    c = [[0.0] * n for _ in range(n)]

    t0 = time.perf_counter_ns()
    # Hoist row binding to avoid repeated attribute lookup on c[i].
    for i in range(n):
        ai = a[i]
        ci = c[i]
        for k in range(n):
            aik = ai[k]
            bk = b[k]
            for j in range(n):
                ci[j] += aik * bk[j]
    elapsed_ns = time.perf_counter_ns() - t0

    # Sum of diagonal, rounded to integer scale.
    total = 0.0
    for i in range(n):
        total += c[i][i]
    cs = round(total * 1e6)

    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
