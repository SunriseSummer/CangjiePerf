// string_search — substring-search tight-loop micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>

int main(int argc, char** argv) {
    int64_t repeats = (argc > 1) ? std::atoll(argv[1]) : 50000;

    std::string hay;
    hay.reserve(10000);
    int64_t seed = 1;
    for (int i = 0; i < 10000; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        hay.push_back(static_cast<char>('a' + (seed % 8)));
    }
    const std::string needle = "abcde";

    auto t0 = std::chrono::steady_clock::now();
    int64_t cs = 0;
    for (int64_t r = 0; r < repeats; ++r) {
        int64_t count = 0;
        std::string::size_type pos = 0;
        while (true) {
            auto i = hay.find(needle, pos);
            if (i == std::string::npos) break;
            ++count;
            pos = i + 1;
        }
        cs ^= (r + 1) * 1000003LL + count;
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
