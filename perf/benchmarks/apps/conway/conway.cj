// conway — Game of Life N-step application benchmark (Cangjie).
package conway

import std.time.*
import std.process.*
import std.convert.*

let W: Int64 = 200

main() {
    let args = Process.current.arguments
    let steps: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 200 }
    let cells: Int64 = W * W
    var grid = Array<UInt8>(cells, repeat: 0u8)
    var nxt = Array<UInt8>(cells, repeat: 0u8)
    var seed: Int64 = 1
    var i: Int64 = 0
    while (i < cells) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        grid[i] = if (((seed >> 16) & 3) < 2) { 1u8 } else { 0u8 }
        i += 1
    }

    let start = MonoTime.now()
    var s: Int64 = 0
    while (s < steps) {
        var y: Int64 = 0
        while (y < W) {
            let yu = (y + W - 1) % W
            let yd = (y + 1) % W
            let row = y * W
            let rowU = yu * W
            let rowD = yd * W
            var x: Int64 = 0
            while (x < W) {
                let xl = (x + W - 1) % W
                let xr = (x + 1) % W
                let n: Int64 = Int64(grid[rowU + xl]) + Int64(grid[rowU + x]) + Int64(grid[rowU + xr])
                             + Int64(grid[row + xl]) + Int64(grid[row + xr])
                             + Int64(grid[rowD + xl]) + Int64(grid[rowD + x]) + Int64(grid[rowD + xr])
                let alive = grid[row + x]
                var nv: UInt8 = 0u8
                if (alive != 0u8) {
                    if (n == 2 || n == 3) { nv = 1u8 }
                } else if (n == 3) {
                    nv = 1u8
                }
                nxt[row + x] = nv
                x += 1
            }
            y += 1
        }
        let tmp = grid
        grid = nxt
        nxt = tmp
        s += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    var cs: Int64 = 0
    var k: Int64 = 0
    while (k < cells) {
        cs += Int64(grid[k])
        k += 1
    }
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
