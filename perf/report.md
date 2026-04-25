# CangjiePerf Benchmark Report

_Generated: 2026-04-25T12:07:21+00:00_

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
| **fibonacci** | micro | 23.64 ms | 3.83 ms | 307.42 ms | C++ |
| **sort** | micro | 2.152 s | 135.12 ms | 751.89 ms | C++ |
| **hashmap_ops** | micro | 494.23 ms | 108.31 ms | 115.78 ms | C++ |
| **string_concat** | micro | 47.30 ms | 31.97 ms | 71.03 ms | C++ |
| **closure_sum** | micro | 100.83 ms | 9.14 ms | 360.79 ms | C++ |
| **enum_eval** | micro | 538.50 ms | 128.14 ms | 4.976 s | C++ |
| **regex_search** | micro | 45.34 ms | 77.80 ms | 42.05 ms | Python |
| **math_loop** | micro | 140.53 ms | 86.38 ms | 927.01 ms | C++ |
| **prime_sieve** | micro | 1.579 s | 51.56 ms | 2.787 s | C++ |
| **quicksort** | micro | 2.313 s | 111.12 ms | 3.330 s | C++ |
| **mandelbrot** | apps | 251.84 ms | 90.91 ms | 3.506 s | C++ |
| **nbody** | apps | 79.00 ms | 14.34 ms | 1.167 s | C++ |
| **binary_trees** | apps | 115.88 ms | 66.12 ms | 845.10 ms | C++ |
| **matrix_multiply** | apps | 897.27 ms | 10.17 ms | 727.85 ms | C++ |
| **word_count** | apps | 732.05 ms | 27.59 ms | 134.02 ms | C++ |
| **spectral_norm** | apps | 2.210 s | 128.94 ms | 15.349 s | C++ |

### Visual comparison

