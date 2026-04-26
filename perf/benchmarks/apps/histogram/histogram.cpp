// histogram — bucket-counts of LCG ints application benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

constexpr int K = 1024;

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 5000000;
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int64_t> buckets(K, 0);
    int64_t seed = 1;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        buckets[(seed >> 8) & (K - 1)] += 1;
    }
    int64_t cs = 0;
    for (auto v : buckets) cs ^= v;
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
