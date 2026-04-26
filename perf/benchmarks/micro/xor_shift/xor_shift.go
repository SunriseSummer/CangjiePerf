// xor_shift — xorshift64 PRNG tight-loop micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	n := int64(50_000_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	t0 := time.Now()
	var s uint64 = 0x123456789ABCDEF0
	for i := int64(0); i < n; i++ {
		s ^= s << 13
		s ^= s >> 7
		s ^= s << 17
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", s)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
