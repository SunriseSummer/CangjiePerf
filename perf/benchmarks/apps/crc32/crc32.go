// crc32 — CRC32 of a deterministic byte stream application benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func buildTable() [256]uint32 {
	var t [256]uint32
	for n := uint32(0); n < 256; n++ {
		c := n
		for k := 0; k < 8; k++ {
			if c&1 != 0 {
				c = (c >> 1) ^ 0xEDB88320
			} else {
				c = c >> 1
			}
		}
		t[n] = c
	}
	return t
}

func main() {
	n := 5_000_000
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		n = v
	}
	src := make([]byte, n)
	var seed int64 = 1
	for i := 0; i < n; i++ {
		seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
		src[i] = byte((seed >> 8) & 0xFF)
	}
	table := buildTable()

	t0 := time.Now()
	var crc uint32 = 0xFFFFFFFF
	for i := 0; i < n; i++ {
		crc = table[(crc^uint32(src[i]))&0xFF] ^ (crc >> 8)
	}
	crc ^= 0xFFFFFFFF
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", crc)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
