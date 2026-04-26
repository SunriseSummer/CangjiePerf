// base64 — base64 encoding application benchmark (Cangjie).
package base64

import std.time.*
import std.process.*
import std.convert.*

let ALPHA: Array<UInt8> = [
    0x41u8, 0x42u8, 0x43u8, 0x44u8, 0x45u8, 0x46u8, 0x47u8, 0x48u8,
    0x49u8, 0x4Au8, 0x4Bu8, 0x4Cu8, 0x4Du8, 0x4Eu8, 0x4Fu8, 0x50u8,
    0x51u8, 0x52u8, 0x53u8, 0x54u8, 0x55u8, 0x56u8, 0x57u8, 0x58u8,
    0x59u8, 0x5Au8, 0x61u8, 0x62u8, 0x63u8, 0x64u8, 0x65u8, 0x66u8,
    0x67u8, 0x68u8, 0x69u8, 0x6Au8, 0x6Bu8, 0x6Cu8, 0x6Du8, 0x6Eu8,
    0x6Fu8, 0x70u8, 0x71u8, 0x72u8, 0x73u8, 0x74u8, 0x75u8, 0x76u8,
    0x77u8, 0x78u8, 0x79u8, 0x7Au8, 0x30u8, 0x31u8, 0x32u8, 0x33u8,
    0x34u8, 0x35u8, 0x36u8, 0x37u8, 0x38u8, 0x39u8, 0x2Bu8, 0x2Fu8
]

main() {
    let args = Process.current.arguments
    let n: Int64 = if (args.size > 0) { Int64.parse(args[0]) } else { 2_000_000 }
    let src = Array<UInt8>(n, repeat: 0u8)
    var seed: Int64 = 1
    var i: Int64 = 0
    while (i < n) {
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        src[i] = UInt8((seed >> 8) & 0xFF)
        i += 1
    }

    let start = MonoTime.now()
    let outLen: Int64 = ((n + 2) / 3) * 4
    let out = Array<UInt8>(outLen, repeat: 0u8)
    var oi: Int64 = 0
    i = 0
    while (i + 3 <= n) {
        let b0 = src[i]
        let b1 = src[i + 1]
        let b2 = src[i + 2]
        out[oi]     = ALPHA[Int64(b0 >> 2)]
        out[oi + 1] = ALPHA[Int64(((b0 & 0x3u8) << 4) | (b1 >> 4))]
        out[oi + 2] = ALPHA[Int64(((b1 & 0xFu8) << 2) | (b2 >> 6))]
        out[oi + 3] = ALPHA[Int64(b2 & 0x3Fu8)]
        oi += 4
        i += 3
    }
    let rem = n - i
    if (rem == 1) {
        let b0 = src[i]
        out[oi]     = ALPHA[Int64(b0 >> 2)]
        out[oi + 1] = ALPHA[Int64((b0 & 0x3u8) << 4)]
        out[oi + 2] = 0x3Du8
        out[oi + 3] = 0x3Du8
    } else if (rem == 2) {
        let b0 = src[i]
        let b1 = src[i + 1]
        out[oi]     = ALPHA[Int64(b0 >> 2)]
        out[oi + 1] = ALPHA[Int64(((b0 & 0x3u8) << 4) | (b1 >> 4))]
        out[oi + 2] = ALPHA[Int64((b1 & 0xFu8) << 2)]
        out[oi + 3] = 0x3Du8
    }
    var cs: Int64 = 0
    var k: Int64 = 0
    while (k < outLen) {
        cs ^= Int64(out[k])
        k += 1
    }
    let elapsed = MonoTime.now() - start
    let ms = Float64(elapsed.toNanoseconds()) / 1_000_000.0
    println("CHECKSUM:${cs}")
    println("ELAPSED_MS:${ms}")
}
