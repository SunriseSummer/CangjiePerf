#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <unordered_map>
#include <vector>

int main(int argc, char** argv) {
    const std::int64_t n = argc > 1 ? std::atoll(argv[1]) : 300000LL;
    constexpr std::int64_t mod = 1000000007LL;
    std::vector<std::int64_t> values;
    values.reserve(static_cast<std::size_t>(n));
    for (std::int64_t i = 0; i < n; ++i) {
        values.push_back((i * 31LL) % 4096LL);
    }

    std::int64_t total = 0;
    for (const auto value : values) {
        total = (total + value) % mod;
    }

    std::unordered_map<std::int64_t, std::int64_t> counts;
    counts.reserve(4096);
    for (const auto value : values) {
        ++counts[value];
    }

    for (std::int64_t key = 0; key < 4096; ++key) {
        auto iter = counts.find(key);
        if (iter != counts.end()) {
            total = (total + iter->second * (key + 1)) % mod;
        }
    }
    std::cout << total << '\n';
    return 0;
}
