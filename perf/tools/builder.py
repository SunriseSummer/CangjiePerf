"""Build benchmark artifacts for each supported language.

Each benchmark directory layout:

  <benchmark>/
    <name>.cj         # Cangjie implementation (built with ``cjc -O2``)
    <name>.cpp        # C++ implementation     (built with ``g++ -O2 -std=c++17``)
    <name>.rs         # Rust implementation    (built with ``rustc -O --edition=2021``)
    <name>.go         # Go implementation      (built with ``go build``)
    <name>.py         # Python implementation  (run directly with ``python3``)

All compiled language build artifacts go to ``perf/build/<language>/<benchmark>/<benchmark>``.
"""
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .env import Toolchain


CPP_FLAGS = ["-O2", "-std=c++17", "-pipe"]
# C++ requires the math library on Linux for some builds.
CPP_LINK_FLAGS = ["-lm"]

# Rust optimization flags. ``-O`` is the rustc shorthand for ``opt-level=3``,
# matching ``-O2`` semantics for our purposes (full optimizer pipeline,
# release-quality code).
RUST_FLAGS = ["-O", "--edition=2021"]


@dataclass
class BuildArtifact:
    """A single language-specific runnable for a benchmark."""

    language: str
    benchmark: str
    command: list[str]
    source: Path
    build_log: str = ""

    def run_command(self, args: list[str]) -> list[str]:
        return [*self.command, *args]


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def benchmark_dir(category: str, name: str) -> Path:
    return _project_root() / "benchmarks" / category / name


def build_dir(language: str, name: str) -> Path:
    out = _project_root() / "build" / language / name
    out.mkdir(parents=True, exist_ok=True)
    return out


def _src(category: str, name: str, suffix: str) -> Path | None:
    p = benchmark_dir(category, name) / f"{name}.{suffix}"
    return p if p.exists() else None


def build_python(category: str, name: str, tc: Toolchain) -> BuildArtifact | None:
    src = _src(category, name, "py")
    if not src or not tc.available or not tc.binary:
        return None
    return BuildArtifact("python", name, [tc.binary, str(src)], src)


def build_cpp(category: str, name: str, tc: Toolchain) -> BuildArtifact | None:
    src = _src(category, name, "cpp")
    if not src or not tc.available or not tc.binary:
        return None
    out_bin = build_dir("cpp", name) / name
    cmd = [tc.binary, *CPP_FLAGS, str(src), "-o", str(out_bin), *CPP_LINK_FLAGS]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        msg = (res.stdout or "") + (res.stderr or "")
        raise BuildError(f"C++ build failed for {name}:\n{msg}", log=msg)
    return BuildArtifact("cpp", name, [str(out_bin)], src,
                         build_log=(res.stdout + res.stderr).strip())


def build_go(category: str, name: str, tc: Toolchain) -> BuildArtifact | None:
    """Build a Go benchmark via ``go build`` with default release settings.

    Each benchmark has a single ``<name>.go`` file declaring ``package main``;
    we invoke ``go build -o <out> <src>``. The Go toolchain optimizes by
    default (no ``-N -l`` flags), matching the spirit of ``-O2`` for C++.
    """
    src = _src(category, name, "go")
    if not src or not tc.available or not tc.binary:
        return None
    out_bin = build_dir("go", name) / name
    cmd = [tc.binary, "build", "-o", str(out_bin), str(src)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        msg = (res.stdout or "") + (res.stderr or "")
        raise BuildError(f"Go build failed for {name}:\n{msg}", log=msg)
    return BuildArtifact("go", name, [str(out_bin)], src,
                         build_log=(res.stdout + res.stderr).strip())


def build_rust(category: str, name: str, tc: Toolchain) -> BuildArtifact | None:
    """Build a Rust benchmark by invoking ``rustc -O`` directly on a single
    source file. This mirrors the flat ``<name>.cpp`` / ``<name>.go`` layout
    used by the other native toolchains in this suite.
    """
    src = _src(category, name, "rs")
    if not src or not tc.available or not tc.binary:
        return None
    out_bin = build_dir("rust", name) / name
    cmd = [tc.binary, *RUST_FLAGS, str(src), "-o", str(out_bin)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        msg = (res.stdout or "") + (res.stderr or "")
        raise BuildError(f"Rust build failed for {name}:\n{msg}", log=msg)
    return BuildArtifact("rust", name, [str(out_bin)], src,
                         build_log=(res.stdout + res.stderr).strip())


def build_cangjie(category: str, name: str, tc: Toolchain) -> BuildArtifact | None:
    """Build a Cangjie benchmark via ``cjc -O2`` on a single source file.

    Each benchmark has a single ``<name>.cj`` file; we invoke
    ``cjc <name>.cj -O2 -o <out>`` directly, mirroring the flat
    ``<name>.cpp`` / ``<name>.go`` / ``<name>.rs`` layout used by the other
    native toolchains in this suite.
    """
    bench_dir = benchmark_dir(category, name)
    src = bench_dir / f"{name}.cj"
    if not src.exists() or not tc.available or not tc.binary:
        return None
    out_bin = build_dir("cangjie", name) / name
    cmd = [tc.binary, str(src), "-O2", "-o", str(out_bin)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        msg = (res.stdout or "") + (res.stderr or "")
        raise BuildError(f"Cangjie build failed for {name}:\n{msg}", log=msg)
    out_bin.chmod(0o755)
    return BuildArtifact("cangjie", name, [str(out_bin)], src,
                         build_log=(res.stdout + res.stderr).strip())


class BuildError(RuntimeError):
    def __init__(self, message: str, *, log: str = "") -> None:
        super().__init__(message)
        self.log = log


_BUILDERS = {
    "python": build_python,
    "cpp": build_cpp,
    "cangjie": build_cangjie,
    "go": build_go,
    "rust": build_rust,
}


def build_one(language: str, category: str, name: str, tc: Toolchain) -> BuildArtifact | None:
    builder = _BUILDERS.get(language)
    if not builder:
        raise ValueError(f"unknown language: {language}")
    return builder(category, name, tc)


def clean(language: str | None = None) -> None:
    """Remove staged build artifacts under ``perf/build/``."""
    root = _project_root() / "build"
    if root.exists():
        if language is None:
            shutil.rmtree(root, ignore_errors=True)
        else:
            target = root / language
            if target.exists():
                shutil.rmtree(target, ignore_errors=True)


__all__ = [
    "BuildArtifact",
    "BuildError",
    "build_one",
    "clean",
    "benchmark_dir",
]
