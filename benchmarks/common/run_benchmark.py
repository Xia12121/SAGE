from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if __package__ in {None, ""}:
    sys.path.insert(0, str(REPO_ROOT))

from benchmarks.common.schema import load_spec


def _resolve_output_dir(output_dir: str) -> Path:
    path = Path(output_dir)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def _resolve_command(command: Sequence[str]) -> list[str]:
    resolved = list(command)
    if resolved and resolved[0] == "<python>":
        resolved[0] = sys.executable
    return resolved


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec_path", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    spec = load_spec(args.spec_path.resolve())
    command = _resolve_command(spec.command)
    output_dir = _resolve_output_dir(spec.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "benchmark": spec.name,
        "command": command,
        "env": spec.env,
        "dry_run": args.dry_run,
    }
    (output_dir / "launch_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    if args.dry_run:
        print(json.dumps(command))
        return 0

    subprocess.run(
        command,
        check=True,
        cwd=REPO_ROOT,
        env={**os.environ, **spec.env},
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
