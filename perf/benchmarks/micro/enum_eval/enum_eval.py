# Enum / algebraic-data-type recursive pattern matching — micro-benchmark.
#
# Builds an arithmetic expression tree of depth D, then evaluates it N times
# using recursive pattern matching. Stresses sum types, recursion, and
# repeated dispatch on a tag.
#
# Args: DEPTH N  (defaults: 18  60).

import sys
import time
from dataclasses import dataclass


# Sum type: Num | Add | Sub | Mul
@dataclass
class Num:
    v: int


@dataclass
class Add:
    l: object
    r: object


@dataclass
class Sub:
    l: object
    r: object


@dataclass
class Mul:
    l: object
    r: object


def build(depth: int, seed: int) -> object:
    if depth == 0:
        return Num((seed & 0x3F) + 1)
    # Mask to keep `seed` non-negative and below 2^31, matching the Cangjie
    # implementation (which would otherwise overflow signed Int64).
    s = ((seed * 1103515245) + 12345) & 0x7FFFFFFF
    tag = (s >> 17) & 3
    left = build(depth - 1, s)
    right = build(depth - 1, s ^ 0xABCDEF)
    if tag == 0:
        return Add(left, right)
    if tag == 1:
        return Sub(left, right)
    if tag == 2:
        return Mul(left, right)
    return Add(left, right)


def _wrap64(v: int) -> int:
    """Truncate to a signed 64-bit integer (matches C++/Cangjie wrap)."""
    v &= 0xFFFFFFFFFFFFFFFF
    if v >= 0x8000000000000000:
        v -= 0x10000000000000000
    return v


def evaluate(e: object) -> int:
    if isinstance(e, Num):
        return e.v
    if isinstance(e, Add):
        return _wrap64(evaluate(e.l) + evaluate(e.r))
    if isinstance(e, Sub):
        return _wrap64(evaluate(e.l) - evaluate(e.r))
    if isinstance(e, Mul):
        return _wrap64(evaluate(e.l) * evaluate(e.r))
    raise TypeError(type(e))


def main() -> None:
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    sys.setrecursionlimit(max(1000, depth * 4))

    tree = build(depth, 1)

    t0 = time.perf_counter_ns()
    cs = 0
    for _ in range(n):
        cs ^= evaluate(tree)
    elapsed_ns = time.perf_counter_ns() - t0

    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
