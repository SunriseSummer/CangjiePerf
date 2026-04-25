// Spectral norm — CLBG numerical kernel (Go).
package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"time"
)

func a(i, j int) float64 {
	return 1.0 / float64(((i+j)*(i+j+1)>>1)+i+1)
}

func av(v, out []float64, n int) {
	for i := 0; i < n; i++ {
		s := 0.0
		for j := 0; j < n; j++ {
			s += a(i, j) * v[j]
		}
		out[i] = s
	}
}

func atv(v, out []float64, n int) {
	for i := 0; i < n; i++ {
		s := 0.0
		for j := 0; j < n; j++ {
			s += a(j, i) * v[j]
		}
		out[i] = s
	}
}

func atav(v, out, tmp []float64, n int) {
	av(v, tmp, n)
	atv(tmp, out, n)
}

func main() {
	n := 1500
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		n = v
	}
	u := make([]float64, n)
	v := make([]float64, n)
	tmp := make([]float64, n)
	for i := 0; i < n; i++ {
		u[i] = 1.0
	}
	t0 := time.Now()
	for i := 0; i < 10; i++ {
		atav(u, v, tmp, n)
		atav(v, u, tmp, n)
	}
	vbv, vv := 0.0, 0.0
	for i := 0; i < n; i++ {
		vbv += u[i] * v[i]
		vv += v[i] * v[i]
	}
	sn := math.Sqrt(vbv / vv)
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	cs := int64(math.Round(sn * 1e9))
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
