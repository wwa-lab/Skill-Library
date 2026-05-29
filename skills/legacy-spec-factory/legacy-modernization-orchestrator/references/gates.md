# Hard Gates Reference

Five gates protect the reverse chain. The orchestrator must
check the applicable gate before routing across the corresponding boundary.

## Gate 1 — Evidence Authorization Gate

**Boundary:** raw legacy evidence → any agent skill

**Pass criteria (all required):**

- every evidence item has `sensitivity: public | internal | confidential`
  (never `unknown`)
- every evidence item has an approved analysis path
- each item has either `source_path_verified: true` for internal source review
  or `redaction_required: true` with `redaction_status: approved`
- raw production data is not in committed paths (`evidence/raw/` is in
  `.gitignore`)
- source authorization or redaction notes are recorded without raw sensitive
  values
- `docs/data-collection-and-redaction.md` checklist completed when governed
  redaction is required

**Block actions:**

1. Refuse to route to any Layer 1 skill
2. Send user to `legacy-ibmi-evidence-intake`
3. List which evidence items have `sensitivity: unknown`, missing source-path
   authorization, or incomplete required redaction

## Gate 2 — Inventory Completeness Gate

**Boundary:** `inventory.yaml` → any downstream Layer 1 analyzer or any Layer 2 skill

**Pass criteria (all required):**

- `inventory.yaml.sme_review.decision` is one of `approved` or
  `approved_with_non_blocking_tbd`
- no `coverage_gaps[]` entry has `blocking: yes` unresolved
- every listed object has at least one `evidence_ids[]` or SME confirmation
- no object has `sensitivity: unknown`

**Block actions:**

1. State `decision` value and the count of blocking gaps
2. List the specific blocking gap IDs (`TBD-<SLUG>-<NNN>`)
3. Route to `legacy-ibmi-inventory` to resume, or to SME for waiver

**Waiver path:** an SME may mark a blocking gap non-blocking by adding a
review note and changing `blocking: pending_sme_judgment` → `no`. Record the
SME decision in `sme_review.notes`.

## Gate 3 — BRD Review Gate

**Boundary:** approved module analysis → `legacy-spec-writer`

**Pass criteria (all required unless an explicit technical-spec-only bypass is
recorded):**

- `05_brds/<CAPABILITY-SLUG>/brd.md` exists for the selected `CAP-*`
- BRD sections 1-9 are present and SME-reviewable
- missing section details are explicit named `TBD-*`, not silent blanks
- BRD review evidence records SME / business approval, such as
  `brd-review.md` sign-off or `review-decision.yaml`
- blocked BRD findings are resolved or explicitly accepted as non-blocking

**Block actions:**

1. Route to `legacy-brd-writer` if the BRD Package is missing or incomplete.
2. Route to `legacy-sme-review-facilitator` if BRD content exists but review /
   approval is missing.
3. Refuse standard spec-writing until the gate passes or the requester records
   a technical-spec-only bypass with approver and risk acceptance.

## Gate 4 — Evidence Approval Gate

**Boundary:** `business-rules.md` (draft) → `legacy-spec-writer`,
or any approval transition on rules / behaviors

**Pass criteria (per claim):**

- `knowledge_type` ≠ `unknown_tbd`
- at least one linked evidence item has `evidence_strength` of:
  - `confirmed_from_code`, or
  - `observed_in_runtime`, or
  - `confirmed_by_sme`, or
  - `strongly_inferred` plus explicit SME approval
- all linked TBDs resolved or marked non-blocking by SME
- `review_status` is `approved`

See repository path `docs/evidence-and-knowledge-taxonomy.md` for the
canonical taxonomy.

**Block actions:**

1. List rule IDs whose status is not `approved`
2. For each, state which approval criterion failed
3. Route to SME review or to additional evidence collection (often
   `legacy-ibmi-runtime-evidence-miner`)

**Exception:** `modernization_decision` claims do not need the same evidence
strength; they need architecture/product approval recorded in
`review_notes`.

## Gate 5 — Forward Handoff Gate

**Boundary:** approved `spec.yaml` → `wwa-lab/build-agent-skill` chain

**Pass criteria (all required):**

- `spec.yaml.status: approved`
- every business-critical rule has `review_status: approved`
- every approved rule has at least one acceptance criterion (`AC-*`)
- every approved rule has at least one linked evidence item
- no `open_questions[].blocking: yes` remains
- data sensitivity reviewed; sample transactions for golden master are
  redacted
- modernization decisions are clearly separated from observed behavior

See repository path `docs/forward-sdlc-contract.md` for the full handoff
contract.

**Block actions:**

1. List the specific gate criteria that failed
2. Route to whichever upstream skill resolves them:
   - missing acceptance criterion → `legacy-spec-writer`
   - failed review → `legacy-spec-reviewer`
   - missing equivalence test for business-critical rule →
     `legacy-equivalence-test-generator`
3. Refuse to provide the handoff manifest until the gate clears

## Gate Interaction Rules

- Gates compound: a downstream gate only matters if all upstream gates have
  already passed.
- The orchestrator may not "skip" a gate even if the user asks. Gate skipping
  is the most common path to a hallucinated spec.
- Every gate failure must produce a specific blocking ID list, not a generic
  "needs work" message.
- A gate that has previously passed must be re-checked when the underlying
  artifact changes (inventory updated -> re-check Gate 2; BRD updated ->
  re-check Gate 3; rule added -> re-check Gate 4).
