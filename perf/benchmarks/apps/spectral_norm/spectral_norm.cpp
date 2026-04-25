// Spectral norm — Computer Language Benchmarks Game numerical kernel (C++).
//
// Algorithmically identical to the Python and Cangjie versions: 10 power
// iterations of v <- A^T A v on the same A(i,j) infinite-matrix function,
// same array layout, same final checksum sqrt(<u,v>/<v,v>) * 1e9.
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

static inline double A(int i, int j) {
    return 1.0 / static_cast<double>(((i + j) * (i + j + 1) >> 1) + i + 1);
}

static void Av(const std::vector<double>& v, std::vector<double>& out, int n) {
    for (int i = 0; i < n; ++i) {
        double s = 0.0;
        for (int j = 0; j < n; ++j) s += A(i, j) * v[static_cast<size_t>(j)];
        out[static_cast<size_t>(i)] = s;
    }
}

static void Atv(const std::vector<double>& v, std::vector<double>& out, int n) {
    for (int i = 0; i < n; ++i) {
        double s = 0.0;
        for (int j = 0; j < n; ++j) s += A(j, i) * v[static_cast<size_t>(j)];
        out[static_cast<size_t>(i)] = s;
    }
}

static void AtAv(const std::vector<double>& v, std::vector<double>& out,
                 std::vector<double>& tmp, int n) {
    Av(v, tmp, n);
    Atv(tmp, out, n);
}

int main(int argc, char** argv) {
    int n = (argc > 1) ? std::atoi(argv[1]) : 1500;

    std::vector<double> u(static_cast<size_t>(n), 1.0);
    std::vector<double> v(static_cast<size_t>(n), 0.0);
    std::vector<double> tmp(static_cast<size_t>(n), 0.0);

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < 10; ++i) {
        AtAv(u, v, tmp, n);
        AtAv(v, u, tmp, n);
    }
    double vbv = 0.0, vv = 0.0;
    for (int i = 0; i < n; ++i) {
        vbv += u[static_cast<size_t>(i)] * v[static_cast<size_t>(i)];
        vv  += v[static_cast<size_t>(i)] * v[static_cast<size_t>(i)];
    }
    double sn = std::sqrt(vbv / vv);
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    int64_t cs = static_cast<int64_t>(std::llround(sn * 1e9));
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
