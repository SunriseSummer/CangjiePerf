// dijkstra — dense-graph SSSP application benchmark (Cangjie).
package dijkstra

import std.time.*
import std.process.*
import std.convert.*

let INF: Int64 = 1 << 30

main() {
    let args = Process.current.arguments
    let v: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 800 }
    var seed: Int64 = 1
    let g = Array<Int64>(v * v, repeat: 0)
    var i: Int64 = 0
    while (i < v) {
        var j: Int64 = 0
        while (j < v) {
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            g[i * v + j] = 1 + ((seed >> 8) % 100)
            j += 1
        }
        g[i * v + i] = 0
        i += 1
    }

    let start = MonoTime.now()
    let dist = Array<Int64>(v, repeat: INF)
    let visited = Array<Bool>(v, repeat: false)
    dist[0] = 0
    var s: Int64 = 0
    while (s < v) {
        var u: Int64 = -1
        var best: Int64 = INF
        var k: Int64 = 0
        while (k < v) {
            if (!visited[k] && dist[k] < best) {
                best = dist[k]
                u = k
            }
            k += 1
        }
        if (u < 0) {
            break
        }
        visited[u] = true
        let du = dist[u]
        let base = u * v
        k = 0
        while (k < v) {
            let nd = du + g[base + k]
            if (nd < dist[k]) {
                dist[k] = nd
            }
            k += 1
        }
        s += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    var cs: Int64 = 0
    var m: Int64 = 0
    while (m < v) {
        cs ^= dist[m]
        m += 1
    }
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
