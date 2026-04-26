# CangjiePerf Benchmark Report

_Generated: 2026-04-26T02:50:47+00:00_

## Environment

- **OS**: Linux 6.17.0-1010-azure
- **Architecture**: x86_64
- **CPU**: AMD EPYC 7763 64-Core Processor
- **Python**: 3.12.3

## Toolchains

The benchmark suite compares **Cangjie** against four reference languages: **C++** and **Rust** as native-compiled baselines, **Go** as a managed-runtime compiled baseline, and **Python** as a scripting-language baseline. The exact toolchain versions used for this run are:

| Language | Available | Version |
|----------|-----------|---------|
| Cangjie | ❌ | not found: cjc (install Cangjie SDK; see project .resource) |
| C++ | ✅ | g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| Rust | ✅ | rustc 1.94.1 (e408947bf 2026-03-25) |
| Go | ✅ | go version go1.24.13 linux/amd64 |
| Python | ✅ | Python 3.12.3 |

## Run Configuration

- Warmup runs: **0**
- Measurement runs: **1**
- Languages enabled: **Python, C++, Rust, Go**
- Reported metric: per-process self-timed wall-clock (`ELAPSED_MS`); **`min`** chosen as the headline number, lower is better.

## Summary

| Benchmark | Category | Cangjie | C++ | Rust | Go | Python | Fastest |
|---|---|---|---|---|---|---|---|
| **fibonacci** | micro | — | 4.35 ms | 6.79 ms | 12.20 ms | 307.48 ms | C++ |
| **sort** | micro | — | 133.93 ms | 56.13 ms | 298.02 ms | 757.66 ms | Rust |
| **hashmap_ops** | micro | — | 108.99 ms | 136.74 ms | 81.06 ms | 125.79 ms | Go |
| **string_concat** | micro | — | 33.26 ms | 12.60 ms | 15.75 ms | 71.31 ms | Rust |
| **closure_sum** | micro | — | 9.70 ms | 1.53 ms | 3.19 ms | 361.54 ms | Rust |
| **enum_eval** | micro | — | 127.52 ms | 194.80 ms | 178.02 ms | 5.180 s | C++ |
| **regex_search** | micro | — | 82.02 ms | 2.35 ms | 99.51 ms | 41.51 ms | Rust |
| **math_loop** | micro | — | 86.71 ms | 85.11 ms | 145.54 ms | 971.15 ms | Rust |
| **prime_sieve** | micro | — | 52.66 ms | 61.73 ms | 53.33 ms | 2.821 s | C++ |
| **quicksort** | micro | — | 111.32 ms | 115.97 ms | 120.86 ms | 4.124 s | C++ |
| **mandelbrot** | apps | — | 90.71 ms | 91.69 ms | 91.30 ms | 3.550 s | C++ |
| **nbody** | apps | — | 14.36 ms | 9.51 ms | 14.94 ms | 1.187 s | Rust |
| **binary_trees** | apps | — | 67.01 ms | 65.89 ms | 95.61 ms | 847.34 ms | Rust |
| **matrix_multiply** | apps | — | 10.16 ms | 4.36 ms | 10.47 ms | 730.34 ms | Rust |
| **word_count** | apps | — | 27.35 ms | 26.07 ms | 25.59 ms | 134.58 ms | Go |
| **spectral_norm** | apps | — | 128.87 ms | 129.71 ms | 129.55 ms | 15.334 s | C++ |
| **bit_count** | micro | — | 149.18 ms | 163.08 ms | 163.67 ms | 11.498 s | C++ |
| **gcd_loop** | micro | — | 55.55 ms | 50.73 ms | 55.15 ms | 636.18 ms | Rust |
| **xor_shift** | micro | — | 93.50 ms | 93.64 ms | 93.83 ms | 15.958 s | C++ |
| **string_split** | micro | — | 23.22 ms | 19.52 ms | 15.13 ms | 31.59 ms | Go |
| **string_search** | micro | — | 406.05 ms | 255.36 ms | 677.97 ms | 128.29 ms | Python |
| **format_loop** | micro | — | 34.86 ms | 18.92 ms | 52.56 ms | 127.44 ms | Rust |
| **set_ops** | micro | — | 40.05 ms | 30.81 ms | 44.83 ms | 266.45 ms | Rust |
| **deque_ops** | micro | — | 9.90 ms | 6.64 ms | 15.55 ms | 367.53 ms | Rust |
| **conway** | apps | — | 34.63 ms | 23.47 ms | 62.87 ms | 3.249 s | Rust |
| **knapsack_dp** | apps | — | 3.85 ms | 4.28 ms | 4.10 ms | 408.51 ms | C++ |
| **levenshtein** | apps | — | 2.67 ms | 6.86 ms | 3.92 ms | 446.40 ms | C++ |
| **monte_carlo_pi** | apps | — | 18.70 ms | 12.75 ms | 18.48 ms | 1.789 s | Rust |
| **histogram** | apps | — | 9.43 ms | 7.05 ms | 8.00 ms | 1.088 s | Rust |
| **dijkstra** | apps | — | 1.14 ms | 709.22 µs | 1.09 ms | 45.18 ms | Rust |
| **base64** | apps | — | 2.87 ms | 2.92 ms | 3.79 ms | 336.11 ms | C++ |
| **crc32** | apps | — | 12.50 ms | 12.58 ms | 12.50 ms | 645.18 ms | C++ |

