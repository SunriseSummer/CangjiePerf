import std.collection.*
import std.convert.*

const MOD = 1000000007

main(args: Array<String>): Int64 {
    let n = if (args.size > 0) { Int64.parse(args[0]) } else { 300000 }
    let values = ArrayList<Int64>(n)
    var i = 0
    while (i < n) {
        values.add((i * 31) % 4096)
        i++
    }

    var total = 0
    for (value in values) {
        total = (total + value) % MOD
    }

    let counts = HashMap<Int64, Int64>(4096)
    for (value in values) {
        if (counts.contains(value)) {
            counts[value] = counts[value] + 1
        } else {
            counts.add(value, 1)
        }
    }

    var key = 0
    while (key < 4096) {
        if (counts.contains(key)) {
            total = (total + counts[key] * (key + 1)) % MOD
        }
        key++
    }
    println(total)
    return 0
}
