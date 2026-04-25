// Sieve of Eratosthenes — micro-benchmark (C++).
//
// Implementation is intentionally kept symmetric with the Cangjie/Python
// versions: same loop bounds (i*i <= n), same inner stride (j += i), same
// final checksum formula.
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 20'000'000LL;

    auto t0 = std::chrono::steady_clock::now();
    // std::vector<uint8_t> rather than std::vector<bool> so the byte-level
    // representation matches the Python `bytearray` and Cangjie `Array<Bool>`
    // baselines (one byte per entry).
    std::vector<uint8_t> sieve(static_cast<size_t>(n + 1), 1);
    sieve[0] = 0;
    sieve[1] = 0;
    for (int64_t i = 2; i * i <= n; ++i) {
        if (sieve[static_cast<size_t>(i)]) {
            for (int64_t j = i * i; j <= n; j += i) {
                sieve[static_cast<size_t>(j)] = 0;
            }
        }
    }
    int64_t count = 0;
    int64_t psum = 0;
    const int64_t mask = 0x7FFFFFFFLL;
    for (int64_t k = 2; k <= n; ++k) {
        if (sieve[static_cast<size_t>(k)]) {
            ++count;
            psum = (psum + k) & mask;
        }
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    int64_t cs = (count * 1'000'003LL + psum) & mask;
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
