# CangjiePerf Benchmark Report

_Generated: 2026-04-25T16:29:07+00:00_

## Environment

- **OS**: Linux 6.17.0-1010-azure
- **Architecture**: x86_64
- **CPU**: AMD EPYC 9V74 80-Core Processor
- **Python**: 3.12.3

## Toolchains

The benchmark suite compares **Cangjie** against four reference languages: **C++** and **Rust** as native-compiled baselines, **Go** as a managed-runtime compiled baseline, and **Python** as a scripting-language baseline. The exact toolchain versions used for this run are:

| Language | Available | Version |
|----------|-----------|---------|
| Cangjie | ✅ | Cangjie Compiler: 1.0.5 (cjnative) |
| C++ | ✅ | g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| Rust | ✅ | rustc 1.94.1 (e408947bf 2026-03-25) |
| Go | ✅ | go version go1.24.13 linux/amd64 |
| Python | ✅ | Python 3.12.3 |

## Run Configuration

- Warmup runs: **1**
- Measurement runs: **5**
- Languages enabled: **Cangjie, C++, Rust, Go, Python**
- Reported metric: per-process self-timed wall-clock (`ELAPSED_MS`); **`min`** chosen as the headline number, lower is better.

## Summary

| Benchmark | Category | Cangjie | C++ | Rust | Go | Python | Fastest |
|---|---|---|---|---|---|---|---|
| **fibonacci** | micro | 7.11 ms | 2.86 ms | 5.77 ms | 9.81 ms | 235.06 ms | C++ |
| **sort** ⚠️ | **micro** | **1.791 s** | **113.98 ms** | **47.28 ms** | **256.66 ms** | **656.32 ms** | **Rust** |
| **hashmap_ops** | micro | 48.63 ms | 89.47 ms | 107.71 ms | 41.73 ms | 101.71 ms | Go |
| **string_concat** | micro | 35.06 ms | 21.90 ms | 9.09 ms | 11.32 ms | 59.57 ms | Rust |
| **closure_sum** | micro | 1.89 ms | 7.34 ms | 2.00 ms | 2.52 ms | 268.70 ms | Cangjie |
| **enum_eval** | micro | 158.04 ms | 106.68 ms | 153.49 ms | 149.17 ms | 4.140 s | C++ |
| **regex_search** ⚠️ | **micro** | **38.46 ms** | **60.88 ms** | **1.47 ms** | **70.25 ms** | **30.29 ms** | **Rust** |
| **math_loop** | micro | 67.86 ms | 68.22 ms | 64.58 ms | 113.20 ms | 752.01 ms | Rust |
| **prime_sieve** | micro | 51.25 ms | 41.52 ms | 53.17 ms | 45.45 ms | 2.265 s | C++ |
| **quicksort** | micro | 133.44 ms | 104.52 ms | 99.99 ms | 104.12 ms | 2.923 s | Rust |
| **mandelbrot** | apps | 75.62 ms | 78.74 ms | 83.23 ms | 78.91 ms | 3.018 s | Cangjie |
| **nbody** | apps | 11.55 ms | 11.43 ms | 7.57 ms | 12.94 ms | 937.49 ms | Rust |
| **binary_trees** | apps | 40.00 ms | 49.95 ms | 51.16 ms | 68.79 ms | 654.55 ms | Cangjie |
| **matrix_multiply** | apps | 13.64 ms | 8.90 ms | 2.89 ms | 9.05 ms | 619.96 ms | Rust |
| **word_count** ⚠️ | **apps** | **143.88 ms** | **16.19 ms** | **18.83 ms** | **17.27 ms** | **100.66 ms** | **C++** |
| **spectral_norm** | apps | 113.97 ms | 113.01 ms | 113.03 ms | 111.14 ms | 13.135 s | Go |

> **Bold rows** marked with ⚠️ are benchmarks where Cangjie's timing is closer (in log scale) to Python's than to C++'s — i.e. cases where the Cangjie implementation is significantly under-performing the native baseline. See [`analyse.md`](./analyse.md) for the root-cause analysis.

