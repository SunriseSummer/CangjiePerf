// Enum / algebraic-data-type recursive pattern matching — micro-benchmark (Go).
//
// Mimics a sum type via a tagged struct (Tag + value/children).
package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

const (
	tagNum = iota
	tagAdd
	tagSub
	tagMul
)

type expr struct {
	tag    int
	v      int64
	l, r   *expr
}

func makeNum(v int64) *expr {
	return &expr{tag: tagNum, v: v}
}

func makeOp(t int, l, r *expr) *expr {
	return &expr{tag: t, l: l, r: r}
}

func build(depth int, seed int64) *expr {
	if depth == 0 {
		return makeNum((seed & 0x3F) + 1)
	}
	s := (seed*1103515245 + 12345) & 0x7FFFFFFF
	tag := int((s >> 17) & 3)
	left := build(depth-1, s)
	right := build(depth-1, s^0xABCDEF)
	switch tag {
	case 0:
		return makeOp(tagAdd, left, right)
	case 1:
		return makeOp(tagSub, left, right)
	case 2:
		return makeOp(tagMul, left, right)
	default:
		return makeOp(tagAdd, left, right)
	}
}

func eval(e *expr) int64 {
	switch e.tag {
	case tagNum:
		return e.v
	case tagAdd:
		return eval(e.l) + eval(e.r)
	case tagSub:
		return eval(e.l) - eval(e.r)
	case tagMul:
		return eval(e.l) * eval(e.r)
	}
	return 0
}

func main() {
	depth := 18
	n := 60
	if len(os.Args) > 1 {
		v, _ := strconv.Atoi(os.Args[1])
		depth = v
	}
	if len(os.Args) > 2 {
		v, _ := strconv.Atoi(os.Args[2])
		n = v
	}
	tree := build(depth, 1)

	t0 := time.Now()
	var cs int64
	for i := 0; i < n; i++ {
		cs ^= eval(tree)
	}
	ms := float64(time.Since(t0).Nanoseconds()) / 1_000_000.0
	fmt.Printf("CHECKSUM:%d\n", cs)
	fmt.Printf("ELAPSED_MS:%.6f\n", ms)
}
