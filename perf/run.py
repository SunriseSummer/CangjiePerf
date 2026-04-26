#!/usr/bin/env python3
"""CangjiePerf — one-click benchmark driver.

Usage:
    python3 perf/run.py                             # run everything
    python3 perf/run.py --filter sort,nbody         # only some benchmarks
    python3 perf/run.py --languages python,cpp      # only some languages
    python3 perf/run.py --iterations 10 --warmup 2  # tuning
    python3 perf/run.py --clean                     # wipe build cache first

Outputs:
    perf/results/results.json   raw measurements (every sample, per language)
    perf/report.md              human-readable comparison report
"""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from dataclasses import asdict
from pathlib import Path

# Allow ``python3 perf/run.py`` from anywhere (no install / no PYTHONPATH).
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from tools import builder, env, reporter  # noqa: E402
from tools.runner import RunOutcome, run_benchmark  # noqa: E402


def _load_config() -> dict:
    cfg_path = _HERE / "config" / "benchmarks.json"
    with cfg_path.open(encoding="utf-8") as f:
        return json.load(f)


def _outcome_to_jsonable(o: RunOutcome) -> dict:
    return {
        "language": o.language,
        "benchmark": o.benchmark,
        "success": o.success,
        "samples_ms": o.samples_ms,
        "summary": o.summary.as_dict() if o.summary else None,
        "checksum": o.checksum,
        "error": o.error,
    }


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run CangjiePerf benchmarks.")
    p.add_argument("--filter", default="",
                   help="Comma-separated benchmark names to include (default: all).")
    p.add_argument("--languages", default="",
                   help="Comma-separated languages to run (cangjie,python,cpp).")
    p.add_argument("--warmup", type=int, default=None,
                   help="Override number of warmup runs (default from config).")
    p.add_argument("--iterations", type=int, default=None,
                   help="Override number of measurement runs (default from config).")
    p.add_argument("--clean", action="store_true",
                   help="Remove build cache before running.")
    p.add_argument("--no-build", action="store_true",
                   help="Skip rebuild step (assume artifacts already exist).")
    p.add_argument("--output", default=str(_HERE / "report.md"),
                   help="Path of the Markdown report to write.")
    p.add_argument("--results-json", default=str(_HERE / "results" / "results.json"),
                   help="Path of the raw JSON results file.")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    cfg = _load_config()
    defaults = cfg["defaults"]
    warmup = args.warmup if args.warmup is not None else int(defaults["warmup"])
    iterations = args.iterations if args.iterations is not None else int(defaults["iterations"])
    languages = (
        [s.strip() for s in args.languages.split(",") if s.strip()]
        if args.languages else list(defaults["languages"])
    )
    name_filter = {s.strip() for s in args.filter.split(",") if s.strip()}

    if args.clean:
        print("[clean] removing perf/build/*")
        builder.clean()

    # Toolchain detection.
    toolchains = env.detect_all()
    print("Detected toolchains:")
    for tc in toolchains.values():
        print(f"  {tc.short()}")

    # Filter benchmarks.
    bench_specs = [
        b for b in cfg["benchmarks"]
        if not name_filter or b["name"] in name_filter
    ]
    if not bench_specs:
        print(f"No benchmarks match filter {name_filter!r}", file=sys.stderr)
        return 2

    # Build all artifacts up front (per language). Skip languages without a
    # toolchain — they will be reported as 'skipped' rather than failing.
    artifacts: dict[tuple[str, str], builder.BuildArtifact] = {}
    if not args.no_build:
        print("\nBuilding benchmark artifacts ...")
    for spec in bench_specs:
        name = spec["name"]
        category = spec["category"]
        for lang in languages:
            tc = toolchains.get(lang)
            if not tc or not tc.available:
                continue
            try:
                if args.no_build:
                    out_bin = builder.build_dir(lang, name) / name
                    if lang == "python":
                        # Python has no build step; just resolve the source.
                        py_src = (builder.benchmark_dir(category, name)
                                  / f"{name}.py")
                        if py_src.exists() and tc.binary:
                            artifacts[(lang, name)] = builder.BuildArtifact(
                                language=lang, benchmark=name,
                                command=[tc.binary, str(py_src)], source=py_src,
                            )
                    elif out_bin.exists():
                        artifacts[(lang, name)] = builder.BuildArtifact(
                            language=lang, benchmark=name,
                            command=[str(out_bin)], source=out_bin,
                        )
                    continue
                art = builder.build_one(lang, category, name, tc)
                if art is not None:
                    artifacts[(lang, name)] = art
                    print(f"  [{lang:7s}] {name:14s} OK")
            except builder.BuildError as e:
                print(f"  [{lang:7s}] {name:14s} BUILD FAILED")
                # Stash the build error so it surfaces in the report.
                artifacts[(lang, name)] = None  # type: ignore[assignment]
                # Save the log alongside other results for inspection.
                _save_build_log(lang, name, e.log)

    # Execute.
    print("\nRunning benchmarks ...")
    benchmarks_out: list[dict] = []
    for spec in bench_specs:
        name = spec["name"]
        results: dict[str, dict] = {}
        for lang in languages:
            art = artifacts.get((lang, name))
            tc = toolchains.get(lang)
            if not tc or not tc.available:
                continue  # skipped — won't appear, reporter shows "skipped"
            if art is None:
                # build failed
                results[lang] = _outcome_to_jsonable(
                    RunOutcome(
                        language=lang, benchmark=name, success=False,
                        error="build failed (see perf/results/build_*.log)",
                    )
                )
                continue
            print(f"  [{lang:7s}] {name:14s} ...", end=" ", flush=True)
            outcome = run_benchmark(
                art, spec.get("args", []),
                warmup=warmup, iterations=iterations,
            )
            if outcome.success and outcome.summary:
                print(f"min={outcome.summary.minimum:8.2f} ms"
                      f"  median={outcome.summary.median:8.2f} ms")
            else:
                print(f"FAILED ({outcome.error.splitlines()[0][:60]})")
            results[lang] = _outcome_to_jsonable(outcome)
        benchmarks_out.append({**spec, "results": results})

    # Persist raw JSON.
    Path(args.results_json).parent.mkdir(parents=True, exist_ok=True)
    raw = {
        "config": {
            "warmup": warmup,
            "iterations": iterations,
            "languages": languages,
            "filter": sorted(name_filter),
        },
        "host": env.host_summary(),
        "toolchains": {k: asdict(v) for k, v in toolchains.items()},
        "benchmarks": benchmarks_out,
    }
    with open(args.results_json, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2)
    print(f"\nRaw results -> {args.results_json}")

    # Render Markdown.
    report = reporter.build_report(
        config=raw["config"],
        host=raw["host"],
        toolchains=raw["toolchains"],
        benchmarks=benchmarks_out,
    )
    md = reporter.render(report)
    Path(args.output).write_text(md, encoding="utf-8")
    print(f"Report      -> {args.output}")

    # Write the bar chart as a sibling SVG file. GitHub-flavored markdown
    # sanitises raw inline `<svg>` blocks but does render linked SVG via an
    # image reference, so the chart is kept as a separate file.
    out_dir = Path(args.output).parent
    chart_path = out_dir / reporter.CHART_FILENAME
    chart_svg = reporter.summary_chart(report)
    if chart_svg:
        chart_path.write_text(chart_svg, encoding="utf-8")
        print(f"Chart       -> {chart_path}")
    # Per-group charts: one for the original "core" 16 benchmarks and one
    # for the additional "extended" 16 benchmarks. Skipped silently when
    # the catalog has no benchmarks in the corresponding group.
    for group, fname in (
        ("core", reporter.CHART_FILENAME_CORE),
        ("extended", reporter.CHART_FILENAME_EXTENDED),
    ):
        svg = reporter.summary_chart(report, chart_group=group)
        if svg:
            (out_dir / fname).write_text(svg, encoding="utf-8")
            print(f"Chart       -> {out_dir / fname}")

    # Exit non-zero only if every measured run failed (so CI can detect total
    # breakage, but individual missing toolchains are tolerated).
    any_success = any(
        any(r.get("success") for r in b["results"].values())
        for b in benchmarks_out
    )
    return 0 if any_success else 1


def _save_build_log(lang: str, name: str, log: str) -> None:
    out_dir = _HERE / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"build_{lang}_{name}.log").write_text(log, encoding="utf-8")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        raise SystemExit(130)
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        raise SystemExit(2)
