from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class BenchmarkSpec:
    name: str
    task_file: str
    output_dir: str
    command: list[str]
    env: dict[str, str]
    description: str


def load_spec(path: Path) -> BenchmarkSpec:
    data = json.loads(path.read_text(encoding="utf-8"))
    return BenchmarkSpec(**data)