> **Bold rows** marked with ⚠️ are benchmarks where Cangjie's timing is closer (in log scale) to Python's than to C++'s — i.e. cases where the Cangjie implementation is significantly under-performing the native baseline. See [`analyse.md`](./analyse.md) for the root-cause analysis.

### Visual comparison

Each benchmark shows five side-by-side bars (Cangjie / C++ / Rust / Go / Python). **Lower bars are faster.** Note the **logarithmic** y-axis: a one-step gridline difference is a 10× speed difference. Open an SVG in a new tab to see exact per-bar tooltips.

**All benchmarks (combined):**

![Benchmark wall-clock comparison (log scale, lower is better)](./report_chart.svg)

The benchmark catalog is split into two groups for easier side-by-side reading:

1. **Core** (the original 16 benchmarks) — recursion, sort, stdlib hash-map, string builder, closures, enum / pattern matching, regex, math loop, prime sieve, hand-written quicksort, Mandelbrot, n-body, binary trees, matrix multiply, word count, spectral norm.
2. **Extended** (the additional 16 benchmarks) — popcount loop, GCD loop, xorshift64 PRNG, stdlib `split`/`indexOf`, integer formatting, `HashSet` ops, dynamic-array push/pop, Conway's Game of Life, 0/1 knapsack DP, Levenshtein DP, integer Monte Carlo PI, histogram bucketing, dense-graph Dijkstra, base64 encode, CRC32.

**Core benchmarks:**

![Core benchmark wall-clock comparison (log scale, lower is better)](./report_chart_core.svg)

**Extended benchmarks:**

![Extended benchmark wall-clock comparison (log scale, lower is better)](./report_chart_extended.svg)

## Per-benchmark Detail

### fibonacci — Recursive Fibonacci (function call / recursion)

_Category_: `micro` &nbsp;&nbsp;_Args_: `32`

Pure recursive fib(N). Stresses function-call overhead and integer arithmetic. No standard-library involvement beyond integers.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 4.35 ms | 4.35 ms | 4.35 ms | 0.00 µs | 1.00× | `2178309` |
| Rust | ✅ | 6.79 ms | 6.79 ms | 6.79 ms | 0.00 µs | 1.56× | `2178309` |
| Go | ✅ | 12.20 ms | 12.20 ms | 12.20 ms | 0.00 µs | 2.80× | `2178309` |
| Python | ✅ | 307.48 ms | 307.48 ms | 307.48 ms | 0.00 µs | 70.69× | `2178309` |

### sort — Sort 2M integers (stdlib sort)

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Generate 2,000,000 deterministic pseudo-random Int64 values then sort ascending using the language's standard sort. Stresses standard library sorting and dynamic arrays.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 133.93 ms | 133.93 ms | 133.93 ms | 0.00 µs | 2.39× | `1074570229` |
| Rust | ✅ | 56.13 ms | 56.13 ms | 56.13 ms | 0.00 µs | 1.00× | `1074570229` |
| Go | ✅ | 298.02 ms | 298.02 ms | 298.02 ms | 0.00 µs | 5.31× | `1074570229` |
| Python | ✅ | 757.66 ms | 757.66 ms | 757.66 ms | 0.00 µs | 13.50× | `1074570229` |

