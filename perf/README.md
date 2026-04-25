# Cross-language performance suite

`perf/` contains a one-click benchmark suite for comparing Cangjie, Python, and C++ implementations of the same workloads.

## Layout

```text
perf/
├── benchmarks.json        # benchmark metadata, toolchain commands, sizes, compiler flags
├── run.py                 # one-click entry point
├── tools/runner.py        # Python-only orchestration, measurement, and report generation
├── cases/
│   ├── cangjie/           # Cangjie benchmark sources
│   ├── cpp/               # C++ benchmark sources
│   └── python/            # Python benchmark sources
├── build/                 # generated native binaries, ignored by git
├── results/               # generated JSON measurement records, ignored by git
└── report.md              # generated comparison report, ignored by git
```

## Benchmarks

- `arith_loop`: core integer arithmetic and loop control.
- `containers`: dynamic sequence containers plus hash-map insert/query operations.
- `word_count`: benchmark-game-style synthetic word-count scenario combining string generation and hash aggregation.

## Run

```bash
python3 perf/run.py
```

For smoke testing:

```bash
python3 perf/run.py --quick --repeat 2 --warmup 0
```

The runner compiles C++ with `g++` and Cangjie with `cjc` when those toolchains are installed. Missing toolchains are marked as skipped so the suite can still produce `perf/report.md` on partial environments.

Useful options:

```bash
python3 perf/run.py --languages python,cpp
python3 perf/run.py --benchmarks containers,word_count
python3 perf/run.py --repeat 7 --warmup 2 --timeout 180
```

## Output

- `perf/report.md`: human-readable comparison table with median/mean/min/stdev and ratios.
- `perf/results/results-*.json`: machine-readable raw samples and environment metadata.

Each benchmark program accepts one input-size argument and prints a deterministic checksum. The checksum helps detect accidental semantic drift between language implementations.
