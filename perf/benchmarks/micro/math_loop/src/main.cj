// Math-intensive loop — std.math micro-benchmark (Cangjie).
package math_loop

import std.math.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 5_000_000 }

    let start = MonoTime.now()
    var s: Float64 = 0.0
    let inv: Float64 = 1.0 / Float64(n)
    for (i in 0..n) {
        let x = Float64(i) * inv
        s += sin(x) * cos(x) + sqrt(x + 1.0) - exp(-x)
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0

    let cs: Int64 = Int64(round(s * 1.0e6))
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
