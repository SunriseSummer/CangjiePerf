// crc32 — CRC32 of a deterministic byte stream application benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

static void buildTable(uint32_t* t) {
    for (uint32_t n = 0; n < 256; ++n) {
        uint32_t c = n;
        for (int k = 0; k < 8; ++k) {
            c = (c >> 1) ^ ((c & 1) ? 0xEDB88320u : 0u);
        }
        t[n] = c;
    }
}

int main(int argc, char** argv) {
    int64_t n = (argc > 1) ? std::atoll(argv[1]) : 5000000;
    std::vector<uint8_t> src(n);
    int64_t seed = 1;
    for (int64_t i = 0; i < n; ++i) {
        seed = (seed * 1103515245LL + 12345LL) & 0x7FFFFFFFLL;
        src[i] = static_cast<uint8_t>((seed >> 8) & 0xFF);
    }
    uint32_t table[256];
    buildTable(table);

    auto t0 = std::chrono::steady_clock::now();
    uint32_t crc = 0xFFFFFFFFu;
    for (int64_t i = 0; i < n; ++i) {
        crc = table[(crc ^ src[i]) & 0xFF] ^ (crc >> 8);
    }
    crc ^= 0xFFFFFFFFu;
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%u\n", crc);
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
