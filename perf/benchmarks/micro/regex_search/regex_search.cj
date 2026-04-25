// Regex find-all — stdlib regex micro-benchmark (Cangjie).
package regex_search

import std.regex.*
import std.time.*
import std.process.*
import std.convert.*

const SAMPLE: String =
    "On 2024-03-21 Alice wrote to bob@example.com about the meeting. " +
    "Charlie replied 2024-04-02 from charlie_99@dev.io with notes about " +
    "Project Kingfisher. References: 1999-12-31, foo@bar.org, Madison.\n"

main() {
    let args = Process.current.arguments
    let repeats: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 4000 }
    let text = SAMPLE * repeats

    let r = Regex(#"(\d{4}-\d{2}-\d{2})|([A-Za-z]+@[a-z]+\.[a-z]+)|(\b[A-Z][a-z]{3,8}\b)"#)

    let start = MonoTime.now()
    var cs: Int64 = 0
    for (_ in r.lazyFindAll(text)) {
        cs++
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
