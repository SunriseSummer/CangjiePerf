// Word-count — typical text-processing application benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

func genText(n int64) string {
	seed := int64(12345)
	var sb strings.Builder
	sb.Grow(int(n) * 7)
	for i := int64(0); i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		idx := seed % 1024
		fmt.Fprintf(&sb, "w%04d", idx)
		if i%12 == 11 {
			sb.WriteByte('\n')
		} else {
			sb.WriteByte(' ')
		}
	}
	return sb.String()
}

func main() {
	n := int64(1_000_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	text := genText(n)

	t0 := time.Now()
	counts := make(map[string]int64, 2048)
	i, sz := 0, len(text)
	for i < sz {
		for i < sz && (text[i] == ' ' || text[i] == '\n') {
			i++
		}
		start := i
		for i < sz && text[i] != ' ' && text[i] != '\n' {
			i++
		}
		if i > start {
			counts[text[start:i]]++
		}
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0

	var cs int64
	for k, v := range counts {
		idx, _ := strconv.ParseInt(k[1:], 10, 64)
		cs ^= idx*1000003 + v
	}
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
