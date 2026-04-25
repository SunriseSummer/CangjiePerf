package fibonacci

import std.time.*

func fib(n: Int64): Int64 {
    if (n <= 1) { return n }
    return fib(n - 1) + fib(n - 2)
}

main(): Int64 {
    let n = 35i64
    let start = MonoTime.now()
    let result = fib(n)
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("fib(${n}) = ${result}")
    println("Time: ${ms} ms")
    return 0
}
