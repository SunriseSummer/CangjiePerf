// Closure / higher-order pipeline — micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	n := int64(2_000_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	data := make([]int64, n)
	for i := int64(0); i < n; i++ {
		data[i] = i
	}

	// Use func-value variables (instead of inlinable literals) so the call is
	// dispatched via a closure pointer, matching the C++ std::function path.
	mapper := func(x int64) int64 { return x*x - 7 }
	pred := func(x int64) bool { return x%3 == 0 }
	reducer := func(a, b int64) int64 { return a + b }

	t0 := time.Now()
	var cs int64
	for i := int64(0); i < n; i++ {
		v := mapper(data[i])
		if pred(v) {
			cs = reducer(cs, v)
		}
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
