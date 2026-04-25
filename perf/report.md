# CangjiePerf Benchmark Report

_Generated: 2026-04-25T16:01:41+00:00_

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
| **fibonacci** | micro | 9.27 ms | 3.71 ms | 7.43 ms | 12.76 ms | 290.72 ms | C++ |
| **sort** ⚠️ | **micro** | **2.285 s** | **147.06 ms** | **61.02 ms** | **330.69 ms** | **810.32 ms** | **Rust** |
| **hashmap_ops** | micro | 62.08 ms | 109.12 ms | 122.46 ms | 51.38 ms | 125.42 ms | Go |
| **string_concat** | micro | 44.22 ms | 26.56 ms | 11.67 ms | 14.53 ms | 75.57 ms | Rust |
| **closure_sum** | micro | 2.46 ms | 9.44 ms | 2.58 ms | 3.26 ms | 345.77 ms | Cangjie |
| **enum_eval** | micro | 204.64 ms | 137.35 ms | 200.17 ms | 192.14 ms | 5.257 s | C++ |
| **regex_search** ⚠️ | **micro** | **48.78 ms** | **78.36 ms** | **1.91 ms** | **91.35 ms** | **38.94 ms** | **Rust** |
| **math_loop** | micro | 84.88 ms | 84.34 ms | 82.97 ms | 145.93 ms | 946.24 ms | Rust |
| **prime_sieve** | micro | 66.51 ms | 53.26 ms | 68.46 ms | 58.83 ms | 2.864 s | C++ |
| **quicksort** | micro | 161.74 ms | 129.35 ms | 129.13 ms | 134.19 ms | 3.713 s | Rust |
| **mandelbrot** | apps | 97.53 ms | 101.65 ms | 107.42 ms | 101.93 ms | 3.924 s | Cangjie |
| **nbody** | apps | 23.46 ms | 14.71 ms | 9.77 ms | 17.11 ms | 1.199 s | Rust |
| **binary_trees** | apps | 49.22 ms | 64.79 ms | 65.52 ms | 89.18 ms | 841.38 ms | Cangjie |
| **matrix_multiply** | apps | 17.63 ms | 11.42 ms | 3.72 ms | 11.64 ms | 803.74 ms | Rust |
| **word_count** ⚠️ | **apps** | **178.13 ms** | **21.29 ms** | **24.54 ms** | **22.16 ms** | **132.61 ms** | **C++** |
| **spectral_norm** | apps | 147.06 ms | 146.49 ms | 145.87 ms | 144.10 ms | 16.618 s | Go |

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
| Cangjie | ✅ | 9.27 ms | 9.29 ms | 9.31 ms | 34.57 µs | 2.50× | `2178309` |
| C++ | ✅ | 3.71 ms | 3.76 ms | 3.75 ms | 21.96 µs | 1.00× | `2178309` |
| Rust | ✅ | 7.43 ms | 7.46 ms | 7.46 ms | 14.59 µs | 2.00× | `2178309` |
| Go | ✅ | 12.76 ms | 13.19 ms | 13.05 ms | 261.23 µs | 3.44× | `2178309` |
| Python | ✅ | 290.72 ms | 295.14 ms | 293.75 ms | 2.76 ms | 78.27× | `2178309` |

### sort — Sort 2M integers (stdlib sort)

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Generate 2,000,000 deterministic pseudo-random Int64 values then sort ascending using the language's standard sort. Stresses standard library sorting and dynamic arrays.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.285 s | 2.293 s | 2.293 s | 5.12 ms | 37.44× | `1074570229` |
| C++ | ✅ | 147.06 ms | 147.13 ms | 147.33 ms | 392.54 µs | 2.41× | `1074570229` |
| Rust | ✅ | 61.02 ms | 61.15 ms | 61.17 ms | 138.73 µs | 1.00× | `1074570229` |
| Go | ✅ | 330.69 ms | 332.71 ms | 332.53 ms | 1.08 ms | 5.42× | `1074570229` |
| Python | ✅ | 810.32 ms | 817.24 ms | 816.25 ms | 4.83 ms | 13.28× | `1074570229` |

