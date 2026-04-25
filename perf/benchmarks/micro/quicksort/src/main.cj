// Hand-written quicksort — micro-benchmark (Cangjie).
//
// Algorithmically identical to the Python and C++ versions: middle element
// pivot, Lomuto partition, recurse-smaller-side / iterate-larger.
package quicksort

import std.time.*
import std.process.*
import std.convert.*

func quicksort(a: Array<Int64>, loIn: Int64, hiIn: Int64): Unit {
    var lo = loIn
    var hi = hiIn
    while (lo < hi) {
        let mid = (lo + hi) >> 1
        let pivot = a[mid]
        // swap a[mid], a[hi]
        let tm = a[mid]; a[mid] = a[hi]; a[hi] = tm
        var i: Int64 = lo - 1
        for (j in lo..hi) {
            if (a[j] <= pivot) {
                i++
                let t = a[i]; a[i] = a[j]; a[j] = t
            }
        }
        i++
        let t2 = a[i]; a[i] = a[hi]; a[hi] = t2
        if ((i - lo) < (hi - i)) {
            quicksort(a, lo, i - 1)
            lo = i + 1
        } else {
            quicksort(a, i + 1, hi)
            hi = i - 1
        }
    }
}

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 1_500_000 }

    let a = Array<Int64>(n, repeat: 0)
    var seed: Int64 = 1234567
    let mask: Int64 = 0x7FFFFFFF
    for (i in 0..n) {
        seed = (seed * 1103515245 + 12345) & mask
        a[i] = seed
    }

    let start = MonoTime.now()
    quicksort(a, 0, n - 1)
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0

    var cs: Int64 = 0
    var k: Int64 = 0
    while (k < n) {
        cs ^= a[k]
        k += 1024
    }
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
