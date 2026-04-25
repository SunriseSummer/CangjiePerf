// Sieve of Eratosthenes — micro-benchmark (Cangjie).
//
// Implementation is intentionally kept symmetric with the C++/Python
// versions: same loop bounds (i*i <= n), same inner stride (j += i),
// same final checksum formula.
package prime_sieve

import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 20_000_000 }

    let start = MonoTime.now()
    let sieve = Array<Bool>(n + 1, repeat: true)
    sieve[0] = false
    sieve[1] = false
    var i: Int64 = 2
    while (i * i <= n) {
        if (sieve[i]) {
            var j: Int64 = i * i
            while (j <= n) {
                sieve[j] = false
                j += i
            }
        }
        i++
    }
    var count: Int64 = 0
    var psum: Int64 = 0
    let mask: Int64 = 0x7FFFFFFF
    for (k in 2..(n + 1)) {
        if (sieve[k]) {
            count++
            psum = (psum + k) & mask
        }
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0

    let cs: Int64 = (count * 1_000_003 + psum) & mask
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
