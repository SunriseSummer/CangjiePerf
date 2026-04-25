# Cangjie Performance Benchmarks

A collection of micro-benchmarks and application benchmarks written in [Cangjie](https://cangjie-lang.cn/) to measure language runtime performance. All benchmarks are compiled with `-O2` optimization.

## Benchmarks

| Benchmark | Description | Time (ms) |
|-----------|-------------|----------:|
| fibonacci | Recursive `fib(35)` | 31.61 |
| mandelbrot | Mandelbrot set 800×800, maxIter=1000 | 406.73 |
| nbody | N-body simulation, 50 000 000 steps | 2768.40 |

> Measured on Linux x86-64, Cangjie 1.0.5, compiled with `-O2`.

## Structure

```
perf/
├── benchmarks/
│   ├── micro/
│   │   ├── fibonacci/      # Classic recursive Fibonacci
│   │   └── mandelbrot/     # Mandelbrot set computation
│   └── apps/
│       └── nbody/          # N-body planetary simulation
├── tools/
│   └── run_benchmarks.sh   # Runs all benchmarks in sequence
└── results.svg             # Bar chart of benchmark results
```

## How to Run

### Prerequisites

1. Install the Cangjie SDK and source the environment:
   ```bash
   source /tmp/cangjie/cangjie/envsetup.sh
   ```

### Run all benchmarks

```bash
bash perf/tools/run_benchmarks.sh
```

### Run a single benchmark

```bash
cd perf/benchmarks/micro/fibonacci
cjpm build
./target/release/bin/main
```

## Results Chart

See [results.svg](./results.svg) for a visual bar chart of the benchmark timings.
