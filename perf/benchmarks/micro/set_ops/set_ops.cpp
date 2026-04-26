// set_ops — HashSet insert + membership micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <unordered_set>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 500000;
    auto t0 = std::chrono::steady_clock::now();
    std::unordered_set<int64_t> s;
    s.reserve(static_cast<size_t>(n));
    int64_t seed = 1;
    int64_t mod = n * 2;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        s.insert(seed % mod);
    }
    int64_t found = 0;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        if (s.count(seed % mod)) ++found;
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(found));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
