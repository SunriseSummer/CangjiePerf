// Mandelbrot — application-style numerical benchmark (Cangjie).
package mandelbrot

import std.time.*
import std.process.*
import std.convert.*

func mandelbrot(width: Int64, maxIter: Int64): Int64 {
    let invW: Float64 = 2.0 / Float64(width)
    var total: Int64 = 0
    for (py in 0..width) {
        let ci: Float64 = Float64(py) * invW - 1.0
        for (px in 0..width) {
            let cr: Float64 = Float64(px) * invW - 1.5
            var zr: Float64 = 0.0
            var zi: Float64 = 0.0
            var n: Int64 = 0
            while (n < maxIter) {
                let zr2 = zr * zr
                let zi2 = zi * zi
                if (zr2 + zi2 > 4.0) {
                    break
                }
                zi = 2.0 * zr * zi + ci
                zr = zr2 - zi2 + cr
                n++
            }
            total += n
        }
    }
    return total
}

main() {
    let args = Process.current.arguments
    let width: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 600 }
    let maxIter: Int64 = if (args.size > 1) { Int64.parse(args[1]) } else { 200 }

    let start = MonoTime.now()
    let cs = mandelbrot(width, maxIter)
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
