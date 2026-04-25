# CangjiePerf Benchmark Report

_Generated: 2026-04-25T15:19:41+00:00_

## Environment

- **OS**: Linux 6.17.0-1010-azure
- **Architecture**: x86_64
- **CPU**: AMD EPYC 7763 64-Core Processor
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
| **fibonacci** | micro | 23.90 ms | 3.87 ms | 6.73 ms | 11.54 ms | 308.03 ms | C++ |
| **sort** ⚠️ | **micro** | **2.134 s** | **133.46 ms** | **55.73 ms** | **297.99 ms** | **773.20 ms** | **Rust** |
| **hashmap_ops** ⚠️ | **micro** | **492.19 ms** | **105.51 ms** | **134.26 ms** | **65.98 ms** | **122.58 ms** | **Go** |
| **string_concat** | micro | 47.25 ms | 32.70 ms | 12.58 ms | 16.08 ms | 70.87 ms | Rust |
| **closure_sum** ⚠️ | **micro** | **100.85 ms** | **9.18 ms** | **1.55 ms** | **2.90 ms** | **359.24 ms** | **Rust** |
| **enum_eval** | micro | 583.14 ms | 133.25 ms | 226.28 ms | 188.05 ms | 5.215 s | C++ |
| **regex_search** ⚠️ | **micro** | **45.60 ms** | **77.83 ms** | **2.01 ms** | **103.34 ms** | **41.63 ms** | **Rust** |
| **math_loop** | micro | 140.38 ms | 86.27 ms | 84.96 ms | 144.94 ms | 916.98 ms | Rust |
| **prime_sieve** ⚠️ | **micro** | **1.561 s** | **53.53 ms** | **61.27 ms** | **53.37 ms** | **2.828 s** | **Go** |
| **quicksort** ⚠️ | **micro** | **2.289 s** | **111.48 ms** | **115.80 ms** | **120.65 ms** | **3.808 s** | **C++** |
| **mandelbrot** | apps | 251.84 ms | 90.78 ms | 91.43 ms | 91.16 ms | 3.465 s | C++ |
| **nbody** | apps | 78.81 ms | 14.36 ms | 9.17 ms | 15.04 ms | 1.161 s | Rust |
| **binary_trees** | apps | 116.15 ms | 66.65 ms | 64.97 ms | 93.32 ms | 855.13 ms | Rust |
| **matrix_multiply** ⚠️ | **apps** | **874.82 ms** | **10.19 ms** | **3.70 ms** | **10.42 ms** | **722.18 ms** | **Rust** |
| **word_count** ⚠️ | **apps** | **727.98 ms** | **27.02 ms** | **25.98 ms** | **25.16 ms** | **135.81 ms** | **Go** |
| **spectral_norm** ⚠️ | **apps** | **2.223 s** | **128.74 ms** | **129.39 ms** | **129.51 ms** | **15.449 s** | **C++** |

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
| Cangjie | ✅ | 23.90 ms | 23.94 ms | 23.95 ms | 44.68 µs | 6.18× | `2178309` |
| C++ | ✅ | 3.87 ms | 3.93 ms | 4.05 ms | 229.46 µs | 1.00× | `2178309` |
| Rust | ✅ | 6.73 ms | 6.75 ms | 6.96 ms | 298.73 µs | 1.74× | `2178309` |
| Go | ✅ | 11.54 ms | 12.19 ms | 12.05 ms | 286.91 µs | 2.99× | `2178309` |
| Python | ✅ | 308.03 ms | 310.40 ms | 312.21 ms | 4.49 ms | 79.69× | `2178309` |

### sort — Sort 2M integers (stdlib sort)

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Generate 2,000,000 deterministic pseudo-random Int64 values then sort ascending using the language's standard sort. Stresses standard library sorting and dynamic arrays.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.134 s | 2.178 s | 2.172 s | 24.07 ms | 38.29× | `1074570229` |
| C++ | ✅ | 133.46 ms | 133.58 ms | 133.75 ms | 478.45 µs | 2.39× | `1074570229` |
| Rust | ✅ | 55.73 ms | 55.82 ms | 55.92 ms | 201.44 µs | 1.00× | `1074570229` |
| Go | ✅ | 297.99 ms | 298.13 ms | 298.16 ms | 189.18 µs | 5.35× | `1074570229` |
| Python | ✅ | 773.20 ms | 790.76 ms | 796.54 ms | 18.13 ms | 13.87× | `1074570229` |

