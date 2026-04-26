// levenshtein — edit-distance DP application benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func makeStr(seed int64, n int) []byte {
	out := make([]byte, n)
	for i := 0; i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		out[i] = byte('a') + byte((seed>>16)&7)
	}
	return out
}

func main() {
	n := 1500
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		n = v
	}
	a := makeStr(1, n)
	b := makeStr(7, n)

	t0 := time.Now()
	prev := make([]int32, n+1)
	cur := make([]int32, n+1)
	for j := 0; j <= n; j++ {
		prev[j] = int32(j)
	}
	for i := 1; i <= n; i++ {
		cur[0] = int32(i)
		ai := a[i-1]
		for j := 1; j <= n; j++ {
			var cost int32
			if ai != b[j-1] {
				cost = 1
			}
			v := prev[j-1] + cost
			if d := cur[j-1] + 1; d < v {
				v = d
			}
			if d := prev[j] + 1; d < v {
				v = d
			}
			cur[j] = v
		}
		prev, cur = cur, prev
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", prev[n])
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
