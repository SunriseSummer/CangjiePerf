// monte_carlo_pi — integer-only Monte-Carlo PI count benchmark (Go).
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
	const R int64 = 65536
	const R2 int64 = R * R
	t0 := time.Now()
	var seed int64 = 1
	var inside int64 = 0
	for i := int64(0); i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		x := seed % R
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		y := seed % R
		if x*x+y*y <= R2 {
			inside++
		}
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", inside)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
