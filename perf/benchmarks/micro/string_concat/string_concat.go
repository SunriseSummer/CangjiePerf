// String building — stdlib strings.Builder micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	n := int64(500_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		n = v
	}
	t0 := time.Now()
	var sb strings.Builder
	sb.Grow(int(n) * 12)
	for i := int64(0); i < n; i++ {
		sb.WriteString("frag")
		sb.WriteString(strconv.FormatInt(i, 10))
		sb.WriteByte(';')
	}
	s := sb.String()
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", len(s))
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