### hashmap_ops — HashMap insert + lookup (stdlib hash table)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N (string,int) pairs then look up the same N keys. Stresses hash maps, string hashing, and string allocation.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 62.08 ms | 62.42 ms | 65.97 ms | 6.32 ms | 1.21× | `0` |
| C++ | ✅ | 109.12 ms | 110.09 ms | 110.05 ms | 585.23 µs | 2.12× | `0` |
| Rust | ✅ | 122.46 ms | 124.42 ms | 124.89 ms | 1.84 ms | 2.38× | `0` |
| Go | ✅ | 51.38 ms | 56.16 ms | 56.00 ms | 3.23 ms | 1.00× | `0` |
| Python | ✅ | 125.42 ms | 126.92 ms | 126.77 ms | 1.34 ms | 2.44× | `0` |

### string_concat — String building (stdlib StringBuilder)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Build a single large string from N small fragments using the recommended efficient builder for each language. Stresses string buffers and memory growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 44.22 ms | 44.49 ms | 44.47 ms | 244.08 µs | 3.79× | `5388890` |
| C++ | ✅ | 26.56 ms | 27.99 ms | 27.61 ms | 645.88 µs | 2.28× | `5388890` |
| Rust | ✅ | 11.67 ms | 11.80 ms | 11.97 ms | 333.59 µs | 1.00× | `5388890` |
| Go | ✅ | 14.53 ms | 14.93 ms | 14.88 ms | 303.53 µs | 1.25× | `5388890` |
| Python | ✅ | 75.57 ms | 76.42 ms | 76.24 ms | 566.25 µs | 6.48× | `5388890` |

### closure_sum — Closure / higher-order pipeline

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Apply a map -> filter -> reduce pipeline of closures over N integers. Stresses higher-order function dispatch, closure allocation, and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.46 ms | 2.49 ms | 2.48 ms | 18.73 µs | 1.00× | `1777776444435777780` |
| C++ | ✅ | 9.44 ms | 9.50 ms | 9.55 ms | 129.75 µs | 3.83× | `1777776444435777780` |
| Rust | ✅ | 2.58 ms | 2.59 ms | 2.59 ms | 8.81 µs | 1.05× | `1777776444435777780` |
| Go | ✅ | 3.26 ms | 3.31 ms | 3.41 ms | 172.43 µs | 1.32× | `1777776444435777780` |
| Python | ✅ | 345.77 ms | 349.53 ms | 349.13 ms | 2.05 ms | 140.30× | `1777776444435777780` |

### enum_eval — Enum / pattern matching (AST evaluation)

_Category_: `micro` &nbsp;&nbsp;_Args_: `18 60`

Build a recursive arithmetic expression tree of depth D and evaluate it N times via recursive pattern matching on a sum-type enum (Num | Add | Sub | Mul). Stresses algebraic data types, recursive calls, and tag dispatch.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 204.64 ms | 204.98 ms | 205.99 ms | 1.94 ms | 1.49× | `0` |
| C++ | ✅ | 137.35 ms | 138.20 ms | 137.96 ms | 557.64 µs | 1.00× | `0` |
| Rust | ✅ | 200.17 ms | 201.55 ms | 201.21 ms | 623.00 µs | 1.46× | `0` |
| Go | ✅ | 192.14 ms | 194.87 ms | 194.53 ms | 1.49 ms | 1.40× | `0` |
| Python | ✅ | 5.257 s | 5.316 s | 5.316 s | 38.36 ms | 38.27× | `0` |

### regex_search — Regex find-all (stdlib regex)

_Category_: `micro` &nbsp;&nbsp;_Args_: `4000`

Run a non-trivial alternation regex (date | email | capitalized word) across REPEATS copies of a sample paragraph. Stresses the standard regex engine.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 48.78 ms | 48.90 ms | 48.90 ms | 113.21 µs | 25.59× | `36000` |
| C++ | ✅ | 78.36 ms | 78.76 ms | 79.41 ms | 1.32 ms | 41.11× | `36000` |
| Rust | ✅ | 1.91 ms | 1.93 ms | 1.93 ms | 18.90 µs | 1.00× | `36000` |
| Go | ✅ | 91.35 ms | 93.48 ms | 92.99 ms | 1.30 ms | 47.92× | `36000` |
| Python | ✅ | 38.94 ms | 38.99 ms | 39.10 ms | 180.99 µs | 20.43× | `36000` |

### math_loop — Math-intensive loop (sin/cos/sqrt/exp)

_Category_: `micro` &nbsp;&nbsp;_Args_: `5000000`

