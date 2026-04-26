// string_split — repeated stdlib string-split micro-benchmark (Cangjie).
package string_split

import std.collection.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let repeats: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 20_000 }

    // Build the input string once, outside the timed region.
    let sb = StringBuilder()
    var seed: Int64 = 1
    for (i in 0..64) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        if (i > 0) {
            sb.append(",")
        }
        sb.append("tok")
        sb.append((seed % 100000).toString().padStart(5, padding: "0"))
    }
    let s = sb.toString()

    let start = MonoTime.now()
    var cs: Int64 = 0
    var r: Int64 = 0
    while (r < repeats) {
        let toks = s.split(",")
        let idx = r % Int64(toks.size)
        cs ^= (r + 1) * 1000003 + Int64(toks.size) + Int64(toks[idx].size)
        r += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
