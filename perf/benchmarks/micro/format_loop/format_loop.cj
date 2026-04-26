// format_loop — integer-formatting tight-loop micro-benchmark (Cangjie).
package format_loop

import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 500_000 }

    let start = MonoTime.now()
    let sb = StringBuilder()
    var i: Int64 = 0
    while (i < n) {
        sb.append(i.toString().padStart(8, padding: "0"))
        sb.append(";")
        i += 1
    }
    let s = sb.toString()
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${s.size}")
    println("ELAPSED_MS:${ms}")
}
