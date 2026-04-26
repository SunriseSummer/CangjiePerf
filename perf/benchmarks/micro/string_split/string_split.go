// string_split — repeated stdlib string-split micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	repeats := int64(20_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		repeats = v
	}

	// Build input once.
	var seed int64 = 1
	parts := make([]string, 0, 64)
	for i := 0; i < 64; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		parts = append(parts, fmt.Sprintf("tok%05d", seed%100000))
	}
	s := strings.Join(parts, ",")

	t0 := time.Now()
	var cs int64 = 0
	for r := int64(0); r < repeats; r++ {
		toks := strings.Split(s, ",")
		idx := r % int64(len(toks))
		cs ^= (r+1)*1000003 + int64(len(toks)) + int64(len(toks[idx]))
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
