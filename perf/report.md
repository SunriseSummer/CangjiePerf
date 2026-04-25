# CangjiePerf Benchmark Report

_Generated: 2026-04-25T15:09:14+00:00_

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
| **fibonacci** | micro | 23.63 ms | 3.90 ms | 6.64 ms | 11.47 ms | 309.29 ms | C++ |
| **sort** ⚠️ | **micro** | **2.158 s** | **133.76 ms** | **55.96 ms** | **298.31 ms** | **801.96 ms** | **Rust** |
| **hashmap_ops** ⚠️ | **micro** | **492.91 ms** | **109.44 ms** | **131.37 ms** | **64.23 ms** | **120.75 ms** | **Go** |
| **string_concat** | micro | 47.31 ms | 32.26 ms | 12.47 ms | 15.76 ms | 71.24 ms | Rust |
| **closure_sum** ⚠️ | **micro** | **101.57 ms** | **9.17 ms** | **1.52 ms** | **2.90 ms** | **357.59 ms** | **Rust** |
| **enum_eval** | micro | 531.60 ms | 130.29 ms | 198.80 ms | 174.37 ms | 5.140 s | C++ |
| **regex_search** ⚠️ | **micro** | **45.81 ms** | **78.07 ms** | **2.02 ms** | **101.69 ms** | **41.94 ms** | **Rust** |
| **math_loop** | micro | 140.81 ms | 86.69 ms | 84.63 ms | 144.37 ms | 916.48 ms | Rust |
| **prime_sieve** ⚠️ | **micro** | **1.579 s** | **55.06 ms** | **66.69 ms** | **57.88 ms** | **2.817 s** | **C++** |
| **quicksort** ⚠️ | **micro** | **2.216 s** | **111.67 ms** | **115.89 ms** | **120.85 ms** | **3.929 s** | **C++** |
| **mandelbrot** | apps | 251.79 ms | 90.73 ms | 91.72 ms | 91.09 ms | 3.448 s | C++ |
| **nbody** | apps | 78.86 ms | 14.01 ms | 9.20 ms | 14.98 ms | 1.159 s | Rust |
| **binary_trees** | apps | 113.74 ms | 67.41 ms | 65.45 ms | 93.30 ms | 840.32 ms | Rust |
| **matrix_multiply** ⚠️ | **apps** | **885.98 ms** | **10.17 ms** | **3.72 ms** | **11.33 ms** | **724.56 ms** | **Rust** |
| **word_count** ⚠️ | **apps** | **724.74 ms** | **27.35 ms** | **26.07 ms** | **25.24 ms** | **135.59 ms** | **Go** |
| **spectral_norm** ⚠️ | **apps** | **2.241 s** | **128.68 ms** | **129.36 ms** | **129.58 ms** | **15.385 s** | **C++** |

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
| Cangjie | ✅ | 23.63 ms | 23.80 ms | 23.76 ms | 76.80 µs | 6.05× | `2178309` |
| C++ | ✅ | 3.90 ms | 4.01 ms | 3.98 ms | 51.98 µs | 1.00× | `2178309` |
| Rust | ✅ | 6.64 ms | 6.65 ms | 6.80 ms | 322.34 µs | 1.70× | `2178309` |
| Go | ✅ | 11.47 ms | 12.12 ms | 11.92 ms | 340.21 µs | 2.94× | `2178309` |
| Python | ✅ | 309.29 ms | 314.85 ms | 315.88 ms | 4.82 ms | 79.23× | `2178309` |

### sort — Sort 2M integers (stdlib sort)

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Generate 2,000,000 deterministic pseudo-random Int64 values then sort ascending using the language's standard sort. Stresses standard library sorting and dynamic arrays.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.158 s | 2.211 s | 2.205 s | 29.77 ms | 38.57× | `1074570229` |
| C++ | ✅ | 133.76 ms | 134.08 ms | 135.67 ms | 3.85 ms | 2.39× | `1074570229` |
| Rust | ✅ | 55.96 ms | 56.30 ms | 56.20 ms | 207.02 µs | 1.00× | `1074570229` |
| Go | ✅ | 298.31 ms | 298.47 ms | 298.48 ms | 207.30 µs | 5.33× | `1074570229` |
| Python | ✅ | 801.96 ms | 811.55 ms | 809.84 ms | 5.25 ms | 14.33× | `1074570229` |

