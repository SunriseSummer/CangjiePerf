# conway — Game of Life N-step application benchmark.
#
# Initialize a W*W grid from a deterministic LCG, simulate STEPS generations
# of Conway's Game of Life with toroidal boundaries, then count live cells.
# Argument: STEPS (default 200), with W fixed at 200.

import sys
import time

W = 200


def main() -> None:
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    cells = W * W
    grid = bytearray(cells)
    seed = 1
    for i in range(cells):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        grid[i] = 1 if ((seed >> 16) & 3) < 2 else 0
    nxt = bytearray(cells)

    t0 = time.perf_counter_ns()
    for _ in range(steps):
        for y in range(W):
            yu = (y - 1) % W
            yd = (y + 1) % W
            row = y * W
            row_u = yu * W
            row_d = yd * W
            for x in range(W):
                xl = (x - 1) % W
                xr = (x + 1) % W
                neighbors = (
                    grid[row_u + xl] + grid[row_u + x] + grid[row_u + xr]
                    + grid[row + xl] + grid[row + xr]
                    + grid[row_d + xl] + grid[row_d + x] + grid[row_d + xr]
                )
                alive = grid[row + x]
                if alive:
                    nxt[row + x] = 1 if neighbors == 2 or neighbors == 3 else 0
                else:
                    nxt[row + x] = 1 if neighbors == 3 else 0
        grid, nxt = nxt, grid
    elapsed_ns = time.perf_counter_ns() - t0
    cs = sum(grid)
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
