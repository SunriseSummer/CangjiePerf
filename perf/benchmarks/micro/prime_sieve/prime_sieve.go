// Sieve of Eratosthenes — micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	n := int64(20_000_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	t0 := time.Now()
	sieve := make([]byte, n+1)
	for i := range sieve {
		sieve[i] = 1
	}
	sieve[0] = 0
	sieve[1] = 0
	for i := int64(2); i*i <= n; i++ {
		if sieve[i] != 0 {
			for j := i * i; j <= n; j += i {
				sieve[j] = 0
			}
		}
	}
	var count, psum int64
	const mask int64 = 0x7FFFFFFF
	for k := int64(2); k <= n; k++ {
		if sieve[k] != 0 {
			count++
			psum = (psum + k) & mask
		}
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	cs := (count*1_000_003 + psum) & mask
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
