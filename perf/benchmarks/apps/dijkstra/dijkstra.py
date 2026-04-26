# dijkstra — dense-graph SSSP application benchmark.
#
# Build a V*V adjacency matrix with integer weights from an LCG, then run
# Dijkstra's algorithm with an O(V^2) array-based priority. Returns the
# XOR-fold of the shortest distances.
# Argument: V (default 800).

import sys
import time

INF = 1 << 30


def main() -> None:
    v = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    seed = 1
    g = [[0] * v for _ in range(v)]
    for i in range(v):
        for j in range(v):
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
            g[i][j] = 1 + ((seed >> 8) % 100)
        g[i][i] = 0

    t0 = time.perf_counter_ns()
    dist = [INF] * v
    visited = [False] * v
    dist[0] = 0
    for _ in range(v):
        u = -1
        best = INF
        for k in range(v):
            if not visited[k] and dist[k] < best:
                best = dist[k]
                u = k
        if u == -1:
            break
        visited[u] = True
        row = g[u]
        du = dist[u]
        for k in range(v):
            nd = du + row[k]
            if nd < dist[k]:
                dist[k] = nd
    elapsed_ns = time.perf_counter_ns() - t0

    cs = 0
    for d in dist:
        cs ^= d
    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
