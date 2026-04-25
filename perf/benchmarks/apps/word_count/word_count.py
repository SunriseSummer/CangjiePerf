# Word-count — typical text-processing application benchmark.
#
# Synthesizes a deterministic large body of text (LCG-generated word ids
# joined with spaces and newlines), then tokenizes it and counts word
# frequencies in a hash-map. Stresses string slicing/comparison, hashing,
# and hash-map updates.
#
# Argument: NUM_WORDS (default 1_000_000).

import sys
import time


def gen_text(n: int) -> str:
    seed = 12345
    parts = []
    for i in range(n):
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        # 1024 distinct words via a small wordlist of 5-letter strings.
        idx = seed % 1024
        parts.append(f"w{idx:04d}")
        if (i % 12) == 11:
            parts.append("\n")
        else:
            parts.append(" ")
    return "".join(parts)


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    text = gen_text(n)

    t0 = time.perf_counter_ns()
    counts: dict[str, int] = {}
    for w in text.split():
        counts[w] = counts.get(w, 0) + 1
    elapsed_ns = time.perf_counter_ns() - t0

    # Deterministic checksum: sum( hash-stable per word ) over distinct keys.
    cs = 0
    for k, v in counts.items():
        # Fold the digits of k (e.g. "w0427") into an integer.
        idx = int(k[1:])
        cs ^= idx * 1000003 + v
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