### hashmap_ops — HashMap insert + lookup (stdlib hash table)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N (string,int) pairs then look up the same N keys. Stresses hash maps, string hashing, and string allocation.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 492.91 ms | 500.86 ms | 501.99 ms | 7.58 ms | 7.67× | `0` |
| C++ | ✅ | 109.44 ms | 114.55 ms | 114.01 ms | 3.73 ms | 1.70× | `0` |
| Rust | ✅ | 131.37 ms | 136.40 ms | 136.53 ms | 4.31 ms | 2.05× | `0` |
| Go | ✅ | 64.23 ms | 66.36 ms | 67.45 ms | 3.21 ms | 1.00× | `0` |
| Python | ✅ | 120.75 ms | 123.08 ms | 123.72 ms | 2.35 ms | 1.88× | `0` |

### string_concat — String building (stdlib StringBuilder)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Build a single large string from N small fragments using the recommended efficient builder for each language. Stresses string buffers and memory growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 47.31 ms | 47.70 ms | 47.81 ms | 444.71 µs | 3.79× | `5388890` |
| C++ | ✅ | 32.26 ms | 33.13 ms | 32.98 ms | 419.35 µs | 2.59× | `5388890` |
| Rust | ✅ | 12.47 ms | 12.54 ms | 12.55 ms | 55.31 µs | 1.00× | `5388890` |
| Go | ✅ | 15.76 ms | 16.11 ms | 16.26 ms | 535.31 µs | 1.26× | `5388890` |
| Python | ✅ | 71.24 ms | 71.92 ms | 71.73 ms | 316.77 µs | 5.71× | `5388890` |

### closure_sum — Closure / higher-order pipeline

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Apply a map -> filter -> reduce pipeline of closures over N integers. Stresses higher-order function dispatch, closure allocation, and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 101.57 ms | 102.35 ms | 102.45 ms | 804.20 µs | 66.75× | `1777776444435777780` |
| C++ | ✅ | 9.17 ms | 9.21 ms | 9.29 ms | 156.05 µs | 6.03× | `1777776444435777780` |
| Rust | ✅ | 1.52 ms | 1.56 ms | 1.55 ms | 26.34 µs | 1.00× | `1777776444435777780` |
| Go | ✅ | 2.90 ms | 2.93 ms | 2.98 ms | 125.82 µs | 1.91× | `1777776444435777780` |
| Python | ✅ | 357.59 ms | 360.91 ms | 362.10 ms | 4.90 ms | 235.00× | `1777776444435777780` |

### enum_eval — Enum / pattern matching (AST evaluation)

_Category_: `micro` &nbsp;&nbsp;_Args_: `18 60`

Build a recursive arithmetic expression tree of depth D and evaluate it N times via recursive pattern matching on a sum-type enum (Num | Add | Sub | Mul). Stresses algebraic data types, recursive calls, and tag dispatch.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 531.60 ms | 555.61 ms | 554.45 ms | 19.23 ms | 4.08× | `0` |
| C++ | ✅ | 130.29 ms | 130.92 ms | 130.94 ms | 419.20 µs | 1.00× | `0` |
| Rust | ✅ | 198.80 ms | 201.48 ms | 201.73 ms | 2.85 ms | 1.53× | `0` |
| Go | ✅ | 174.37 ms | 175.75 ms | 177.22 ms | 3.07 ms | 1.34× | `0` |
| Python | ✅ | 5.140 s | 5.167 s | 5.178 s | 35.23 ms | 39.45× | `0` |

### regex_search — Regex find-all (stdlib regex)

_Category_: `micro` &nbsp;&nbsp;_Args_: `4000`

Run a non-trivial alternation regex (date | email | capitalized word) across REPEATS copies of a sample paragraph. Stresses the standard regex engine.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 45.81 ms | 45.89 ms | 45.95 ms | 129.25 µs | 22.72× | `36000` |
| C++ | ✅ | 78.07 ms | 78.24 ms | 78.32 ms | 305.99 µs | 38.72× | `36000` |
| Rust | ✅ | 2.02 ms | 2.06 ms | 2.10 ms | 93.63 µs | 1.00× | `36000` |
| Go | ✅ | 101.69 ms | 103.33 ms | 103.27 ms | 1.39 ms | 50.44× | `36000` |
| Python | ✅ | 41.94 ms | 42.36 ms | 42.81 ms | 1.30 ms | 20.80× | `36000` |

### math_loop — Math-intensive loop (sin/cos/sqrt/exp)

_Category_: `micro` &nbsp;&nbsp;_Args_: `5000000`

