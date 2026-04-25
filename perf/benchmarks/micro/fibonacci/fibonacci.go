// Fibonacci — recursive function-call micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func fib(n int64) int64 {
	if n < 2 {
		return n
	}
	return fib(n-1) + fib(n-2)
}

func main() {
	n := int64(32)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	t0 := time.Now()
	result := fib(n)
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", result)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