### hashmap_ops — HashMap insert + lookup (stdlib hash table)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N (string,int) pairs then look up the same N keys. Stresses hash maps, string hashing, and string allocation.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 492.19 ms | 510.90 ms | 507.99 ms | 9.43 ms | 7.46× | `0` |
| C++ | ✅ | 105.51 ms | 115.89 ms | 113.84 ms | 6.66 ms | 1.60× | `0` |
| Rust | ✅ | 134.26 ms | 141.25 ms | 140.55 ms | 3.93 ms | 2.03× | `0` |
| Go | ✅ | 65.98 ms | 73.94 ms | 73.93 ms | 5.99 ms | 1.00× | `0` |
| Python | ✅ | 122.58 ms | 125.08 ms | 126.96 ms | 4.94 ms | 1.86× | `0` |

### string_concat — String building (stdlib StringBuilder)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Build a single large string from N small fragments using the recommended efficient builder for each language. Stresses string buffers and memory growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 47.25 ms | 47.35 ms | 47.36 ms | 106.73 µs | 3.76× | `5388890` |
| C++ | ✅ | 32.70 ms | 33.12 ms | 33.08 ms | 222.24 µs | 2.60× | `5388890` |
| Rust | ✅ | 12.58 ms | 12.60 ms | 12.60 ms | 22.28 µs | 1.00× | `5388890` |
| Go | ✅ | 16.08 ms | 16.17 ms | 16.29 ms | 231.37 µs | 1.28× | `5388890` |
| Python | ✅ | 70.87 ms | 71.05 ms | 71.46 ms | 943.09 µs | 5.63× | `5388890` |

### closure_sum — Closure / higher-order pipeline

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Apply a map -> filter -> reduce pipeline of closures over N integers. Stresses higher-order function dispatch, closure allocation, and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 100.85 ms | 102.13 ms | 101.75 ms | 731.80 µs | 65.26× | `1777776444435777780` |
| C++ | ✅ | 9.18 ms | 9.56 ms | 9.45 ms | 215.48 µs | 5.94× | `1777776444435777780` |
| Rust | ✅ | 1.55 ms | 1.57 ms | 1.63 ms | 114.44 µs | 1.00× | `1777776444435777780` |
| Go | ✅ | 2.90 ms | 2.96 ms | 3.02 ms | 146.53 µs | 1.87× | `1777776444435777780` |
| Python | ✅ | 359.24 ms | 361.46 ms | 364.88 ms | 9.19 ms | 232.47× | `1777776444435777780` |

### enum_eval — Enum / pattern matching (AST evaluation)

_Category_: `micro` &nbsp;&nbsp;_Args_: `18 60`

Build a recursive arithmetic expression tree of depth D and evaluate it N times via recursive pattern matching on a sum-type enum (Num | Add | Sub | Mul). Stresses algebraic data types, recursive calls, and tag dispatch.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 583.14 ms | 621.37 ms | 629.26 ms | 41.78 ms | 4.38× | `0` |
| C++ | ✅ | 133.25 ms | 136.36 ms | 135.58 ms | 2.02 ms | 1.00× | `0` |
| Rust | ✅ | 226.28 ms | 243.86 ms | 243.01 ms | 10.48 ms | 1.70× | `0` |
| Go | ✅ | 188.05 ms | 203.83 ms | 202.67 ms | 8.97 ms | 1.41× | `0` |
| Python | ✅ | 5.215 s | 5.277 s | 5.276 s | 48.34 ms | 39.14× | `0` |

### regex_search — Regex find-all (stdlib regex)

_Category_: `micro` &nbsp;&nbsp;_Args_: `4000`

Run a non-trivial alternation regex (date | email | capitalized word) across REPEATS copies of a sample paragraph. Stresses the standard regex engine.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 45.60 ms | 45.82 ms | 45.94 ms | 389.77 µs | 22.73× | `36000` |
| C++ | ✅ | 77.83 ms | 77.90 ms | 78.09 ms | 413.65 µs | 38.80× | `36000` |
| Rust | ✅ | 2.01 ms | 2.09 ms | 2.10 ms | 66.93 µs | 1.00× | `36000` |
| Go | ✅ | 103.34 ms | 104.41 ms | 104.27 ms | 578.57 µs | 51.52× | `36000` |
| Python | ✅ | 41.63 ms | 42.12 ms | 42.08 ms | 365.59 µs | 20.75× | `36000` |

### math_loop — Math-intensive loop (sin/cos/sqrt/exp)

_Category_: `micro` &nbsp;&nbsp;_Args_: `5000000`

