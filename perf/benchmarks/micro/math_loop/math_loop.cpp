// Math-intensive loop — std math micro-benchmark (C++).
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 5'000'000LL;

    auto t0 = std::chrono::steady_clock::now();
    double s = 0.0;
    double inv = 1.0 / static_cast<double>(n);
    for (int64_t i = 0; i < n; ++i) {
        double x = static_cast<double>(i) * inv;
        s += std::sin(x) * std::cos(x) + std::sqrt(x + 1.0) - std::exp(-x);
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    int64_t cs = static_cast<int64_t>(std::llround(s * 1e6));
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
