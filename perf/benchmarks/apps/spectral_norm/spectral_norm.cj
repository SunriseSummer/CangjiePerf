// Spectral norm — Computer Language Benchmarks Game numerical kernel (Cangjie).
//
// Algorithmically identical to the Python and C++ versions: 10 power
// iterations of v <- A^T A v on the same A(i,j) infinite-matrix function,
// same array layout, same final checksum sqrt(<u,v>/<v,v>) * 1e9.
package spectral_norm

import std.math.*
import std.time.*
import std.process.*
import std.convert.*

func aij(i: Int64, j: Int64): Float64 {
    return 1.0 / Float64(((i + j) * (i + j + 1) >> 1) + i + 1)
}

func mulAv(v: Array<Float64>, out: Array<Float64>, n: Int64): Unit {
    for (i in 0..n) {
        var s: Float64 = 0.0
        for (j in 0..n) {
            s += aij(i, j) * v[j]
        }
        out[i] = s
    }
}

func mulAtv(v: Array<Float64>, out: Array<Float64>, n: Int64): Unit {
    for (i in 0..n) {
        var s: Float64 = 0.0
        for (j in 0..n) {
            s += aij(j, i) * v[j]
        }
        out[i] = s
    }
}

func mulAtAv(v: Array<Float64>, out: Array<Float64>, tmp: Array<Float64>, n: Int64): Unit {
    mulAv(v, tmp, n)
    mulAtv(tmp, out, n)
}

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 1500 }

    let u = Array<Float64>(n, repeat: 1.0)
    let v = Array<Float64>(n, repeat: 0.0)
    let tmp = Array<Float64>(n, repeat: 0.0)

    let start = MonoTime.now()
    for (_ in 0..10) {
        mulAtAv(u, v, tmp, n)
        mulAtAv(v, u, tmp, n)
    }
    var vbv: Float64 = 0.0
    var vv: Float64 = 0.0
    for (i in 0..n) {
        vbv += u[i] * v[i]
        vv  += v[i] * v[i]
    }
    let sn = sqrt(vbv / vv)
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0

    let cs: Int64 = Int64(round(sn * 1.0e9))
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
