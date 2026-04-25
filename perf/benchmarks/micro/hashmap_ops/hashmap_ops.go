// HashMap insert + lookup — stdlib hash-table micro-benchmark (Go).
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

	keys := make([]string, n)
	for i := int64(0); i < n; i++ {
		keys[i] = "key-" + strconv.FormatInt(i, 10)
	}

	t0 := time.Now()
	m := make(map[string]int64, n)
	for i := int64(0); i < n; i++ {
		m[keys[i]] = i
	}
	var cs int64
	for i := int64(0); i < n; i++ {
		cs ^= m[keys[i]]
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
