from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_readme_references_existing_scripts() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "scripts/check_env.py" not in readme
    assert "scripts/run_one.py" not in readme
    assert (REPO_ROOT / "scripts" / "run_benchmark.py").is_file()
    assert (REPO_ROOT / "scripts" / "run_all.py").is_file()
    assert (REPO_ROOT / "scripts" / "make_aaai_supplement.py").is_file()
    assert (REPO_ROOT / "tools" / "anonymize_scan.py").is_file()


def test_example_configs_are_yaml() -> None:
    for name in [
        "model.example.yaml",
        "sage_gate.example.yaml",
        "skillopt_strict_gate.example.yaml",
    ]:
        path = REPO_ROOT / "configs" / name
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(loaded, dict)


def test_reproduction_doc_lists_all_benchmarks() -> None:
    text = (REPO_ROOT / "docs" / "reproduction.md").read_text(encoding="utf-8")

    for benchmark in [
        "spreadsheetbench",
        "livemath",
        "searchqa",
        "officeqa",
        "alfworld",
    ]:
        assert benchmark in text


def test_aaai_docs_and_homepage_are_present() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    aaai = (REPO_ROOT / "AAAI_REPRODUCIBILITY.md").read_text(encoding="utf-8")
    guide = (REPO_ROOT / "docs" / "reviewer_guide.md").read_text(encoding="utf-8")
    homepage = (REPO_ROOT / "index.html").read_text(encoding="utf-8")

    assert "AAAI_REPRODUCIBILITY.md" in readme
    assert "docs/reviewer_guide.md" in readme
    assert "python scripts/make_aaai_supplement.py" in readme
    assert "Statistical test" in aaai
    assert "15-Minute Smoke Test" in guide
    assert "http://" not in homepage
    assert "https://" not in homepage
    assert "SAGE Reproduction Package" in homepage


def test_aaai_supplement_dry_run_excludes_public_web_pages() -> None:
    script = REPO_ROOT / "scripts" / "make_aaai_supplement.py"
    result = subprocess.run(
        [sys.executable, str(script), "--dry-run"],
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    manifest = json.loads(result.stdout)
    assert "SkillOpt/index.html" in manifest["excluded"]
    assert "SkillOpt/skillopt.html" in manifest["excluded"]
    assert "SkillOpt/README.md" in manifest["included"]
    assert "SkillOpt/README.md" in manifest["overlays"]
    assert "SkillOpt/pyproject.toml" in manifest["overlays"]
