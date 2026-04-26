// set_ops — HashSet insert + membership micro-benchmark (Cangjie).
package set_ops

import std.collection.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 500_000 }

    let start = MonoTime.now()
    let s = HashSet<Int64>(n)
    var seed: Int64 = 1
    let modV: Int64 = n * 2
    var i: Int64 = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        s.add(seed % modV)
        i += 1
    }
    var found: Int64 = 0
    i = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        if (s.contains(seed % modV)) {
            found += 1
        }
        i += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${found}")
    println("ELAPSED_MS:${ms}")
}
