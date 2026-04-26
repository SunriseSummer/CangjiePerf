// gcd_loop — Euclidean GCD tight-loop micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

static int64_t gcd(int64_t a, int64_t b) {
    while (b != 0) {
        int64_t t = a % b;
        a = b;
        b = t;
    }
    return a;
}

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 2000000;
    auto t0 = std::chrono::steady_clock::now();
    int64_t cs = 0;
    int64_t seed = 1;
    for (int64_t i = 1; i <= n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        cs = (cs + gcd(i, seed)) & 0x7FFFFFFFLL;
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