Sum sin(x)*cos(x)+sqrt(x+1)-exp(-x) over N points. Stresses the math standard library and floating-point throughput.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 140.81 ms | 141.06 ms | 144.58 ms | 8.06 ms | 1.66× | `4704337083537` |
| C++ | ✅ | 86.69 ms | 86.95 ms | 87.22 ms | 597.47 µs | 1.02× | `4704337083537` |
| Rust | ✅ | 84.63 ms | 85.19 ms | 85.09 ms | 266.91 µs | 1.00× | `4704337083537` |
| Go | ✅ | 144.37 ms | 144.89 ms | 144.89 ms | 419.80 µs | 1.71× | `4704337083537` |
| Python | ✅ | 916.48 ms | 921.73 ms | 921.12 ms | 4.78 ms | 10.83× | `4704337083537` |

### prime_sieve — Sieve of Eratosthenes

_Category_: `micro` &nbsp;&nbsp;_Args_: `20000000`

Classic Sieve of Eratosthenes up to N on a one-byte-per-cell boolean array, then count primes and sum them mod 2^31. Algorithmically identical across all three languages: same loop bounds, same inner stride, same checksum formula.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 1.579 s | 1.596 s | 1.595 s | 12.08 ms | 28.68× | `1156745585` |
| C++ | ✅ | 55.06 ms | 55.64 ms | 56.00 ms | 993.16 µs | 1.00× | `1156745585` |
| Rust | ✅ | 66.69 ms | 66.95 ms | 67.05 ms | 329.30 µs | 1.21× | `1156745585` |
| Go | ✅ | 57.88 ms | 58.24 ms | 58.43 ms | 700.16 µs | 1.05× | `1156745585` |
| Python | ✅ | 2.817 s | 2.826 s | 2.835 s | 18.24 ms | 51.17× | `1156745585` |

### quicksort — Hand-written quicksort

_Category_: `micro` &nbsp;&nbsp;_Args_: `1500000`

Lomuto-partition quicksort with middle-element pivot and recurse-smaller-side / iterate-larger-side, implemented by hand in all three languages so the algorithm itself is identical (complements the stdlib `sort` benchmark).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.216 s | 2.303 s | 2.297 s | 52.65 ms | 19.84× | `612429648` |
| C++ | ✅ | 111.67 ms | 111.86 ms | 111.96 ms | 349.51 µs | 1.00× | `612429648` |
| Rust | ✅ | 115.89 ms | 116.19 ms | 116.18 ms | 208.57 µs | 1.04× | `612429648` |
| Go | ✅ | 120.85 ms | 121.09 ms | 121.13 ms | 191.40 µs | 1.08× | `612429648` |
| Python | ✅ | 3.929 s | 3.952 s | 3.968 s | 57.18 ms | 35.18× | `612429648` |

### mandelbrot — Mandelbrot set (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `600 200`

Compute a Mandelbrot escape-time bitmap of size W*W with up to MAX_ITER iterations. Inspired by the Computer Language Benchmarks Game. Stresses tight numeric loops and floating-point arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 251.79 ms | 251.83 ms | 251.86 ms | 83.38 µs | 2.78× | `29624109` |
| C++ | ✅ | 90.73 ms | 90.95 ms | 90.95 ms | 145.32 µs | 1.00× | `29624109` |
| Rust | ✅ | 91.72 ms | 91.77 ms | 91.80 ms | 78.80 µs | 1.01× | `29624109` |
| Go | ✅ | 91.09 ms | 91.34 ms | 91.35 ms | 184.20 µs | 1.00× | `29624109` |
| Python | ✅ | 3.448 s | 3.488 s | 3.487 s | 35.67 ms | 38.00× | `29624109` |

### nbody — N-Body simulation (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200000`

Symplectic integrator for the classic 5-body solar system from the Benchmarks Game over N steps. Stresses tight floating-point loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 78.86 ms | 79.13 ms | 79.84 ms | 1.76 ms | 8.57× | `-169083713` |
| C++ | ✅ | 14.01 ms | 14.41 ms | 14.33 ms | 183.88 µs | 1.52× | `-169083713` |
| Rust | ✅ | 9.20 ms | 9.24 ms | 9.36 ms | 196.24 µs | 1.00× | `-169083713` |
| Go | ✅ | 14.98 ms | 15.54 ms | 15.40 ms | 246.96 µs | 1.63× | `-169083713` |
| Python | ✅ | 1.159 s | 1.172 s | 1.174 s | 12.47 ms | 126.01× | `-169083713` |

### binary_trees — Binary trees (allocation / GC pressure)

_Category_: `apps` &nbsp;&nbsp;_Args_: `14`

