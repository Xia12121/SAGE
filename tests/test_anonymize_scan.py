from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "anonymize_scan.py"


def _scan(*paths: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(path) for path in paths)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_clean_temp_file_passes(tmp_path: Path) -> None:
    clean_file = tmp_path / "clean.txt"
    clean_file.write_text("public reproduction notes\n", encoding="utf-8")

    result = _scan(clean_file)

    assert result.returncode == 0
    assert result.stdout == ""


def test_split_constructed_private_marker_is_detected(tmp_path: Path) -> None:
    private_marker = "DEEP" + "SEEK" + "_" + "KEY"
    leak_file = tmp_path / "leak.txt"
    leak_file.write_text(f"credential={private_marker}\n", encoding="utf-8")

    result = _scan(leak_file)

    assert result.returncode == 1
    assert f"{leak_file}: private marker" in result.stdout


def test_private_marker_matching_is_case_and_slash_normalized(tmp_path: Path) -> None:
    leak_file = tmp_path / "path-leak.txt"
    private_path = "C:/" + "Users" + "/name"
    leak_file.write_text(f"path={private_path}\n", encoding="utf-8")

    result = _scan(leak_file)

    assert result.returncode == 1
    assert f"{leak_file}: private marker" in result.stdout


def test_public_api_key_variable_names_are_allowed(tmp_path: Path) -> None:
    config_file = tmp_path / "config.py"
    config_file.write_text(
        "API" + "_KEY = os.environ.get('SERVICE_" + "API" + "_KEY', '')\n",
        encoding="utf-8",
    )

    result = _scan(config_file)

    assert result.returncode == 0
    assert result.stdout == ""


def test_secret_like_values_are_detected(tmp_path: Path) -> None:
    leak_file = tmp_path / "secret.txt"
    secret_value = "sk-" + "a" * 24
    leak_file.write_text(f"token={secret_value}\n", encoding="utf-8")

    result = _scan(leak_file)

    assert result.returncode == 1
    assert f"{leak_file}: private marker" in result.stdout


def test_unix_home_path_is_detected(tmp_path: Path) -> None:
    leak_file = tmp_path / "home-leak.txt"
    leak_file.write_text("path=/ho" + "me/name/project\n", encoding="utf-8")

    result = _scan(leak_file)

    assert result.returncode == 1
    assert f"{leak_file}: private marker" in result.stdout


def test_result_artifact_filename_is_detected(tmp_path: Path) -> None:
    artifact_file = tmp_path / "summary.json"
    artifact_file.write_text("{}\n", encoding="utf-8")

    result = _scan(artifact_file)

    assert result.returncode == 1
    assert f"{artifact_file}: result artifact" in result.stdout


def test_result_artifact_directory_is_detected(tmp_path: Path) -> None:
    artifact_dir = tmp_path / "outputs"
    artifact_dir.mkdir()

    result = _scan(artifact_dir)

    assert result.returncode == 1
    assert f"{artifact_dir}: result artifact" in result.stdout


def test_binary_file_is_skipped(tmp_path: Path) -> None:
    private_marker = ("API" + "_" + "KEY").encode("ascii")
    binary_file = tmp_path / "binary.bin"
    binary_file.write_bytes(b"\x00\xff" + private_marker)

    result = _scan(binary_file)

    assert result.returncode == 0
    assert result.stdout == ""


def test_ignored_metadata_file_is_skipped(tmp_path: Path) -> None:
    private_marker = "SECRET" + "_" + "KEY"
    metadata_file = tmp_path / ".git"
    metadata_file.write_text(private_marker, encoding="utf-8")

    result = _scan(tmp_path)

    assert result.returncode == 0
    assert result.stdout == ""


def test_internal_planning_notes_are_detected(tmp_path: Path) -> None:
    note_dir = tmp_path / "docs" / ("super" + "powers") / "plans"
    note_dir.mkdir(parents=True)
    note = note_dir / "implementation.md"
    note.write_text("internal task breakdown\n", encoding="utf-8")

    result = _scan(tmp_path)

    assert result.returncode == 1
    assert "internal planning note" in result.stdout
