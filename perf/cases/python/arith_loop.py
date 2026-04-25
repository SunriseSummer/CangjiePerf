#!/usr/bin/env python3
from __future__ import annotations

import sys

MOD = 1_000_000_007


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    x = 0
    for i in range(n):
        x = (x * 1_664_525 + i + 1_013_904_223) % MOD
    print(x)


if __name__ == "__main__":
    main()
