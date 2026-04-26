// knapsack_dp — 0/1 knapsack DP application benchmark (Cangjie).
package knapsack_dp

import std.time.*
import std.process.*
import std.convert.*

let C: Int64 = 4000
let MAXW: Int64 = 200
let MAXV: Int64 = 1000

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 1500 }
    let w = Array<Int64>(n, repeat: 0)
    let v = Array<Int64>(n, repeat: 0)
    var seed: Int64 = 1
    var i: Int64 = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        w[i] = 1 + (seed % MAXW)
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        v[i] = 1 + (seed % MAXV)
        i += 1
    }

    let start = MonoTime.now()
    let dp = Array<Int64>(C + 1, repeat: 0)
    i = 0
    while (i < n) {
        let wi = w[i]
        let vi = v[i]
        var c: Int64 = C
        while (c >= wi) {
            let nv = dp[c - wi] + vi
            if (nv > dp[c]) {
                dp[c] = nv
            }
            c -= 1
        }
        i += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${dp[C]}")
    println("ELAPSED_MS:${ms}")
}
