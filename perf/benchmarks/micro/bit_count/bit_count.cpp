// bit_count — popcount tight-loop micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 5000000;
    auto t0 = std::chrono::steady_clock::now();
    int64_t cs = 0;
    for (int64_t i = 0; i < n; ++i) {
        uint32_t v = static_cast<uint32_t>(i * 2654435761ULL);
        // Manual popcount to keep all five implementations apples-to-apples.
        uint32_t x = v;
        int c = 0;
        while (x) { x &= x - 1; ++c; }
        cs += c;
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