Each benchmark shows three side-by-side bars (Cangjie / C++ / Python). **Lower bars are faster.** Note the **logarithmic** y-axis: a one-step gridline difference is a 10× speed difference. Hover any bar to see its exact timing.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1086 360" width="100%" role="img" aria-label="Benchmark timings (log scale)" font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" font-size="11"><rect x="0" y="0" width="1086" height="360" fill="#ffffff"/><text x="543.0" y="22" text-anchor="middle" font-size="14" font-weight="600" fill="#222">Benchmark wall-clock time per implementation (min of 3 runs, log scale, lower is better)</text><rect x="60" y="27" width="12" height="12" fill="#d9534f" rx="2"/><text x="78" y="37" fill="#333">Cangjie</text><rect x="170" y="27" width="12" height="12" fill="#5cb85c" rx="2"/><text x="188" y="37" fill="#333">C++</text><rect x="280" y="27" width="12" height="12" fill="#5bc0de" rx="2"/><text x="298" y="37" fill="#333">Python</text><line x1="60" y1="290.0" x2="1066" y2="290.0" stroke="#e5e5e5" stroke-width="1"/><text x="54" y="293.0" text-anchor="end" fill="#555">1 ms</text><line x1="60" y1="242.0" x2="1066" y2="242.0" stroke="#e5e5e5" stroke-width="1"/><text x="54" y="245.0" text-anchor="end" fill="#555">10 ms</text><line x1="60" y1="194.0" x2="1066" y2="194.0" stroke="#e5e5e5" stroke-width="1"/><text x="54" y="197.0" text-anchor="end" fill="#555">100 ms</text><line x1="60" y1="146.0" x2="1066" y2="146.0" stroke="#e5e5e5" stroke-width="1"/><text x="54" y="149.0" text-anchor="end" fill="#555">1 s</text><line x1="60" y1="98.0" x2="1066" y2="98.0" stroke="#e5e5e5" stroke-width="1"/><text x="54" y="101.0" text-anchor="end" fill="#555">10 s</text><line x1="60" y1="50.0" x2="1066" y2="50.0" stroke="#e5e5e5" stroke-width="1"/><text x="54" y="53.0" text-anchor="end" fill="#555">100 s</text><line x1="60" y1="50" x2="60" y2="290" stroke="#888" stroke-width="1"/><line x1="60" y1="290" x2="1066" y2="290" stroke="#888" stroke-width="1"/><rect x="60.0" y="224.1" width="14" height="65.9" fill="#d9534f" rx="1"><title>Cangjie fibonacci: 23.64 ms</title></rect><rect x="76.0" y="262.0" width="14" height="28.0" fill="#5cb85c" rx="1"><title>C++ fibonacci: 3.83 ms</title></rect><rect x="92.0" y="170.6" width="14" height="119.4" fill="#5bc0de" rx="1"><title>Python fibonacci: 307.42 ms</title></rect><text x="83.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 83.0,298.0)">fibonacci</text><rect x="124.0" y="130.0" width="14" height="160.0" fill="#d9534f" rx="1"><title>Cangjie sort: 2.152 s</title></rect><rect x="140.0" y="187.7" width="14" height="102.3" fill="#5cb85c" rx="1"><title>C++ sort: 135.12 ms</title></rect><rect x="156.0" y="151.9" width="14" height="138.1" fill="#5bc0de" rx="1"><title>Python sort: 751.89 ms</title></rect><text x="147.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 147.0,298.0)">sort</text><rect x="188.0" y="160.7" width="14" height="129.3" fill="#d9534f" rx="1"><title>Cangjie hashmap_ops: 494.23 ms</title></rect><rect x="204.0" y="192.3" width="14" height="97.7" fill="#5cb85c" rx="1"><title>C++ hashmap_ops: 108.31 ms</title></rect><rect x="220.0" y="190.9" width="14" height="99.1" fill="#5bc0de" rx="1"><title>Python hashmap_ops: 115.78 ms</title></rect><text x="211.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 211.0,298.0)">hashmap_ops</text><rect x="252.0" y="209.6" width="14" height="80.4" fill="#d9534f" rx="1"><title>Cangjie string_concat: 47.30 ms</title></rect><rect x="268.0" y="217.8" width="14" height="72.2" fill="#5cb85c" rx="1"><title>C++ string_concat: 31.97 ms</title></rect><rect x="284.0" y="201.1" width="14" height="88.9" fill="#5bc0de" rx="1"><title>Python string_concat: 71.03 ms</title></rect><text x="275.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 275.0,298.0)">string_concat</text><rect x="316.0" y="193.8" width="14" height="96.2" fill="#d9534f" rx="1"><title>Cangjie closure_sum: 100.83 ms</title></rect><rect x="332.0" y="243.9" width="14" height="46.1" fill="#5cb85c" rx="1"><title>C++ closure_sum: 9.14 ms</title></rect><rect x="348.0" y="167.3" width="14" height="122.7" fill="#5bc0de" rx="1"><title>Python closure_sum: 360.79 ms</title></rect><text x="339.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 339.0,298.0)">closure_sum</text><rect x="380.0" y="158.9" width="14" height="131.1" fill="#d9534f" rx="1"><title>Cangjie enum_eval: 538.50 ms</title></rect><rect x="396.0" y="188.8" width="14" height="101.2" fill="#5cb85c" rx="1"><title>C++ enum_eval: 128.14 ms</title></rect><rect x="412.0" y="112.6" width="14" height="177.4" fill="#5bc0de" rx="1"><title>Python enum_eval: 4.976 s</title></rect><text x="403.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 403.0,298.0)">enum_eval</text><rect x="444.0" y="210.5" width="14" height="79.5" fill="#d9534f" rx="1"><title>Cangjie regex_search: 45.34 ms</title></rect><rect x="460.0" y="199.2" width="14" height="90.8" fill="#5cb85c" rx="1"><title>C++ regex_search: 77.80 ms</title></rect><rect x="476.0" y="212.1" width="14" height="77.9" fill="#5bc0de" rx="1"><title>Python regex_search: 42.05 ms</title></rect><text x="467.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 467.0,298.0)">regex_search</text><rect x="508.0" y="186.9" width="14" height="103.1" fill="#d9534f" rx="1"><title>Cangjie math_loop: 140.53 ms</title></rect><rect x="524.0" y="197.1" width="14" height="92.9" fill="#5cb85c" rx="1"><title>C++ math_loop: 86.38 ms</title></rect><rect x="540.0" y="147.6" width="14" height="142.4" fill="#5bc0de" rx="1"><title>Python math_loop: 927.01 ms</title></rect><text x="531.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 531.0,298.0)">math_loop</text><rect x="572.0" y="136.5" width="14" height="153.5" fill="#d9534f" rx="1"><title>Cangjie prime_sieve: 1.579 s</title></rect><rect x="588.0" y="207.8" width="14" height="82.2" fill="#5cb85c" rx="1"><title>C++ prime_sieve: 51.56 ms</title></rect><rect x="604.0" y="124.6" width="14" height="165.4" fill="#5bc0de" rx="1"><title>Python prime_sieve: 2.787 s</title></rect><text x="595.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 595.0,298.0)">prime_sieve</text><rect x="636.0" y="128.5" width="14" height="161.5" fill="#d9534f" rx="1"><title>Cangjie quicksort: 2.313 s</title></rect><rect x="652.0" y="191.8" width="14" height="98.2" fill="#5cb85c" rx="1"><title>C++ quicksort: 111.12 ms</title></rect><rect x="668.0" y="120.9" width="14" height="169.1" fill="#5bc0de" rx="1"><title>Python quicksort: 3.330 s</title></rect><text x="659.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 659.0,298.0)">quicksort</text><rect x="700.0" y="174.7" width="14" height="115.3" fill="#d9534f" rx="1"><title>Cangjie mandelbrot: 251.84 ms</title></rect><rect x="716.0" y="196.0" width="14" height="94.0" fill="#5cb85c" rx="1"><title>C++ mandelbrot: 90.91 ms</title></rect><rect x="732.0" y="119.8" width="14" height="170.2" fill="#5bc0de" rx="1"><title>Python mandelbrot: 3.506 s</title></rect><text x="723.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 723.0,298.0)">mandelbrot</text><rect x="764.0" y="198.9" width="14" height="91.1" fill="#d9534f" rx="1"><title>Cangjie nbody: 79.00 ms</title></rect><rect x="780.0" y="234.5" width="14" height="55.5" fill="#5cb85c" rx="1"><title>C++ nbody: 14.34 ms</title></rect><rect x="796.0" y="142.8" width="14" height="147.2" fill="#5bc0de" rx="1"><title>Python nbody: 1.167 s</title></rect><text x="787.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 787.0,298.0)">nbody</text><rect x="828.0" y="190.9" width="14" height="99.1" fill="#d9534f" rx="1"><title>Cangjie binary_trees: 115.88 ms</title></rect><rect x="844.0" y="202.6" width="14" height="87.4" fill="#5cb85c" rx="1"><title>C++ binary_trees: 66.12 ms</title></rect><rect x="860.0" y="149.5" width="14" height="140.5" fill="#5bc0de" rx="1"><title>Python binary_trees: 845.10 ms</title></rect><text x="851.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 851.0,298.0)">binary_trees</text><rect x="892.0" y="148.3" width="14" height="141.7" fill="#d9534f" rx="1"><title>Cangjie matrix_multiply: 897.27 ms</title></rect><rect x="908.0" y="241.6" width="14" height="48.4" fill="#5cb85c" rx="1"><title>C++ matrix_multiply: 10.17 ms</title></rect><rect x="924.0" y="152.6" width="14" height="137.4" fill="#5bc0de" rx="1"><title>Python matrix_multiply: 727.85 ms</title></rect><text x="915.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 915.0,298.0)">matrix_multiply</text><rect x="956.0" y="152.5" width="14" height="137.5" fill="#d9534f" rx="1"><title>Cangjie word_count: 732.05 ms</title></rect><rect x="972.0" y="220.8" width="14" height="69.2" fill="#5cb85c" rx="1"><title>C++ word_count: 27.59 ms</title></rect><rect x="988.0" y="187.9" width="14" height="102.1" fill="#5bc0de" rx="1"><title>Python word_count: 134.02 ms</title></rect><text x="979.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 979.0,298.0)">word_count</text><rect x="1020.0" y="129.5" width="14" height="160.5" fill="#d9534f" rx="1"><title>Cangjie spectral_norm: 2.210 s</title></rect><rect x="1036.0" y="188.7" width="14" height="101.3" fill="#5cb85c" rx="1"><title>C++ spectral_norm: 128.94 ms</title></rect><rect x="1052.0" y="89.1" width="14" height="200.9" fill="#5bc0de" rx="1"><title>Python spectral_norm: 15.349 s</title></rect><text x="1043.0" y="298.0" text-anchor="end" fill="#333" transform="rotate(-45 1043.0,298.0)">spectral_norm</text></svg>

