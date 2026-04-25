# CangjiePerf Benchmark Report

_Generated: 2026-04-25T12:29:10+00:00_

## Environment

- **OS**: Linux 6.17.0-1010-azure
- **Architecture**: x86_64
- **CPU**: AMD EPYC 9V74 80-Core Processor
- **Python**: 3.12.3

## Toolchains

| Language | Available | Version |
|----------|-----------|---------|
| Cangjie | ✅ | Cangjie Compiler: 1.0.5 (cjnative) |
| C++ | ✅ | g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0 |
| Python | ✅ | Python 3.12.3 |

## Run Configuration

- Warmup runs: **1**
- Measurement runs: **3**
- Languages enabled: **Cangjie, Python, C++**
- Reported metric: per-process self-timed wall-clock (`ELAPSED_MS`); **`min`** chosen as the headline number, lower is better.

## Summary

| Benchmark | Category | Cangjie | C++ | Python | Fastest |
|---|---|---|---|---|---|
| **fibonacci** | micro | 25.54 ms | 3.74 ms | 290.13 ms | C++ |
| **sort** ⚠️ | **micro** | **2.277 s** | **146.86 ms** | **821.31 ms** | **C++** |
| **hashmap_ops** ⚠️ | **micro** | **469.78 ms** | **115.22 ms** | **122.79 ms** | **C++** |
| **string_concat** ⚠️ | **micro** | **46.58 ms** | **27.61 ms** | **76.30 ms** | **C++** |
| **closure_sum** ⚠️ | **micro** | **96.86 ms** | **9.57 ms** | **343.53 ms** | **C++** |
| **enum_eval** | micro | 601.60 ms | 137.33 ms | 5.236 s | C++ |
| **regex_search** ⚠️ | **micro** | **44.89 ms** | **77.49 ms** | **39.07 ms** | **Python** |
| **math_loop** | micro | 142.26 ms | 84.82 ms | 982.51 ms | C++ |
| **prime_sieve** ⚠️ | **micro** | **1.563 s** | **54.25 ms** | **3.123 s** | **C++** |
| **quicksort** ⚠️ | **micro** | **2.382 s** | **134.92 ms** | **3.802 s** | **C++** |
| **mandelbrot** | apps | 282.85 ms | 101.47 ms | 3.873 s | C++ |
| **nbody** | apps | 71.86 ms | 14.77 ms | 1.206 s | C++ |
| **binary_trees** | apps | 126.01 ms | 63.81 ms | 840.50 ms | C++ |
| **matrix_multiply** ⚠️ | **apps** | **897.94 ms** | **11.44 ms** | **803.21 ms** | **C++** |
| **word_count** ⚠️ | **apps** | **672.91 ms** | **21.31 ms** | **132.77 ms** | **C++** |
| **spectral_norm** ⚠️ | **apps** | **2.219 s** | **146.14 ms** | **16.947 s** | **C++** |

> **Bold rows** marked with ⚠️ are benchmarks where Cangjie's timing is closer (in log scale) to Python's than to C++'s — i.e. cases where the Cangjie implementation is significantly under-performing the native baseline. See [`analyse.md`](./analyse.md) for the root-cause analysis.

### Visual comparison

Each benchmark shows three side-by-side bars (Cangjie / C++ / Python). **Lower bars are faster.** Note the **logarithmic** y-axis: a one-step gridline difference is a 10× speed difference. Open the SVG in a new tab to see exact per-bar tooltips.

![Benchmark wall-clock comparison (log scale, lower is better)](./report_chart.svg)

## Per-benchmark Detail

### fibonacci — Recursive Fibonacci (function call / recursion)

_Category_: `micro` &nbsp;&nbsp;_Args_: `32`

Pure recursive fib(N). Stresses function-call overhead and integer arithmetic. No standard-library involvement beyond integers.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 25.54 ms | 25.59 ms | 25.58 ms | 32.22 µs | 6.83× | `2178309` |
| C++ | ✅ | 3.74 ms | 3.75 ms | 3.75 ms | 9.91 µs | 1.00× | `2178309` |
| Python | ✅ | 290.13 ms | 295.59 ms | 295.00 ms | 4.61 ms | 77.58× | `2178309` |

### sort — Sort 2M integers (stdlib sort)

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Generate 2,000,000 deterministic pseudo-random Int64 values then sort ascending using the language's standard sort. Stresses standard library sorting and dynamic arrays.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.277 s | 2.310 s | 2.300 s | 20.04 ms | 15.50× | `1074570229` |
| C++ | ✅ | 146.86 ms | 146.99 ms | 146.98 ms | 107.09 µs | 1.00× | `1074570229` |
| Python | ✅ | 821.31 ms | 822.85 ms | 824.34 ms | 3.99 ms | 5.59× | `1074570229` |