### hashmap_ops — HashMap insert + lookup (stdlib hash table)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N (string,int) pairs then look up the same N keys. Stresses hash maps, string hashing, and string allocation.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 108.99 ms | 108.99 ms | 108.99 ms | 0.00 µs | 1.34× | `0` |
| Rust | ✅ | 136.74 ms | 136.74 ms | 136.74 ms | 0.00 µs | 1.69× | `0` |
| Go | ✅ | 81.06 ms | 81.06 ms | 81.06 ms | 0.00 µs | 1.00× | `0` |
| Python | ✅ | 125.79 ms | 125.79 ms | 125.79 ms | 0.00 µs | 1.55× | `0` |

### string_concat — String building (stdlib StringBuilder)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Build a single large string from N small fragments using the recommended efficient builder for each language. Stresses string buffers and memory growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 33.26 ms | 33.26 ms | 33.26 ms | 0.00 µs | 2.64× | `5388890` |
| Rust | ✅ | 12.60 ms | 12.60 ms | 12.60 ms | 0.00 µs | 1.00× | `5388890` |
| Go | ✅ | 15.75 ms | 15.75 ms | 15.75 ms | 0.00 µs | 1.25× | `5388890` |
| Python | ✅ | 71.31 ms | 71.31 ms | 71.31 ms | 0.00 µs | 5.66× | `5388890` |

### closure_sum — Closure / higher-order pipeline

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Apply a map -> filter -> reduce pipeline of closures over N integers. Stresses higher-order function dispatch, closure allocation, and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 9.70 ms | 9.70 ms | 9.70 ms | 0.00 µs | 6.35× | `1777776444435777780` |
| Rust | ✅ | 1.53 ms | 1.53 ms | 1.53 ms | 0.00 µs | 1.00× | `1777776444435777780` |
| Go | ✅ | 3.19 ms | 3.19 ms | 3.19 ms | 0.00 µs | 2.09× | `1777776444435777780` |
| Python | ✅ | 361.54 ms | 361.54 ms | 361.54 ms | 0.00 µs | 236.60× | `1777776444435777780` |

### enum_eval — Enum / pattern matching (AST evaluation)

_Category_: `micro` &nbsp;&nbsp;_Args_: `18 60`

Build a recursive arithmetic expression tree of depth D and evaluate it N times via recursive pattern matching on a sum-type enum (Num | Add | Sub | Mul). Stresses algebraic data types, recursive calls, and tag dispatch.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 127.52 ms | 127.52 ms | 127.52 ms | 0.00 µs | 1.00× | `0` |
| Rust | ✅ | 194.80 ms | 194.80 ms | 194.80 ms | 0.00 µs | 1.53× | `0` |
| Go | ✅ | 178.02 ms | 178.02 ms | 178.02 ms | 0.00 µs | 1.40× | `0` |
| Python | ✅ | 5.180 s | 5.180 s | 5.180 s | 0.00 µs | 40.62× | `0` |

### regex_search — Regex find-all (stdlib regex)

_Category_: `micro` &nbsp;&nbsp;_Args_: `4000`

Run a non-trivial alternation regex (date | email | capitalized word) across REPEATS copies of a sample paragraph. Stresses the standard regex engine.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 82.02 ms | 82.02 ms | 82.02 ms | 0.00 µs | 34.91× | `36000` |
| Rust | ✅ | 2.35 ms | 2.35 ms | 2.35 ms | 0.00 µs | 1.00× | `36000` |
| Go | ✅ | 99.51 ms | 99.51 ms | 99.51 ms | 0.00 µs | 42.35× | `36000` |
| Python | ✅ | 41.51 ms | 41.51 ms | 41.51 ms | 0.00 µs | 17.67× | `36000` |

### math_loop — Math-intensive loop (sin/cos/sqrt/exp)

_Category_: `micro` &nbsp;&nbsp;_Args_: `5000000`

