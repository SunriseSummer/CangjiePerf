// Sort N integers — stdlib-sort micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"time"
)

func main() {
	n := int64(2_000_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	arr := make([]int64, n)
	seed := int64(12345)
	for i := int64(0); i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		arr[i] = seed
	}
	t0 := time.Now()
	sort.Slice(arr, func(i, j int) bool { return arr[i] < arr[j] })
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	cs := arr[0] ^ arr[n/2] ^ arr[n-1]
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
