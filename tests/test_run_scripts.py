from __future__ import annotations

import subprocess
from pathlib import Path

from benchmarks.common import run_benchmark as common_runner
from scripts import run_all
from scripts import run_benchmark


REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARKS = [
    "spreadsheetbench",
    "livemath",
    "searchqa",
    "officeqa",
    "alfworld",
]


def _spec_path(benchmark: str) -> str:
    return str(REPO_ROOT / "benchmarks" / benchmark / "spec.json")


def test_run_benchmark_delegates_selected_spec_and_dry_run(monkeypatch) -> None:
    calls: list[list[str]] = []

    def capture(argv: list[str]) -> int:
        calls.append(argv)
        return 0

    monkeypatch.setattr(common_runner, "main", capture)

    exit_code = run_benchmark.main(["livemath", "--dry-run"])

    assert exit_code == 0
    assert calls == [[_spec_path("livemath"), "--dry-run"]]


def test_run_all_delegates_all_benchmarks_in_order_with_dry_run(monkeypatch) -> None:
    calls: list[list[str]] = []

    def capture(argv: list[str]) -> int:
        calls.append(argv)
        return 0

    monkeypatch.setattr(common_runner, "main", capture)

    exit_code = run_all.main(["--dry-run"])

    assert exit_code == 0
    assert calls == [[_spec_path(benchmark), "--dry-run"] for benchmark in BENCHMARKS]


def test_run_all_stops_on_nonzero_and_returns_that_code(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fail_on_searchqa(argv: list[str]) -> int:
        calls.append(argv)
        if argv[0] == _spec_path("searchqa"):
            return 17
        return 0

    monkeypatch.setattr(common_runner, "main", fail_on_searchqa)

    exit_code = run_all.main([])

    assert exit_code == 17
    assert calls == [[_spec_path(benchmark)] for benchmark in BENCHMARKS[:3]]


def test_run_benchmark_translates_called_process_error(monkeypatch) -> None:
    def fail(argv: list[str]) -> int:
        raise subprocess.CalledProcessError(returncode=23, cmd=argv)

    monkeypatch.setattr(common_runner, "main", fail)

    assert run_benchmark.main(["officeqa"]) == 23


def test_run_all_translates_called_process_error_and_stops(monkeypatch) -> None:
    calls: list[list[str]] = []

    def fail_on_searchqa(argv: list[str]) -> int:
        calls.append(argv)
        if argv[0] == _spec_path("searchqa"):
            raise subprocess.CalledProcessError(returncode=29, cmd=argv)
        return 0

    monkeypatch.setattr(common_runner, "main", fail_on_searchqa)

    assert run_all.main([]) == 29
    assert calls == [[_spec_path(benchmark)] for benchmark in BENCHMARKS[:3]]
