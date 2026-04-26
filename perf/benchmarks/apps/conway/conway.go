// conway — Game of Life N-step application benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

const W = 200

func main() {
	steps := 200
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		steps = v
	}
	cells := W * W
	grid := make([]byte, cells)
	nxt := make([]byte, cells)
	var seed int64 = 1
	for i := 0; i < cells; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		if (seed>>16)&3 < 2 {
			grid[i] = 1
		}
	}

	t0 := time.Now()
	for s := 0; s < steps; s++ {
		for y := 0; y < W; y++ {
			yu := (y + W - 1) % W
			yd := (y + 1) % W
			row := y * W
			rowU := yu * W
			rowD := yd * W
			for x := 0; x < W; x++ {
				xl := (x + W - 1) % W
				xr := (x + 1) % W
				n := grid[rowU+xl] + grid[rowU+x] + grid[rowU+xr] +
					grid[row+xl] + grid[row+xr] +
					grid[rowD+xl] + grid[rowD+x] + grid[rowD+xr]
				alive := grid[row+x]
				var nv byte
				if alive != 0 {
					if n == 2 || n == 3 {
						nv = 1
					}
				} else if n == 3 {
					nv = 1
				}
				nxt[row+x] = nv
			}
		}
		grid, nxt = nxt, grid
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	var cs int64 = 0
	for _, c := range grid {
		cs += int64(c)
	}
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
