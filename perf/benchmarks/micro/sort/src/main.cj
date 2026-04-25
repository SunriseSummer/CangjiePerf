// Sort N integers — stdlib-sort micro-benchmark (Cangjie).
package sort_bench

import std.collection.*
import std.sort.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 2_000_000 }
    let arr = Array<Int64>(n, repeat: 0)
    var seed: Int64 = 12345
    for (i in 0..n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        arr[i] = seed
    }
    let start = MonoTime.now()
    sort(arr)
    let elapsed = MonoTime.now() - start
    let cs = arr[0] ^ arr[n / 2] ^ arr[n - 1]
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
