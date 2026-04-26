// knapsack_dp — 0/1 knapsack DP application benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

const C = 4000
const MAXW = 200
const MAXV = 1000

func main() {
	n := 1500
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		n = v
	}
	w := make([]int, n)
	val := make([]int, n)
	var seed int64 = 1
	for i := 0; i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		w[i] = 1 + int(seed%MAXW)
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		val[i] = 1 + int(seed%MAXV)
	}
	t0 := time.Now()
	dp := make([]int, C+1)
	for i := 0; i < n; i++ {
		wi := w[i]
		vi := val[i]
		for c := C; c >= wi; c-- {
			nv := dp[c-wi] + vi
			if nv > dp[c] {
				dp[c] = nv
			}
		}
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", dp[C])
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
