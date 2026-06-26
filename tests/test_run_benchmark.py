import json
import subprocess
import sys
from pathlib import Path

from benchmarks.common import run_benchmark


def test_dry_run_writes_launch_manifest_without_executing(tmp_path, monkeypatch, capsys):
    output_dir = tmp_path / "outputs"
    spec_path = tmp_path / "spec.json"
    command = ["python", "-c", "print('should not run')"]
    spec_path.write_text(
        json.dumps(
            {
                "name": "dry-run-demo",
                "task_file": "tasks/demo.jsonl",
                "output_dir": str(output_dir),
                "command": command,
                "env": {"DEMO_ENV": "1"},
                "description": "Demo dry run",
            }
        ),
        encoding="utf-8",
    )

    def fail_if_called(*args, **kwargs):
        raise AssertionError("subprocess.run should not be called for dry runs")

    monkeypatch.setattr(run_benchmark.subprocess, "run", fail_if_called)

    exit_code = run_benchmark.main([str(spec_path), "--dry-run"])

    assert exit_code == 0
    assert json.loads(capsys.readouterr().out) == command
    assert json.loads((output_dir / "launch_manifest.json").read_text(encoding="utf-8")) == {
        "benchmark": "dry-run-demo",
        "command": command,
        "env": {"DEMO_ENV": "1"},
        "dry_run": True,
    }


def test_relative_output_dir_resolves_against_repo_root(tmp_path, monkeypatch):
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(
        json.dumps(
            {
                "name": "relative-output",
                "task_file": "tasks/demo.jsonl",
                "output_dir": "outputs/test-relative-runner",
                "command": ["python", "-c", "print('should not run')"],
                "env": {},
                "description": "Relative output demo",
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    exit_code = run_benchmark.main([str(spec_path), "--dry-run"])

    assert exit_code == 0
    manifest = run_benchmark.REPO_ROOT / "outputs" / "test-relative-runner" / "launch_manifest.json"
    try:
        assert manifest.exists()
    finally:
        if manifest.exists():
            manifest.unlink()
        for directory in (manifest.parent, manifest.parent.parent):
            try:
                directory.rmdir()
            except OSError:
                pass


def test_run_benchmark_script_help_works_from_repo_root():
    script = Path(__file__).resolve().parents[1] / "benchmarks" / "common" / "run_benchmark.py"

    result = subprocess.run(
        [sys.executable, str(script), "--help"],
        cwd=run_benchmark.REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode == 0
    assert "spec_path" in result.stdout
