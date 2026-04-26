// dijkstra — dense-graph SSSP application benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

const INF int32 = 1 << 30

func main() {
	v := 800
	if len(os.Args) > 1 {
		x, _ := strconv.Atoi(os.Args[1])
		v = x
	}
	var seed int64 = 1
	g := make([]int32, v*v)
	for i := 0; i < v; i++ {
		for j := 0; j < v; j++ {
			seed = (seed*1103515245 + 12345) & 0x7FFFFFFF
			g[i*v+j] = 1 + int32((seed>>8)%100)
		}
		g[i*v+i] = 0
	}

	t0 := time.Now()
	dist := make([]int32, v)
	visited := make([]bool, v)
	for i := range dist {
		dist[i] = INF
	}
	dist[0] = 0
	for s := 0; s < v; s++ {
		u := -1
		best := INF
		for k := 0; k < v; k++ {
			if !visited[k] && dist[k] < best {
				best = dist[k]
				u = k
			}
		}
		if u < 0 {
			break
		}
		visited[u] = true
		du := dist[u]
		base := u * v
		for k := 0; k < v; k++ {
			nd := du + g[base+k]
			if nd < dist[k] {
				dist[k] = nd
			}
		}
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	var cs int64 = 0
	for _, d := range dist {
		cs ^= int64(d)
	}
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
