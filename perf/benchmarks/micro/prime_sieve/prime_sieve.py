# Sieve of Eratosthenes — micro-benchmark.
#
# Builds a boolean sieve of size N+1, then marks composites with the
# textbook outer-loop-up-to-sqrt(N) variant. Implementations are kept
# algorithmically identical across the three languages: same loop bounds,
# same inner step (`for j in i*i..N+1 step i: sieve[j] = False`), same
# checksum (count of primes XOR sum of primes mod 2^31).
#
# Argument: N (default 20_000_000).

import sys
import time


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20_000_000

    t0 = time.perf_counter_ns()
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0] = 0
    sieve[1] = 0
    i = 2
    while i * i <= n:
        if sieve[i]:
            j = i * i
            while j <= n:
                sieve[j] = 0
                j += i
        i += 1
    # Compute checksum: count of primes, plus sum of primes (mod 2^31).
    count = 0
    psum = 0
    mask = 0x7FFFFFFF
    for k in range(2, n + 1):
        if sieve[k]:
            count += 1
            psum = (psum + k) & mask
    elapsed_ns = time.perf_counter_ns() - t0

    cs = (count * 1_000_003 + psum) & mask
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
