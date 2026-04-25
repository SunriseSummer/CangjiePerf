// Matrix multiplication — naive O(N^3) double-precision matmul (Go).
package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"time"
)

func main() {
	n := 250
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		n = v
	}
	a := make([]float64, n*n)
	b := make([]float64, n*n)
	c := make([]float64, n*n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			a[i*n+j] = float64((i*7+j*13)%100) * 0.01
			b[i*n+j] = float64((i*11+j*17)%100) * 0.01
		}
	}
	t0 := time.Now()
	for i := 0; i < n; i++ {
		for k := 0; k < n; k++ {
			aik := a[i*n+k]
			bk := b[k*n : k*n+n]
			ci := c[i*n : i*n+n]
			for j := 0; j < n; j++ {
				ci[j] += aik * bk[j]
			}
		}
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	total := 0.0
	for i := 0; i < n; i++ {
		total += c[i*n+i]
	}
	cs := int64(math.Round(total * 1e6))
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
