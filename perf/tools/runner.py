"""Run benchmark artifacts and collect timing samples.

Each implementation must print, as the last two non-empty lines of stdout:

  CHECKSUM:<string>
  ELAPSED_MS:<float>

The runner enforces this contract, verifies CHECKSUMs across implementations of
the same benchmark, and aggregates ELAPSED_MS samples through ``stats``.
"""
from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass, field
from typing import Iterable

from .builder import BuildArtifact
from .stats import Summary, summarize


@dataclass
class RunOutcome:
    """Per-language result for one benchmark."""

    language: str
    benchmark: str
    success: bool
    samples_ms: list[float] = field(default_factory=list)
    summary: Summary | None = None
    checksum: str = ""
    error: str = ""
    raw_output: list[str] = field(default_factory=list)


_PROCESS_HARD_TIMEOUT_S = 600  # safety net per individual run


def _parse(output: str) -> tuple[str, float]:
    elapsed: float | None = None
    checksum: str | None = None
    for line in reversed(output.strip().splitlines()):
        line = line.strip()
        if not line:
            continue
        if elapsed is None and line.startswith("ELAPSED_MS:"):
            elapsed = float(line.split(":", 1)[1].strip())
        elif checksum is None and line.startswith("CHECKSUM:"):
            checksum = line.split(":", 1)[1].strip()
        if elapsed is not None and checksum is not None:
            break
    if elapsed is None or checksum is None:
        raise ValueError(
            "implementation did not emit ELAPSED_MS / CHECKSUM lines; got:\n"
            + output[-1000:]
        )
    return checksum, elapsed


def _execute(cmd: list[str]) -> str:
    start = time.monotonic()
    res = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
        timeout=_PROCESS_HARD_TIMEOUT_S,
    )
    elapsed = time.monotonic() - start
    if res.returncode != 0:
        raise RuntimeError(
            f"command exited with status {res.returncode} after {elapsed:.2f}s\n"
            f"cmd: {cmd}\nstdout:\n{res.stdout}\nstderr:\n{res.stderr}"
        )
    return res.stdout


def run_benchmark(
    artifact: BuildArtifact,
    args: Iterable[str],
    *,
    warmup: int,
    iterations: int,
) -> RunOutcome:
    args_list = list(args)
    cmd = artifact.run_command(args_list)
    outcome = RunOutcome(
        language=artifact.language, benchmark=artifact.benchmark, success=False
    )
    raw: list[str] = []
    try:
        # Warmup runs are not measured but still validated.
        for _ in range(max(0, warmup)):
            out = _execute(cmd)
            checksum, _elapsed = _parse(out)
            outcome.checksum = checksum
            raw.append(out)

        # Measurement runs.
        samples: list[float] = []
        last_checksum = outcome.checksum
        for _ in range(max(1, iterations)):
            out = _execute(cmd)
            checksum, elapsed = _parse(out)
            raw.append(out)
            if last_checksum and checksum != last_checksum:
                raise RuntimeError(
                    f"checksum drift between runs: {last_checksum!r} vs {checksum!r}"
                )
            last_checksum = checksum
            samples.append(elapsed)
        outcome.checksum = last_checksum
        outcome.samples_ms = samples
        outcome.summary = summarize(samples)
        outcome.success = True
    except (RuntimeError, ValueError, subprocess.TimeoutExpired, OSError) as exc:
        outcome.error = str(exc)
    finally:
        outcome.raw_output = raw[-3:]  # keep last few outputs only
    return outcome
