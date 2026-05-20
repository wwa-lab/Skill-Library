# Stage 07: Forward SDLC Handoff

**You are here if:** at least one `spec.yaml.status: approved` exists AND
you are ready to hand off to the forward SDLC chain
(`wwa-lab/build-agent-skill`).

This is the **last reverse-chain stage**. Crossing this gate moves the work
out of Legacy Spec Factory into the forward repo.

## Need before starting

- `05_specs/<CAP-ID>/spec.yaml` with `status: approved` for every
  capability in this delivery
- `05_specs/<CAP-ID>/spec.md` + `traceability.md`
- Equivalence test pack: `06_quality/<CAP-ID>/golden-master-tests.md` plus
  the referenced sample-data and expected-output files
- Redacted sample transactions sufficient to run the golden-master tests
- Target-platform authority approval for any `DEC-*` modernization
  decisions in the spec

## Run

- **Skill:** `legacy-brd-to-sdd-handoff` (Implemented v0.1.0) — packages and
  validates the handoff bundle
- **Skill (planning, earlier):** `legacy-golden-master-test-planner` —
  produces the equivalence pack required above
- **Skill (governance):** `legacy-traceability-packager` — audits and seals
  the end-to-end capability bundle before handoff
- **Skill (optional review view):** `legacy-html-exporter` — exports approved
  human-facing Markdown companions for stakeholder browsing; it does not
  replace the handoff bundle or `spec.yaml`.

## Produce

- **Artifact:** handoff bundle (machine-readable + human-readable) and an
  audit / findings report
- **Save under:** `09_forward-sdlc/<CAP-ID>/` *(relative to your
  `project.root`, e.g. `docs/XXX260004-demo/09_forward-sdlc/CAP-ORDER-PRICING/`)*
- **Consumed by:** `wwa-lab/build-agent-skill` (Functional Spec → Technical
  Design → Program Spec → Code Generator)

## Gate before advancing

- **Name:** Forward Handoff Gate
- **Check:**
  - `spec.yaml.status: approved` for every in-scope capability
  - Every critical rule has SME approval
  - No blocking `TBD-*` remains
  - `acceptance_criteria` present for every approved rule
  - Equivalence pack present, traceable to approved rules, and references
    redacted sample data only
  - Target-platform authority approval recorded for every `DEC-*`
- **Blocks if:** any of the above fail. The orchestrator must refuse to
  cross the boundary into `wwa-lab/build-agent-skill` and route back to
  the failing prerequisite.
- **HTML export note:** HTML may help stakeholders read the approved package,
  but it is not evidence of approval and does not satisfy the Forward Handoff
  Gate.

See `docs/forward-sdlc-contract.md` for the full gate text.

## SME action

- **Required:** final business sign-off on the handoff bundle (separate
  from per-rule sign-off done during spec writing)
- **Plus:** target-platform / architecture authority approval for every
  `DEC-*` modernization decision
- **Recorded in:** handoff bundle approval block + `DEC-*` decision records

## Next card

End of the reverse chain. From here, work continues in the **forward** repo:

- `wwa-lab/build-agent-skill` → `ibm-i-workflow-orchestrator`,
  `ibm-i-program-spec`, code generator, etc.

If a new capability or a new module enters scope later, restart from
[`01-evidence-ready.md`](01-evidence-ready.md) (or earlier if new raw
evidence must be redacted).
