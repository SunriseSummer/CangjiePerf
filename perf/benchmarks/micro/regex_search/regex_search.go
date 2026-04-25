// Regex find-all — stdlib regexp micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

const sample = "On 2024-03-21 Alice wrote to bob@example.com about the meeting. " +
	"Charlie replied 2024-04-02 from charlie_99@dev.io with notes about " +
	"Project Kingfisher. References: 1999-12-31, foo@bar.org, Madison."

func main() {
	repeats := 4000
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		repeats = v
	}
	var b strings.Builder
	b.Grow(repeats * (len(sample) + 1))
	for i := 0; i < repeats; i++ {
		b.WriteString(sample)
		b.WriteByte('\n')
	}
	text := b.String()
	rx := regexp.MustCompile(`(\d{4}-\d{2}-\d{2})|([A-Za-z]+@[a-z]+\.[a-z]+)|(\b[A-Z][a-z]{3,8}\b)`)

	t0 := time.Now()
	matches := rx.FindAllStringIndex(text, -1)
	cs := int64(len(matches))
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
