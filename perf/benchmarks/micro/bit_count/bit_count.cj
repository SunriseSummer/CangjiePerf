// bit_count — popcount tight-loop micro-benchmark (Cangjie).
package bit_count

import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 5_000_000 }

    let start = MonoTime.now()
    var cs: Int64 = 0
    let mask: Int64 = 0xFFFFFFFF
    for (i in 0..n) {
        var x: Int64 = (i * 2654435761) & mask
        var c: Int64 = 0
        while (x != 0) {
            x &= x - 1
            c += 1
        }
        cs += c
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
