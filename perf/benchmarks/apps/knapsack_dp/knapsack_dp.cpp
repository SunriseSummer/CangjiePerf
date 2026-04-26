// knapsack_dp — 0/1 knapsack DP application benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

constexpr int C = 4000;
constexpr int MAXW = 200;
constexpr int MAXV = 1000;

int main(int argc, char** argv) {
    int n = (argc > 1) ? std::atoi(argv[1]) : 1500;
    std::vector<int> w(n), v(n);
    int64_t seed = 1;
    for (int i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        w[i] = 1 + static_cast<int>(seed % MAXW);
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        v[i] = 1 + static_cast<int>(seed % MAXV);
    }

    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> dp(C + 1, 0);
    for (int i = 0; i < n; ++i) {
        int wi = w[i], vi = v[i];
        for (int c = C; c >= wi; --c) {
            int nv = dp[c - wi] + vi;
            if (nv > dp[c]) dp[c] = nv;
        }
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%d\n", dp[C]);
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
