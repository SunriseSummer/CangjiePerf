// String building — stdlib StringBuilder-style micro-benchmark (Cangjie).
package string_concat

import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 500_000 }

    let start = MonoTime.now()
    let sb = StringBuilder()
    for (i in 0..n) {
        sb.append("frag")
        sb.append(i.toString())
        sb.append(";")
    }
    let s = sb.toString()
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${s.size}")
    println("ELAPSED_MS:${ms}")
}
