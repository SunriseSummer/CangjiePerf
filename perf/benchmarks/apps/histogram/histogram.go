// histogram — bucket-counts of LCG ints application benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

const K = 1024

func main() {
	n := int64(5_000_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	t0 := time.Now()
	buckets := make([]int64, K)
	var seed int64 = 1
	for i := int64(0); i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		buckets[(seed>>8)&(K-1)]++
	}
	var cs int64 = 0
	for _, v := range buckets {
		cs ^= v
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
