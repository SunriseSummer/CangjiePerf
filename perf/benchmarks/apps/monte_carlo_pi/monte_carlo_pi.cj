// monte_carlo_pi — integer-only Monte-Carlo PI count benchmark (Cangjie).
package monte_carlo_pi

import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 5_000_000 }
    let R: Int64 = 65536
    let R2: Int64 = R * R

    let start = MonoTime.now()
    var seed: Int64 = 1
    var inside: Int64 = 0
    var i: Int64 = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        let x = seed % R
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        let y = seed % R
        if (x * x + y * y <= R2) {
            inside += 1
        }
        i += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${inside}")
    println("ELAPSED_MS:${ms}")
}