Sum sin(x)*cos(x)+sqrt(x+1)-exp(-x) over N points. Stresses the math standard library and floating-point throughput.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 86.71 ms | 86.71 ms | 86.71 ms | 0.00 µs | 1.02× | `4704337083537` |
| Rust | ✅ | 85.11 ms | 85.11 ms | 85.11 ms | 0.00 µs | 1.00× | `4704337083537` |
| Go | ✅ | 145.54 ms | 145.54 ms | 145.54 ms | 0.00 µs | 1.71× | `4704337083537` |
| Python | ✅ | 971.15 ms | 971.15 ms | 971.15 ms | 0.00 µs | 11.41× | `4704337083537` |

### prime_sieve — Sieve of Eratosthenes

_Category_: `micro` &nbsp;&nbsp;_Args_: `20000000`

Classic Sieve of Eratosthenes up to N on a one-byte-per-cell boolean array, then count primes and sum them mod 2^31. Algorithmically identical across all three languages: same loop bounds, same inner stride, same checksum formula.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 52.66 ms | 52.66 ms | 52.66 ms | 0.00 µs | 1.00× | `1156745585` |
| Rust | ✅ | 61.73 ms | 61.73 ms | 61.73 ms | 0.00 µs | 1.17× | `1156745585` |
| Go | ✅ | 53.33 ms | 53.33 ms | 53.33 ms | 0.00 µs | 1.01× | `1156745585` |
| Python | ✅ | 2.821 s | 2.821 s | 2.821 s | 0.00 µs | 53.56× | `1156745585` |

### quicksort — Hand-written quicksort

_Category_: `micro` &nbsp;&nbsp;_Args_: `1500000`

Lomuto-partition quicksort with middle-element pivot and recurse-smaller-side / iterate-larger-side, implemented by hand in all three languages so the algorithm itself is identical (complements the stdlib `sort` benchmark).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 111.32 ms | 111.32 ms | 111.32 ms | 0.00 µs | 1.00× | `612429648` |
| Rust | ✅ | 115.97 ms | 115.97 ms | 115.97 ms | 0.00 µs | 1.04× | `612429648` |
| Go | ✅ | 120.86 ms | 120.86 ms | 120.86 ms | 0.00 µs | 1.09× | `612429648` |
| Python | ✅ | 4.124 s | 4.124 s | 4.124 s | 0.00 µs | 37.05× | `612429648` |

### mandelbrot — Mandelbrot set (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `600 200`

Compute a Mandelbrot escape-time bitmap of size W*W with up to MAX_ITER iterations. Inspired by the Computer Language Benchmarks Game. Stresses tight numeric loops and floating-point arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 90.71 ms | 90.71 ms | 90.71 ms | 0.00 µs | 1.00× | `29624109` |
| Rust | ✅ | 91.69 ms | 91.69 ms | 91.69 ms | 0.00 µs | 1.01× | `29624109` |
| Go | ✅ | 91.30 ms | 91.30 ms | 91.30 ms | 0.00 µs | 1.01× | `29624109` |
| Python | ✅ | 3.550 s | 3.550 s | 3.550 s | 0.00 µs | 39.14× | `29624109` |

### nbody — N-Body simulation (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200000`

Symplectic integrator for the classic 5-body solar system from the Benchmarks Game over N steps. Stresses tight floating-point loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 14.36 ms | 14.36 ms | 14.36 ms | 0.00 µs | 1.51× | `-169083713` |
| Rust | ✅ | 9.51 ms | 9.51 ms | 9.51 ms | 0.00 µs | 1.00× | `-169083713` |
| Go | ✅ | 14.94 ms | 14.94 ms | 14.94 ms | 0.00 µs | 1.57× | `-169083713` |
| Python | ✅ | 1.187 s | 1.187 s | 1.187 s | 0.00 µs | 124.85× | `-169083713` |

### binary_trees — Binary trees (allocation / GC pressure)

_Category_: `apps` &nbsp;&nbsp;_Args_: `14`

