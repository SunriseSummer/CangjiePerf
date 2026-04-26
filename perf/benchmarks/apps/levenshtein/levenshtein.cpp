// levenshtein — edit-distance DP application benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

static std::string make_str(int64_t seed, int n) {
    std::string s;
    s.reserve(n);
    for (int i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        s.push_back(static_cast<char>('a' + ((seed >> 16) & 7)));
    }
    return s;
}

int main(int argc, char** argv) {
    int n = (argc > 1) ? std::atoi(argv[1]) : 1500;
    std::string a = make_str(1, n);
    std::string b = make_str(7, n);

    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> prev(n + 1), cur(n + 1);
    for (int j = 0; j <= n; ++j) prev[j] = j;
    for (int i = 1; i <= n; ++i) {
        cur[0] = i;
        char ai = a[i - 1];
        for (int j = 1; j <= n; ++j) {
            int cost = (ai == b[j - 1]) ? 0 : 1;
            int v = prev[j - 1] + cost;
            int d = cur[j - 1] + 1;
            if (d < v) v = d;
            d = prev[j] + 1;
            if (d < v) v = d;
            cur[j] = v;
        }
        std::swap(prev, cur);
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%d\n", prev[n]);
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
