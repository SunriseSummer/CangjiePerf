// Matrix multiplication — naive O(N^3) double-precision matmul (Cangjie).
package matrix_multiply

import std.math.*
import std.time.*
import std.process.*
import std.convert.*

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 250 }

    // Row-major, contiguous storage.
    let a = Array<Float64>(n * n, repeat: 0.0)
    let b = Array<Float64>(n * n, repeat: 0.0)
    let c = Array<Float64>(n * n, repeat: 0.0)
    for (i in 0..n) {
        for (j in 0..n) {
            a[i * n + j] = Float64((i * 7 + j * 13) % 100) * 0.01
            b[i * n + j] = Float64((i * 11 + j * 17) % 100) * 0.01
        }
    }

    let start = MonoTime.now()
    for (i in 0..n) {
        for (k in 0..n) {
            let aik = a[i * n + k]
            let bRow = k * n
            let cRow = i * n
            for (j in 0..n) {
                c[cRow + j] += aik * b[bRow + j]
            }
        }
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0

    var total: Float64 = 0.0
    for (i in 0..n) {
        total += c[i * n + i]
    }
    let cs: Int64 = Int64(round(total * 1.0e6))
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
