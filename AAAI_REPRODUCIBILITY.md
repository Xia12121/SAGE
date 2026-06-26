# AAAI Reproducibility Map

This file maps the repository to the AAAI-26 reproducibility and supplementary
material expectations. It is written for reviewers and for preparing the
blind-review code appendix.

## Submission Form

- Use the paper PDF for the official reproducibility checklist answers.
- For blind review, submit a static ZIP created by:

```bash
python scripts/make_aaai_supplement.py
```

- Do not point the submitted blind-review PDF to a mutable website or GitHub
  URL. The root `index.html` is intended for a post-review GitHub Pages project
  page and for local navigation after the repository is public.

## Checklist Mapping

| AAAI item | Repository evidence |
| --- | --- |
| Conceptual outline or pseudocode | `docs/reproduction.md`, `sage/evidence.py`, `sage/denoise.py`, `sage/gate.py` |
| Source code for the method | `sage/`, `SkillOpt/sage/`, `SkillOpt/skillopt/evaluation/gate.py`, `SkillOpt/skillopt/engine/trainer.py` |
| Source code for experiments | `SkillOpt/scripts/train.py`, `SkillOpt/scripts/eval_only.py`, `benchmarks/*/launch.py`, `scripts/run_benchmark.py`, `scripts/run_all.py` |
| Pre-processing and loaders | `SkillOpt/skillopt/envs/*/dataloader.py`, `SkillOpt/skillopt/envs/*/adapter.py` |
| Requirements and install commands | `pyproject.toml`, `requirements.txt`, `README.md`, `docs/reviewer_guide.md` |
| Randomness and seeds | `SkillOpt/configs/_base_/default.yaml` (`seed: 42`, `split_seed: 42`) |
| Metrics and motivation | `docs/reproduction.md`, `docs/reviewer_guide.md`, `SkillOpt/skillopt/utils/scoring.py`, `SkillOpt/skillopt/evaluation/gate.py` |
| Hyperparameters | `SkillOpt/configs/_base_/default.yaml`, `configs/sage_gate.example.yaml`, `configs/skillopt_strict_gate.example.yaml` |
| Statistical test | `sage/denoise.py`, `sage/gate.py`, `tests/test_denoise.py`, `tests/test_gate_baseline_recovery.py` |
| Data availability | `docs/reviewer_guide.md`; benchmark launchers expect user-materialized `data/raw/*` paths |
| Anonymous supplementary material | `tools/anonymize_scan.py`, `scripts/make_aaai_supplement.py` |
| Public license for research use | `LICENSE`; vendored `SkillOpt/LICENSE` is retained for upstream code notice |

## Boundaries

This repository is a code and protocol package. It intentionally excludes
measured run outputs, result tables, local credentials, private paths, and the
paper source. The benchmark launchers support dry-run validation without model
calls; full reproduction requires materialized datasets and local model
credentials.

The vendored `SkillOpt/` tree contains the runtime needed to execute the
baseline and SAGE-integrated training loop. Some upstream documentation is kept
in the public repository for provenance, but the generated AAAI ZIP excludes
nonessential upstream project pages and documentation that are not needed to run
the code appendix.
