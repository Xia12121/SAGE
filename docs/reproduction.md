# Reproduction Protocol

This repository is a code-only reproduction package. It intentionally excludes measured results, run bundles, paper source, private paths, and credentials.

## Method

SAGE replaces scalar acceptance with a paired validation protocol:

- build a per-item candidate-versus-incumbent ledger on the shared selection split;
- count wins, losses, ties, incumbent-correct regressions, and common item ids;
- denoise candidate improvements with an exact one-sided sign test;
- accept only when denoised gain is positive and regression accounting passes;
- recover the strict SkillOpt baseline by using the strict gate path or by disabling SAGE safeguards with the documented recovery parameters.

## Benchmarks

The repository contains launcher specs for five benchmarks:

- `spreadsheetbench`
- `livemath`
- `searchqa`
- `officeqa`
- `alfworld`

Dry-run launchers write a launch manifest and do not call models:

```bash
python scripts/run_all.py --dry-run
```

Run one launcher:

```bash
python scripts/run_benchmark.py spreadsheetbench --dry-run
```

## SkillOpt

`SkillOpt/` is vendored from upstream `41012e2` plus the SAGE patch in `patches/skillopt/sage_gate.patch`. The patch is expected to apply cleanly with whitespace checks and to reconstruct the vendored tree exactly.

Smoke-check the vendored package:

```bash
cd SkillOpt
python -c "import skillopt.engine.trainer"
```

For live training, start from a benchmark config under `SkillOpt/configs/` and enable SAGE:

```bash
python scripts/train.py --config configs/searchqa/default.yaml --gate_select sage
```

Use `configs/model.example.yaml` as the template for local model credentials. Keep the filled copy untracked.

## Repository Checks

```bash
python -m pytest -q
python tools/anonymize_scan.py
```

