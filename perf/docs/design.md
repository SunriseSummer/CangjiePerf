# CangjiePerf — Design

This document describes the design of the `perf/` benchmark suite: what it
measures, how it measures it, and how to extend it. For day-to-day usage
see [`../README.md`](../README.md).

---

## 1. Goals

* **Apples-to-apples** comparison of Cangjie, Python, and C++ on the same
  workload.
* Cover both **language-level features** (recursion, function calls, integer
  arithmetic) and **standard-library** primitives (sort, hash-map,
  `StringBuilder`), plus realistic **numerical kernels** in the spirit of the
  Computer Language Benchmarks Game.
* **One-click** execution: a single `python3 perf/run.py` builds everything,
  runs everything, and produces a Markdown report.
* **Reproducibility**: deterministic inputs, identical algorithms across
  languages, cross-language `CHECKSUM` verification.
* **Tooling-only Python**: helper / orchestration scripts use the Python
  standard library exclusively (no `pip install` required).

---

## 2. Output contract

Every implementation, regardless of language, prints the same final two lines
to stdout:

```
CHECKSUM:<string>
ELAPSED_MS:<float>
```

* `CHECKSUM` is a deterministic value derived from the benchmark's result
  (e.g. an XOR of selected array elements after sorting, or a rounded
  integer derived from a final floating-point energy). The runner enforces
  that all implementations of the same benchmark emit the **same string**.
  Mismatches are reported in `report.md` and invalidate the comparison.
* `ELAPSED_MS` is the wall-clock time, in milliseconds, of the benchmark's
  hot path **measured inside the process** with a monotonic clock
  (`time.perf_counter_ns` in Python, `std::chrono::steady_clock` in C++,
  `MonoTime.now()` in Cangjie). Process startup, argument parsing, JIT/JVM
  warm-up costs etc. are deliberately excluded.

By measuring inside the process we focus on the pure compute / stdlib cost,
which is the property the suite advertises. If you want startup cost too,
the Python driver also records the *external* wall-clock time of the whole
process — see `samples_ms` in `results.json`.

---

## 3. Build pipeline

| Language | Tool      | Command                                           | Optimization |
|----------|-----------|---------------------------------------------------|--------------|
| Cangjie  | `cjpm`    | `cjpm build` (cwd = benchmark dir)                | `-O2` set in each benchmark's `cjpm.toml` under `[profile.build] compile-option` |
| C++      | `g++`     | `g++ -O2 -std=c++17 -pipe <src>.cpp -o build/cpp/<name>/<name> -lm` | `-O2` |
| Python   | `python3` | n/a (interpreted)                                 | none — bare CPython, no `-O` |

### Why `cjpm` (not `cjc` directly)?

The Cangjie team's recommended way to build production code is via the
project manager `cjpm`, with optimization configured in `cjpm.toml`. This
matches how a real Cangjie project would be shipped (the `[profile.build]`
section enables `-O2` for *every* package automatically) and means each
benchmark is itself a self-contained miniature Cangjie project that you can
inspect / tweak / build / run on its own.

`cjpm`'s default release output path is
`<project>/target/release/bin/main`. The Python builder then copies this
binary to `perf/build/cangjie/<benchmark>/<benchmark>` so the runner can
invoke it by a stable path.

---

## 4. Measurement protocol

For each `(benchmark, language)` pair the runner performs:

1. **Build** the artifact (or skip Python, which is interpreted).
2. **Warmup** runs (default `1`): execute the binary once or more, validate
   the `CHECKSUM`/`ELAPSED_MS` lines, but discard the timing.
3. **Measurement** runs (default `5`): execute the binary again, record
   each `ELAPSED_MS`. If any `CHECKSUM` differs between runs the entire
   benchmark is marked failed.
4. **Aggregate** the measurement samples into min / median / mean / stddev.

