// set_ops — HashSet insert + membership micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	n := int64(500_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	t0 := time.Now()
	s := make(map[int64]struct{}, n)
	var seed int64 = 1
	mod := n * 2
	for i := int64(0); i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		s[seed%mod] = struct{}{}
	}
	var found int64 = 0
	for i := int64(0); i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		if _, ok := s[seed%mod]; ok {
			found++
		}
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", found)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
