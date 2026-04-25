// Regex find-all — stdlib regex micro-benchmark (C++).
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <regex>
#include <string>

static const char* SAMPLE =
    "On 2024-03-21 Alice wrote to bob@example.com about the meeting. "
    "Charlie replied 2024-04-02 from charlie_99@dev.io with notes about "
    "Project Kingfisher. References: 1999-12-31, foo@bar.org, Madison.";

int main(int argc, char** argv) {
    int repeats = (argc > 1) ? std::atoi(argv[1]) : 4000;
    std::string text;
    text.reserve(static_cast<size_t>(repeats) * 200);
    for (int i = 0; i < repeats; ++i) {
        text.append(SAMPLE);
        text.push_back('\n');
    }
    std::regex rx(R"((\d{4}-\d{2}-\d{2})|([A-Za-z]+@[a-z]+\.[a-z]+)|(\b[A-Z][a-z]{3,8}\b))");

    auto t0 = std::chrono::steady_clock::now();
    int64_t cs = 0;
    auto begin = std::sregex_iterator(text.begin(), text.end(), rx);
    auto end   = std::sregex_iterator();
    for (auto it = begin; it != end; ++it) ++cs;
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("CHECKSUM:%lld\n", static_cast<long long>(cs));
    std::printf("ELAPSED_MS:%.6f\n", ms);
    return 0;
}
