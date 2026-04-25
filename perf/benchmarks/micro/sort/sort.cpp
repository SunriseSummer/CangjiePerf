// Sort N integers — stdlib-sort micro-benchmark (C++).
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 2'000'000LL;
    std::vector<int64_t> arr(static_cast<size_t>(n));
    int64_t seed = 12345;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        arr[static_cast<size_t>(i)] = seed;
    }
    auto t0 = std::chrono::steady_clock::now();
    std::sort(arr.begin(), arr.end());
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    int64_t cs = arr.front() ^ arr[static_cast<size_t>(n / 2)] ^ arr.back();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
