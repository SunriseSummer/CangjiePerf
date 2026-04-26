// bit_count — popcount tight-loop micro-benchmark (Go).
package main

import (
	"fmt"
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
	var cs int64 = 0
	for i := int64(0); i < n; i++ {
		v := uint32(uint64(i) * 2654435761)
		c := int64(0)
		for v != 0 {
			v &= v - 1
			c++
		}
		cs += c
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
