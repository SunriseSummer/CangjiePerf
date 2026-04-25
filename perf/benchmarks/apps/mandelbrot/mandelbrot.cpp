// Mandelbrot — application-style numerical benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>

static int64_t mandelbrot(int width, int max_iter) {
    const double inv_w = 2.0 / width;
    int64_t total = 0;
    for (int py = 0; py < width; ++py) {
        const double ci = py * inv_w - 1.0;
        for (int px = 0; px < width; ++px) {
            const double cr = px * inv_w - 1.5;
            double zr = 0.0, zi = 0.0;
            int n = 0;
            while (n < max_iter) {
                const double zr2 = zr * zr;
                const double zi2 = zi * zi;
                if (zr2 + zi2 > 4.0) break;
                zi = 2.0 * zr * zi + ci;
                zr = zr2 - zi2 + cr;
                ++n;
            }
            total += n;
        }
    }
    return total;
}

int main(int argc, char** argv) {
    int width = (argc > 1) ? std::atoi(argv[1]) : 600;
    int max_iter = (argc > 2) ? std::atoi(argv[2]) : 200;

    auto t0 = std::chrono::steady_clock::now();
    int64_t cs = mandelbrot(width, max_iter);
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
