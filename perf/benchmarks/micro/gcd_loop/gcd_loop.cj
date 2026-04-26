// gcd_loop — Euclidean GCD tight-loop micro-benchmark (Cangjie).
package gcd_loop

import std.time.*
import std.process.*
import std.convert.*

func gcd(a0: Int64, b0: Int64): Int64 {
    var a = a0
    var b = b0
    while (b != 0) {
        let t = a % b
        a = b
        b = t
    }
    return a
}

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 2_000_000 }

    let start = MonoTime.now()
    var cs: Int64 = 0
    var seed: Int64 = 1
    var i: Int64 = 1
    while (i <= n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        cs = (cs + gcd(i, seed)) & 0x7FFFFFFF
        i += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
