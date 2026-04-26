// dijkstra — dense-graph SSSP application benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

constexpr int INF = 1 << 30;

int main(int argc, char** argv) {
    int v = (argc > 1) ? std::atoi(argv[1]) : 800;
    int64_t seed = 1;
    std::vector<int> g(static_cast<size_t>(v) * v);
    for (int i = 0; i < v; ++i) {
        for (int j = 0; j < v; ++j) {
            seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
            g[i * v + j] = 1 + static_cast<int>((seed >> 8) % 100);
        }
        g[i * v + i] = 0;
    }

    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> dist(v, INF);
    std::vector<uint8_t> visited(v, 0);
    dist[0] = 0;
    for (int s = 0; s < v; ++s) {
        int u = -1, best = INF;
        for (int k = 0; k < v; ++k) {
            if (!visited[k] && dist[k] < best) { best = dist[k]; u = k; }
        }
        if (u == -1) break;
        visited[u] = 1;
        int du = dist[u];
        const int* row = &g[u * v];
        for (int k = 0; k < v; ++k) {
            int nd = du + row[k];
            if (nd < dist[k]) dist[k] = nd;
        }
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    int64_t cs = 0;
    for (int d : dist) cs ^= d;
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
