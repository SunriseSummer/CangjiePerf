# base64 — base64 encoding application benchmark.
#
# Generate N deterministic bytes via LCG, encode in base64 (manual table),
# and return the XOR of all encoded byte values as the checksum.
# Argument: N (default 2_000_000).

import sys
import time

ALPHA = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    src = bytearray(n)
    seed = 1
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        src[i] = (seed >> 8) & 0xFF

    t0 = time.perf_counter_ns()
    out = bytearray(((n + 2) // 3) * 4)
    oi = 0
    i = 0
    while i + 3 <= n:
        b0 = src[i]; b1 = src[i + 1]; b2 = src[i + 2]
        out[oi] = ALPHA[b0 >> 2]
        out[oi + 1] = ALPHA[((b0 & 0x3) << 4) | (b1 >> 4)]
        out[oi + 2] = ALPHA[((b1 & 0xF) << 2) | (b2 >> 6)]
        out[oi + 3] = ALPHA[b2 & 0x3F]
        oi += 4
        i += 3
    rem = n - i
    if rem == 1:
        b0 = src[i]
        out[oi] = ALPHA[b0 >> 2]
        out[oi + 1] = ALPHA[(b0 & 0x3) << 4]
        out[oi + 2] = ord('=')
        out[oi + 3] = ord('=')
    elif rem == 2:
        b0 = src[i]; b1 = src[i + 1]
        out[oi] = ALPHA[b0 >> 2]
        out[oi + 1] = ALPHA[((b0 & 0x3) << 4) | (b1 >> 4)]
        out[oi + 2] = ALPHA[(b1 & 0xF) << 2]
        out[oi + 3] = ord('=')

    cs = 0
    for v in out:
        cs ^= v
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
