#include <cstdint>
#include <cstdlib>
#include <iostream>

int main(int argc, char** argv) {
    const std::int64_t n = argc > 1 ? std::atoll(argv[1]) : 2000000LL;
    constexpr std::int64_t mod = 1000000007LL;
    std::int64_t x = 0;
    for (std::int64_t i = 0; i < n; ++i) {
        x = (x * 1664525LL + i + 1013904223LL) % mod;
    }
    std::cout << x << '\n';
    return 0;
}
