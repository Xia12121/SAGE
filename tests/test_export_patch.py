from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_export_patch_rejects_plain_vendored_directory(tmp_path: Path) -> None:
    repo = tmp_path / "outer"
    repo.mkdir()
    subprocess.run(["git", "init", str(repo)], check=True, stdout=subprocess.PIPE)
    vendored = repo / "SkillOpt"
    vendored.mkdir()
    out = tmp_path / "patches" / "sage_gate.patch"
    script = Path(__file__).resolve().parents[1] / "scripts" / "export_patch.py"

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--skillopt",
            str(vendored),
            "--out",
            str(out),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode != 0
    assert "Git worktree root" in result.stderr
    assert not out.exists()
