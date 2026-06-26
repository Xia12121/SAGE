# SAGE Reproduction Package

This anonymous repository contains the process code for SAGE, a statistical acceptance gate for skill self-evolution. SAGE accepts a candidate skill only from per-item paired validation evidence, exact sign-test denoising, and regression accounting; with safeguards disabled it recovers the strict SkillOpt baseline gate. The repository includes the SAGE implementation, a vendored SkillOpt integration, five benchmark launchers, and zero-API tests.

This repository intentionally excludes measured results, run outputs, credentials, private machine details, and paper source files.

## Reviewer Entry Points

- `AAAI_REPRODUCIBILITY.md` maps AAAI checklist items to repository files.
- `docs/reviewer_guide.md` gives the 15-minute smoke test and full-run protocol.
- `docs/reproduction.md` describes the SAGE method protocol.
- `docs/repository_review.md` records the repository review and residual boundaries.
- `index.html` is a static GitHub Pages homepage for the public project page.

## Quick Start

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pytest -q
python tools/anonymize_scan.py
```

## Benchmark Launchers

```bash
python scripts/run_benchmark.py spreadsheetbench --dry-run
python scripts/run_benchmark.py livemath --dry-run
python scripts/run_benchmark.py searchqa --dry-run
python scripts/run_benchmark.py officeqa --dry-run
python scripts/run_benchmark.py alfworld --dry-run
python scripts/run_all.py --dry-run
```

## AAAI Blind-Review ZIP

Do not cite a mutable GitHub or web URL in the blind-review PDF. Create the static code appendix ZIP from tracked files:

```bash
python scripts/make_aaai_supplement.py
```

The archive is written to `dist/sage-aaai-code.zip` and excludes caches, outputs, local data, and nonessential public web pages.

## Vendored SkillOpt

```bash
cd SkillOpt
python -m pip install -e .
python -c "import skillopt.engine.trainer"
python scripts/train.py --config configs/searchqa/default.yaml --gate_select sage
```

Live model runs require local credentials derived from `configs/model.example.yaml`. Measured results and run bundles are intentionally not committed.
