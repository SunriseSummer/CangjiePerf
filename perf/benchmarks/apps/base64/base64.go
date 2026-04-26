// base64 — base64 encoding application benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

var alpha = []byte("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/")

func main() {
	n := 2_000_000
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

	t0 := time.Now()
	outLen := ((n + 2) / 3) * 4
	out := make([]byte, outLen)
	oi := 0
	i := 0
	for i+3 <= n {
		b0 := src[i]
		b1 := src[i+1]
		b2 := src[i+2]
		out[oi] = alpha[b0>>2]
		out[oi+1] = alpha[((b0&0x3)<<4)|(b1>>4)]
		out[oi+2] = alpha[((b1&0xF)<<2)|(b2>>6)]
		out[oi+3] = alpha[b2&0x3F]
		oi += 4
		i += 3
	}
	rem := n - i
	if rem == 1 {
		b0 := src[i]
		out[oi] = alpha[b0>>2]
		out[oi+1] = alpha[(b0&0x3)<<4]
		out[oi+2] = '='
		out[oi+3] = '='
	} else if rem == 2 {
		b0 := src[i]
		b1 := src[i+1]
		out[oi] = alpha[b0>>2]
		out[oi+1] = alpha[((b0&0x3)<<4)|(b1>>4)]
		out[oi+2] = alpha[(b1&0xF)<<2]
		out[oi+3] = '='
	}
	var cs int64 = 0
	for _, v := range out {
		cs ^= int64(v)
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