## Per-benchmark Detail

### fibonacci — Recursive Fibonacci (function call / recursion)

_Category_: `micro` &nbsp;&nbsp;_Args_: `32`

Pure recursive fib(N). Stresses function-call overhead and integer arithmetic. No standard-library involvement beyond integers.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 23.64 ms | 23.90 ms | 23.83 ms | 168.30 µs | 6.17× | `2178309` |
| C++ | ✅ | 3.83 ms | 4.00 ms | 3.96 ms | 114.31 µs | 1.00× | `2178309` |
| Python | ✅ | 307.42 ms | 308.25 ms | 308.07 ms | 584.66 µs | 80.28× | `2178309` |

### sort — Sort 2M integers (stdlib sort)

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Generate 2,000,000 deterministic pseudo-random Int64 values then sort ascending using the language's standard sort. Stresses standard library sorting and dynamic arrays.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.152 s | 2.170 s | 2.170 s | 17.16 ms | 15.93× | `1074570229` |
| C++ | ✅ | 135.12 ms | 135.88 ms | 135.83 ms | 689.07 µs | 1.00× | `1074570229` |
| Python | ✅ | 751.89 ms | 754.43 ms | 754.42 ms | 2.53 ms | 5.56× | `1074570229` |

### hashmap_ops — HashMap insert + lookup (stdlib hash table)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Insert N (string,int) pairs then look up the same N keys. Stresses hash maps, string hashing, and string allocation.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 494.23 ms | 498.72 ms | 506.08 ms | 16.78 ms | 4.56× | `0` |
| C++ | ✅ | 108.31 ms | 108.68 ms | 108.83 ms | 606.33 µs | 1.00× | `0` |
| Python | ✅ | 115.78 ms | 117.48 ms | 117.93 ms | 2.41 ms | 1.07× | `0` |

