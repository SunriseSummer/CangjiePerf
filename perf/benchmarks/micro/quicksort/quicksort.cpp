// Hand-written quicksort — micro-benchmark (C++).
//
// Algorithmically identical to the Python and Cangjie versions: middle
// element pivot, Lomuto partition, recurse-smaller-side / iterate-larger.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

static void quicksort(std::vector<int64_t>& a, int64_t lo, int64_t hi) {
    while (lo < hi) {
        int64_t mid = (lo + hi) >> 1;
        int64_t pivot = a[static_cast<size_t>(mid)];
        std::swap(a[static_cast<size_t>(mid)], a[static_cast<size_t>(hi)]);
        int64_t i = lo - 1;
        for (int64_t j = lo; j < hi; ++j) {
            if (a[static_cast<size_t>(j)] <= pivot) {
                ++i;
                std::swap(a[static_cast<size_t>(i)], a[static_cast<size_t>(j)]);
            }
        }
        ++i;
        std::swap(a[static_cast<size_t>(i)], a[static_cast<size_t>(hi)]);
        if ((i - lo) < (hi - i)) {
            quicksort(a, lo, i - 1);
            lo = i + 1;
        } else {
            quicksort(a, i + 1, hi);
            hi = i - 1;
        }
    }
}

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 1'500'000LL;

    std::vector<int64_t> a(static_cast<size_t>(n));
    int64_t seed = 1234567;
    const int64_t mask = 0x7FFFFFFFLL;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & mask;
        a[static_cast<size_t>(i)] = seed;
    }

    auto t0 = std::chrono::steady_clock::now();
    quicksort(a, 0, n - 1);
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    int64_t cs = 0;
    for (int64_t k = 0; k < n; k += 1024) {
        cs ^= a[static_cast<size_t>(k)];
    }
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
