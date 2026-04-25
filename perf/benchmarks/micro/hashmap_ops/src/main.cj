// HashMap insert + lookup — stdlib hash-table micro-benchmark (Cangjie).
package hashmap_ops

import std.collection.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 500_000 }

    // Pre-build keys outside the timed region.
    let keys = Array<String>(n, repeat: "")
    for (i in 0..n) {
        keys[i] = "key-${i}"
    }

    let start = MonoTime.now()
    let m = HashMap<String, Int64>(n)
    for (i in 0..n) {
        m[keys[i]] = i
    }
    var cs: Int64 = 0
    for (i in 0..n) {
        match (m.get(keys[i])) {
            case Some(v) => cs ^= v
            case None => ()
        }
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