### string_concat — String building (stdlib StringBuilder)

_Category_: `micro` &nbsp;&nbsp;_Args_: `500000`

Build a single large string from N small fragments using the recommended efficient builder for each language. Stresses string buffers and memory growth.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 47.30 ms | 47.37 ms | 47.39 ms | 97.92 µs | 1.48× | `5388890` |
| C++ | ✅ | 31.97 ms | 33.35 ms | 32.93 ms | 828.77 µs | 1.00× | `5388890` |
| Python | ✅ | 71.03 ms | 71.09 ms | 71.36 ms | 522.19 µs | 2.22× | `5388890` |

### closure_sum — Closure / higher-order pipeline

_Category_: `micro` &nbsp;&nbsp;_Args_: `2000000`

Apply a map -> filter -> reduce pipeline of closures over N integers. Stresses higher-order function dispatch, closure allocation, and integer arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 100.83 ms | 102.56 ms | 101.99 ms | 1.00 ms | 11.03× | `1777776444435777780` |
| C++ | ✅ | 9.14 ms | 9.22 ms | 9.22 ms | 74.91 µs | 1.00× | `1777776444435777780` |
| Python | ✅ | 360.79 ms | 364.62 ms | 365.72 ms | 5.56 ms | 39.47× | `1777776444435777780` |

### enum_eval — Enum / pattern matching (AST evaluation)

_Category_: `micro` &nbsp;&nbsp;_Args_: `18 60`

