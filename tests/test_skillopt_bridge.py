import pytest

from sage.skillopt_bridge import gate_action_from_sage, per_item_scores


def test_per_item_scores_stringifies_ids_and_defaults_missing_hard_scores():
    results = [
        {"id": "a", "hard": 1},
        {"id": 2, "hard": "0.25"},
        {"id": "none", "hard": None},
        {"id": 0, "hard": ""},
        {"id": "missing"},
        {"hard": 1},
    ]

    assert per_item_scores(results) == {
        "a": 1.0,
        "2": 0.25,
        "none": 0.0,
        "0": 0.0,
        "missing": 0.0,
    }


def test_per_item_scores_reads_result_objects():
    class Result:
        def __init__(self, item_id, hard):
            self.id = item_id
            self.hard = hard

    assert per_item_scores([Result("x1", 1), Result("x2", 0)]) == {
        "x1": 1.0,
        "x2": 0.0,
    }


@pytest.mark.parametrize(
    ("commit", "beats_best", "expected"),
    [
        (False, False, "reject"),
        (False, True, "reject"),
        (True, False, "accept"),
        (True, True, "accept_new_best"),
    ],
)
def test_gate_action_from_sage_maps_commit_and_best_flags(commit, beats_best, expected):
    assert gate_action_from_sage(commit=commit, beats_best=beats_best) == expected
