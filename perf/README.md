# CangjiePerf

A side-by-side **performance benchmark suite** comparing the same workload
implemented in three languages:

| Language | Toolchain      | Build mode                          |
|----------|----------------|-------------------------------------|
| Cangjie  | `cjc` + `cjpm` | `cjpm build` with `-O2` (per `cjpm.toml`) |
| C++      | `g++`          | `g++ -O2 -std=c++17`                |
| Python   | CPython 3      | run directly with `python3`         |

The suite covers two flavors of comparison:

1. **Micro-benchmarks** — single-feature / standard-library shoot-outs:
   recursion (Fibonacci), stdlib sort on 2M integers, hash-map insert+lookup,
   `StringBuilder`-style string composition.
2. **Application-style benchmarks** — small, realistic numerical kernels in
   the spirit of [Computer Language Benchmarks Game]: the **Mandelbrot set**
   and the classic **N-Body** 5-planet solar-system simulation.

[Computer Language Benchmarks Game]: https://benchmarksgame-team.pages.debian.net/benchmarksgame/

---

## Quick start

```bash
# 1. Make sure prerequisites are on PATH:
#      python3   (always required to run the driver)
#      g++       (for C++ benchmarks)
#      cjc cjpm  (for Cangjie benchmarks; install from the SDK referenced
#                 in the project's top-level .resource file)

# 2. Run everything (build + run + report):
python3 perf/run.py
```

This will:

* detect available toolchains and skip languages that are missing,
* build every C++ implementation with `g++ -O2 -std=c++17`,
* build every Cangjie implementation with `cjpm build`
  (each benchmark's `cjpm.toml` sets `[profile.build] compile-option = "-O2"`),
* run each implementation with `<warmup>` warm-up + `<iterations>` measured
  runs (defaults: 1 + 5),
* aggregate min/median/mean/stddev,
* write raw measurements to `perf/results/results.json`,
* render a Markdown comparison report to `perf/report.md`.

### Useful flags

```bash
python3 perf/run.py --filter sort,nbody         # only some benchmarks
python3 perf/run.py --languages python,cpp      # only some languages
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
│   │   │   ├── cjpm.toml            # name = "fibonacci"; -O2 in [profile.build]
│   │   │   ├── src/main.cj
│   │   │   ├── fibonacci.cpp
│   │   │   └── fibonacci.py
│   │   ├── sort/                    # 2M Int64 stdlib-sort
│   │   ├── hashmap_ops/             # 500k string→int insert + lookup
│   │   └── string_concat/           # 500k fragments via StringBuilder
│   └── apps/
│       ├── mandelbrot/              # 600x600, 200 iters
│       └── nbody/                   # 5-body, 200 000 steps
├── docs/
│   └── design.md                    # detailed design / extension guide
├── results/                         # raw JSON + build logs (generated)
└── report.md                        # final comparison report (generated)
```

---

## How the timing is captured

Process startup time is **not** the focus of this suite, so each implementation
times its own hot path with a monotonic clock and prints the result on the
last two lines of stdout:

```
CHECKSUM:<value>      # used to verify all 3 implementations agree
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
   * `cjpm.toml` (set `name = "<name>"` and the `-O2` profile),
   * `src/main.cj`,
   * `<name>.cpp`,
   * `<name>.py`.
2. Each implementation must take problem-size CLI arguments and print the two
   trailing `CHECKSUM:` / `ELAPSED_MS:` lines.
3. Add an entry in `perf/config/benchmarks.json` describing it (name,
   category, title, description, default args).

See `perf/docs/design.md` for the full contract.