Build and check many small balanced binary trees up to depth D. Adapted from the Computer Language Benchmarks Game. Stresses small-object allocation and GC (or heap allocator).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 113.74 ms | 114.50 ms | 115.86 ms | 2.57 ms | 1.74× | `13250584224` |
| C++ | ✅ | 67.41 ms | 67.60 ms | 67.81 ms | 394.80 µs | 1.03× | `13250584224` |
| Rust | ✅ | 65.45 ms | 65.66 ms | 65.65 ms | 188.46 µs | 1.00× | `13250584224` |
| Go | ✅ | 93.30 ms | 94.30 ms | 94.22 ms | 862.99 µs | 1.43× | `13250584224` |
| Python | ✅ | 840.32 ms | 852.96 ms | 853.08 ms | 10.73 ms | 12.84× | `13250584224` |

### matrix_multiply — Matrix multiplication (naive O(N^3))

_Category_: `apps` &nbsp;&nbsp;_Args_: `250`

Compute C = A * B for two NxN double-precision matrices using the textbook triple-loop algorithm. Stresses memory layout, FP multiply-add throughput, and cache behaviour.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 885.98 ms | 889.37 ms | 894.35 ms | 8.79 ms | 238.28× | `15315135000` |
| C++ | ✅ | 10.17 ms | 10.37 ms | 10.53 ms | 402.47 µs | 2.74× | `15315135000` |
| Rust | ✅ | 3.72 ms | 3.90 ms | 3.94 ms | 294.31 µs | 1.00× | `15315135000` |
| Go | ✅ | 11.33 ms | 11.40 ms | 11.39 ms | 40.33 µs | 3.05× | `15315135000` |
| Python | ✅ | 724.56 ms | 728.82 ms | 732.04 ms | 11.34 ms | 194.86× | `15315135000` |

### word_count — Word count (text processing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1000000`

Tokenize a synthesized N-word text and count word frequencies in a hash-map. Stresses string slicing/comparison, hashing, and hash-map updates — a typical scripting workload.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 724.74 ms | 741.84 ms | 741.79 ms | 12.89 ms | 28.72× | `638309952` |
| C++ | ✅ | 27.35 ms | 27.65 ms | 28.00 ms | 914.56 µs | 1.08× | `638309952` |
| Rust | ✅ | 26.07 ms | 26.22 ms | 26.20 ms | 88.26 µs | 1.03× | `638309952` |
| Go | ✅ | 25.24 ms | 25.37 ms | 26.09 ms | 1.07 ms | 1.00× | `638309952` |
| Python | ✅ | 135.59 ms | 136.47 ms | 136.31 ms | 514.35 µs | 5.37× | `638309952` |

### spectral_norm — Spectral norm (CLBG numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Approximates the largest eigenvalue of an infinite matrix A[i][j] = 1 / ((i+j)(i+j+1)/2 + i + 1) via 10 power iterations of v <- A^T A v. Adapted from the Computer Language Benchmarks Game; algorithmically identical across all three languages.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.241 s | 2.253 s | 2.260 s | 20.31 ms | 17.41× | `1274224151` |
| C++ | ✅ | 128.68 ms | 128.96 ms | 129.00 ms | 339.85 µs | 1.00× | `1274224151` |
| Rust | ✅ | 129.36 ms | 129.74 ms | 129.78 ms | 367.20 µs | 1.01× | `1274224151` |
| Go | ✅ | 129.58 ms | 129.87 ms | 129.84 ms | 185.08 µs | 1.01× | `1274224151` |
| Python | ✅ | 15.385 s | 15.565 s | 15.557 s | 114.01 ms | 119.56× | `1274224151` |

## Methodology

- Each implementation is invoked as a fresh OS process and measures its own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. This excludes interpreter / runtime startup from the measurement.
- Each implementation also prints `CHECKSUM:<value>` of its computed result; the runner verifies all implementations of the same benchmark agree, otherwise the comparison is flagged as invalid.
- Per benchmark we run `warmup` unmeasured iterations, then `iterations` measured iterations and report **min / median / mean / stddev**. The _min_ is used for the headline ratio because it is the most robust estimate of best-case wall-clock cost when other system noise is present.
- Compiler flags: `g++ -O2 -std=c++17` for C++, `rustc -O --edition=2021` (release-equivalent ``opt-level=3``) for Rust, `go build` (default release optimisation) for Go, `cjpm build` for Cangjie (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`), CPython 3 for Python (no `-O`), all with no extra runtime tuning.
