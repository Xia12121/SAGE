from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def _require_git_root(path: Path) -> Path:
    root = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    resolved_root = Path(root.stdout.strip()).resolve()
    resolved_path = path.resolve()
    if resolved_root != resolved_path:
        raise SystemExit(
            f"--skillopt must point at a SkillOpt Git worktree root, got {resolved_path}"
        )
    return resolved_root


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export a SkillOpt Git worktree diff as a patch file."
    )
    parser.add_argument("--skillopt", default="SkillOpt")
    parser.add_argument("--out", default="patches/skillopt/sage_gate.patch")
    args = parser.parse_args()

    skillopt = _require_git_root(Path(args.skillopt))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    diff = subprocess.run(
        ["git", "-C", str(skillopt), "diff", "--binary"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    out.write_text(diff.stdout, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
