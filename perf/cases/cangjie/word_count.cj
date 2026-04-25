import std.collection.*
import std.convert.*

const MOD = 1000000007

main(args: Array<String>): Int64 {
    let n = if (args.size > 0) { Int64.parse(args[0]) } else { 500000 }
    let counts = HashMap<String, Int64>(4096)
    var i = 0
    while (i < n) {
        let word = "w${(i * 1315423911) & 4095}"
        if (counts.contains(word)) {
            counts[word] = counts[word] + 1
        } else {
            counts.add(word, 1)
        }
        i++
    }

    var checksum = 0
    for ((word, count) in counts) {
        checksum = (checksum + word.size * count + count * count) % MOD
    }
    println(checksum)
    return 0
}