The **minimum** is used as the headline ratio in the summary table because
in the presence of random system noise (other processes, frequency scaling,
page faults) the *minimum* is the most robust estimator of the true cost
of the workload itself.

The **median** is also reported, which is more sensitive to systematic
slow-downs (such as GC pauses) and so is useful as a complementary signal.

---

## 5. Benchmark catalog

The list of benchmarks lives in [`config/benchmarks.json`](../config/benchmarks.json).
Each entry has:

```json
{
  "name": "sort",
  "category": "micro",
  "title": "Sort 2M integers (stdlib sort)",
  "description": "...",
  "args": ["2000000"]
}
```

Sizes are tuned so the entire suite finishes in roughly one minute on a
modern laptop with a working Cangjie SDK. Pass a different size on the
command line if needed:

```bash
python3 perf/run.py --filter sort   # uses default 2_000_000
# manually edit config/benchmarks.json to tweak sizes globally
```

---

## 6. Adding a new benchmark

Suppose you want to add a benchmark called `regex_search` under `apps/`:

1. **Create the directory and the three implementations**:
   ```
   perf/benchmarks/apps/regex_search/
     cjpm.toml
     src/main.cj
     regex_search.cpp
     regex_search.py
   ```
2. **Write `cjpm.toml`** following the same template as existing benchmarks
   (don't forget `[profile.build] compile-option = "-O2"`).
3. **Implement** the kernel in each language. The kernel must:
   * accept its problem size from `argv`;
   * time only the hot path with a monotonic clock;
   * print `CHECKSUM:<x>` then `ELAPSED_MS:<x>` on the last two lines.
4. **Register** the benchmark in `config/benchmarks.json` with a description
   and a default args list.
5. **Verify**: `python3 perf/run.py --filter regex_search`. The runner
   will fail loudly if the `CHECKSUM`s differ across languages, helping you
   prove the implementations compute the same thing.

---

## 7. Why these benchmarks?

| Benchmark        | What it actually stresses                                          |
|------------------|--------------------------------------------------------------------|
| `fibonacci`      | function-call cost, recursion, integer arithmetic                  |
| `sort`           | stdlib sort, dynamic array indexing, comparator dispatch           |
| `hashmap_ops`    | hash function quality, collision handling, string allocation       |
| `string_concat`  | `StringBuilder` / amortized buffer growth, allocator behavior      |
| `closure_sum`    | closure dispatch, higher-order iteration, integer arithmetic       |
| `enum_eval`      | algebraic data types, recursive `match` dispatch, tag-tag chains   |
| `regex_search`   | the language's regex engine (NFA/DFA), backtracking, alternation   |
| `math_loop`      | `sin`/`cos`/`sqrt`/`exp` performance and FP throughput              |
| `mandelbrot`     | tight nested numeric loop, FP arithmetic, branch prediction         |
| `nbody`          | small-array data layout, FP multiply-add density, `sqrt` cost      |
| `binary_trees`   | small-object allocation rate, GC throughput / heap allocator       |
| `matrix_multiply`| memory layout, FP multiply-add throughput, cache behaviour          |
| `word_count`     | string slicing/comparison, hashing, hash-map updates               |

This selection covers the most common day-to-day perf concerns when picking
a language for either systems-style or scripting-style code, while staying
small enough to read end-to-end in one sitting.

---

## 8. Limitations & caveats

* The Python driver's `ELAPSED_MS` excludes process-startup. CPython startup
  alone is ≥10–20 ms, which would dominate small benchmarks if included.
  For the wall-clock-including-startup view, look at the runner's external
  timing reported in stderr / `results.json`.
* Each benchmark uses its language's *idiomatic* recommended primitive
  (e.g. `dict` in Python, `std::unordered_map` in C++, `HashMap` in
  Cangjie). It's not an attempt to find the absolute fastest data
  structure in each ecosystem.
* Compiler version, CPU governor settings, and concurrent system load all
  affect results. The `report.md` always records the host environment so
  the numbers can be interpreted in context.
