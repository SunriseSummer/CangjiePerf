// xor_shift — xorshift64 PRNG tight-loop micro-benchmark (Cangjie).
package xor_shift

import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 50_000_000 }

    let start = MonoTime.now()
    var s: UInt64 = 0x123456789ABCDEF0
    var i: Int64 = 0
    while (i < n) {
        s ^= s << 13
        s ^= s >> 7
        s ^= s << 17
        i += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${s}")
    println("ELAPSED_MS:${ms}")
}
