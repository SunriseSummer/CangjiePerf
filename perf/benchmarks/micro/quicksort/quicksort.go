// Hand-written quicksort — micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func quicksort(a []int64, lo, hi int64) {
	for lo < hi {
		mid := (lo + hi) >> 1
		pivot := a[mid]
		a[mid], a[hi] = a[hi], a[mid]
		i := lo - 1
		for j := lo; j < hi; j++ {
			if a[j] <= pivot {
				i++
				a[i], a[j] = a[j], a[i]
			}
		}
		i++
		a[i], a[hi] = a[hi], a[i]
		if (i - lo) < (hi - i) {
			quicksort(a, lo, i-1)
			lo = i + 1
		} else {
			quicksort(a, i+1, hi)
			hi = i - 1
		}
	}
}

func main() {
	n := int64(1_500_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	a := make([]int64, n)
	seed := int64(1234567)
	const mask int64 = 0x7FFFFFFF
	for i := int64(0); i < n; i++ {
		seed = (seed*1103515245 + 12345) & mask
		a[i] = seed
	}
	t0 := time.Now()
	quicksort(a, 0, n-1)
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	var cs int64
	for k := int64(0); k < n; k += 1024 {
		cs ^= a[k]
	}
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
