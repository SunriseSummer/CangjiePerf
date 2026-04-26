// base64 — base64 encoding application benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

static const char ALPHA[] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 2000000;
    std::vector<uint8_t> src(n);
    int64_t seed = 1;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        src[i] = static_cast<uint8_t>((seed >> 8) & 0xFF);
    }

    auto t0 = std::chrono::steady_clock::now();
    int64_t outLen = ((n + 2) / 3) * 4;
    std::vector<uint8_t> out(outLen);
    int64_t oi = 0, i = 0;
    while (i + 3 <= n) {
        uint8_t b0 = src[i], b1 = src[i + 1], b2 = src[i + 2];
        out[oi]     = ALPHA[b0 >> 2];
        out[oi + 1] = ALPHA[((b0 & 0x3) << 4) | (b1 >> 4)];
        out[oi + 2] = ALPHA[((b1 & 0xF) << 2) | (b2 >> 6)];
        out[oi + 3] = ALPHA[b2 & 0x3F];
        oi += 4; i += 3;
    }
    int64_t rem = n - i;
    if (rem == 1) {
        uint8_t b0 = src[i];
        out[oi]     = ALPHA[b0 >> 2];
        out[oi + 1] = ALPHA[(b0 & 0x3) << 4];
        out[oi + 2] = '=';
        out[oi + 3] = '=';
    } else if (rem == 2) {
        uint8_t b0 = src[i], b1 = src[i + 1];
        out[oi]     = ALPHA[b0 >> 2];
        out[oi + 1] = ALPHA[((b0 & 0x3) << 4) | (b1 >> 4)];
        out[oi + 2] = ALPHA[(b1 & 0xF) << 2];
        out[oi + 3] = '=';
    }
    int64_t cs = 0;
    for (auto v : out) cs ^= v;
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