Build and check many small balanced binary trees up to depth D. Adapted from the Computer Language Benchmarks Game. Stresses small-object allocation and GC (or heap allocator).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 67.01 ms | 67.01 ms | 67.01 ms | 0.00 µs | 1.02× | `13250584224` |
| Rust | ✅ | 65.89 ms | 65.89 ms | 65.89 ms | 0.00 µs | 1.00× | `13250584224` |
| Go | ✅ | 95.61 ms | 95.61 ms | 95.61 ms | 0.00 µs | 1.45× | `13250584224` |
| Python | ✅ | 847.34 ms | 847.34 ms | 847.34 ms | 0.00 µs | 12.86× | `13250584224` |

### matrix_multiply — Matrix multiplication (naive O(N^3))

_Category_: `apps` &nbsp;&nbsp;_Args_: `250`

Compute C = A * B for two NxN double-precision matrices using the textbook triple-loop algorithm. Stresses memory layout, FP multiply-add throughput, and cache behaviour.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 10.16 ms | 10.16 ms | 10.16 ms | 0.00 µs | 2.33× | `15315135000` |
| Rust | ✅ | 4.36 ms | 4.36 ms | 4.36 ms | 0.00 µs | 1.00× | `15315135000` |
| Go | ✅ | 10.47 ms | 10.47 ms | 10.47 ms | 0.00 µs | 2.40× | `15315135000` |
| Python | ✅ | 730.34 ms | 730.34 ms | 730.34 ms | 0.00 µs | 167.40× | `15315135000` |

### word_count — Word count (text processing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1000000`

Tokenize a synthesized N-word text and count word frequencies in a hash-map. Stresses string slicing/comparison, hashing, and hash-map updates — a typical scripting workload.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 27.35 ms | 27.35 ms | 27.35 ms | 0.00 µs | 1.07× | `638309952` |
| Rust | ✅ | 26.07 ms | 26.07 ms | 26.07 ms | 0.00 µs | 1.02× | `638309952` |
| Go | ✅ | 25.59 ms | 25.59 ms | 25.59 ms | 0.00 µs | 1.00× | `638309952` |
| Python | ✅ | 134.58 ms | 134.58 ms | 134.58 ms | 0.00 µs | 5.26× | `638309952` |

### spectral_norm — Spectral norm (CLBG numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Approximates the largest eigenvalue of an infinite matrix A[i][j] = 1 / ((i+j)(i+j+1)/2 + i + 1) via 10 power iterations of v <- A^T A v. Adapted from the Computer Language Benchmarks Game; algorithmically identical across all three languages.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 128.87 ms | 128.87 ms | 128.87 ms | 0.00 µs | 1.00× | `1274224151` |
| Rust | ✅ | 129.71 ms | 129.71 ms | 129.71 ms | 0.00 µs | 1.01× | `1274224151` |
| Go | ✅ | 129.55 ms | 129.55 ms | 129.55 ms | 0.00 µs | 1.01× | `1274224151` |
| Python | ✅ | 15.334 s | 15.334 s | 15.334 s | 0.00 µs | 118.98× | `1274224151` |

### bit_count — Population-count tight loop (bitwise / integer ops)

_Category_: `micro` &nbsp;&nbsp;_Args_: `10000000`

Compute the population count (Hamming weight) of (i * 2654435761) for i = 0..N-1 via a hand-written 4-operation SWAR popcount kernel that is algorithmically identical across all five languages, and return the total bit count. Stresses bitwise / shift / multiply throughput on 64-bit integers without leaning on each language's stdlib popcount intrinsic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 149.18 ms | 149.18 ms | 149.18 ms | 0.00 µs | 1.00× | `160000012` |
| Rust | ✅ | 163.08 ms | 163.08 ms | 163.08 ms | 0.00 µs | 1.09× | `160000012` |
| Go | ✅ | 163.67 ms | 163.67 ms | 163.67 ms | 0.00 µs | 1.10× | `160000012` |
| Python | ✅ | 11.498 s | 11.498 s | 11.498 s | 0.00 µs | 77.07× | `160000012` |

### gcd_loop — Euclidean GCD tight loop (integer arithmetic)

_Category_: `micro` &nbsp;&nbsp;_Args_: `1000000`

