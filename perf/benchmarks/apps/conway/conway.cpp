// conway — Game of Life N-step application benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

constexpr int W = 200;

int main(int argc, char** argv) {
    int steps = (argc > 1) ? std::atoi(argv[1]) : 200;
    const int cells = W * W;
    std::vector<uint8_t> grid(cells), nxt(cells);
    int64_t seed = 1;
    for (int i = 0; i < cells; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        grid[i] = (((seed >> 16) & 3) < 2) ? 1 : 0;
    }

    auto t0 = std::chrono::steady_clock::now();
    for (int s = 0; s < steps; ++s) {
        for (int y = 0; y < W; ++y) {
            int yu = (y - 1 + W) % W;
            int yd = (y + 1) % W;
            int row = y * W;
            int row_u = yu * W;
            int row_d = yd * W;
            for (int x = 0; x < W; ++x) {
                int xl = (x - 1 + W) % W;
                int xr = (x + 1) % W;
                int n = grid[row_u + xl] + grid[row_u + x] + grid[row_u + xr]
                      + grid[row + xl] + grid[row + xr]
                      + grid[row_d + xl] + grid[row_d + x] + grid[row_d + xr];
                int alive = grid[row + x];
                nxt[row + x] = alive ? ((n == 2 || n == 3) ? 1 : 0)
                                     : ((n == 3) ? 1 : 0);
            }
        }
        grid.swap(nxt);
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    int64_t cs = 0;
    for (auto c : grid) cs += c;
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