Build a recursive arithmetic expression tree of depth D and evaluate it N times via recursive pattern matching on a sum-type enum (Num | Add | Sub | Mul). Stresses algebraic data types, recursive calls, and tag dispatch.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 538.50 ms | 541.81 ms | 546.42 ms | 10.98 ms | 4.20× | `0` |
| C++ | ✅ | 128.14 ms | 129.53 ms | 129.14 ms | 875.65 µs | 1.00× | `0` |
| Python | ✅ | 4.976 s | 5.012 s | 5.007 s | 29.15 ms | 38.83× | `0` |

### regex_search — Regex find-all (stdlib regex)

_Category_: `micro` &nbsp;&nbsp;_Args_: `4000`

Run a non-trivial alternation regex (date | email | capitalized word) across REPEATS copies of a sample paragraph. Stresses the standard regex engine.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 45.34 ms | 46.13 ms | 46.13 ms | 793.15 µs | 1.08× | `36000` |
| C++ | ✅ | 77.80 ms | 78.88 ms | 78.61 ms | 715.55 µs | 1.85× | `36000` |
| Python | ✅ | 42.05 ms | 42.11 ms | 42.13 ms | 102.60 µs | 1.00× | `36000` |

### math_loop — Math-intensive loop (sin/cos/sqrt/exp)

_Category_: `micro` &nbsp;&nbsp;_Args_: `5000000`

Sum sin(x)*cos(x)+sqrt(x+1)-exp(-x) over N points. Stresses the math standard library and floating-point throughput.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 140.53 ms | 140.61 ms | 140.63 ms | 110.99 µs | 1.63× | `4704337083537` |
| C++ | ✅ | 86.38 ms | 87.02 ms | 87.96 ms | 2.20 ms | 1.00× | `4704337083537` |
| Python | ✅ | 927.01 ms | 928.68 ms | 933.77 ms | 10.29 ms | 10.73× | `4704337083537` |

### prime_sieve — Sieve of Eratosthenes

_Category_: `micro` &nbsp;&nbsp;_Args_: `20000000`

Classic Sieve of Eratosthenes up to N on a one-byte-per-cell boolean array, then count primes and sum them mod 2^31. Algorithmically identical across all three languages: same loop bounds, same inner stride, same checksum formula.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 1.579 s | 1.597 s | 1.593 s | 12.97 ms | 30.62× | `1156745585` |
| C++ | ✅ | 51.56 ms | 51.63 ms | 51.64 ms | 76.00 µs | 1.00× | `1156745585` |
| Python | ✅ | 2.787 s | 2.788 s | 2.805 s | 29.07 ms | 54.05× | `1156745585` |

### quicksort — Hand-written quicksort

_Category_: `micro` &nbsp;&nbsp;_Args_: `1500000`

Lomuto-partition quicksort with middle-element pivot and recurse-smaller-side / iterate-larger-side, implemented by hand in all three languages so the algorithm itself is identical (complements the stdlib `sort` benchmark).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.313 s | 2.336 s | 2.347 s | 41.44 ms | 20.82× | `612429648` |
| C++ | ✅ | 111.12 ms | 111.24 ms | 111.49 ms | 545.35 µs | 1.00× | `612429648` |
| Python | ✅ | 3.330 s | 3.374 s | 3.360 s | 25.73 ms | 29.97× | `612429648` |

### mandelbrot — Mandelbrot set (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `600 200`

Compute a Mandelbrot escape-time bitmap of size W*W with up to MAX_ITER iterations. Inspired by the Computer Language Benchmarks Game. Stresses tight numeric loops and floating-point arithmetic.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 251.84 ms | 251.85 ms | 251.88 ms | 68.78 µs | 2.77× | `29624109` |
| C++ | ✅ | 90.91 ms | 90.91 ms | 90.92 ms | 17.30 µs | 1.00× | `29624109` |
| Python | ✅ | 3.506 s | 3.545 s | 3.539 s | 30.06 ms | 38.57× | `29624109` |

### nbody — N-Body simulation (numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `200000`

