#!/usr/bin/env python3
from __future__ import annotations

import sys

MOD = 1_000_000_007


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 500_000
    counts: dict[str, int] = {}
    for i in range(n):
        word = f"w{(i * 1315423911) & 4095}"
        counts[word] = counts.get(word, 0) + 1

    checksum = 0
    for word, count in counts.items():
        checksum = (checksum + len(word) * count + count * count) % MOD
    print(checksum)


if __name__ == "__main__":
    main()
