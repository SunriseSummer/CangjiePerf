#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <string>
#include <unordered_map>

int main(int argc, char** argv) {
    const std::int64_t n = argc > 1 ? std::atoll(argv[1]) : 500000LL;
    constexpr std::int64_t mod = 1000000007LL;
    std::unordered_map<std::string, std::int64_t> counts;
    counts.reserve(4096);
    for (std::int64_t i = 0; i < n; ++i) {
        std::string word = "w" + std::to_string((i * 1315423911LL) & 4095LL);
        ++counts[word];
    }

    std::int64_t checksum = 0;
    for (const auto& [word, count] : counts) {
        checksum = (checksum + static_cast<std::int64_t>(word.size()) * count + count * count) % mod;
    }
    std::cout << checksum << '\n';
    return 0;
}
