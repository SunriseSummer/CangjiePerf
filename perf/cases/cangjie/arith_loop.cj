import std.convert.*

const MOD = 1000000007

main(args: Array<String>): Int64 {
    let n = if (args.size > 0) { Int64.parse(args[0]) } else { 2000000 }
    var x = 0
    var i = 0
    while (i < n) {
        x = (x * 1664525 + i + 1013904223) % MOD
        i++
    }
    println(x)
    return 0
}
