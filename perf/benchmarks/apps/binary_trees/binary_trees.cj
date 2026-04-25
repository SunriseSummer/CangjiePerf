// Binary trees — allocation / GC-pressure benchmark (Cangjie).
//
// Adapted from the Computer Language Benchmarks Game. Builds many small
// balanced binary trees on the heap (via class instances) so the GC has to
// collect them.
package binary_trees

import std.time.*
import std.process.*
import std.convert.*

class Node {
    var l: ?Node
    var r: ?Node

    init(l: ?Node, r: ?Node) {
        this.l = l
        this.r = r
    }
}

func makeTree(depth: Int64): Node {
    if (depth == 0) {
        return Node(None, None)
    }
    return Node(Some(makeTree(depth - 1)), Some(makeTree(depth - 1)))
}

func checkTree(n: Node): Int64 {
    return match (n.l) {
        case None => 1
        case Some(left) => match (n.r) {
            case None => 1
            case Some(right) => 1 + checkTree(left) + checkTree(right)
        }
    }
}

main() {
    let args = Process.current.arguments
    let maxDepth: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 14 }
    let minDepth: Int64 = 4
    let stretchDepth: Int64 = maxDepth + 1

    let start = MonoTime.now()

    let stretch = checkTree(makeTree(stretchDepth))
    let longLived = makeTree(maxDepth)

    var total: Int64 = stretch
    var d: Int64 = minDepth
    while (d <= maxDepth) {
        let iterations: Int64 = 1 << (maxDepth - d + minDepth)
        var s: Int64 = 0
        for (_ in 0..iterations) {
            s += checkTree(makeTree(d))
        }
        total ^= (iterations * 1000003 + s)
        d += 2
    }
    total ^= checkTree(longLived)

    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${total}")
    println("ELAPSED_MS:${ms}")
}
