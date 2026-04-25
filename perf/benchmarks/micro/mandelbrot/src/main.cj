package mandelbrot

import std.time.*

func mandelbrot(cx: Float64, cy: Float64, maxIter: Int64): Int64 {
    var x = 0.0
    var y = 0.0
    var iter = 0i64
    while (iter < maxIter && x * x + y * y <= 4.0) {
        let tmp = x * x - y * y + cx
        y = 2.0 * x * y + cy
        x = tmp
        iter++
    }
    return iter
}

main(): Int64 {
    let size = 800
    let maxIter = 1000i64
    let start = MonoTime.now()
    var count = 0i64
    for (py in 0..size) {
        for (px in 0..size) {
            let cx = Float64(px) / Float64(size) * 3.5 - 2.5
            let cy = Float64(py) / Float64(size) * 2.0 - 1.0
            if (mandelbrot(cx, cy, maxIter) == maxIter) {
                count++
            }
        }
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("Mandelbrot 800x800 maxIter=1000: ${count} interior points")
    println("Time: ${ms} ms")
    return 0
}
