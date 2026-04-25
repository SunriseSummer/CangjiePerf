// Fibonacci — recursive function-call micro-benchmark (Cangjie).
package fibonacci

import std.time.*
import std.process.*
import std.convert.*

func fib(n: Int64): Int64 {
    if (n < 2) {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 32 }
    let start = MonoTime.now()
    let result = fib(n)
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${result}")
    println("ELAPSED_MS:${ms}")
}