### hashmap_ops — HashMap insert + lookup (stdlib hash table)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N (string,int) pairs then look up the same N keys. Stresses hash maps, string hashing, and string allocation.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 469.78 ms | 471.47 ms | 472.34 ms | 3.08 ms | 4.08× | `0` |
| C++ | ✅ | 115.22 ms | 118.46 ms | 117.74 ms | 2.24 ms | 1.00× | `0` |
| Python | ✅ | 122.79 ms | 123.57 ms | 127.65 ms | 7.75 ms | 1.07× | `0` |

### string_concat — String building (stdlib StringBuilder)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Build a single large string from N small fragments using the recommended efficient builder for each language. Stresses string buffers and memory growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 46.58 ms | 46.74 ms | 46.79 ms | 236.57 µs | 1.69× | `5388890` |
| C++ | ✅ | 27.61 ms | 28.08 ms | 27.94 ms | 285.10 µs | 1.00× | `5388890` |
| Python | ✅ | 76.30 ms | 78.04 ms | 77.49 ms | 1.03 ms | 2.76× | `5388890` |

### closure_sum — Closure / higher-order pipeline

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Apply a map -> filter -> reduce pipeline of closures over N integers. Stresses higher-order function dispatch, closure allocation, and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 96.86 ms | 98.00 ms | 97.82 ms | 877.03 µs | 10.12× | `1777776444435777780` |
| C++ | ✅ | 9.57 ms | 9.64 ms | 10.00 ms | 692.38 µs | 1.00× | `1777776444435777780` |
| Python | ✅ | 343.53 ms | 345.86 ms | 345.21 ms | 1.46 ms | 35.91× | `1777776444435777780` |

### enum_eval — Enum / pattern matching (AST evaluation)

_Category_: `micro` &nbsp;&nbsp;_Args_: `18 60`

Build a recursive arithmetic expression tree of depth D and evaluate it N times via recursive pattern matching on a sum-type enum (Num | Add | Sub | Mul). Stresses algebraic data types, recursive calls, and tag dispatch.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 601.60 ms | 611.64 ms | 608.83 ms | 6.32 ms | 4.38× | `0` |
| C++ | ✅ | 137.33 ms | 138.16 ms | 137.91 ms | 508.96 µs | 1.00× | `0` |
| Python | ✅ | 5.236 s | 5.296 s | 5.359 s | 164.38 ms | 38.13× | `0` |

### regex_search — Regex find-all (stdlib regex)

_Category_: `micro` &nbsp;&nbsp;_Args_: `4000`

Run a non-trivial alternation regex (date | email | capitalized word) across REPEATS copies of a sample paragraph. Stresses the standard regex engine.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 44.89 ms | 44.95 ms | 44.96 ms | 70.21 µs | 1.15× | `36000` |
| C++ | ✅ | 77.49 ms | 78.53 ms | 78.28 ms | 697.61 µs | 1.98× | `36000` |
| Python | ✅ | 39.07 ms | 39.34 ms | 39.27 ms | 166.98 µs | 1.00× | `36000` |

### math_loop — Math-intensive loop (sin/cos/sqrt/exp)

_Category_: `micro` &nbsp;&nbsp;_Args_: `5000000`

Sum sin(x)*cos(x)+sqrt(x+1)-exp(-x) over N points. Stresses the math standard library and floating-point throughput.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 142.26 ms | 142.30 ms | 142.39 ms | 196.74 µs | 1.68× | `4704337083537` |
| C++ | ✅ | 84.82 ms | 84.93 ms | 84.90 ms | 72.66 µs | 1.00× | `4704337083537` |
| Python | ✅ | 982.51 ms | 984.06 ms | 986.95 ms | 6.38 ms | 11.58× | `4704337083537` |

### prime_sieve — Sieve of Eratosthenes

_Category_: `micro` &nbsp;&nbsp;_Args_: `20000000`

Classic Sieve of Eratosthenes up to N on a one-byte-per-cell boolean array, then count primes and sum them mod 2^31. Algorithmically identical across all three languages: same loop bounds, same inner stride, same checksum formula.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 1.563 s | 1.625 s | 1.609 s | 40.93 ms | 28.80× | `1156745585` |
| C++ | ✅ | 54.25 ms | 54.47 ms | 54.40 ms | 126.88 µs | 1.00× | `1156745585` |
| Python | ✅ | 3.123 s | 3.183 s | 3.446 s | 508.96 ms | 57.56× | `1156745585` |

### quicksort — Hand-written quicksort

_Category_: `micro` &nbsp;&nbsp;_Args_: `1500000`

Lomuto-partition quicksort with middle-element pivot and recurse-smaller-side / iterate-larger-side, implemented by hand in all three languages so the algorithm itself is identical (complements the stdlib `sort` benchmark).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.382 s | 2.393 s | 2.402 s | 25.49 ms | 17.66× | `612429648` |
| C++ | ✅ | 134.92 ms | 135.18 ms | 135.11 ms | 164.50 µs | 1.00× | `612429648` |
| Python | ✅ | 3.802 s | 3.893 s | 3.876 s | 67.28 ms | 28.18× | `612429648` |

