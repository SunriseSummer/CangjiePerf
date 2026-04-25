// HashMap insert + lookup — stdlib hash-table micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <unordered_map>
#include <vector>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 500'000LL;

    // Pre-build keys.
    std::vector<std::string> keys;
    keys.reserve(static_cast<size_t>(n));
    char buf[32];
    for (int64_t i = 0; i < n; ++i) {
        std::snprintf(buf, sizeof(buf), "key-%lld", static_cast<long long>(i));
        keys.emplace_back(buf);
    }

    auto t0 = std::chrono::steady_clock::now();
    std::unordered_map<std::string, int64_t> m;
    m.reserve(static_cast<size_t>(n));
    for (int64_t i = 0; i < n; ++i) {
        m.emplace(keys[static_cast<size_t>(i)], i);
    }
    int64_t cs = 0;
    for (int64_t i = 0; i < n; ++i) {
        cs ^= m[keys[static_cast<size_t>(i)]];
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
