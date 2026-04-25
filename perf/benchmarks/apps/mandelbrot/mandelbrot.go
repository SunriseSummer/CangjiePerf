// Mandelbrot — application-style numerical benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func mandelbrot(width, maxIter int) int64 {
	invW := 2.0 / float64(width)
	var total int64
	for py := 0; py < width; py++ {
		ci := float64(py)*invW - 1.0
		for px := 0; px < width; px++ {
			cr := float64(px)*invW - 1.5
			zr, zi := 0.0, 0.0
			n := 0
			for n < maxIter {
				zr2 := zr * zr
				zi2 := zi * zi
				if zr2+zi2 > 4.0 {
					break
				}
				zi = 2.0*zr*zi + ci
				zr = zr2 - zi2 + cr
				n++
			}
			total += int64(n)
		}
	}
	return total
}

func main() {
	width := 600
	maxIter := 200
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		width = v
	}
	if len(os.Args) > 2 {
		v, _ := strconv.Atoi(os.Args[2])
		maxIter = v
	}
	t0 := time.Now()
	cs := mandelbrot(width, maxIter)
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
