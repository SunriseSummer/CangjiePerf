// String building — stdlib StringBuilder-style micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 500'000LL;

    auto t0 = std::chrono::steady_clock::now();
    std::string s;
    s.reserve(static_cast<size_t>(n) * 12);
    char buf[32];
    for (int64_t i = 0; i < n; ++i) {
        s.append("frag");
        int len = std::snprintf(buf, sizeof(buf), "%lld", static_cast<long long>(i));
        s.append(buf, static_cast<size_t>(len));
        s.push_back(';');
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%zu\n", s.size());
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