Sum sin(x)*cos(x)+sqrt(x+1)-exp(-x) over N points. Stresses the math standard library and floating-point throughput.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 84.88 ms | 85.18 ms | 85.95 ms | 1.60 ms | 1.02× | `4704337083537` |
| C++ | ✅ | 84.34 ms | 84.95 ms | 84.79 ms | 269.01 µs | 1.02× | `4704337083537` |
| Rust | ✅ | 82.97 ms | 83.12 ms | 83.15 ms | 171.18 µs | 1.00× | `4704337083537` |
| Go | ✅ | 145.93 ms | 145.98 ms | 146.10 ms | 230.27 µs | 1.76× | `4704337083537` |
| Python | ✅ | 946.24 ms | 987.98 ms | 985.01 ms | 24.05 ms | 11.41× | `4704337083537` |

### prime_sieve — Sieve of Eratosthenes

_Category_: `micro` &nbsp;&nbsp;_Args_: `20000000`

Classic Sieve of Eratosthenes up to N on a one-byte-per-cell boolean array, then count primes and sum them mod 2^31. Algorithmically identical across all three languages: same loop bounds, same inner stride, same checksum formula.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 66.51 ms | 66.58 ms | 66.75 ms | 416.42 µs | 1.25× | `1156745585` |
| C++ | ✅ | 53.26 ms | 53.65 ms | 53.81 ms | 430.40 µs | 1.00× | `1156745585` |
| Rust | ✅ | 68.46 ms | 68.58 ms | 68.69 ms | 257.97 µs | 1.29× | `1156745585` |
| Go | ✅ | 58.83 ms | 59.08 ms | 59.26 ms | 435.95 µs | 1.10× | `1156745585` |
| Python | ✅ | 2.864 s | 2.945 s | 2.949 s | 76.77 ms | 53.78× | `1156745585` |

### quicksort — Hand-written quicksort

_Category_: `micro` &nbsp;&nbsp;_Args_: `1500000`

Lomuto-partition quicksort with middle-element pivot and recurse-smaller-side / iterate-larger-side, implemented by hand in all three languages so the algorithm itself is identical (complements the stdlib `sort` benchmark).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 161.74 ms | 163.65 ms | 163.11 ms | 870.26 µs | 1.25× | `612429648` |
| C++ | ✅ | 129.35 ms | 135.15 ms | 134.20 ms | 2.75 ms | 1.00× | `612429648` |
| Rust | ✅ | 129.13 ms | 129.54 ms | 129.53 ms | 439.09 µs | 1.00× | `612429648` |
| Go | ✅ | 134.19 ms | 134.30 ms | 134.98 ms | 1.53 ms | 1.04× | `612429648` |
| Python | ✅ | 3.713 s | 3.726 s | 3.734 s | 18.90 ms | 28.75× | `612429648` |

### mandelbrot — Mandelbrot set (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `600 200`

Compute a Mandelbrot escape-time bitmap of size W*W with up to MAX_ITER iterations. Inspired by the Computer Language Benchmarks Game. Stresses tight numeric loops and floating-point arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 97.53 ms | 97.55 ms | 97.56 ms | 44.60 µs | 1.00× | `29624109` |
| C++ | ✅ | 101.65 ms | 101.67 ms | 101.67 ms | 19.30 µs | 1.04× | `29624109` |
| Rust | ✅ | 107.42 ms | 107.49 ms | 107.49 ms | 47.94 µs | 1.10× | `29624109` |
| Go | ✅ | 101.93 ms | 101.98 ms | 102.01 ms | 87.40 µs | 1.05× | `29624109` |
| Python | ✅ | 3.924 s | 3.952 s | 3.966 s | 39.19 ms | 40.24× | `29624109` |

### nbody — N-Body simulation (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200000`

Symplectic integrator for the classic 5-body solar system from the Benchmarks Game over N steps. Stresses tight floating-point loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 23.46 ms | 23.48 ms | 23.51 ms | 64.30 µs | 2.40× | `-169083713` |
| C++ | ✅ | 14.71 ms | 15.06 ms | 15.00 ms | 160.36 µs | 1.51× | `-169083713` |
| Rust | ✅ | 9.77 ms | 9.80 ms | 9.90 ms | 152.44 µs | 1.00× | `-169083713` |
| Go | ✅ | 17.11 ms | 17.17 ms | 17.18 ms | 64.34 µs | 1.75× | `-169083713` |
| Python | ✅ | 1.199 s | 1.206 s | 1.205 s | 4.85 ms | 122.64× | `-169083713` |

### binary_trees — Binary trees (allocation / GC pressure)

_Category_: `apps` &nbsp;&nbsp;_Args_: `14`

