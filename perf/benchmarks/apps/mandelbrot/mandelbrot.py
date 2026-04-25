# Mandelbrot — application-style numerical benchmark.
#
# Computes a W*W escape-time bitmap of the Mandelbrot set with up to MAX_ITER
# iterations per pixel. Inspired by the Computer Language Benchmarks Game.
# Args: WIDTH MAX_ITER (defaults: 600 200).

import sys
import time


def mandelbrot(width: int, max_iter: int) -> int:
    inv_w = 2.0 / width
    total = 0
    for py in range(width):
        ci = py * inv_w - 1.0
        for px in range(width):
            cr = px * inv_w - 1.5
            zr = 0.0
            zi = 0.0
            n = 0
            while n < max_iter:
                zr2 = zr * zr
                zi2 = zi * zi
                if zr2 + zi2 > 4.0:
                    break
                zi = 2.0 * zr * zi + ci
                zr = zr2 - zi2 + cr
                n += 1
            total += n
    return total


def main() -> None:
    width = int(sys.argv[1]) if len(sys.argv) > 1 else 600
    max_iter = int(sys.argv[2]) if len(sys.argv) > 2 else 200

    t0 = time.perf_counter_ns()
    cs = mandelbrot(width, max_iter)
    elapsed_ns = time.perf_counter_ns() - t0

    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
