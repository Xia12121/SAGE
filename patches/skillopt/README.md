# SkillOpt Patches

The vendored SkillOpt tree is provided for direct reproduction. Patch files in
this directory provide transparency for the SAGE gate changes relative to the
clean SkillOpt source tree used for vendoring.

`sage_gate.patch` records only the SAGE integration in SkillOpt:

- the vendored SAGE package required for standalone SkillOpt imports;
- SAGE gate configuration fields;
- SAGE config flattening;
- the SkillOpt gate action/state transition helper;
- the trainer hook that replaces scalar acceptance with paired SAGE acceptance
  when `evaluation.gate_select=sage`.

Export the current SkillOpt checkout diff with:

```bash
python scripts/export_patch.py --skillopt /path/to/SkillOpt-git-checkout --out patches/skillopt/sage_gate.patch
```

The `--skillopt` path must be the root of a Git worktree. A plain vendored
directory is intentionally rejected so the export cannot accidentally capture
the outer reproduction repository diff. For the committed journal artifact,
`sage_gate.patch` was generated from a clean exported SkillOpt source tree, not
from local debug files or result outputs.
