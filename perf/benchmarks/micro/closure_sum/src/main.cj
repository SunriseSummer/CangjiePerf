// Closure / higher-order pipeline — micro-benchmark (Cangjie).
package closure_sum

import std.collection.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 2_000_000 }
    let data = Array<Int64>(n, {i => i})

    // Closures with explicit type annotations to keep the comparison fair
    // (no inlining tricks, parameters typed Int64).
    let mapper:  (Int64) -> Int64       = {x: Int64 => x * x - 7}
    let pred:    (Int64) -> Bool        = {x: Int64 => x % 3 == 0}
    let reducer: (Int64, Int64) -> Int64 = {a: Int64, b: Int64 => a + b}

    let start = MonoTime.now()
    var cs: Int64 = 0
    for (i in 0..n) {
        let v = mapper(data[i])
        if (pred(v)) {
            cs = reducer(cs, v)
        }
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
