// deque_ops — dynamic-array push/pop micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 2000000;
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int64_t> a;
    int64_t seed = 1;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        a.push_back(seed);
    }
    int64_t cs = 0;
    while (!a.empty()) {
        cs ^= a.back();
        a.pop_back();
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
