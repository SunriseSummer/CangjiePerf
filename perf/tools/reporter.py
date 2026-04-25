"""Render benchmark results into a human-readable Markdown report."""
from __future__ import annotations

import datetime as _dt
import math as _math
from typing import Any


_LANG_LABEL = {"cangjie": "Cangjie", "python": "Python", "cpp": "C++"}
_LANG_ORDER = ["cangjie", "cpp", "python"]
_LANG_COLOR = {
    "cangjie": "#d9534f",  # red
    "cpp":     "#5cb85c",  # green
    "python":  "#5bc0de",  # blue
}


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


def _summary_chart(report: dict[str, Any]) -> str:
    """Render a grouped log-scale bar chart of all benchmark timings as SVG.

    GitHub markdown renders inline SVG, so the chart is embedded directly in
    `report.md` and needs no images / external assets.
    """
    # Collect (benchmark_name, {lang: min_ms}) for benchmarks where at least
    # one language has a successful result.
    rows: list[tuple[str, dict[str, float]]] = []
    for bench in report["benchmarks"]:
        per_lang: dict[str, float] = {}
        for lang in _LANG_ORDER:
            r = bench["results"].get(lang)
            if r and r.get("success") and r.get("summary"):
                per_lang[lang] = r["summary"]["min_ms"]
        if per_lang:
            rows.append((bench["name"], per_lang))

    if not rows:
        return "_(no successful results — chart skipped)_"

    # Layout constants.
    n_groups = len(rows)
    n_langs = len(_LANG_ORDER)
    bar_w = 14
    bar_gap = 2
    group_w = n_langs * bar_w + (n_langs - 1) * bar_gap
    group_gap = 18
    plot_left = 60
    plot_right = 20
    plot_top = 50
    plot_bottom = 70
    plot_h = 240
    plot_w = n_groups * group_w + (n_groups - 1) * group_gap
    width = plot_left + plot_w + plot_right
    height = plot_top + plot_h + plot_bottom

    # Y axis: log10(ms). Anchor min/max to powers of ten so gridlines are nice.
    all_ms = [v for _, per in rows for v in per.values()]
    ymin_ms = max(min(all_ms), 0.001)
    ymax_ms = max(all_ms)
    log_min = _math.floor(_math.log10(ymin_ms))
    log_max = _math.ceil(_math.log10(ymax_ms))
    if log_max == log_min:
        log_max = log_min + 1

    def y_for(ms: float) -> float:
        ms = max(ms, 10 ** log_min)
        frac = (_math.log10(ms) - log_min) / (log_max - log_min)
        return plot_top + plot_h - frac * plot_h

    def label_for(power: int) -> str:
        ms = 10 ** power
        if ms >= 1000:
            return f"{ms / 1000:g} s"
        if ms >= 1:
            return f"{ms:g} ms"
        return f"{ms * 1000:g} µs"

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'width="100%" role="img" aria-label="Benchmark timings (log scale)" '
        f'font-family="-apple-system,Segoe UI,Helvetica,Arial,sans-serif" '
        f'font-size="11">'
    )
    parts.append(
        f'<rect x="0" y="0" width="{width}" height="{height}" '
        f'fill="#ffffff"/>'
    )
    # Title
    parts.append(
        f'<text x="{width/2:.1f}" y="22" text-anchor="middle" '
        f'font-size="14" font-weight="600" fill="#222">'
        f'Benchmark wall-clock time per implementation '
        f'(min of {report["config"]["iterations"]} runs, log scale, lower is better)'
        f'</text>'
    )
    # Legend
    legend_x = plot_left
    legend_y = 36
    for i, lang in enumerate(_LANG_ORDER):
        x = legend_x + i * 110
        parts.append(
            f'<rect x="{x}" y="{legend_y - 9}" width="12" height="12" '
            f'fill="{_LANG_COLOR[lang]}" rx="2"/>'
        )
        parts.append(
            f'<text x="{x + 18}" y="{legend_y + 1}" fill="#333">'
            f'{_LANG_LABEL[lang]}</text>'
        )

    # Y gridlines & labels.
    for power in range(int(log_min), int(log_max) + 1):
        y = y_for(10 ** power)
        parts.append(
            f'<line x1="{plot_left}" y1="{y:.1f}" '
            f'x2="{plot_left + plot_w}" y2="{y:.1f}" '
            f'stroke="#e5e5e5" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{plot_left - 6}" y="{y + 3:.1f}" '
            f'text-anchor="end" fill="#555">{label_for(power)}</text>'
        )
    # Axis lines.
    parts.append(
        f'<line x1="{plot_left}" y1="{plot_top}" '
        f'x2="{plot_left}" y2="{plot_top + plot_h}" '
        f'stroke="#888" stroke-width="1"/>'
    )
    parts.append(
        f'<line x1="{plot_left}" y1="{plot_top + plot_h}" '
        f'x2="{plot_left + plot_w}" y2="{plot_top + plot_h}" '
        f'stroke="#888" stroke-width="1"/>'
    )

    # Bars.
    for gi, (name, per_lang) in enumerate(rows):
        gx = plot_left + gi * (group_w + group_gap)
        baseline = plot_top + plot_h
        for li, lang in enumerate(_LANG_ORDER):
            bx = gx + li * (bar_w + bar_gap)
            if lang in per_lang:
                ms = per_lang[lang]
                top = y_for(ms)
                h = max(baseline - top, 1.0)
                parts.append(
                    f'<rect x="{bx:.1f}" y="{top:.1f}" '
                    f'width="{bar_w}" height="{h:.1f}" '
                    f'fill="{_LANG_COLOR[lang]}" rx="1">'
                    f'<title>{_LANG_LABEL[lang]} {name}: {_fmt_ms(ms)}</title>'
                    f'</rect>'
                )
            else:
                # Hatched placeholder for unavailable / failed languages.
                parts.append(
                    f'<rect x="{bx:.1f}" y="{baseline - 3}" '
                    f'width="{bar_w}" height="3" fill="#cccccc" rx="1">'
                    f'<title>{_LANG_LABEL[lang]} {name}: missing</title>'
                    f'</rect>'
                )
        # Group label (rotated).
        cx = gx + group_w / 2
        ly = plot_top + plot_h + 8
        parts.append(
            f'<text x="{cx:.1f}" y="{ly:.1f}" text-anchor="end" fill="#333" '
            f'transform="rotate(-45 {cx:.1f},{ly:.1f})">{name}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


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
    lines.append("### Visual comparison")
    lines.append("")
    lines.append(
        "Each benchmark shows three side-by-side bars (Cangjie / C++ / Python). "
        "**Lower bars are faster.** Note the **logarithmic** y-axis: a one-step "
        "gridline difference is a 10× speed difference. Hover any bar to see "
        "its exact timing."
    )
    lines.append("")
    lines.append(_summary_chart(report))
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
