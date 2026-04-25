#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PERF_DIR="$(dirname "$SCRIPT_DIR")"

# Source Cangjie environment if available
if [ -f "/tmp/cangjie/cangjie/envsetup.sh" ]; then
    source /tmp/cangjie/cangjie/envsetup.sh
fi

echo "==============================="
echo " Cangjie Perf Benchmarks"
echo "==============================="
echo ""

run_bench() {
    local name="$1"
    local dir="$2"
    echo "--- $name ---"
    cd "$PERF_DIR/$dir"
    cjpm build --quiet 2>/dev/null || cjpm build
    ./target/release/bin/main
    echo ""
}

run_bench "fibonacci"   "benchmarks/micro/fibonacci"
run_bench "mandelbrot"  "benchmarks/micro/mandelbrot"
run_bench "nbody"       "benchmarks/apps/nbody"

echo "==============================="
echo " All benchmarks complete"
echo "==============================="