### mandelbrot — Mandelbrot set (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `600 200`

Compute a Mandelbrot escape-time bitmap of size W*W with up to MAX_ITER iterations. Inspired by the Computer Language Benchmarks Game. Stresses tight numeric loops and floating-point arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 282.85 ms | 282.88 ms | 283.01 ms | 255.96 µs | 2.79× | `29624109` |
| C++ | ✅ | 101.47 ms | 101.53 ms | 101.56 ms | 105.11 µs | 1.00× | `29624109` |
| Python | ✅ | 3.873 s | 3.894 s | 3.897 s | 25.53 ms | 38.16× | `29624109` |

### nbody — N-Body simulation (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200000`

Symplectic integrator for the classic 5-body solar system from the Benchmarks Game over N steps. Stresses tight floating-point loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 71.86 ms | 71.96 ms | 71.96 ms | 91.34 µs | 4.86× | `-169083713` |
| C++ | ✅ | 14.77 ms | 14.78 ms | 14.79 ms | 17.39 µs | 1.00× | `-169083713` |
| Python | ✅ | 1.206 s | 1.215 s | 1.244 s | 58.59 ms | 81.61× | `-169083713` |

### binary_trees — Binary trees (allocation / GC pressure)

_Category_: `apps` &nbsp;&nbsp;_Args_: `14`

Build and check many small balanced binary trees up to depth D. Adapted from the Computer Language Benchmarks Game. Stresses small-object allocation and GC (or heap allocator).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 126.01 ms | 126.06 ms | 126.53 ms | 859.56 µs | 1.97× | `13250584224` |
| C++ | ✅ | 63.81 ms | 69.07 ms | 67.82 ms | 3.55 ms | 1.00× | `13250584224` |
| Python | ✅ | 840.50 ms | 842.58 ms | 842.22 ms | 1.57 ms | 13.17× | `13250584224` |

### matrix_multiply — Matrix multiplication (naive O(N^3))

_Category_: `apps` &nbsp;&nbsp;_Args_: `250`

Compute C = A * B for two NxN double-precision matrices using the textbook triple-loop algorithm. Stresses memory layout, FP multiply-add throughput, and cache behaviour.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 897.94 ms | 944.20 ms | 930.82 ms | 28.64 ms | 78.50× | `15315135000` |
| C++ | ✅ | 11.44 ms | 11.47 ms | 11.47 ms | 33.29 µs | 1.00× | `15315135000` |
| Python | ✅ | 803.21 ms | 809.64 ms | 809.07 ms | 5.59 ms | 70.21× | `15315135000` |

### word_count — Word count (text processing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1000000`

Tokenize a synthesized N-word text and count word frequencies in a hash-map. Stresses string slicing/comparison, hashing, and hash-map updates — a typical scripting workload.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 672.91 ms | 684.18 ms | 682.23 ms | 8.51 ms | 31.58× | `638309952` |
| C++ | ✅ | 21.31 ms | 21.33 ms | 21.76 ms | 757.84 µs | 1.00× | `638309952` |
| Python | ✅ | 132.77 ms | 133.03 ms | 133.16 ms | 481.40 µs | 6.23× | `638309952` |

### spectral_norm — Spectral norm (CLBG numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Approximates the largest eigenvalue of an infinite matrix A[i][j] = 1 / ((i+j)(i+j+1)/2 + i + 1) via 10 power iterations of v <- A^T A v. Adapted from the Computer Language Benchmarks Game; algorithmically identical across all three languages.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.219 s | 2.222 s | 2.222 s | 2.85 ms | 15.18× | `1274224151` |
| C++ | ✅ | 146.14 ms | 146.36 ms | 146.44 ms | 343.34 µs | 1.00× | `1274224151` |
| Python | ✅ | 16.947 s | 17.089 s | 17.054 s | 94.37 ms | 115.97× | `1274224151` |

## Methodology

- Each implementation is invoked as a fresh OS process and measures its own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. This excludes interpreter / runtime startup from the measurement.
- Each implementation also prints `CHECKSUM:<value>` of its computed result; the runner verifies all implementations of the same benchmark agree, otherwise the comparison is flagged as invalid.
- Per benchmark we run `warmup` unmeasured iterations, then `iterations` measured iterations and report **min / median / mean / stddev**. The _min_ is used for the headline ratio because it is the most robust estimate of best-case wall-clock cost when other system noise is present.
- Compiler flags: `g++ -O2 -std=c++17` for C++, `cjpm build` for Cangjie (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`), CPython 3 for Python (no `-O`), all with no extra runtime tuning.
