// Word-count — typical text-processing application benchmark (Cangjie).
package word_count

import std.collection.*
import std.time.*
import std.process.*
import std.convert.*

func genText(n: Int64): String {
    var seed: Int64 = 12345
    let sb = StringBuilder()
    for (i in 0..n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        let idx = seed % 1024
        sb.append("w")
        sb.append(idx.toString().padStart(4, padding: "0"))
        if ((i % 12) == 11) {
            sb.append("\n")
        } else {
            sb.append(" ")
        }
    }
    return sb.toString()
}

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 1_000_000 }
    let text = genText(n)

    let start = MonoTime.now()
    let counts = HashMap<String, Int64>()
    // String.split with " " then with "\n" would over-allocate; use lazySplit
    // by whitespace via two passes (split on '\n' then on ' '). This still
    // gives us the same words in the same order.
    for (line in text.lazySplit("\n", removeEmpty: true)) {
        for (w in line.lazySplit(" ", removeEmpty: true)) {
            match (counts.get(w)) {
                case Some(v) => counts[w] = v + 1
                case None    => counts[w] = 1
            }
        }
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0

    var cs: Int64 = 0
    for ((k, v) in counts) {
        // Parse "wNNNN" → NNNN.
        let idx = Int64.parse(k[1..])
        cs ^= idx * 1000003 + v
    }
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
