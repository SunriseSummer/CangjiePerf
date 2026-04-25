#!/usr/bin/env python3
from __future__ import annotations

import sys

MOD = 1_000_000_007


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 300_000
    values: list[int] = []
    for i in range(n):
        values.append((i * 31) % 4096)

    total = 0
    for value in values:
        total = (total + value) % MOD

    counts: dict[int, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1

    for key in range(4096):
        total = (total + counts.get(key, 0) * (key + 1)) % MOD
    print(total)


if __name__ == "__main__":
    main()
