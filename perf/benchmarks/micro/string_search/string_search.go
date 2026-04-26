// string_search — substring-search tight-loop micro-benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

func main() {
	repeats := int64(50_000)
	if len(os.Args) > 1 {
		v, _ := strconv.ParseInt(os.Args[1], 10, 64)
		repeats = v
	}
	var seed int64 = 1
	buf := make([]byte, 0, 10_000)
	for i := 0; i < 10_000; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		buf = append(buf, byte('a')+byte(seed%8))
	}
	hay := string(buf)
	needle := "abcde"

	t0 := time.Now()
	var cs int64 = 0
	for r := int64(0); r < repeats; r++ {
		var count int64 = 0
		pos := 0
		for {
			i := strings.Index(hay[pos:], needle)
			if i < 0 {
				break
			}
			count++
			pos += i + 1
		}
		cs ^= (r+1)*1000003 + count
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
