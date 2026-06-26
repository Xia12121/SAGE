"""Per-item paired evidence for SAGE."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

_CORRECT_THRESHOLD = 0.5


@dataclass(frozen=True)
class PairedLedger:
    """Paired comparison ledger for a candidate skill against an incumbent."""

    n: int
    wins: int
    losses: int
    ties: int
    incumbent_correct: int
    common_ids: tuple[str, ...]

    def discounted_gain(self, *, lam: float = 1.0) -> float:
        """Return wins minus lambda-weighted losses."""
        return float(self.wins) - float(lam) * float(self.losses)

    @property
    def regression_rate(self) -> float:
        """Fraction of incumbent-correct items broken by the candidate."""
        if self.incumbent_correct <= 0:
            return 0.0
        return self.losses / self.incumbent_correct


def _is_correct(value: float) -> bool:
    return float(value) > _CORRECT_THRESHOLD


def build_paired_ledger(
    candidate_items: Mapping[str, float],
    incumbent_items: Mapping[str, float],
) -> PairedLedger:
    """Build a paired wins/losses/ties ledger over the id intersection."""
    ids = tuple(sorted(set(candidate_items) & set(incumbent_items)))
    wins = losses = ties = incumbent_correct = 0
    for item_id in ids:
        cand_ok = _is_correct(candidate_items[item_id])
        inc_ok = _is_correct(incumbent_items[item_id])
        if inc_ok:
            incumbent_correct += 1
        if cand_ok and not inc_ok:
            wins += 1
        elif inc_ok and not cand_ok:
            losses += 1
        else:
            ties += 1
    return PairedLedger(
        n=len(ids),
        wins=wins,
        losses=losses,
        ties=ties,
        incumbent_correct=incumbent_correct,
        common_ids=ids,
    )
