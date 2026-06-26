from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

IGNORED_NAMES = {
    ".git",
    ".worktrees",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "venv",
    ".venv",
    "build",
    "dist",
}

ARTIFACT_NAMES = {
    "summary.json",
    "events.jsonl",
    "returned",
    "results",
    "outputs",
    "runs",
}


def _private_markers() -> tuple[str, ...]:
    return (
        "bo" + "x2",
        "deep" + "seek" + "_" + "key",
        "c:/u" + "sers",
        "/u" + "sers",
        "/ho" + "me/",
        "".join(chr(part) for part in (0x738B, 0x5955, 0x8C6A)),
    )


def _secret_value_patterns() -> tuple[re.Pattern[str], ...]:
    return (
        re.compile(r"\bsk-[a-z0-9][a-z0-9_-]{12,}", re.IGNORECASE),
        re.compile(r"\bsk-ant-[a-z0-9][a-z0-9_-]{12,}", re.IGNORECASE),
        re.compile(
            r"(api|secret|token)[_-]?key\s*[:=]\s*['\"]?[a-z0-9][a-z0-9_-]{20,}",
            re.IGNORECASE,
        ),
    )


def _is_ignored_name(path: Path) -> bool:
    name = path.name
    return name in IGNORED_NAMES or name.endswith(".egg-info")


def _is_artifact_name(path: Path) -> bool:
    name = path.name.lower()
    return name in ARTIFACT_NAMES or name.endswith(".docx")


def _is_internal_note(path: Path) -> bool:
    parts = tuple(part.lower() for part in path.parts)
    for index in range(len(parts) - 1):
        if parts[index] == "docs" and parts[index + 1] == "superpowers":
            return True
    return False


def _iter_entries(start: Path) -> list[Path]:
    if not start.exists() or _is_ignored_name(start):
        return []
    if start.is_file():
        return [start]
    if _is_artifact_name(start):
        return [start]

    entries: list[Path] = []
    for root, dirs, files in os.walk(start):
        root_path = Path(root)

        kept_dirs = []
        for dirname in dirs:
            dir_path = root_path / dirname
            if _is_ignored_name(dir_path):
                continue
            entries.append(dir_path)
            if not _is_artifact_name(dir_path):
                kept_dirs.append(dirname)
        dirs[:] = kept_dirs

        entries.extend(
            file_path
            for filename in files
            if not _is_ignored_name(file_path := root_path / filename)
        )

    return entries


def _read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None

    if b"\0" in data:
        return None

    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def scan(paths: list[Path]) -> list[tuple[Path, str]]:
    issues: list[tuple[Path, str]] = []
    private_markers = _private_markers()
    secret_value_patterns = _secret_value_patterns()

    for scan_path in paths:
        for path in _iter_entries(scan_path):
            if _is_internal_note(path):
                issues.append((path, "internal planning note"))
                if path.is_dir():
                    continue

            if _is_artifact_name(path):
                issues.append((path, "result artifact"))
                if path.is_dir():
                    continue

            if not path.is_file():
                continue

            text = _read_text(path)
            if text is None:
                continue

            normalized_text = text.replace(chr(92), "/").lower()
            if any(marker in normalized_text for marker in private_markers) or any(
                pattern.search(text) for pattern in secret_value_patterns
            ):
                issues.append((path, "private marker"))

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args(argv)

    paths = args.paths or [REPO_ROOT]
    issues = scan(paths)
    for path, label in issues:
        print(f"{_display_path(path)}: {label}")

    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
