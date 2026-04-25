# Spectral norm — Computer Language Benchmarks Game numerical kernel.
#
# Approximates the largest eigenvalue of an infinite matrix A with
# A[i][j] = 1 / ((i+j)*(i+j+1)/2 + i + 1) by 10 power-iteration steps of
# v <- A^T * A * v. Highly symmetric across all three implementations:
# same matrix function, same number of iterations, same array layout,
# same checksum (sqrt(<u,v>/<v,v>)).
#
# Argument: N (default 1500).

import math
import sys
import time


def A(i: int, j: int) -> float:
    return 1.0 / (((i + j) * (i + j + 1) >> 1) + i + 1)


def Av(v: list, out: list, n: int) -> None:
    for i in range(n):
        s = 0.0
        for j in range(n):
            s += A(i, j) * v[j]
        out[i] = s


def Atv(v: list, out: list, n: int) -> None:
    for i in range(n):
        s = 0.0
        for j in range(n):
            s += A(j, i) * v[j]
        out[i] = s


def AtAv(v: list, out: list, tmp: list, n: int) -> None:
    Av(v, tmp, n)
    Atv(tmp, out, n)


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1500

    u = [1.0] * n
    v = [0.0] * n
    tmp = [0.0] * n

    t0 = time.perf_counter_ns()
    for _ in range(10):
        AtAv(u, v, tmp, n)
        AtAv(v, u, tmp, n)
    vbv = 0.0
    vv = 0.0
    for i in range(n):
        vbv += u[i] * v[i]
        vv += v[i] * v[i]
    sn = math.sqrt(vbv / vv)
    elapsed_ns = time.perf_counter_ns() - t0

    cs = round(sn * 1e9)
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