Symplectic integrator for the classic 5-body solar system from the Benchmarks Game over N steps. Stresses tight floating-point loops and array indexing.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 79.00 ms | 79.15 ms | 79.13 ms | 114.18 µs | 5.51× | `-169083713` |
| C++ | ✅ | 14.34 ms | 14.35 ms | 14.37 ms | 31.26 µs | 1.00× | `-169083713` |
| Python | ✅ | 1.167 s | 1.168 s | 1.171 s | 6.69 ms | 81.35× | `-169083713` |

### binary_trees — Binary trees (allocation / GC pressure)

_Category_: `apps` &nbsp;&nbsp;_Args_: `14`

Build and check many small balanced binary trees up to depth D. Adapted from the Computer Language Benchmarks Game. Stresses small-object allocation and GC (or heap allocator).

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 115.88 ms | 116.08 ms | 117.09 ms | 1.91 ms | 1.75× | `13250584224` |
| C++ | ✅ | 66.12 ms | 66.44 ms | 66.64 ms | 638.63 µs | 1.00× | `13250584224` |
| Python | ✅ | 845.10 ms | 850.92 ms | 855.99 ms | 14.13 ms | 12.78× | `13250584224` |

### matrix_multiply — Matrix multiplication (naive O(N^3))

_Category_: `apps` &nbsp;&nbsp;_Args_: `250`

Compute C = A * B for two NxN double-precision matrices using the textbook triple-loop algorithm. Stresses memory layout, FP multiply-add throughput, and cache behaviour.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 897.27 ms | 905.40 ms | 905.09 ms | 7.67 ms | 88.20× | `15315135000` |
| C++ | ✅ | 10.17 ms | 10.22 ms | 10.22 ms | 40.69 µs | 1.00× | `15315135000` |
| Python | ✅ | 727.85 ms | 729.89 ms | 736.00 ms | 12.39 ms | 71.54× | `15315135000` |

### word_count — Word count (text processing)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1000000`

Tokenize a synthesized N-word text and count word frequencies in a hash-map. Stresses string slicing/comparison, hashing, and hash-map updates — a typical scripting workload.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 732.05 ms | 732.26 ms | 733.88 ms | 2.99 ms | 26.53× | `638309952` |
| C++ | ✅ | 27.59 ms | 27.77 ms | 28.15 ms | 816.07 µs | 1.00× | `638309952` |
| Python | ✅ | 134.02 ms | 134.05 ms | 134.45 ms | 728.47 µs | 4.86× | `638309952` |

### spectral_norm — Spectral norm (CLBG numerical kernel)

_Category_: `apps` &nbsp;&nbsp;_Args_: `1500`

Approximates the largest eigenvalue of an infinite matrix A[i][j] = 1 / ((i+j)(i+j+1)/2 + i + 1) via 10 power iterations of v <- A^T A v. Adapted from the Computer Language Benchmarks Game; algorithmically identical across all three languages.

| Language | Status | min | median | mean | stddev | vs fastest | Checksum |
|----------|--------|-----|--------|------|--------|------------|----------|
| Cangjie | ✅ | 2.210 s | 2.216 s | 2.217 s | 6.80 ms | 17.14× | `1274224151` |
| C++ | ✅ | 128.94 ms | 128.96 ms | 129.04 ms | 150.40 µs | 1.00× | `1274224151` |
| Python | ✅ | 15.349 s | 15.514 s | 15.483 s | 122.35 ms | 119.04× | `1274224151` |

## Methodology

- Each implementation is invoked as a fresh OS process and measures its own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. This excludes interpreter / runtime startup from the measurement.
- Each implementation also prints `CHECKSUM:<value>` of its computed result; the runner verifies all implementations of the same benchmark agree, otherwise the comparison is flagged as invalid.
- Per benchmark we run `warmup` unmeasured iterations, then `iterations` measured iterations and report **min / median / mean / stddev**. The _min_ is used for the headline ratio because it is the most robust estimate of best-case wall-clock cost when other system noise is present.
- Compiler flags: `g++ -O2 -std=c++17` for C++, `cjpm build` for Cangjie (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`), CPython 3 for Python (no `-O`), all with no extra runtime tuning.
