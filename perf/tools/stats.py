"""Lightweight statistics helpers for benchmark measurements (stdlib only)."""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Summary:
    n: int
    minimum: float
    maximum: float
    median: float
    mean: float
    stddev: float

    def as_dict(self) -> dict[str, float | int]:
        return {
            "n": self.n,
            "min_ms": self.minimum,
            "max_ms": self.maximum,
            "median_ms": self.median,
            "mean_ms": self.mean,
            "stddev_ms": self.stddev,
        }


def summarize(samples: list[float]) -> Summary:
    if not samples:
        raise ValueError("no samples to summarize")
    n = len(samples)
    s = sorted(samples)
    mid = n // 2
    median = s[mid] if n % 2 else 0.5 * (s[mid - 1] + s[mid])
    mean = math.fsum(s) / n
    if n > 1:
        variance = math.fsum((x - mean) ** 2 for x in s) / (n - 1)
        stddev = math.sqrt(variance)
    else:
        stddev = 0.0
    return Summary(
        n=n, minimum=s[0], maximum=s[-1], median=median, mean=mean, stddev=stddev
    )
