// Binary trees — heap-allocation pressure benchmark (Go).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

type node struct {
	l, r *node
}

func makeTree(depth int) *node {
	if depth == 0 {
		return &node{}
	}
	return &node{l: makeTree(depth - 1), r: makeTree(depth - 1)}
}

func checkTree(n *node) int64 {
	if n.l == nil {
		return 1
	}
	return 1 + checkTree(n.l) + checkTree(n.r)
}

func main() {
	maxDepth := 14
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		maxDepth = v
	}
	minDepth := 4
	stretchDepth := maxDepth + 1

	t0 := time.Now()
	stretch := checkTree(makeTree(stretchDepth))
	longLived := makeTree(maxDepth)

	total := stretch
	for d := minDepth; d <= maxDepth; d += 2 {
		iterations := int64(1) << uint(maxDepth-d+minDepth)
		var s int64
		for i := int64(0); i < iterations; i++ {
			s += checkTree(makeTree(d))
		}
		total ^= iterations*1000003 + s
	}
	total ^= checkTree(longLived)
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", total)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
