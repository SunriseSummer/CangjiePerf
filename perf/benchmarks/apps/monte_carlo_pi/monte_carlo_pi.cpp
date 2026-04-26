// monte_carlo_pi — integer-only Monte-Carlo PI count benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 5000000;
    const int64_t R = 65536;
    const int64_t R2 = R * R;
    auto t0 = std::chrono::steady_clock::now();
    int64_t seed = 1, inside = 0;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        int64_t x = seed % R;
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        int64_t y = seed % R;
        if (x * x + y * y <= R2) ++inside;
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(inside));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
