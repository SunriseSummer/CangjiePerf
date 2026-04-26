// format_loop — integer-formatting tight-loop micro-benchmark (Go).
package main

import (
	"fmt"
	"math"
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
	// Capacity hint, with explicit bounds so the int64→int conversion can
	// never silently truncate. ``math.MaxInt32`` is well above any realistic
	// benchmark input but small enough that ``int(n) * 9`` cannot overflow
	// ``int`` on either 32-bit or 64-bit platforms.
	if n > 0 && n <= math.MaxInt32 {
		sb.Grow(int(n) * 9)
	}
	for i := int64(0); i < n; i++ {
		fmt.Fprintf(&sb, "%08d;", i)
	}
	s := sb.String()
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", len(s))
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
