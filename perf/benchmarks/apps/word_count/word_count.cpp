// Word-count — typical text-processing application benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <unordered_map>

static std::string gen_text(int64_t n) {
    int64_t seed = 12345;
    std::string s;
    s.reserve(static_cast<size_t>(n) * 7);
    char buf[16];
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        int idx = static_cast<int>(seed % 1024);
        std::snprintf(buf, sizeof(buf), "w%04d", idx);
        s.append(buf);
        if ((i % 12) == 11) s.push_back('\n');
        else                s.push_back(' ');
    }
    return s;
}

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 1'000'000LL;
    std::string text = gen_text(n);

    auto t0 = std::chrono::steady_clock::now();
    std::unordered_map<std::string, int64_t> counts;
    counts.reserve(2048);
    size_t i = 0, sz = text.size();
    while (i < sz) {
        // Skip whitespace
        while (i < sz && (text[i] == ' ' || text[i] == '\n')) ++i;
        size_t start = i;
        while (i < sz && text[i] != ' ' && text[i] != '\n') ++i;
        if (i > start) {
            ++counts[text.substr(start, i - start)];
        }
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    int64_t cs = 0;
    for (const auto& kv : counts) {
        // Parse digits after leading 'w'.
        int idx = std::atoi(kv.first.c_str() + 1);
        cs ^= static_cast<int64_t>(idx) * 1000003LL + kv.second;
    }
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