Sum sin(x)*cos(x)+sqrt(x+1)-exp(-x) over N points. Stresses the math standard library and floating-point throughput.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 140.38 ms | 140.68 ms | 140.68 ms | 273.63 µs | 1.65× | `4704337083537` |
| C++ | ✅ | 86.27 ms | 86.85 ms | 86.71 ms | 391.18 µs | 1.02× | `4704337083537` |
| Rust | ✅ | 84.96 ms | 85.00 ms | 85.22 ms | 418.68 µs | 1.00× | `4704337083537` |
| Go | ✅ | 144.94 ms | 145.10 ms | 145.14 ms | 155.69 µs | 1.71× | `4704337083537` |
| Python | ✅ | 916.98 ms | 922.02 ms | 922.73 ms | 5.59 ms | 10.79× | `4704337083537` |

### prime_sieve — Sieve of Eratosthenes

_Category_: `micro` &nbsp;&nbsp;_Args_: `20000000`

Classic Sieve of Eratosthenes up to N on a one-byte-per-cell boolean array, then count primes and sum them mod 2^31. Algorithmically identical across all three languages: same loop bounds, same inner stride, same checksum formula.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 1.561 s | 1.632 s | 1.624 s | 49.54 ms | 29.24× | `1156745585` |
| C++ | ✅ | 53.53 ms | 55.23 ms | 56.24 ms | 2.61 ms | 1.00× | `1156745585` |
| Rust | ✅ | 61.27 ms | 66.07 ms | 65.52 ms | 3.26 ms | 1.15× | `1156745585` |
| Go | ✅ | 53.37 ms | 53.84 ms | 54.68 ms | 2.36 ms | 1.00× | `1156745585` |
| Python | ✅ | 2.828 s | 2.849 s | 3.021 s | 390.83 ms | 53.00× | `1156745585` |

### quicksort — Hand-written quicksort

_Category_: `micro` &nbsp;&nbsp;_Args_: `1500000`

Lomuto-partition quicksort with middle-element pivot and recurse-smaller-side / iterate-larger-side, implemented by hand in all three languages so the algorithm itself is identical (complements the stdlib `sort` benchmark).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.289 s | 2.306 s | 2.306 s | 16.34 ms | 20.53× | `612429648` |
| C++ | ✅ | 111.48 ms | 112.05 ms | 112.22 ms | 706.30 µs | 1.00× | `612429648` |
| Rust | ✅ | 115.80 ms | 115.97 ms | 116.02 ms | 205.91 µs | 1.04× | `612429648` |
| Go | ✅ | 120.65 ms | 120.89 ms | 120.94 ms | 248.94 µs | 1.08× | `612429648` |
| Python | ✅ | 3.808 s | 3.946 s | 3.939 s | 87.26 ms | 34.15× | `612429648` |

### mandelbrot — Mandelbrot set (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `600 200`

Compute a Mandelbrot escape-time bitmap of size W*W with up to MAX_ITER iterations. Inspired by the Computer Language Benchmarks Game. Stresses tight numeric loops and floating-point arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 251.84 ms | 251.90 ms | 251.95 ms | 104.97 µs | 2.77× | `29624109` |
| C++ | ✅ | 90.78 ms | 90.94 ms | 91.07 ms | 361.64 µs | 1.00× | `29624109` |
| Rust | ✅ | 91.43 ms | 91.80 ms | 91.80 ms | 304.40 µs | 1.01× | `29624109` |
| Go | ✅ | 91.16 ms | 91.20 ms | 91.22 ms | 66.18 µs | 1.00× | `29624109` |
| Python | ✅ | 3.465 s | 3.486 s | 3.491 s | 19.73 ms | 38.17× | `29624109` |

### nbody — N-Body simulation (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200000`

Symplectic integrator for the classic 5-body solar system from the Benchmarks Game over N steps. Stresses tight floating-point loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 78.81 ms | 78.83 ms | 78.85 ms | 50.91 µs | 8.59× | `-169083713` |
| C++ | ✅ | 14.36 ms | 14.37 ms | 14.38 ms | 15.90 µs | 1.57× | `-169083713` |
| Rust | ✅ | 9.17 ms | 9.31 ms | 9.36 ms | 202.46 µs | 1.00× | `-169083713` |
| Go | ✅ | 15.04 ms | 15.33 ms | 15.29 ms | 246.18 µs | 1.64× | `-169083713` |
| Python | ✅ | 1.161 s | 1.183 s | 1.188 s | 23.70 ms | 126.61× | `-169083713` |

### binary_trees — Binary trees (allocation / GC pressure)

