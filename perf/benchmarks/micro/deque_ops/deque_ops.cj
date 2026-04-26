// deque_ops — dynamic-array push/pop micro-benchmark (Cangjie).
package deque_ops

import std.collection.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 2_000_000 }

    let start = MonoTime.now()
    let a = ArrayList<Int64>(n)
    var seed: Int64 = 1
    var i: Int64 = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        a.add(seed)
        i += 1
    }
    var cs: Int64 = 0
    while (a.size > 0) {
        cs ^= a.remove(at: a.size - 1)
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