For each i = 1..N, compute gcd((i * 2654435761) mod 10^9, (i * 40503) mod 10^9 + 7) via the iterative Euclidean algorithm, and XOR-fold all results into a checksum. Stresses integer division / modulo throughput in a tight inner loop.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 55.55 ms | 55.55 ms | 55.55 ms | 0.00 µs | 1.10× | `5755332` |
| Rust | ✅ | 50.73 ms | 50.73 ms | 50.73 ms | 0.00 µs | 1.00× | `5755332` |
| Go | ✅ | 55.15 ms | 55.15 ms | 55.15 ms | 0.00 µs | 1.09× | `5755332` |
| Python | ✅ | 636.18 ms | 636.18 ms | 636.18 ms | 0.00 µs | 12.54× | `5755332` |

### xor_shift — xorshift64 PRNG tight loop (bit ops + state)

_Category_: `micro` &nbsp;&nbsp;_Args_: `50000000`

Iterate the classic three-shift xorshift64 PRNG N times starting from a fixed seed and return the final state. Pure 64-bit shift / XOR throughput, no memory traffic or stdlib calls.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 93.50 ms | 93.50 ms | 93.50 ms | 0.00 µs | 1.00× | `14559293861578202768` |
| Rust | ✅ | 93.64 ms | 93.64 ms | 93.64 ms | 0.00 µs | 1.00× | `14559293861578202768` |
| Go | ✅ | 93.83 ms | 93.83 ms | 93.83 ms | 0.00 µs | 1.00× | `14559293861578202768` |
| Python | ✅ | 15.958 s | 15.958 s | 15.958 s | 0.00 µs | 170.68× | `14559293861578202768` |

### string_split — Repeated stdlib String.split

_Category_: `micro` &nbsp;&nbsp;_Args_: `20000`

Build a fixed comma-separated 64-token string once, then split it REPEATS times using each language's stdlib split, folding the per-iteration token count and selected token length into a checksum. Stresses string parsing and small-array allocation in the standard library.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 23.22 ms | 23.22 ms | 23.22 ms | 0.00 µs | 1.53× | `19336929664` |
| Rust | ✅ | 19.52 ms | 19.52 ms | 19.52 ms | 0.00 µs | 1.29× | `19336929664` |
| Go | ✅ | 15.13 ms | 15.13 ms | 15.13 ms | 0.00 µs | 1.00× | `19336929664` |
| Python | ✅ | 31.59 ms | 31.59 ms | 31.59 ms | 0.00 µs | 2.09× | `19336929664` |

### string_search — Repeated stdlib substring search (indexOf)

_Category_: `micro` &nbsp;&nbsp;_Args_: `50000`

Construct a fixed ~10 KB pseudo-random ASCII haystack, then count occurrences of a 5-character needle in a sliding loop using stdlib substring search (indexOf / find / Index), REPEATS times. Stresses string-search throughput without regex.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 406.05 ms | 406.05 ms | 406.05 ms | 0.00 µs | 3.17× | `47355938304` |
| Rust | ✅ | 255.36 ms | 255.36 ms | 255.36 ms | 0.00 µs | 1.99× | `47355938304` |
| Go | ✅ | 677.97 ms | 677.97 ms | 677.97 ms | 0.00 µs | 5.28× | `47355938304` |
| Python | ✅ | 128.29 ms | 128.29 ms | 128.29 ms | 0.00 µs | 1.00× | `47355938304` |

### format_loop — Integer formatting + string-builder loop

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Format N integers (zero-padded to width 8) into a single growing string via the language's recommended efficient builder. Stresses integer-to-string formatting and string-buffer growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 34.86 ms | 34.86 ms | 34.86 ms | 0.00 µs | 1.84× | `4500000` |
| Rust | ✅ | 18.92 ms | 18.92 ms | 18.92 ms | 0.00 µs | 1.00× | `4500000` |
| Go | ✅ | 52.56 ms | 52.56 ms | 52.56 ms | 0.00 µs | 2.78× | `4500000` |
| Python | ✅ | 127.44 ms | 127.44 ms | 127.44 ms | 0.00 µs | 6.74× | `4500000` |

### set_ops — HashSet insert + membership (stdlib)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N pseudo-random Int64 values into a hash set, then test membership of N more values from the same stream. Stresses hash-set inserts and lookups (the set-shaped complement to the hashmap_ops benchmark).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 40.05 ms | 40.05 ms | 40.05 ms | 0.00 µs | 1.30× | `196957` |
| Rust | ✅ | 30.81 ms | 30.81 ms | 30.81 ms | 0.00 µs | 1.00× | `196957` |
| Go | ✅ | 44.83 ms | 44.83 ms | 44.83 ms | 0.00 µs | 1.45× | `196957` |
| Python | ✅ | 266.45 ms | 266.45 ms | 266.45 ms | 0.00 µs | 8.65× | `196957` |

