# crc32 — CRC32 of a deterministic byte stream application benchmark.
#
# Generate N bytes via LCG, then compute CRC32 (IEEE 802.3 polynomial) byte
# by byte using a precomputed 256-entry table built from the same polynomial.
# Argument: N (default 5_000_000).

import sys
import time


def build_table() -> list[int]:
    table = [0] * 256
    for n in range(256):
        c = n
        for _ in range(8):
            c = (c >> 1) ^ (0xEDB88320 if c & 1 else 0)
        table[n] = c
    return table


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    src = bytearray(n)
    seed = 1
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        src[i] = (seed >> 8) & 0xFF
    table = build_table()

    t0 = time.perf_counter_ns()
    crc = 0xFFFFFFFF
    for b in src:
        crc = table[(crc ^ b) & 0xFF] ^ (crc >> 8)
    crc ^= 0xFFFFFFFF
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{crc}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
