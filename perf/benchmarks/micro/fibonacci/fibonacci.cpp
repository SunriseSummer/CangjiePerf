// Fibonacci — recursive function-call micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

static int64_t fib(int n) {
    if (n < 2) return n;
    return fib(n - 1) + fib(n - 2);
}

int main(int argc, char** argv) {
    int n = (argc > 1) ? std::atoi(argv[1]) : 32;
    auto t0 = std::chrono::steady_clock::now();
    int64_t result = fib(n);
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(result));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
