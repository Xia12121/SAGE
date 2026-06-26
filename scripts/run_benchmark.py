from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmarks.common import run_benchmark as common_runner


BENCHMARKS = (
    "spreadsheetbench",
    "livemath",
    "searchqa",
    "officeqa",
    "alfworld",
)


def _spec_path(benchmark: str) -> Path:
    return REPO_ROOT / "benchmarks" / benchmark / "spec.json"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run one benchmark from its repository spec."
    )
    parser.add_argument("benchmark", choices=BENCHMARKS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    delegated_argv = [str(_spec_path(args.benchmark))]
    if args.dry_run:
        delegated_argv.append("--dry-run")
    try:
        return common_runner.main(delegated_argv)
    except subprocess.CalledProcessError as exc:
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main())
