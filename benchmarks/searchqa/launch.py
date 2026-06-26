from __future__ import annotations

import argparse
from typing import Sequence


BENCHMARK_NAME = "searchqa"
DEFAULT_TASKS = "data/raw/searchqa/tasks.jsonl"
DEFAULT_OUTPUT_DIR = "outputs/searchqa"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SearchQA launcher scaffold.")
    parser.add_argument("--tasks", default=DEFAULT_TASKS)
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args(argv)

    print(f"benchmark: {BENCHMARK_NAME}")
    print(f"tasks: {args.tasks}")
    print(f"output_dir: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