Build and check many small balanced binary trees up to depth D. Adapted from the Computer Language Benchmarks Game. Stresses small-object allocation and GC (or heap allocator).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 49.22 ms | 50.03 ms | 50.01 ms | 692.04 µs | 1.00× | `13250584224` |
| C++ | ✅ | 64.79 ms | 68.51 ms | 67.80 ms | 1.94 ms | 1.32× | `13250584224` |
| Rust | ✅ | 65.52 ms | 65.89 ms | 66.09 ms | 773.93 µs | 1.33× | `13250584224` |
| Go | ✅ | 89.18 ms | 89.47 ms | 89.58 ms | 438.17 µs | 1.81× | `13250584224` |
| Python | ✅ | 841.38 ms | 843.26 ms | 845.06 ms | 4.09 ms | 17.10× | `13250584224` |

### matrix_multiply — Matrix multiplication (naive O(N^3))

_Category_: `apps` &nbsp;&nbsp;_Args_: `250`

Compute C = A * B for two NxN double-precision matrices using the textbook triple-loop algorithm. Stresses memory layout, FP multiply-add throughput, and cache behaviour.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 17.63 ms | 17.70 ms | 17.71 ms | 77.00 µs | 4.73× | `15315135000` |
| C++ | ✅ | 11.42 ms | 11.54 ms | 11.65 ms | 251.38 µs | 3.07× | `15315135000` |
| Rust | ✅ | 3.72 ms | 3.75 ms | 3.92 ms | 364.19 µs | 1.00× | `15315135000` |
| Go | ✅ | 11.64 ms | 11.72 ms | 11.84 ms | 240.53 µs | 3.13× | `15315135000` |
| Python | ✅ | 803.74 ms | 806.46 ms | 808.73 ms | 6.37 ms | 215.87× | `15315135000` |

### word_count — Word count (text processing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1000000`

Tokenize a synthesized N-word text and count word frequencies in a hash-map. Stresses string slicing/comparison, hashing, and hash-map updates — a typical scripting workload.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 178.13 ms | 178.78 ms | 178.73 ms | 555.89 µs | 8.37× | `638309952` |
| C++ | ✅ | 21.29 ms | 21.87 ms | 21.71 ms | 380.03 µs | 1.00× | `638309952` |
| Rust | ✅ | 24.54 ms | 24.65 ms | 27.35 ms | 4.35 ms | 1.15× | `638309952` |
| Go | ✅ | 22.16 ms | 22.62 ms | 22.62 ms | 325.99 µs | 1.04× | `638309952` |
| Python | ✅ | 132.61 ms | 133.68 ms | 133.41 ms | 701.79 µs | 6.23× | `638309952` |

### spectral_norm — Spectral norm (CLBG numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Approximates the largest eigenvalue of an infinite matrix A[i][j] = 1 / ((i+j)(i+j+1)/2 + i + 1) via 10 power iterations of v <- A^T A v. Adapted from the Computer Language Benchmarks Game; algorithmically identical across all three languages.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 147.06 ms | 147.41 ms | 147.45 ms | 394.40 µs | 1.02× | `1274224151` |
| C++ | ✅ | 146.49 ms | 146.67 ms | 146.68 ms | 122.95 µs | 1.02× | `1274224151` |
| Rust | ✅ | 145.87 ms | 146.29 ms | 146.30 ms | 283.80 µs | 1.01× | `1274224151` |
| Go | ✅ | 144.10 ms | 144.57 ms | 144.75 ms | 621.08 µs | 1.00× | `1274224151` |
| Python | ✅ | 16.618 s | 16.712 s | 17.758 s | 2.432 s | 115.32× | `1274224151` |

## Methodology

- Each implementation is invoked as a fresh OS process and measures its own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. This excludes interpreter / runtime startup from the measurement.
- Each implementation also prints `CHECKSUM:<value>` of its computed result; the runner verifies all implementations of the same benchmark agree, otherwise the comparison is flagged as invalid.
- Per benchmark we run `warmup` unmeasured iterations, then `iterations` measured iterations and report **min / median / mean / stddev**. The _min_ is used for the headline ratio because it is the most robust estimate of best-case wall-clock cost when other system noise is present.
- Compiler flags: `g++ -O2 -std=c++17` for C++, `rustc -O --edition=2021` (release-equivalent `opt-level=3`) for Rust, `go build` (default release optimization) for Go, `cjpm build` for Cangjie (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`), CPython 3 for Python (no `-O`), all with no extra runtime tuning.
