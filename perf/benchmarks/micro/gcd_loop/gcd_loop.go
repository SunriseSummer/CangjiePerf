// gcd_loop — Euclidean GCD tight-loop micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func gcd(a, b int64) int64 {
	for b != 0 {
		a, b = b, a%b
	}
	return a
}

func main() {
	n := int64(2_000_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	t0 := time.Now()
	var cs int64 = 0
	var seed int64 = 1
	for i := int64(1); i <= n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		cs = (cs + gcd(i, seed)) & 0x7FFFFFFF
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
