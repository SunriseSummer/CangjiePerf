# Binary trees — allocation / GC pressure (Computer Language Benchmarks Game).
#
# Builds and walks many small balanced binary trees. Stresses small-object
# allocation, deallocation, and (where applicable) GC.
#
# Argument: DEPTH (default 14). Total work ~ 2^DEPTH nodes.

import sys
import time


class Node:
    __slots__ = ("l", "r")

    def __init__(self, l, r):
        self.l = l
        self.r = r


def make_tree(depth: int) -> object:
    if depth == 0:
        return Node(None, None)
    return Node(make_tree(depth - 1), make_tree(depth - 1))


def check_tree(node) -> int:
    if node.l is None:
        return 1
    return 1 + check_tree(node.l) + check_tree(node.r)


def main() -> None:
    max_depth = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    min_depth = 4
    sys.setrecursionlimit(max(1000, max_depth * 4))
    stretch_depth = max_depth + 1

    t0 = time.perf_counter_ns()

    # Stretch tree
    stretch = check_tree(make_tree(stretch_depth))

    # Long-lived tree
    long_lived = make_tree(max_depth)

    total = stretch
    d = min_depth
    while d <= max_depth:
        iterations = 1 << (max_depth - d + min_depth)
        s = 0
        for _ in range(iterations):
            s += check_tree(make_tree(d))
        total ^= (iterations * 1000003 + s)
        d += 2

    total ^= check_tree(long_lived)
    elapsed_ns = time.perf_counter_ns() - t0

    print(f"CHECKSUM:{total}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
