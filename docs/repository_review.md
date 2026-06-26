# Repository Review

## Findings

1. Resolved: the root README gave only minimal reproduction guidance. It now
   points reviewers to the AAAI reproducibility map, reviewer guide, benchmark
   launchers, SkillOpt smoke checks, and blind-review ZIP generation.
2. Resolved: the repository lacked a root license for the SAGE wrapper code.
   `LICENSE` now provides an MIT license for the anonymous artifact while
   retaining `SkillOpt/LICENSE` for the vendored upstream code.
3. Resolved: AAAI-specific requirements were implicit. `AAAI_REPRODUCIBILITY.md`
   now maps code, metrics, seeds, hyperparameters, statistical tests, and data
   boundaries to concrete files.
4. Resolved: public GitHub Pages material should not be submitted as a mutable
   blind-review pointer. `scripts/make_aaai_supplement.py` creates a static ZIP
   for OpenReview-style code appendix upload.
5. Residual requirement: full live reproduction still depends on local model
   credentials and materialized benchmark data. The repository documents those
   paths and keeps credentials/results out of version control.

## Review Basis

The review follows the AAAI-26 public instructions: the reproducibility
checklist is part of the paper PDF, code/data supplementary material is uploaded
as a ZIP for reviewers, supplementary material must preserve double blindness,
and checklist items ask for code, preprocessing, seeds, compute environment,
metrics, statistical tests, and hyperparameters.
