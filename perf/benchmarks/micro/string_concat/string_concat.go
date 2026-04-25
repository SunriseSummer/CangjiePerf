// String building — stdlib strings.Builder micro-benchmark (Go).
package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

// Average bytes appended per iteration: "frag" (4) + decimal digits (~7) + ';'.
// Used only as a capacity hint for strings.Builder.
const bytesPerIter = 12

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
	// benchmark input but small enough that ``int(n) * bytesPerIter`` cannot
	// overflow ``int`` on either 32-bit or 64-bit platforms.
	if n > 0 && n <= math.MaxInt32 {
		sb.Grow(int(n) * bytesPerIter)
	}
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
