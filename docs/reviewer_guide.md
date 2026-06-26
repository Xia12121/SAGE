# Reviewer Guide

This guide gives a short path for checking the artifact without running live
models, followed by the commands needed for full reproduction.

## 15-Minute Smoke Test

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pytest -q
python tools/anonymize_scan.py
python scripts/run_all.py --dry-run
```

Expected behavior:

- tests pass without API credentials;
- the anonymization scan prints nothing;
- each benchmark launcher prints the command it would execute and writes a
  dry-run launch manifest under `outputs/`, which may be deleted afterward.

## Method Check

SAGE accepts candidate skills from paired validation evidence. The key code is:

- `sage/evidence.py`: builds the candidate-versus-incumbent item ledger;
- `sage/denoise.py`: exact one-sided sign test over non-tied paired outcomes;
- `sage/gate.py`: combines denoised gain, loss weighting, and regression rate;
- `sage/skillopt_bridge.py`: converts SkillOpt rollout rows into paired scores.

The strict SkillOpt recovery mode is exercised in
`tests/test_gate_baseline_recovery.py` and configured by
`configs/skillopt_strict_gate.example.yaml`.

## Benchmark Launchers

Each launcher has a JSON spec under `benchmarks/<name>/spec.json`.

```bash
python scripts/run_benchmark.py spreadsheetbench --dry-run
python scripts/run_benchmark.py livemath --dry-run
python scripts/run_benchmark.py searchqa --dry-run
python scripts/run_benchmark.py officeqa --dry-run
python scripts/run_benchmark.py alfworld --dry-run
```

Full runs expect task files under:

- `data/raw/spreadsheetbench/tasks.jsonl`
- `data/raw/livemath/tasks.jsonl`
- `data/raw/searchqa/tasks.jsonl`
- `data/raw/officeqa/tasks.jsonl`
- `data/raw/alfworld/tasks.jsonl`

These data paths are intentionally ignored by Git so reviewers can materialize
licensed datasets locally without committing them.

## SkillOpt Reproduction

The vendored SkillOpt integration is under `SkillOpt/`. Smoke-check it with:

```bash
cd SkillOpt
python -m pip install -e .
python -c "import skillopt.engine.trainer"
```

Enable SAGE in a SkillOpt training run with:

```bash
python scripts/train.py --config configs/searchqa/default.yaml --gate_select sage
```

Recover the strict SkillOpt baseline with:

```bash
python scripts/train.py --config configs/searchqa/default.yaml --gate_select strict
```

## Environment and Seeds

- Python: `>=3.10`.
- Zero-API tests: `pytest>=8.0`, `pyyaml>=6.0`.
- Full SkillOpt runs: see `SkillOpt/pyproject.toml`.
- Default random seeds: `seed: 42` and `split_seed: 42` in
  `SkillOpt/configs/_base_/default.yaml`.
- Default training knobs: `num_epochs: 4`, `batch_size: 40`,
  `minibatch_size: 8`, `merge_batch_size: 8`, `learning_rate: 4`.
- SAGE knobs: `sage_alpha: 0.05`, `sage_loss_weight: 1.0`,
  `sage_regression_tau: 1.0`.

## Blind-Review Appendix

Create the submitted ZIP with:

```bash
python scripts/make_aaai_supplement.py
```

The ZIP is written to `dist/sage-aaai-code.zip`. It is generated from tracked
files and excludes caches, outputs, local data, and nonessential public web
pages. Re-run `python tools/anonymize_scan.py` before submission.
