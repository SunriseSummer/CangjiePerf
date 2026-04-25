# CangjiePerf Benchmark Report

_Generated: 2026-04-25T11:44:37+00:00_

## Environment

- **OS**: Linux 6.17.0-1010-azure
- **Architecture**: x86_64
- **CPU**: AMD EPYC 7763 64-Core Processor
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
| **fibonacci** | micro | 23.93 ms | 3.91 ms | 309.01 ms | C++ |
| **sort** | micro | 2.180 s | 133.72 ms | 803.19 ms | C++ |
| **hashmap_ops** | micro | 505.39 ms | 119.86 ms | 131.11 ms | C++ |
| **string_concat** | micro | 46.79 ms | 32.38 ms | 71.39 ms | C++ |
| **closure_sum** | micro | 102.14 ms | 9.60 ms | 356.19 ms | C++ |
| **enum_eval** | micro | 643.99 ms | 134.24 ms | 5.096 s | C++ |
| **regex_search** | micro | 45.30 ms | 78.02 ms | 41.86 ms | Python |
| **math_loop** | micro | 140.84 ms | 86.30 ms | 955.17 ms | C++ |
| **mandelbrot** | apps | 251.98 ms | 90.67 ms | 3.508 s | C++ |
| **nbody** | apps | 79.73 ms | 14.44 ms | 1.167 s | C++ |
| **binary_trees** | apps | 117.89 ms | 60.62 ms | 845.33 ms | C++ |
| **matrix_multiply** | apps | 883.33 ms | 10.91 ms | 726.79 ms | C++ |
| **word_count** | apps | 745.25 ms | 27.27 ms | 136.33 ms | C++ |

## Per-benchmark Detail

### fibonacci — Recursive Fibonacci (function call / recursion)

_Category_: `micro` &nbsp;&nbsp;_Args_: `32`

Pure recursive fib(N). Stresses function-call overhead and integer arithmetic. No standard-library involvement beyond integers.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 23.93 ms | 23.95 ms | 24.10 ms | 287.05 µs | 6.11× | `2178309` |
| C++ | ✅ | 3.91 ms | 3.93 ms | 3.95 ms | 49.43 µs | 1.00× | `2178309` |
| Python | ✅ | 309.01 ms | 311.18 ms | 310.63 ms | 1.43 ms | 78.93× | `2178309` |

### sort — Sort 2M integers (stdlib sort)

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Generate 2,000,000 deterministic pseudo-random Int64 values then sort ascending using the language's standard sort. Stresses standard library sorting and dynamic arrays.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.180 s | 2.197 s | 2.193 s | 11.29 ms | 16.31× | `1074570229` |
| C++ | ✅ | 133.72 ms | 133.82 ms | 133.82 ms | 105.31 µs | 1.00× | `1074570229` |
| Python | ✅ | 803.19 ms | 816.58 ms | 815.28 ms | 11.50 ms | 6.01× | `1074570229` |

### hashmap_ops — HashMap insert + lookup (stdlib hash table)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N (string,int) pairs then look up the same N keys. Stresses hash maps, string hashing, and string allocation.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 505.39 ms | 512.58 ms | 512.49 ms | 7.06 ms | 4.22× | `0` |
| C++ | ✅ | 119.86 ms | 120.33 ms | 123.59 ms | 6.06 ms | 1.00× | `0` |
| Python | ✅ | 131.11 ms | 140.63 ms | 139.46 ms | 7.84 ms | 1.09× | `0` |

### string_concat — String building (stdlib StringBuilder)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Build a single large string from N small fragments using the recommended efficient builder for each language. Stresses string buffers and memory growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 46.79 ms | 46.92 ms | 46.97 ms | 210.07 µs | 1.44× | `5388890` |
| C++ | ✅ | 32.38 ms | 33.01 ms | 32.96 ms | 557.58 µs | 1.00× | `5388890` |
| Python | ✅ | 71.39 ms | 71.52 ms | 71.52 ms | 126.44 µs | 2.20× | `5388890` |

### closure_sum — Closure / higher-order pipeline

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Apply a map -> filter -> reduce pipeline of closures over N integers. Stresses higher-order function dispatch, closure allocation, and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 102.14 ms | 135.55 ms | 125.13 ms | 19.94 ms | 10.64× | `1777776444435777780` |
| C++ | ✅ | 9.60 ms | 9.61 ms | 9.61 ms | 7.68 µs | 1.00× | `1777776444435777780` |
| Python | ✅ | 356.19 ms | 368.67 ms | 365.56 ms | 8.26 ms | 37.09× | `1777776444435777780` |

### enum_eval — Enum / pattern matching (AST evaluation)

_Category_: `micro` &nbsp;&nbsp;_Args_: `18 60`

Build a recursive arithmetic expression tree of depth D and evaluate it N times via recursive pattern matching on a sum-type enum (Num | Add | Sub | Mul). Stresses algebraic data types, recursive calls, and tag dispatch.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 643.99 ms | 644.35 ms | 649.75 ms | 9.67 ms | 4.80× | `0` |
| C++ | ✅ | 134.24 ms | 134.52 ms | 134.96 ms | 1.01 ms | 1.00× | `0` |
| Python | ✅ | 5.096 s | 5.110 s | 5.121 s | 31.87 ms | 37.96× | `0` |