### deque_ops — Dynamic-array push/pop tight loop

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Push N pseudo-random Int64 values onto each language's growable array (Cangjie ArrayList, C++ vector, Rust Vec, Go slice, Python list), then pop them all, XOR-folding popped values into a checksum. Stresses dynamic-array growth and end-removal.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 9.90 ms | 9.90 ms | 9.90 ms | 0.00 µs | 1.49× | `799129856` |
| Rust | ✅ | 6.64 ms | 6.64 ms | 6.64 ms | 0.00 µs | 1.00× | `799129856` |
| Go | ✅ | 15.55 ms | 15.55 ms | 15.55 ms | 0.00 µs | 2.34× | `799129856` |
| Python | ✅ | 367.53 ms | 367.53 ms | 367.53 ms | 0.00 µs | 55.34× | `799129856` |

### conway — Conway's Game of Life (cellular automaton)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200`

Simulate STEPS generations of Conway's Game of Life on a 200x200 toroidal grid initialised deterministically from an LCG, then count live cells. Stresses tight 2-D array indexing and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 34.63 ms | 34.63 ms | 34.63 ms | 0.00 µs | 1.48× | `2782` |
| Rust | ✅ | 23.47 ms | 23.47 ms | 23.47 ms | 0.00 µs | 1.00× | `2782` |
| Go | ✅ | 62.87 ms | 62.87 ms | 62.87 ms | 0.00 µs | 2.68× | `2782` |
| Python | ✅ | 3.249 s | 3.249 s | 3.249 s | 0.00 µs | 138.42× | `2782` |

### knapsack_dp — 0/1 knapsack DP (classic DP)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Generate N items with deterministic weights and values from an LCG, then solve the 0/1 knapsack problem with capacity 4000 using a 1-D rolling DP array. Stresses tight integer DP loops and array updates.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 3.85 ms | 3.85 ms | 3.85 ms | 0.00 µs | 1.00× | `137386` |
| Rust | ✅ | 4.28 ms | 4.28 ms | 4.28 ms | 0.00 µs | 1.11× | `137386` |
| Go | ✅ | 4.10 ms | 4.10 ms | 4.10 ms | 0.00 µs | 1.06× | `137386` |
| Python | ✅ | 408.51 ms | 408.51 ms | 408.51 ms | 0.00 µs | 105.97× | `137386` |

### levenshtein — Levenshtein edit-distance DP

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Compute the Levenshtein edit distance between two deterministic length-L strings drawn from an 8-letter alphabet via two LCG streams, using a 1-D rolling DP. Stresses tight DP inner loops and string indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 2.67 ms | 2.67 ms | 2.67 ms | 0.00 µs | 1.00× | `1046` |
| Rust | ✅ | 6.86 ms | 6.86 ms | 6.86 ms | 0.00 µs | 2.57× | `1046` |
| Go | ✅ | 3.92 ms | 3.92 ms | 3.92 ms | 0.00 µs | 1.47× | `1046` |
| Python | ✅ | 446.40 ms | 446.40 ms | 446.40 ms | 0.00 µs | 167.17× | `1046` |

### monte_carlo_pi — Integer Monte-Carlo PI estimation

_Category_: `apps` &nbsp;&nbsp;_Args_: `5000000`

For N pseudo-random points (x, y) drawn from an LCG modulo R = 65536, count how many satisfy x*x + y*y <= R*R. Pure integer arithmetic, no floating-point, identical algorithm across all languages.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 18.70 ms | 18.70 ms | 18.70 ms | 0.00 µs | 1.47× | `3927392` |
| Rust | ✅ | 12.75 ms | 12.75 ms | 12.75 ms | 0.00 µs | 1.00× | `3927392` |
| Go | ✅ | 18.48 ms | 18.48 ms | 18.48 ms | 0.00 µs | 1.45× | `3927392` |
| Python | ✅ | 1.789 s | 1.789 s | 1.789 s | 0.00 µs | 140.32× | `3927392` |

