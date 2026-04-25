# Regex find-all — stdlib regex micro-benchmark.
#
# Generates a deterministic mixed text and counts occurrences of a fairly
# expressive pattern (date-like and word-like alternations) across N copies.
#
# Argument: REPEATS (default 4000).

import re
import sys
import time

PATTERN = r"(\d{4}-\d{2}-\d{2})|([A-Za-z]+@[a-z]+\.[a-z]+)|(\b[A-Z][a-z]{3,8}\b)"
SAMPLE = (
    "On 2024-03-21 Alice wrote to bob@example.com about the meeting. "
    "Charlie replied 2024-04-02 from charlie_99@dev.io with notes about "
    "Project Kingfisher. References: 1999-12-31, foo@bar.org, Madison."
)


def main() -> None:
    repeats = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    text = (SAMPLE + "\n") * repeats
    rx = re.compile(PATTERN)

    t0 = time.perf_counter_ns()
    cs = sum(1 for _ in rx.finditer(text))
    elapsed_ns = time.perf_counter_ns() - t0

    print(f"CHECKSUM:{cs}")
    print(f"ELAPSED_MS:{elapsed_ns / 1_000_000:.6f}")


if __name__ == "__main__":
    main()
