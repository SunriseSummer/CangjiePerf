# CangjiePerf

A side-by-side **performance benchmark suite** comparing the same workload
implemented in five languages:

| Language | Toolchain      | Build mode                          |
|----------|----------------|-------------------------------------|
| Cangjie  | `cjc`          | `cjc <name>.cj -O2` (single-file)  |
| C++      | `g++`          | `g++ -O2 -std=c++17`                |
| Rust     | `rustc`        | `rustc -O --edition=2021` (release-equivalent `opt-level=3`) |
| Go       | `go`           | `go build` (default release optimization) |
| Python   | CPython 3      | run directly with `python3`         |

Cangjie / C++ / Rust / Go are the four **compiled** languages we compare
head-to-head. Python is included as a scripting-language baseline.

The suite covers two flavors of comparison:

1. **Micro-benchmarks** — single-feature / standard-library shoot-outs:
   * `fibonacci` — recursion / function-call overhead.
   * `sort` — stdlib sort on 2M Int64.
   * `hashmap_ops` — string→int hash-map insert + lookup.
   * `string_concat` — `StringBuilder`-style string composition.
   * `closure_sum` — closures + map/filter/reduce-style higher-order pipeline.
   * `enum_eval` — algebraic data types & recursive pattern matching (AST eval).
   * `regex_search` — stdlib regex find-all over a non-trivial alternation pattern.
   * `math_loop` — `sin`/`cos`/`sqrt`/`exp` tight loop (math stdlib).
   * `prime_sieve` — Sieve of Eratosthenes (algorithmically identical in all 3 languages).
   * `quicksort` — hand-written Lomuto-partition quicksort (algorithmically identical in all 3 languages).
   * `bit_count` — hand-written SWAR popcount tight loop (bitwise/integer ops).
   * `gcd_loop` — Euclidean GCD tight loop (integer division/modulo throughput).
   * `xor_shift` — xorshift64 PRNG tight loop (64-bit shift / XOR throughput).
   * `string_split` — repeated stdlib `split` over a comma-separated token string.
   * `string_search` — repeated stdlib substring search (`indexOf` / `find`).
   * `format_loop` — integer formatting + string-builder loop.
   * `set_ops` — `HashSet` insert + membership (the set-shaped complement of `hashmap_ops`).
   * `deque_ops` — dynamic-array push/pop tight loop.
2. **Application-style benchmarks** — small, realistic kernels in the spirit
   of the [Computer Language Benchmarks Game]:
   * `mandelbrot` — Mandelbrot escape-time bitmap.
   * `nbody` — 5-body solar-system symplectic integrator.
   * `binary_trees` — heap-allocation / GC-pressure stress test.
   * `matrix_multiply` — naive O(N³) double-precision matmul.
   * `word_count` — typical text-processing app (tokenize + hash-map count).
   * `spectral_norm` — power-iteration spectral norm (CLBG numerical kernel).
   * `conway` — Conway's Game of Life on a 200×200 toroidal grid.
   * `knapsack_dp` — 0/1 knapsack with a 1-D rolling DP array.
   * `levenshtein` — Levenshtein edit-distance DP between two strings.
   * `monte_carlo_pi` — integer-only Monte-Carlo PI estimation.
   * `histogram` — bucket counts of LCG ints (data-analysis kernel).
   * `dijkstra` — single-source shortest paths on a dense integer graph.
   * `base64` — table-driven base64 encoder.
   * `crc32` — IEEE 802.3 CRC32 with a 256-entry lookup table.

Benchmarks are tagged with a `chart_group` (`core` for the original 16,
`extended` for the additional 16). The generated `report.md` includes the
per-benchmark **comparison tables** _and_ three **log-scale grouped bar
charts** (linked SVGs):

* `report_chart.svg` — all benchmarks in one chart.
* `report_chart_core.svg` — only the original 16 benchmarks.
* `report_chart_extended.svg` — only the additional 16 benchmarks.

So cross-language differences are immediately visible at a glance, and you
can compare the two waves of benchmarks side by side.

[Computer Language Benchmarks Game]: https://benchmarksgame-team.pages.debian.net/benchmarksgame/

---

## Quick start

```bash
# 1. Make sure prerequisites are on PATH:
#      python3   (always required to run the driver)
#      g++       (for C++ benchmarks)
#      rustc     (for Rust benchmarks)
#      go        (for Go benchmarks)
#      cjc       (for Cangjie benchmarks; install from the SDK referenced
#                 in the project's top-level .resource file)

# 2. Run everything (build + run + report):
python3 perf/run.py
```

