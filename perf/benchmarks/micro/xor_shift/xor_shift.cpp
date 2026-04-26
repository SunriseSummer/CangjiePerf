// xor_shift — xorshift64 PRNG tight-loop micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 50000000;
    auto t0 = std::chrono::steady_clock::now();
    uint64_t s = 0x123456789ABCDEF0ULL;
    for (int64_t i = 0; i < n; ++i) {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%llu\n", static_cast<unsigned long long>(s));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
