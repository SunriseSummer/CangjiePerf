# xor_shift — xorshift64 PRNG tight-loop micro-benchmark.
#
# Iterate xorshift64 N times starting from a fixed seed and return the final
# state. Pure 64-bit bitwise / shift ops. Argument: N (default 50_000_000).

import sys
import time

MASK = 0xFFFFFFFFFFFFFFFF


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50_000_000
    t0 = time.perf_counter_ns()
    s = 0x123456789ABCDEF0
    for _ in range(n):
        s ^= (s << 13) & MASK
        s ^= (s >> 7) & MASK
        s ^= (s << 17) & MASK
        s &= MASK
    elapsed_ns = time.perf_counter_ns() - t0
    print(f"CHECKSUM:{s}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