This will:

* detect available toolchains and skip languages that are missing,
* build every C++ implementation with `g++ -O2 -std=c++17`,
* build every Rust implementation with `rustc -O --edition=2021`,
* build every Go implementation with `go build` (default release optimization),
* build every Cangjie implementation with `cjc <name>.cj -O2`
  (single-file compilation, no `cjpm` project required),
* run each implementation with `<warmup>` warm-up + `<iterations>` measured
  runs (defaults: 1 + 5),
* aggregate min/median/mean/stddev,
* write raw measurements to `perf/results/results.json`,
* render a Markdown comparison report to `perf/report.md`.

### Useful flags

```bash
python3 perf/run.py --filter sort,nbody         # only some benchmarks
python3 perf/run.py --languages python,cpp      # only some languages (cangjie,cpp,rust,go,python)
python3 perf/run.py --iterations 10 --warmup 2  # more measurement cycles
python3 perf/run.py --clean                     # wipe build cache first
python3 perf/run.py --no-build                  # rerun without rebuilding
```

---

## Layout

```
perf/
├── run.py                           # one-click entry point
├── config/
│   └── benchmarks.json              # benchmark catalog (sizes, descriptions)
├── tools/                           # Python orchestration helpers (stdlib only)
│   ├── env.py                       # detect cjc/cjpm/g++/python3
│   ├── builder.py                   # build C++ and Cangjie artifacts
│   ├── runner.py                    # execute & sample timings
│   ├── stats.py                     # min/median/mean/stddev helpers
│   └── reporter.py                  # render report.md
├── benchmarks/
│   ├── micro/
│   │   ├── fibonacci/
│   │   │   ├── fibonacci.cj         # single-file Cangjie source (cjc -O2)
│   │   │   ├── fibonacci.cpp
│   │   │   ├── fibonacci.rs
│   │   │   ├── fibonacci.go
│   │   │   └── fibonacci.py
│   │   ├── sort/                    # 2M Int64 stdlib-sort
│   │   ├── hashmap_ops/             # 500k string→int insert + lookup
│   │   ├── string_concat/           # 500k fragments via StringBuilder
│   │   ├── closure_sum/             # higher-order map/filter/reduce
│   │   ├── enum_eval/               # ADT + recursive pattern match (AST eval)
│   │   ├── regex_search/            # stdlib regex find-all
│   │   ├── math_loop/               # sin/cos/sqrt/exp tight loop
│   │   ├── prime_sieve/             # Sieve of Eratosthenes
│   │   └── quicksort/               # hand-written Lomuto quicksort
│   └── apps/
│       ├── mandelbrot/              # 600x600, 200 iters
│       ├── nbody/                   # 5-body, 200 000 steps
│       ├── binary_trees/            # depth 14 — alloc/GC pressure
│       ├── matrix_multiply/         # 250×250 double matmul
│       ├── word_count/              # 1M words tokenize + count
│       └── spectral_norm/           # CLBG power iteration, N=1500
├── docs/
│   └── design.md                    # detailed design / extension guide
├── results/                         # raw JSON + build logs (generated)
└── report.md                        # final comparison report (committed)
```

---

## How the timing is captured

Process startup time is **not** the focus of this suite, so each implementation
times its own hot path with a monotonic clock and prints the result on the
last two lines of stdout:

```
CHECKSUM:<value>      # used to verify all 5 implementations agree
ELAPSED_MS:<float>    # wall-clock milliseconds, measured inside the process
```

The Python driver runs each command `warmup + iterations` times, validates
that all `CHECKSUM` lines match across runs and across languages, and
aggregates the `ELAPSED_MS` samples. The headline number reported is the
**minimum** of the measured runs (a robust estimator of best-case wall-clock
cost in the presence of system noise).

---

## Adding a new benchmark

1. Create `perf/benchmarks/<category>/<name>/` containing:
   * `<name>.cj` (single-file Cangjie source, compiled with `cjc -O2`),
   * `<name>.cpp`,
   * `<name>.rs`,
   * `<name>.go`,
   * `<name>.py`.
2. Each implementation must take problem-size CLI arguments and print the two
   trailing `CHECKSUM:` / `ELAPSED_MS:` lines, **and** all five
   implementations of the same benchmark must produce identical `CHECKSUM`
   values (the runner verifies this and aborts the comparison otherwise).
3. Add an entry in `perf/config/benchmarks.json` describing it (name,
   category, title, description, default args).

See `perf/docs/design.md` for the full contract.