### Visual comparison

Each benchmark shows five side-by-side bars (Cangjie / C++ / Rust / Go / Python). **Lower bars are faster.** Note the **logarithmic** y-axis: a one-step gridline difference is a 10× speed difference. Open the SVG in a new tab to see exact per-bar tooltips.

![Benchmark wall-clock comparison (log scale, lower is better)](./report_chart.svg)

## Per-benchmark Detail

### fibonacci — Recursive Fibonacci (function call / recursion)

_Category_: `micro` &nbsp;&nbsp;_Args_: `32`

Pure recursive fib(N). Stresses function-call overhead and integer arithmetic. No standard-library involvement beyond integers.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 7.11 ms | 7.31 ms | 7.27 ms | 91.60 µs | 2.48× | `2178309` |
| C++ | ✅ | 2.86 ms | 2.90 ms | 2.97 ms | 174.86 µs | 1.00× | `2178309` |
| Rust | ✅ | 5.77 ms | 5.78 ms | 5.91 ms | 185.47 µs | 2.02× | `2178309` |
| Go | ✅ | 9.81 ms | 10.01 ms | 10.01 ms | 172.16 µs | 3.43× | `2178309` |
| Python | ✅ | 235.06 ms | 235.43 ms | 236.29 ms | 1.90 ms | 82.08× | `2178309` |

### sort — Sort 2M integers (stdlib sort)

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Generate 2,000,000 deterministic pseudo-random Int64 values then sort ascending using the language's standard sort. Stresses standard library sorting and dynamic arrays.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 1.791 s | 1.832 s | 1.824 s | 21.72 ms | 37.89× | `1074570229` |
| C++ | ✅ | 113.98 ms | 114.11 ms | 114.25 ms | 353.61 µs | 2.41× | `1074570229` |
| Rust | ✅ | 47.28 ms | 47.38 ms | 47.44 ms | 151.74 µs | 1.00× | `1074570229` |
| Go | ✅ | 256.66 ms | 257.04 ms | 257.57 ms | 959.17 µs | 5.43× | `1074570229` |
| Python | ✅ | 656.32 ms | 663.36 ms | 661.46 ms | 3.15 ms | 13.88× | `1074570229` |

### hashmap_ops — HashMap insert + lookup (stdlib hash table)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N (string,int) pairs then look up the same N keys. Stresses hash maps, string hashing, and string allocation.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 48.63 ms | 51.50 ms | 51.16 ms | 1.47 ms | 1.17× | `0` |
| C++ | ✅ | 89.47 ms | 91.01 ms | 90.97 ms | 1.19 ms | 2.14× | `0` |
| Rust | ✅ | 107.71 ms | 109.76 ms | 109.65 ms | 1.28 ms | 2.58× | `0` |
| Go | ✅ | 41.73 ms | 43.58 ms | 44.00 ms | 2.35 ms | 1.00× | `0` |
| Python | ✅ | 101.71 ms | 102.48 ms | 102.77 ms | 1.03 ms | 2.44× | `0` |

### string_concat — String building (stdlib StringBuilder)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Build a single large string from N small fragments using the recommended efficient builder for each language. Stresses string buffers and memory growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 35.06 ms | 35.10 ms | 35.19 ms | 225.17 µs | 3.86× | `5388890` |
| C++ | ✅ | 21.90 ms | 21.93 ms | 21.94 ms | 36.16 µs | 2.41× | `5388890` |
| Rust | ✅ | 9.09 ms | 9.23 ms | 9.32 ms | 239.51 µs | 1.00× | `5388890` |
| Go | ✅ | 11.32 ms | 11.61 ms | 11.56 ms | 234.03 µs | 1.24× | `5388890` |
| Python | ✅ | 59.57 ms | 60.27 ms | 60.21 ms | 398.22 µs | 6.55× | `5388890` |

