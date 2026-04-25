// Closure / higher-order pipeline — micro-benchmark (C++).
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <numeric>
#include <vector>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 2'000'000LL;
    std::vector<int64_t> data(static_cast<size_t>(n));
    std::iota(data.begin(), data.end(), 0LL);

    // Use std::function to force closure-style indirect dispatch (fair to
    // languages that don't statically devirtualize lambda calls).
    std::function<int64_t(int64_t)>      mapper  = [](int64_t x){ return x*x - 7; };
    std::function<bool(int64_t)>         pred    = [](int64_t x){ return x % 3 == 0; };
    std::function<int64_t(int64_t,int64_t)> reducer = [](int64_t a, int64_t b){ return a + b; };

    auto t0 = std::chrono::steady_clock::now();
    int64_t cs = 0;
    for (int64_t i = 0; i < n; ++i) {
        int64_t v = mapper(data[static_cast<size_t>(i)]);
        if (pred(v)) cs = reducer(cs, v);
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
