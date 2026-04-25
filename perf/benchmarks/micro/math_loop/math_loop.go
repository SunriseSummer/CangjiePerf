// Math-intensive loop — std math micro-benchmark (Go).
package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"time"
)

func main() {
	n := int64(5_000_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	t0 := time.Now()
	s := 0.0
	inv := 1.0 / float64(n)
	for i := int64(0); i < n; i++ {
		x := float64(i) * inv
		s += math.Sin(x)*math.Cos(x) + math.Sqrt(x+1.0) - math.Exp(-x)
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	cs := int64(math.Round(s * 1e6))
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