### closure_sum — Closure / higher-order pipeline

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Apply a map -> filter -> reduce pipeline of closures over N integers. Stresses higher-order function dispatch, closure allocation, and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 1.89 ms | 1.91 ms | 1.92 ms | 22.62 µs | 1.00× | `1777776444435777780` |
| C++ | ✅ | 7.34 ms | 7.56 ms | 7.48 ms | 116.97 µs | 3.88× | `1777776444435777780` |
| Rust | ✅ | 2.00 ms | 2.01 ms | 2.02 ms | 28.89 µs | 1.06× | `1777776444435777780` |
| Go | ✅ | 2.52 ms | 2.54 ms | 2.58 ms | 87.53 µs | 1.33× | `1777776444435777780` |
| Python | ✅ | 268.70 ms | 270.05 ms | 271.60 ms | 3.27 ms | 142.00× | `1777776444435777780` |

### enum_eval — Enum / pattern matching (AST evaluation)

_Category_: `micro` &nbsp;&nbsp;_Args_: `18 60`

Build a recursive arithmetic expression tree of depth D and evaluate it N times via recursive pattern matching on a sum-type enum (Num | Add | Sub | Mul). Stresses algebraic data types, recursive calls, and tag dispatch.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 158.04 ms | 159.69 ms | 162.84 ms | 5.63 ms | 1.48× | `0` |
| C++ | ✅ | 106.68 ms | 107.34 ms | 107.28 ms | 446.26 µs | 1.00× | `0` |
| Rust | ✅ | 153.49 ms | 154.17 ms | 154.37 ms | 754.54 µs | 1.44× | `0` |
| Go | ✅ | 149.17 ms | 150.59 ms | 150.44 ms | 804.69 µs | 1.40× | `0` |
| Python | ✅ | 4.140 s | 4.205 s | 4.197 s | 40.71 ms | 38.81× | `0` |

### regex_search — Regex find-all (stdlib regex)

_Category_: `micro` &nbsp;&nbsp;_Args_: `4000`

Run a non-trivial alternation regex (date | email | capitalized word) across REPEATS copies of a sample paragraph. Stresses the standard regex engine.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 38.46 ms | 38.65 ms | 38.61 ms | 94.47 µs | 26.14× | `36000` |
| C++ | ✅ | 60.88 ms | 61.04 ms | 61.63 ms | 1.32 ms | 41.38× | `36000` |
| Rust | ✅ | 1.47 ms | 1.54 ms | 1.54 ms | 52.64 µs | 1.00× | `36000` |
| Go | ✅ | 70.25 ms | 70.61 ms | 70.84 ms | 568.95 µs | 47.75× | `36000` |
| Python | ✅ | 30.29 ms | 30.35 ms | 30.41 ms | 144.59 µs | 20.59× | `36000` |

### math_loop — Math-intensive loop (sin/cos/sqrt/exp)

_Category_: `micro` &nbsp;&nbsp;_Args_: `5000000`

Sum sin(x)*cos(x)+sqrt(x+1)-exp(-x) over N points. Stresses the math standard library and floating-point throughput.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 67.86 ms | 67.95 ms | 67.96 ms | 71.09 µs | 1.05× | `4704337083537` |
| C++ | ✅ | 68.22 ms | 68.34 ms | 68.48 ms | 397.99 µs | 1.06× | `4704337083537` |
| Rust | ✅ | 64.58 ms | 64.67 ms | 64.81 ms | 327.73 µs | 1.00× | `4704337083537` |
| Go | ✅ | 113.20 ms | 113.63 ms | 117.74 ms | 9.34 ms | 1.75× | `4704337083537` |
| Python | ✅ | 752.01 ms | 763.03 ms | 762.26 ms | 6.10 ms | 11.64× | `4704337083537` |

### prime_sieve — Sieve of Eratosthenes

_Category_: `micro` &nbsp;&nbsp;_Args_: `20000000`

