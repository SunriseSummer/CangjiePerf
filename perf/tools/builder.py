"""Build benchmark artifacts for each supported language.

Each benchmark directory layout:

  <benchmark>/
    cjpm.toml         # Cangjie package config (sets [profile.build] -O2)
    src/main.cj       # Cangjie implementation
    <name>.cpp        # C++ implementation     (built with `g++ -O2 -std=c++17`)
    <name>.py         # Python implementation  (run directly with `python3`)

C++ build artifacts go to ``perf/build/cpp/<benchmark>/<benchmark>``.
Cangjie binaries are produced by ``cjpm build`` into the benchmark's own
``target/release/bin/main`` (cjpm's default release output path).
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


def build_cangjie(category: str, name: str, tc: Toolchain) -> BuildArtifact | None:
    """Build a Cangjie benchmark via ``cjpm build``.

    The benchmark's ``cjpm.toml`` configures ``[profile.build] compile-option =
    "-O2"`` so this is equivalent to invoking ``cjc -O2`` but driven through
    the canonical project-manager workflow, matching how a real Cangjie
    project would be built and shipped.
    """
    bench_dir = benchmark_dir(category, name)
    toml = bench_dir / "cjpm.toml"
    src_main = bench_dir / "src" / "main.cj"
    if not toml.exists() or not src_main.exists() or not tc.available or not tc.binary:
        return None
    cmd = [tc.binary, "build"]
    res = subprocess.run(
        cmd, cwd=bench_dir, capture_output=True, text=True, check=False
    )
    if res.returncode != 0:
        msg = (res.stdout or "") + (res.stderr or "")
        raise BuildError(f"Cangjie build failed for {name}:\n{msg}", log=msg)
    # cjpm default release output: <project>/target/release/bin/main
    out_bin = bench_dir / "target" / "release" / "bin" / "main"
    if not out_bin.exists():
        # Fallback search (older / future cjpm versions may differ).
        candidates = list((bench_dir / "target").rglob("main"))
        candidates = [c for c in candidates if c.is_file() and "release" in c.parts]
        if not candidates:
            raise BuildError(
                f"Cangjie build for {name} succeeded but no executable was "
                f"found under {bench_dir / 'target'}"
            )
        out_bin = candidates[0]
    # Stage a copy under build/cangjie/<name>/<name> so the runner can locate
    # it predictably (and so cjpm clean from inside the project doesn't break
    # subsequent runs).
    staged = build_dir("cangjie", name) / name
    shutil.copy2(out_bin, staged)
    staged.chmod(0o755)
    return BuildArtifact("cangjie", name, [str(staged)], src_main,
                         build_log=(res.stdout + res.stderr).strip())


class BuildError(RuntimeError):
    def __init__(self, message: str, *, log: str = "") -> None:
        super().__init__(message)
        self.log = log


_BUILDERS = {
    "python": build_python,
    "cpp": build_cpp,
    "cangjie": build_cangjie,
}


def build_one(language: str, category: str, name: str, tc: Toolchain) -> BuildArtifact | None:
    builder = _BUILDERS.get(language)
    if not builder:
        raise ValueError(f"unknown language: {language}")
    return builder(category, name, tc)


def clean(language: str | None = None) -> None:
    """Remove staged artifacts. For Cangjie, also clean each benchmark's
    cjpm ``target/`` directory."""
    root = _project_root() / "build"
    if root.exists():
        if language is None:
            shutil.rmtree(root, ignore_errors=True)
        else:
            target = root / language
            if target.exists():
                shutil.rmtree(target, ignore_errors=True)
    if language in (None, "cangjie"):
        for toml in (_project_root() / "benchmarks").rglob("cjpm.toml"):
            shutil.rmtree(toml.parent / "target", ignore_errors=True)


__all__ = [
    "BuildArtifact",
    "BuildError",
    "build_one",
    "clean",
    "benchmark_dir",
]
