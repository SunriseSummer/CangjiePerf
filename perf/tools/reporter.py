"""Render benchmark results into a human-readable Markdown report."""
from __future__ import annotations

import datetime as _dt
from typing import Any


_LANG_LABEL = {"cangjie": "Cangjie", "python": "Python", "cpp": "C++"}
_LANG_ORDER = ["cangjie", "cpp", "python"]


def _fmt_ms(v: float) -> str:
    if v >= 1000:
        return f"{v/1000:.3f} s"
    if v >= 1:
        return f"{v:.2f} ms"
    return f"{v*1000:.2f} µs"


def _ratio(value: float, base: float) -> str:
    if base <= 0:
        return "—"
    return f"{value/base:.2f}×"


def _benchmark_table(bench: dict[str, Any]) -> str:
    """One per-benchmark table comparing languages."""
    rows = []
    # Header
    rows.append(
        "| Language | Status | min | median | mean | stddev | vs fastest | Checksum |"
    )
    rows.append(
        "|----------|--------|-----|--------|------|--------|------------|----------|"
    )

    successful = [
        r for r in bench["results"].values() if r.get("success") and r.get("summary")
    ]
    fastest_min = min((r["summary"]["min_ms"] for r in successful), default=0.0)

    for lang in _LANG_ORDER:
        res = bench["results"].get(lang)
        if not res:
            rows.append(
                f"| {_LANG_LABEL[lang]} | _skipped (toolchain unavailable)_ | — | — | — | — | — | — |"
            )
            continue
        if not res["success"]:
            err = (res.get("error") or "build/run failed").splitlines()[0][:80]
            rows.append(
                f"| {_LANG_LABEL[lang]} | ❌ {err} | — | — | — | — | — | — |"
            )
            continue
        s = res["summary"]
        ratio = _ratio(s["min_ms"], fastest_min) if fastest_min else "—"
        rows.append(
            f"| {_LANG_LABEL[lang]} | ✅ "
            f"| {_fmt_ms(s['min_ms'])} "
            f"| {_fmt_ms(s['median_ms'])} "
            f"| {_fmt_ms(s['mean_ms'])} "
            f"| {_fmt_ms(s['stddev_ms'])} "
            f"| {ratio} "
            f"| `{res.get('checksum','')[:24]}` |"
        )

    # Detect checksum disagreement.
    checksums = {r["checksum"] for r in successful if r.get("checksum")}
    notes = []
    if len(checksums) > 1:
        notes.append(
            "> ⚠️ **Checksum mismatch detected across implementations** — "
            "the implementations are not computing the same thing; treat the "
            "comparison as invalid until reconciled. Checksums: "
            + ", ".join(sorted(checksums))
        )
    return "\n".join(rows + ([""] + notes if notes else []))


def _summary_table(report: dict[str, Any]) -> str:
    """Top-level matrix: one row per benchmark, one column per language."""
    rows = ["| Benchmark | Category | " + " | ".join(_LANG_LABEL[l] for l in _LANG_ORDER)
            + " | Fastest |"]
    rows.append("|" + "---|" * (3 + len(_LANG_ORDER)))
    for bench in report["benchmarks"]:
        cells = []
        successful = []
        for lang in _LANG_ORDER:
            r = bench["results"].get(lang)
            if not r:
                cells.append("—")
            elif not r.get("success"):
                cells.append("❌")
            else:
                cells.append(_fmt_ms(r["summary"]["min_ms"]))
                successful.append((lang, r["summary"]["min_ms"]))
        if successful:
            best_lang, _ = min(successful, key=lambda kv: kv[1])
            fastest = _LANG_LABEL[best_lang]
        else:
            fastest = "—"
        rows.append(
            f"| **{bench['name']}** | {bench['category']} | "
            + " | ".join(cells)
            + f" | {fastest} |"
        )
    return "\n".join(rows)


def render(report: dict[str, Any]) -> str:
    cfg = report["config"]
    host = report["host"]
    tcs = report["toolchains"]

    lines: list[str] = []
    lines.append("# CangjiePerf Benchmark Report")
    lines.append("")
    lines.append(f"_Generated: {report['generated_at']}_")
    lines.append("")
    lines.append("## Environment")
    lines.append("")
    lines.append(f"- **OS**: {host.get('os','?')}")
    lines.append(f"- **Architecture**: {host.get('machine','?')}")
    lines.append(f"- **CPU**: {host.get('cpu','?')}")
    lines.append(f"- **Python**: {host.get('python','?')}")
    lines.append("")
    lines.append("## Toolchains")
    lines.append("")
    lines.append("| Language | Available | Version |")
    lines.append("|----------|-----------|---------|")
    for lang in _LANG_ORDER:
        tc = tcs.get(lang, {})
        ok = "✅" if tc.get("available") else "❌"
        ver = tc.get("version", "—")
        lines.append(f"| {_LANG_LABEL[lang]} | {ok} | {ver} |")
    lines.append("")
    lines.append("## Run Configuration")
    lines.append("")
    lines.append(f"- Warmup runs: **{cfg['warmup']}**")
    lines.append(f"- Measurement runs: **{cfg['iterations']}**")
    lines.append(
        f"- Languages enabled: **{', '.join(_LANG_LABEL[l] for l in cfg['languages'])}**"
    )
    lines.append(
        "- Reported metric: per-process self-timed wall-clock (`ELAPSED_MS`); "
        "**`min`** chosen as the headline number, lower is better."
    )
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(_summary_table(report))
    lines.append("")
    lines.append("## Per-benchmark Detail")
    lines.append("")
    for bench in report["benchmarks"]:
        lines.append(f"### {bench['name']} — {bench['title']}")
        lines.append("")
        lines.append(f"_Category_: `{bench['category']}` &nbsp;&nbsp;"
                     f"_Args_: `{ ' '.join(bench['args']) }`")
        lines.append("")
        lines.append(bench["description"])
        lines.append("")
        lines.append(_benchmark_table(bench))
        lines.append("")

    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "- Each implementation is invoked as a fresh OS process and measures its "
        "own hot-path execution using a monotonic clock, printing `ELAPSED_MS:<value>`. "
        "This excludes interpreter / runtime startup from the measurement."
    )
    lines.append(
        "- Each implementation also prints `CHECKSUM:<value>` of its computed "
        "result; the runner verifies all implementations of the same benchmark "
        "agree, otherwise the comparison is flagged as invalid."
    )
    lines.append(
        "- Per benchmark we run `warmup` unmeasured iterations, then `iterations` "
        "measured iterations and report **min / median / mean / stddev**. The "
        "_min_ is used for the headline ratio because it is the most robust "
        "estimate of best-case wall-clock cost when other system noise is present."
    )
    lines.append(
        "- Compiler flags: `g++ -O2 -std=c++17` for C++, `cjpm build` for "
        "Cangjie (each benchmark's `cjpm.toml` sets "
        "`[profile.build] compile-option = \"-O2\"`), CPython 3 for Python "
        "(no `-O`), all with no extra runtime tuning."
    )
    lines.append("")
    return "\n".join(lines)


def build_report(
    *,
    config: dict[str, Any],
    host: dict[str, str],
    toolchains: dict[str, dict[str, Any]],
    benchmarks: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
        "config": config,
        "host": host,
        "toolchains": toolchains,
        "benchmarks": benchmarks,
    }
