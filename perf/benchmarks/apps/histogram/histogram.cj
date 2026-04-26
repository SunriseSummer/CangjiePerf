// histogram — bucket-counts of LCG ints application benchmark (Cangjie).
package histogram

import std.time.*
import std.process.*
import std.convert.*

let K: Int64 = 1024

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 5_000_000 }

    let start = MonoTime.now()
    let buckets = Array<Int64>(K, repeat: 0)
    var seed: Int64 = 1
    var i: Int64 = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        let idx = (seed >> 8) & (K - 1)
        buckets[idx] = buckets[idx] + 1
        i += 1
    }
    var cs: Int64 = 0
    var k: Int64 = 0
    while (k < K) {
        cs ^= buckets[k]
        k += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