Classic Sieve of Eratosthenes up to N on a one-byte-per-cell boolean array, then count primes and sum them mod 2^31. Algorithmically identical across all three languages: same loop bounds, same inner stride, same checksum formula.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 51.25 ms | 51.55 ms | 51.51 ms | 217.13 µs | 1.23× | `1156745585` |
| C++ | ✅ | 41.52 ms | 41.70 ms | 41.83 ms | 450.40 µs | 1.00× | `1156745585` |
| Rust | ✅ | 53.17 ms | 53.24 ms | 53.27 ms | 105.32 µs | 1.28× | `1156745585` |
| Go | ✅ | 45.45 ms | 45.81 ms | 45.86 ms | 323.25 µs | 1.09× | `1156745585` |
| Python | ✅ | 2.265 s | 2.281 s | 2.292 s | 30.67 ms | 54.57× | `1156745585` |

### quicksort — Hand-written quicksort

_Category_: `micro` &nbsp;&nbsp;_Args_: `1500000`

Lomuto-partition quicksort with middle-element pivot and recurse-smaller-side / iterate-larger-side, implemented by hand in all three languages so the algorithm itself is identical (complements the stdlib `sort` benchmark).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 133.44 ms | 133.55 ms | 133.61 ms | 161.39 µs | 1.33× | `612429648` |
| C++ | ✅ | 104.52 ms | 104.77 ms | 104.77 ms | 189.69 µs | 1.05× | `612429648` |
| Rust | ✅ | 99.99 ms | 100.20 ms | 100.31 ms | 373.15 µs | 1.00× | `612429648` |
| Go | ✅ | 104.12 ms | 107.20 ms | 107.20 ms | 2.05 ms | 1.04× | `612429648` |
| Python | ✅ | 2.923 s | 2.966 s | 2.959 s | 23.18 ms | 29.23× | `612429648` |

### mandelbrot — Mandelbrot set (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `600 200`

Compute a Mandelbrot escape-time bitmap of size W*W with up to MAX_ITER iterations. Inspired by the Computer Language Benchmarks Game. Stresses tight numeric loops and floating-point arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 75.62 ms | 75.72 ms | 75.74 ms | 130.58 µs | 1.00× | `29624109` |
| C++ | ✅ | 78.74 ms | 78.84 ms | 78.84 ms | 62.01 µs | 1.04× | `29624109` |
| Rust | ✅ | 83.23 ms | 83.37 ms | 83.34 ms | 65.41 µs | 1.10× | `29624109` |
| Go | ✅ | 78.91 ms | 78.99 ms | 79.00 ms | 83.33 µs | 1.04× | `29624109` |
| Python | ✅ | 3.018 s | 3.050 s | 3.062 s | 46.89 ms | 39.91× | `29624109` |

### nbody — N-Body simulation (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200000`

Symplectic integrator for the classic 5-body solar system from the Benchmarks Game over N steps. Stresses tight floating-point loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 11.55 ms | 11.55 ms | 11.55 ms | 2.98 µs | 1.52× | `-169083713` |
| C++ | ✅ | 11.43 ms | 11.44 ms | 11.54 ms | 133.47 µs | 1.51× | `-169083713` |
| Rust | ✅ | 7.57 ms | 7.61 ms | 7.72 ms | 253.85 µs | 1.00× | `-169083713` |
| Go | ✅ | 12.94 ms | 12.98 ms | 13.06 ms | 144.69 µs | 1.71× | `-169083713` |
| Python | ✅ | 937.49 ms | 939.00 ms | 939.86 ms | 2.33 ms | 123.78× | `-169083713` |

### binary_trees — Binary trees (allocation / GC pressure)

_Category_: `apps` &nbsp;&nbsp;_Args_: `14`

Build and check many small balanced binary trees up to depth D. Adapted from the Computer Language Benchmarks Game. Stresses small-object allocation and GC (or heap allocator).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 40.00 ms | 40.61 ms | 40.45 ms | 360.70 µs | 1.00× | `13250584224` |
| C++ | ✅ | 49.95 ms | 52.59 ms | 52.46 ms | 2.08 ms | 1.25× | `13250584224` |
| Rust | ✅ | 51.16 ms | 51.70 ms | 51.72 ms | 518.70 µs | 1.28× | `13250584224` |
| Go | ✅ | 68.79 ms | 69.02 ms | 69.08 ms | 239.28 µs | 1.72× | `13250584224` |
| Python | ✅ | 654.55 ms | 656.51 ms | 658.27 ms | 5.22 ms | 16.36× | `13250584224` |

