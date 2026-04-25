"""Toolchain detection helpers."""
from __future__ import annotations

import platform
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class Toolchain:
    """Information about a single language toolchain."""

    language: str            # 'cangjie' / 'python' / 'cpp'
    available: bool
    binary: str | None       # path to compiler / interpreter actually used
    version: str             # short version string (or 'not found')

    def short(self) -> str:
        return f"{self.language:8s} : {'OK ' if self.available else 'N/A'}  {self.version}"


def _run_version(cmd: list[str]) -> str:
    try:
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10, check=False
        )
        text = (out.stdout or "") + (out.stderr or "")
        first = text.strip().splitlines()[0] if text.strip() else ""
        return first[:120]
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def detect_python() -> Toolchain:
    binary = shutil.which("python3") or shutil.which("python")
    if not binary:
        return Toolchain("python", False, None, "not found")
    return Toolchain("python", True, binary, _run_version([binary, "--version"]))


def detect_cpp() -> Toolchain:
    # Prefer g++, fall back to clang++.
    for cand in ("g++", "clang++"):
        binary = shutil.which(cand)
        if binary:
            return Toolchain("cpp", True, binary, _run_version([binary, "--version"]))
    return Toolchain("cpp", False, None, "not found")


def detect_go() -> Toolchain:
    binary = shutil.which("go")
    if not binary:
        return Toolchain("go", False, None, "not found")
    return Toolchain("go", True, binary, _run_version([binary, "version"]))


def detect_rust() -> Toolchain:
    """Detect the Rust toolchain.

    We drive Rust builds with ``rustc`` directly (single-file ``-O`` builds)
    to mirror the flat ``<name>.cpp`` / ``<name>.go`` layout used elsewhere.
    """
    binary = shutil.which("rustc")
    if not binary:
        return Toolchain("rust", False, None, "not found")
    return Toolchain("rust", True, binary, _run_version([binary, "--version"]))


def detect_cangjie() -> Toolchain:
    """Detect the Cangjie toolchain.

    We require both ``cjc`` (compiler) and ``cjpm`` (project manager) because
    we drive Cangjie builds through ``cjpm build`` so that each benchmark's
    ``cjpm.toml`` (with ``compile-option = "-O2"`` under ``[package]``) applies.
    """
    cjc = shutil.which("cjc")
    cjpm = shutil.which("cjpm")
    if not cjc or not cjpm:
        missing = ", ".join(n for n, p in (("cjc", cjc), ("cjpm", cjpm)) if not p)
        return Toolchain(
            "cangjie", False, None,
            f"not found: {missing} (install Cangjie SDK; see project .resource)",
        )
    # Report the cjc version as the canonical version line.
    return Toolchain("cangjie", True, cjpm, _run_version([cjc, "--version"]))


def detect_all() -> dict[str, Toolchain]:
    return {
        "cangjie": detect_cangjie(),
        "cpp": detect_cpp(),
        "go": detect_go(),
        "rust": detect_rust(),
        "python": detect_python(),
    }


def host_summary() -> dict[str, str]:
    """Best-effort host description for the report."""
    info = {
        "os": f"{platform.system()} {platform.release()}",
        "machine": platform.machine(),
        "python": platform.python_version(),
    }
    # CPU model on Linux.
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("model name"):
                    info["cpu"] = line.split(":", 1)[1].strip()
                    break
    except OSError:
        pass
    info.setdefault("cpu", platform.processor() or "unknown")
    return info
