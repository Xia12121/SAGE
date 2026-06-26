import importlib
import json
import sys
from pathlib import Path

import pytest

from benchmarks.common import run_benchmark
from benchmarks.common.schema import load_spec


REPO_ROOT = Path(__file__).resolve().parents[1]

BENCHMARKS = {
    "spreadsheetbench": {
        "task_file": "data/raw/spreadsheetbench/tasks.jsonl",
        "output_dir": "outputs/spreadsheetbench",
        "module": "benchmarks.spreadsheetbench.launch",
    },
    "livemath": {
        "task_file": "data/raw/livemath/tasks.jsonl",
        "output_dir": "outputs/livemath",
        "module": "benchmarks.livemath.launch",
    },
    "searchqa": {
        "task_file": "data/raw/searchqa/tasks.jsonl",
        "output_dir": "outputs/searchqa",
        "module": "benchmarks.searchqa.launch",
    },
    "officeqa": {
        "task_file": "data/raw/officeqa/tasks.jsonl",
        "output_dir": "outputs/officeqa",
        "module": "benchmarks.officeqa.launch",
    },
    "alfworld": {
        "task_file": "data/raw/alfworld/tasks.jsonl",
        "output_dir": "outputs/alfworld",
        "module": "benchmarks.alfworld.launch",
    },
}


def _spec_path(benchmark: str) -> Path:
    return REPO_ROOT / "benchmarks" / benchmark / "spec.json"


@pytest.mark.parametrize(("benchmark", "expected"), BENCHMARKS.items())
def test_benchmark_spec_matches_launcher_contract(benchmark, expected):
    spec = load_spec(_spec_path(benchmark))

    assert spec.name == benchmark
    assert spec.task_file == expected["task_file"]
    assert spec.output_dir == expected["output_dir"]
    assert spec.command == [
        "<python>",
        "-m",
        expected["module"],
        "--tasks",
        expected["task_file"],
        "--output-dir",
        expected["output_dir"],
    ]
    assert spec.env == {}
    assert spec.description


def test_benchmark_specs_dry_run_write_manifests_in_temp_outputs(tmp_path, capsys):
    for benchmark in BENCHMARKS:
        spec = load_spec(_spec_path(benchmark))
        temp_output = tmp_path / benchmark
        temp_spec_path = tmp_path / f"{benchmark}.json"
        temp_spec_path.write_text(
            json.dumps(
                {
                    "name": spec.name,
                    "task_file": spec.task_file,
                    "output_dir": str(temp_output),
                    "command": spec.command,
                    "env": spec.env,
                    "description": spec.description,
                }
            ),
            encoding="utf-8",
        )

        exit_code = run_benchmark.main([str(temp_spec_path), "--dry-run"])

        expected_command = [sys.executable, *spec.command[1:]]
        assert exit_code == 0
        assert json.loads(capsys.readouterr().out) == expected_command
        manifest = temp_output / "launch_manifest.json"
        assert json.loads(manifest.read_text(encoding="utf-8")) == {
            "benchmark": spec.name,
            "command": expected_command,
            "env": spec.env,
            "dry_run": True,
        }


@pytest.mark.parametrize(("benchmark", "expected"), BENCHMARKS.items())
def test_benchmark_launcher_accepts_task_and_output_arguments(benchmark, expected, capsys):
    launcher = importlib.import_module(expected["module"])

    exit_code = launcher.main(["--tasks", "custom/tasks.jsonl", "--output-dir", "custom/output"])

    assert exit_code == 0
    output = capsys.readouterr().out
    assert benchmark in output
    assert "custom/tasks.jsonl" in output
