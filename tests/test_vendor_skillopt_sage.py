from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from sage.gate import GateAction, sage_accept


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLOPT_ROOT = REPO_ROOT / "SkillOpt"


def _import_vendor_skillopt(monkeypatch):
    monkeypatch.syspath_prepend(str(SKILLOPT_ROOT))
    return __import__("skillopt.evaluation.gate", fromlist=["gate_result_for_action"])


def test_vendor_gate_result_for_action_matches_skillopt_state(monkeypatch):
    gate_module = _import_vendor_skillopt(monkeypatch)

    result = gate_module.gate_result_for_action(
        "accept_new_best",
        candidate_skill="candidate",
        cand_score=0.75,
        current_skill="current",
        current_score=0.5,
        best_skill="best",
        best_score=0.6,
        best_step=2,
        global_step=3,
    )

    assert result.action == "accept_new_best"
    assert result.current_skill == "candidate"
    assert result.best_skill == "candidate"
    assert result.best_score == 0.75
    assert result.best_step == 3


def test_vendor_config_flattens_sage_gate_options(monkeypatch):
    monkeypatch.syspath_prepend(str(SKILLOPT_ROOT))
    config_module = __import__("skillopt.config", fromlist=["flatten_config"])

    flat = config_module.flatten_config(
        {
            "evaluation": {
                "gate_select": "sage",
                "sage_alpha": 1.0,
                "sage_loss_weight": 1.0,
                "sage_regression_tau": 1.0,
            }
        }
    )

    assert flat["gate_select"] == "sage"
    assert flat["sage_alpha"] == 1.0
    assert flat["sage_loss_weight"] == 1.0
    assert flat["sage_regression_tau"] == 1.0


def test_vendor_trainer_imports_from_skillopt_directory():
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)

    result = subprocess.run(
        [sys.executable, "-c", "import skillopt.engine.trainer"],
        cwd=SKILLOPT_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_vendor_selection_items_snapshot_round_trips_for_resume(monkeypatch):
    monkeypatch.syspath_prepend(str(SKILLOPT_ROOT))
    trainer_module = __import__(
        "skillopt.engine.trainer",
        fromlist=["_coerce_selection_items", "_selection_items_snapshot"],
    )

    snapshot = trainer_module._selection_items_snapshot(
        {"skill-hash": {"x1": 1, 2: "0.25"}}
    )

    assert snapshot == {"skill-hash": {"x1": 1.0, "2": 0.25}}
    assert trainer_module._coerce_selection_items(snapshot["skill-hash"]) == {
        "x1": 1.0,
        "2": 0.25,
    }


def test_vendor_slow_update_gate_uses_sage_route():
    text = (SKILLOPT_ROOT / "skillopt" / "engine" / "trainer.py").read_text(
        encoding="utf-8"
    )

    assert 'slow_result["sage_gate"]' in text
    assert 'if gate_select == "sage":' in text
    assert "slow_sage_payload" in text


def test_sage_parameters_recover_strict_paired_baseline():
    result = sage_accept(
        {"a": 1.0, "b": 1.0, "c": 0.0},
        {"a": 0.0, "b": 1.0, "c": 0.0},
        alpha=1.0,
        lam=1.0,
        tau=1.0,
    )

    assert result.action == GateAction.COMMIT
    assert result.ledger.wins == 1
    assert result.ledger.losses == 0


def test_vendor_skillopt_excludes_old_exploratory_branches():
    text = (SKILLOPT_ROOT / "skillopt" / "engine" / "trainer.py").read_text(
        encoding="utf-8"
    )

    forbidden = [
        "beam_proposal",
        "dual_evidence",
        "curriculum_mode",
        "qd.",
    ]
    assert not any(token in text for token in forbidden)


def test_vendor_preserves_upstream_tracked_support_files():
    expected = [
        "ckpt/README.md",
        "ckpt/alfworld/gpt5.5_skill.md",
        "ckpt/docvqa/gpt5.5_skill.md",
        "ckpt/livemath/gpt5.5_skill.md",
        "ckpt/officeqa/gpt5.5_skill.md",
        "ckpt/searchqa/gpt5.5_skill.md",
        "ckpt/spreadsheetbench/gpt5.5_skill.md",
        "data/searchqa_id_split/test/test.json",
        "data/searchqa_id_split/train/train.json",
        "data/searchqa_id_split/val/sel.json",
    ]

    missing = [path for path in expected if not (SKILLOPT_ROOT / path).exists()]

    assert missing == []