### histogram — Histogram bucketing (data-analysis kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `5000000`

Generate N pseudo-random integers via an LCG and bucket each into one of 1024 buckets, returning the XOR-fold of bucket counts. Stresses scatter-style array updates and integer hashing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 9.43 ms | 9.43 ms | 9.43 ms | 0.00 µs | 1.34× | `30` |
| Rust | ✅ | 7.05 ms | 7.05 ms | 7.05 ms | 0.00 µs | 1.00× | `30` |
| Go | ✅ | 8.00 ms | 8.00 ms | 8.00 ms | 0.00 µs | 1.14× | `30` |
| Python | ✅ | 1.088 s | 1.088 s | 1.088 s | 0.00 µs | 154.41× | `30` |

### dijkstra — Dense-graph Dijkstra SSSP

_Category_: `apps` &nbsp;&nbsp;_Args_: `800`

Build a V*V adjacency matrix with deterministic LCG-derived integer weights, then run Dijkstra's single-source shortest-paths algorithm with an O(V^2) array-based priority. Stresses tight nested integer loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 1.14 ms | 1.14 ms | 1.14 ms | 0.00 µs | 1.61× | `6` |
| Rust | ✅ | 709.22 µs | 709.22 µs | 709.22 µs | 0.00 µs | 1.00× | `6` |
| Go | ✅ | 1.09 ms | 1.09 ms | 1.09 ms | 0.00 µs | 1.53× | `6` |
| Python | ✅ | 45.18 ms | 45.18 ms | 45.18 ms | 0.00 µs | 63.70× | `6` |

### base64 — Base64 encoder (byte-stream codec)

_Category_: `apps` &nbsp;&nbsp;_Args_: `2000000`

Generate N deterministic bytes via an LCG, then encode them in base64 using a hand-written table-driven encoder, XOR-folding all output bytes into a checksum. Stresses byte-level bitwise operations and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 2.87 ms | 2.87 ms | 2.87 ms | 0.00 µs | 1.00× | `10` |
| Rust | ✅ | 2.92 ms | 2.92 ms | 2.92 ms | 0.00 µs | 1.02× | `10` |
| Go | ✅ | 3.79 ms | 3.79 ms | 3.79 ms | 0.00 µs | 1.32× | `10` |
| Python | ✅ | 336.11 ms | 336.11 ms | 336.11 ms | 0.00 µs | 117.21× | `10` |

### crc32 — CRC32 checksum (table-driven hashing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `5000000`

Generate N deterministic bytes via an LCG, then compute the IEEE 802.3 CRC32 byte-by-byte using a precomputed 256-entry lookup table. Identical algorithm across all five languages; stresses tight byte-loop throughput and table lookup.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |
| C++ | ✅ | 12.50 ms | 12.50 ms | 12.50 ms | 0.00 µs | 1.00× | `3626342857` |
| Rust | ✅ | 12.58 ms | 12.58 ms | 12.58 ms | 0.00 µs | 1.01× | `3626342857` |
| Go | ✅ | 12.50 ms | 12.50 ms | 12.50 ms | 0.00 µs | 1.00× | `3626342857` |
| Python | ✅ | 645.18 ms | 645.18 ms | 645.18 ms | 0.00 µs | 51.60× | `3626342857` |

## Methodology

- Each implementation is invoked as a fresh OS process and measures its own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. This excludes interpreter / runtime startup from the measurement.
- Each implementation also prints `CHECKSUM:<value>` of its computed result; the runner verifies all implementations of the same benchmark agree, otherwise the comparison is flagged as invalid.
- Per benchmark we run `warmup` unmeasured iterations, then `iterations` measured iterations and report **min / median / mean / stddev**. The _min_ is used for the headline ratio because it is the most robust estimate of best-case wall-clock cost when other system noise is present.
- Compiler flags: `g++ -O2 -std=c++17` for C++, `rustc -O --edition=2021` (release-equivalent `opt-level=3`) for Rust, `go build` (default release optimization) for Go, `cjpm build` for Cangjie (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`), CPython 3 for Python (no `-O`), all with no extra runtime tuning.
