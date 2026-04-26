// levenshtein — edit-distance DP application benchmark (Cangjie).
package levenshtein

import std.time.*
import std.process.*
import std.convert.*

func makeStr(seedIn: Int64, n: Int64): Array<UInt8> {
    let out = Array<UInt8>(n, repeat: 0u8)
    var seed = seedIn
    var i: Int64 = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        out[i] = UInt8(0x61) + UInt8((seed >> 16) & 7)
        i += 1
    }
    return out
}

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 1500 }
    let a = makeStr(1, n)
    let b = makeStr(7, n)

    let start = MonoTime.now()
    var prev = Array<Int64>(n + 1, repeat: 0)
    var cur = Array<Int64>(n + 1, repeat: 0)
    var j: Int64 = 0
    while (j <= n) {
        prev[j] = j
        j += 1
    }
    var i: Int64 = 1
    while (i <= n) {
        cur[0] = i
        let ai = a[i - 1]
        var k: Int64 = 1
        while (k <= n) {
            let cost: Int64 = if (ai == b[k - 1]) { 0 } else { 1 }
            var v = prev[k - 1] + cost
            let d1 = cur[k - 1] + 1
            if (d1 < v) { v = d1 }
            let d2 = prev[k] + 1
            if (d2 < v) { v = d2 }
            cur[k] = v
            k += 1
        }
        let tmp = prev
        prev = cur
        cur = tmp
        i += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${prev[n]}")
    println("ELAPSED_MS:${ms}")
}
