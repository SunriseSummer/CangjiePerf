// Matrix multiplication — naive O(N^3) double-precision matmul (C++).
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

int main(int argc, char** argv) {
    int n = (argc > 1) ? std::atoi(argv[1]) : 250;
    size_t nn = static_cast<size_t>(n);

    // Row-major, contiguous storage.
    std::vector<double> a(nn * nn);
    std::vector<double> b(nn * nn);
    std::vector<double> c(nn * nn, 0.0);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            a[static_cast<size_t>(i) * nn + j] = ((i * 7 + j * 13) % 100) * 0.01;
            b[static_cast<size_t>(i) * nn + j] = ((i * 11 + j * 17) % 100) * 0.01;
        }
    }

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < n; ++i) {
        for (int k = 0; k < n; ++k) {
            double aik = a[static_cast<size_t>(i) * nn + k];
            const double* bk = &b[static_cast<size_t>(k) * nn];
            double* ci = &c[static_cast<size_t>(i) * nn];
            for (int j = 0; j < n; ++j) {
                ci[j] += aik * bk[j];
            }
        }
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    double total = 0.0;
    for (int i = 0; i < n; ++i) total += c[static_cast<size_t>(i) * nn + i];
    int64_t cs = static_cast<int64_t>(std::llround(total * 1e6));

    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