### matrix_multiply — Matrix multiplication (naive O(N^3))

_Category_: `apps` &nbsp;&nbsp;_Args_: `250`

Compute C = A * B for two NxN double-precision matrices using the textbook triple-loop algorithm. Stresses memory layout, FP multiply-add throughput, and cache behaviour.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 13.64 ms | 13.70 ms | 13.70 ms | 68.51 µs | 4.73× | `15315135000` |
| C++ | ✅ | 8.90 ms | 8.91 ms | 8.97 ms | 134.30 µs | 3.09× | `15315135000` |
| Rust | ✅ | 2.89 ms | 2.92 ms | 2.92 ms | 27.35 µs | 1.00× | `15315135000` |
| Go | ✅ | 9.05 ms | 9.42 ms | 9.32 ms | 176.40 µs | 3.14× | `15315135000` |
| Python | ✅ | 619.96 ms | 626.27 ms | 626.28 ms | 6.39 ms | 214.81× | `15315135000` |

### word_count — Word count (text processing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1000000`

Tokenize a synthesized N-word text and count word frequencies in a hash-map. Stresses string slicing/comparison, hashing, and hash-map updates — a typical scripting workload.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 143.88 ms | 144.27 ms | 144.83 ms | 1.30 ms | 8.89× | `638309952` |
| C++ | ✅ | 16.19 ms | 16.21 ms | 16.33 ms | 174.74 µs | 1.00× | `638309952` |
| Rust | ✅ | 18.83 ms | 18.91 ms | 18.90 ms | 49.85 µs | 1.16× | `638309952` |
| Go | ✅ | 17.27 ms | 17.64 ms | 17.62 ms | 299.43 µs | 1.07× | `638309952` |
| Python | ✅ | 100.66 ms | 102.06 ms | 102.76 ms | 2.48 ms | 6.22× | `638309952` |

### spectral_norm — Spectral norm (CLBG numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Approximates the largest eigenvalue of an infinite matrix A[i][j] = 1 / ((i+j)(i+j+1)/2 + i + 1) via 10 power iterations of v <- A^T A v. Adapted from the Computer Language Benchmarks Game; algorithmically identical across all three languages.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 113.97 ms | 114.09 ms | 114.17 ms | 172.84 µs | 1.03× | `1274224151` |
| C++ | ✅ | 113.01 ms | 113.72 ms | 113.58 ms | 501.35 µs | 1.02× | `1274224151` |
| Rust | ✅ | 113.03 ms | 113.23 ms | 113.23 ms | 147.94 µs | 1.02× | `1274224151` |
| Go | ✅ | 111.14 ms | 111.89 ms | 111.97 ms | 714.93 µs | 1.00× | `1274224151` |
| Python | ✅ | 13.135 s | 13.295 s | 13.312 s | 146.81 ms | 118.18× | `1274224151` |

## Methodology

- Each implementation is invoked as a fresh OS process and measures its own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. This excludes interpreter / runtime startup from the measurement.
- Each implementation also prints `CHECKSUM:<value>` of its computed result; the runner verifies all implementations of the same benchmark agree, otherwise the comparison is flagged as invalid.
- Per benchmark we run `warmup` unmeasured iterations, then `iterations` measured iterations and report **min / median / mean / stddev**. The _min_ is used for the headline ratio because it is the most robust estimate of best-case wall-clock cost when other system noise is present.
- Compiler flags: `g++ -O2 -std=c++17` for C++, `rustc -O --edition=2021` (release-equivalent `opt-level=3`) for Rust, `go build` (default release optimization) for Go, `cjpm build` for Cangjie (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`), CPython 3 for Python (no `-O`), all with no extra runtime tuning.
