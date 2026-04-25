// Enum / algebraic-data-type recursive pattern matching — micro-benchmark (Cangjie).
//
// Builds an arithmetic expression tree of depth D using a recursive enum,
// then evaluates it N times via recursive `match` pattern matching.
package enum_eval

import std.overflow.*
import std.time.*
import std.process.*
import std.convert.*

enum Expr {
    | Num(Int64)
    | Add(Expr, Expr)
    | Sub(Expr, Expr)
    | Mul(Expr, Expr)
}

func build(depth: Int64, seed: Int64): Expr {
    if (depth == 0) {
        return Num((seed & 0x3F) + 1)
    }
    // Mask to keep `seed` non-negative and below 2^31, matching the Python
    // and C++ versions and avoiding signed-integer overflow in the LCG.
    let s: Int64 = (seed.wrappingMul(1103515245).wrappingAdd(12345)) & 0x7FFFFFFF
    let tag = (s >> 17) & 3
    let left = build(depth - 1, s)
    let right = build(depth - 1, s ^ 0xABCDEF)
    return match (tag) {
        case 0 => Add(left, right)
        case 1 => Sub(left, right)
        case 2 => Mul(left, right)
        case _ => Add(left, right)
    }
}

func eval(e: Expr): Int64 {
    return match (e) {
        case Num(v) => v
        case Add(l, r) => eval(l).wrappingAdd(eval(r))
        case Sub(l, r) => eval(l).wrappingSub(eval(r))
        case Mul(l, r) => eval(l).wrappingMul(eval(r))
    }
}

main() {
    let args = Process.current.arguments
    let depth: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 18 }
    let n: Int64     = if (args.size > 1) { Int64.parse(args[1]) } else { 60 }

    let tree = build(depth, 1)

    let start = MonoTime.now()
    var cs: Int64 = 0
    for (_ in 0..n) {
        cs ^= eval(tree)
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
