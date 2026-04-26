// crc32 — CRC32 of a deterministic byte stream application benchmark (Cangjie).
package crc32

import std.time.*
import std.process.*
import std.convert.*

func buildTable(): Array<UInt32> {
    let t = Array<UInt32>(256, repeat: 0u32)
    var n: UInt32 = 0
    while (n < 256) {
        var c: UInt32 = n
        var k: Int64 = 0
        while (k < 8) {
            if ((c & 1u32) != 0u32) {
                c = (c >> 1) ^ 0xEDB88320u32
            } else {
                c = c >> 1
            }
            k += 1
        }
        t[Int64(n)] = c
        n += 1
    }
    return t
}

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 5_000_000 }
    let src = Array<UInt8>(n, repeat: 0u8)
    var seed: Int64 = 1
    var i: Int64 = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        src[i] = UInt8((seed >> 8) & 0xFF)
        i += 1
    }
    let table = buildTable()

    let start = MonoTime.now()
    var crc: UInt32 = 0xFFFFFFFFu32
    i = 0
    while (i < n) {
        crc = table[Int64((crc ^ UInt32(src[i])) & 0xFFu32)] ^ (crc >> 8)
        i += 1
    }
    crc ^= 0xFFFFFFFFu32
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${crc}")
    println("ELAPSED_MS:${ms}")
}
