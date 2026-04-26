// string_split — repeated stdlib string-split micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

static std::vector<std::string> split(const std::string& s, char sep) {
    std::vector<std::string> out;
    std::string::size_type prev = 0, pos;
    while ((pos = s.find(sep, prev)) != std::string::npos) {
        out.emplace_back(s.substr(prev, pos - prev));
        prev = pos + 1;
    }
    out.emplace_back(s.substr(prev));
    return out;
}

int main(int argc, char** argv) {
    int64_t repeats = (argc > 1) ? std::atoll(argv[1]) : 20000;

    // Build the input once outside the timed region.
    std::string s;
    int64_t seed = 1;
    for (int i = 0; i < 64; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        char buf[32];
        std::snprintf(buf, sizeof(buf), "tok%05lld", static_cast<long long>(seed % 100000));
        if (i) s.push_back(',');
        s.append(buf);
    }

    auto t0 = std::chrono::steady_clock::now();
    int64_t cs = 0;
    for (int64_t r = 0; r < repeats; ++r) {
        auto toks = split(s, ',');
        int64_t idx = r % static_cast<int64_t>(toks.size());
        cs ^= (r + 1) * 1000003LL
              + static_cast<int64_t>(toks.size())
              + static_cast<int64_t>(toks[idx].size());
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