_Category_: `apps` &nbsp;&nbsp;_Args_: `14`

Build and check many small balanced binary trees up to depth D. Adapted from the Computer Language Benchmarks Game. Stresses small-object allocation and GC (or heap allocator).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 116.15 ms | 119.56 ms | 118.94 ms | 1.63 ms | 1.79× | `13250584224` |
| C++ | ✅ | 66.65 ms | 67.35 ms | 67.19 ms | 455.73 µs | 1.03× | `13250584224` |
| Rust | ✅ | 64.97 ms | 65.58 ms | 65.62 ms | 512.13 µs | 1.00× | `13250584224` |
| Go | ✅ | 93.32 ms | 94.03 ms | 93.97 ms | 580.05 µs | 1.44× | `13250584224` |
| Python | ✅ | 855.13 ms | 865.90 ms | 865.73 ms | 8.57 ms | 13.16× | `13250584224` |

### matrix_multiply — Matrix multiplication (naive O(N^3))

_Category_: `apps` &nbsp;&nbsp;_Args_: `250`

Compute C = A * B for two NxN double-precision matrices using the textbook triple-loop algorithm. Stresses memory layout, FP multiply-add throughput, and cache behaviour.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 874.82 ms | 905.61 ms | 900.78 ms | 15.82 ms | 236.59× | `15315135000` |
| C++ | ✅ | 10.19 ms | 10.28 ms | 10.53 ms | 399.66 µs | 2.76× | `15315135000` |
| Rust | ✅ | 3.70 ms | 3.73 ms | 3.86 ms | 255.36 µs | 1.00× | `15315135000` |
| Go | ✅ | 10.42 ms | 11.32 ms | 11.14 ms | 438.51 µs | 2.82× | `15315135000` |
| Python | ✅ | 722.18 ms | 733.81 ms | 733.04 ms | 7.42 ms | 195.31× | `15315135000` |

### word_count — Word count (text processing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1000000`

Tokenize a synthesized N-word text and count word frequencies in a hash-map. Stresses string slicing/comparison, hashing, and hash-map updates — a typical scripting workload.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 727.98 ms | 740.21 ms | 742.19 ms | 12.34 ms | 28.94× | `638309952` |
| C++ | ✅ | 27.02 ms | 27.51 ms | 27.79 ms | 833.75 µs | 1.07× | `638309952` |
| Rust | ✅ | 25.98 ms | 26.03 ms | 26.06 ms | 79.21 µs | 1.03× | `638309952` |
| Go | ✅ | 25.16 ms | 27.13 ms | 26.40 ms | 1.03 ms | 1.00× | `638309952` |
| Python | ✅ | 135.81 ms | 136.04 ms | 136.26 ms | 594.47 µs | 5.40× | `638309952` |

### spectral_norm — Spectral norm (CLBG numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Approximates the largest eigenvalue of an infinite matrix A[i][j] = 1 / ((i+j)(i+j+1)/2 + i + 1) via 10 power iterations of v <- A^T A v. Adapted from the Computer Language Benchmarks Game; algorithmically identical across all three languages.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.223 s | 2.240 s | 2.249 s | 27.64 ms | 17.27× | `1274224151` |
| C++ | ✅ | 128.74 ms | 128.86 ms | 128.88 ms | 128.37 µs | 1.00× | `1274224151` |
| Rust | ✅ | 129.39 ms | 129.43 ms | 129.46 ms | 107.83 µs | 1.01× | `1274224151` |
| Go | ✅ | 129.51 ms | 129.90 ms | 129.85 ms | 252.76 µs | 1.01× | `1274224151` |
| Python | ✅ | 15.449 s | 15.630 s | 15.655 s | 165.85 ms | 120.00× | `1274224151` |

## Methodology

- Each implementation is invoked as a fresh OS process and measures its own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. This excludes interpreter / runtime startup from the measurement.
- Each implementation also prints `CHECKSUM:<value>` of its computed result; the runner verifies all implementations of the same benchmark agree, otherwise the comparison is flagged as invalid.
- Per benchmark we run `warmup` unmeasured iterations, then `iterations` measured iterations and report **min / median / mean / stddev**. The _min_ is used for the headline ratio because it is the most robust estimate of best-case wall-clock cost when other system noise is present.
- Compiler flags: `g++ -O2 -std=c++17` for C++, `rustc -O --edition=2021` (release-equivalent ``opt-level=3``) for Rust, `go build` (default release optimization) for Go, `cjpm build` for Cangjie (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`), CPython 3 for Python (no `-O`), all with no extra runtime tuning.
