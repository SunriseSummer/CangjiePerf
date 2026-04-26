// format_loop — integer-formatting tight-loop micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 500000;
    auto t0 = std::chrono::steady_clock::now();
    std::string s;
    s.reserve(static_cast<size_t>(n) * 9);
    char buf[32];
    for (int64_t i = 0; i < n; ++i) {
        int len = std::snprintf(buf, sizeof(buf), "%08lld;", static_cast<long long>(i));
        s.append(buf, len);
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(s.size()));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
