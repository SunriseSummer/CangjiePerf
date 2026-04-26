// string_search — substring-search tight-loop micro-benchmark (Cangjie).
package string_search

import std.collection.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let repeats: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 50_000 }

    let sb = StringBuilder()
    var seed: Int64 = 1
    for (_ in 0..10000) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        let c: UInt8 = UInt8(0x61) + UInt8(seed % 8)  // 'a' + offset
        sb.append(Rune(UInt32(c)))
    }
    let hay = sb.toString()
    let needle = "abcde"

    let start = MonoTime.now()
    var cs: Int64 = 0
    var r: Int64 = 0
    while (r < repeats) {
        var count: Int64 = 0
        var pos: Int64 = 0
        while (true) {
            match (hay.indexOf(needle, pos)) {
                case Some(i) =>
                    count += 1
                    pos = i + 1
                case None => break
            }
        }
        cs ^= (r + 1) * 1000003 + count
        r += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