### regex_search — Regex find-all (stdlib regex)

_Category_: `micro` &nbsp;&nbsp;_Args_: `4000`

Run a non-trivial alternation regex (date | email | capitalized word) across REPEATS copies of a sample paragraph. Stresses the standard regex engine.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 45.30 ms | 45.69 ms | 45.65 ms | 327.36 µs | 1.08× | `36000` |
| C++ | ✅ | 78.02 ms | 78.27 ms | 78.40 ms | 460.12 µs | 1.86× | `36000` |
| Python | ✅ | 41.86 ms | 42.01 ms | 42.09 ms | 262.66 µs | 1.00× | `36000` |

### math_loop — Math-intensive loop (sin/cos/sqrt/exp)

_Category_: `micro` &nbsp;&nbsp;_Args_: `5000000`

Sum sin(x)*cos(x)+sqrt(x+1)-exp(-x) over N points. Stresses the math standard library and floating-point throughput.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 140.84 ms | 141.17 ms | 141.12 ms | 259.59 µs | 1.63× | `4704337083537` |
| C++ | ✅ | 86.30 ms | 86.41 ms | 86.50 ms | 254.91 µs | 1.00× | `4704337083537` |
| Python | ✅ | 955.17 ms | 959.75 ms | 958.91 ms | 3.41 ms | 11.07× | `4704337083537` |

### mandelbrot — Mandelbrot set (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `600 200`

Compute a Mandelbrot escape-time bitmap of size W*W with up to MAX_ITER iterations. Inspired by the Computer Language Benchmarks Game. Stresses tight numeric loops and floating-point arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 251.98 ms | 252.02 ms | 252.01 ms | 22.83 µs | 2.78× | `29624109` |
| C++ | ✅ | 90.67 ms | 90.93 ms | 90.85 ms | 157.61 µs | 1.00× | `29624109` |
| Python | ✅ | 3.508 s | 3.538 s | 3.532 s | 21.87 ms | 38.69× | `29624109` |

### nbody — N-Body simulation (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200000`

Symplectic integrator for the classic 5-body solar system from the Benchmarks Game over N steps. Stresses tight floating-point loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 79.73 ms | 79.81 ms | 79.86 ms | 163.52 µs | 5.52× | `-169083713` |
| C++ | ✅ | 14.44 ms | 14.44 ms | 14.45 ms | 7.85 µs | 1.00× | `-169083713` |
| Python | ✅ | 1.167 s | 1.169 s | 1.169 s | 1.86 ms | 80.79× | `-169083713` |

### binary_trees — Binary trees (allocation / GC pressure)

_Category_: `apps` &nbsp;&nbsp;_Args_: `14`

Build and check many small balanced binary trees up to depth D. Adapted from the Computer Language Benchmarks Game. Stresses small-object allocation and GC (or heap allocator).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 117.89 ms | 118.82 ms | 118.93 ms | 1.10 ms | 1.94× | `13250584224` |
| C++ | ✅ | 60.62 ms | 61.11 ms | 61.03 ms | 374.06 µs | 1.00× | `13250584224` |
| Python | ✅ | 845.33 ms | 848.22 ms | 850.88 ms | 7.26 ms | 13.94× | `13250584224` |

### matrix_multiply — Matrix multiplication (naive O(N^3))

_Category_: `apps` &nbsp;&nbsp;_Args_: `250`

Compute C = A * B for two NxN double-precision matrices using the textbook triple-loop algorithm. Stresses memory layout, FP multiply-add throughput, and cache behaviour.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 883.33 ms | 911.95 ms | 904.40 ms | 18.49 ms | 80.96× | `15315135000` |
| C++ | ✅ | 10.91 ms | 11.04 ms | 11.01 ms | 88.20 µs | 1.00× | `15315135000` |
| Python | ✅ | 726.79 ms | 727.59 ms | 727.71 ms | 984.58 µs | 66.61× | `15315135000` |

### word_count — Word count (text processing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1000000`

Tokenize a synthesized N-word text and count word frequencies in a hash-map. Stresses string slicing/comparison, hashing, and hash-map updates — a typical scripting workload.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 745.25 ms | 753.48 ms | 754.65 ms | 10.03 ms | 27.33× | `638309952` |
| C++ | ✅ | 27.27 ms | 27.57 ms | 27.88 ms | 822.53 µs | 1.00× | `638309952` |
| Python | ✅ | 136.33 ms | 136.68 ms | 137.21 ms | 1.24 ms | 5.00× | `638309952` |

## Methodology

- Each implementation is invoked as a fresh OS process and measures its own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. This excludes interpreter / runtime startup from the measurement.
- Each implementation also prints `CHECKSUM:<value>` of its computed result; the runner verifies all implementations of the same benchmark agree, otherwise the comparison is flagged as invalid.
- Per benchmark we run `warmup` unmeasured iterations, then `iterations` measured iterations and report **min / median / mean / stddev**. The _min_ is used for the headline ratio because it is the most robust estimate of best-case wall-clock cost when other system noise is present.
- Compiler flags: `g++ -O2 -std=c++17` for C++, `cjpm build` for Cangjie (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`), CPython 3 for Python (no `-O`), all with no extra runtime tuning.
