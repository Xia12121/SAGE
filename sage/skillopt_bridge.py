"""Thin adapters between SkillOpt records and SAGE gate inputs."""
from __future__ import annotations


def per_item_scores(results: list[dict]) -> dict[str, float]:
    """Convert SkillOpt result rows into per-item hard scores."""
    scores: dict[str, float] = {}
    for row in results:
        if hasattr(row, "get"):
            item_id = row.get("id")
            hard = row.get("hard", 0.0)
        else:
            item_id = getattr(row, "id", None)
            hard = getattr(row, "hard", 0.0)
        if item_id is None:
            continue
        scores[str(item_id)] = float(hard or 0.0)
    return scores


def gate_action_from_sage(*, commit: bool, beats_best: bool) -> str:
    """Map SAGE commit and best-score flags onto SkillOpt gate actions."""
    if not commit:
        return "reject"
    if beats_best:
        return "accept_new_best"
    return "accept"
