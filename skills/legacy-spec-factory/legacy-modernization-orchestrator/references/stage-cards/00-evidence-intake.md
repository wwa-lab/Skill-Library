# Stage 00: Evidence Intake

**You are here if:** you have raw IBM i artifacts (RPGLE / CLLE / DDS / DB2
metadata / job logs / spool / screen samples / SME notes) and **any** of the
following is true:

- no `evidence-manifest.yaml` exists yet
- any item has `sensitivity: unknown`
- any item lacks either source-path authorization or a recorded redaction note

This stage is non-bypassable, but redaction is not always required. The
**Evidence Authorization Gate** blocks downstream skills until every item has a
reviewed source path or required redaction record.

## Need before starting

- Raw source / metadata / runtime evidence collected from the IBM i system
- Permission from the data owner to use/store the evidence internally
- A developer/reviewer owner for the intake decision
- An SME contact only when Step 0 needs business judgment or redaction-quality
  approval; it is valid for SME ownership to be unknown/deferred during initial
  developer-led source intake

## Run

- **Skill:** `legacy-ibmi-evidence-intake` (Implemented v0.1.0)
- **Manual fallback:** Follow `docs/data-collection-and-redaction.md`
  step-by-step if the skill is not available in your runtime

## Produce

- **Artifact:** `evidence-manifest.yaml` + `redaction-log.md` + approved
  analysis bundle
- **Save under:** `evidence/redacted/` or `evidence/intake/` *(relative to your
  `project.root`, e.g. `docs/XXX260004-demo/evidence/intake/`)* — raw production
  samples are **never** committed unless explicitly authorized and recorded
- **Consumed by:** `legacy-ibmi-inventory`

Each evidence item must carry:

- `evidence_id` (e.g. `EV-SRC-001`, `EV-JOBLOG-014`)
- `sensitivity` set to `public`, `internal`, or `confidential` (never
  `unknown` after intake)
- `source_path_verified: true` when the user-provided path is authorized for
  internal analysis, or `redaction_required: true` with a completed redaction
  note when masking is required

## Gate before advancing

- **Name:** Evidence Authorization Gate
- **Check:** every item in `evidence-manifest.yaml` has known sensitivity, an
  approved analysis path, and either source-path authorization or required
  redaction approval
- **Blocks if:** any item has `sensitivity: unknown`, lacks
  `source_path_verified: true` and has no completed redaction record, or lacks a
  required reviewer/owner approval

## SME action

- **Required:** no by default for developer-led source intake; yes only when
  business meaning, production data, masking strategy, or compliance judgment is
  needed before inventory
- **Ask when required:** "Is field X / dataset Y safe to use? What must be
  masked or removed?"
- **Recorded in:** `evidence-manifest.yaml[].sme_required` and
  `evidence-manifest.yaml[].sme_approval`

## Next card

[`01-evidence-ready.md`](01-evidence-ready.md) — start inventory once
redaction is approved.
