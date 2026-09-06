---
skill: legacy-document-evidence-intake
scorecard_version: v0.1.0
static_score: 9.42
decision: repo-ready
status: current
last_verified: not-yet-tested
runtimes_tested:
  codex: { status: synced, model: gpt-5.4-mini, date: not-yet-tested }
  claude_code: { status: synced, model: haiku, date: not-yet-tested }
  opencode: { status: synced, model: minimax-m2.5-free, date: not-yet-tested }
evidence_source: local structural validation + validator unit tests + adapter drift checks
---

# Skill Review Scorecard: legacy-document-evidence-intake v0.1.0

## Review Focus

v0.1.0 introduces the pre-normalization entry layer that turns legacy
enterprise documents trapped in raw Office / Visio / PDF / image formats into a
machine-consumable, evidence-coordinate document-intake package before
`legacy-flow-context-normalizer`. The review focuses on five contracts:

1. **Source registration** — every document recorded with path, type, size,
   `sha256`, owner, sensitivity, and authorization status.
2. **Authorization/sensitivity gate** — unknown-sensitivity, unauthorized,
   unapproved-production, or redaction-required material routes to
   `legacy-ibmi-evidence-intake`; the skill never opens unauthorized content.
3. **Honest conversion** — legacy binaries (`.xls`/`.doc`/`.ppt`/`.vsd`) are
   normalized with LibreOffice / a documented converter; missing tooling is
   recorded honestly and never faked as success.
4. **Static-only macro policy** — `.xlsm`/macro-enabled Office never executes
   VBA; uninspectable macro logic is `promotion: blocked` and capped at
   `ready_with_warnings` pending a named security reviewer.
5. **Boundary** — produces only `DOC-*`/`FRAG-*`/`TBD-*` coordinates and format
   outputs; no flow-view classification, business rules, BRD/spec content, or
   evidence approval.

## Decision

Repo-ready, not field-pilot ready.

Static score before cap: **9.42 / 10**

Current score after cap: **9.0 / 10**

## Findings Fixed In Review

| ID | Finding | Fix |
| --- | --- | --- |
| LDEI-V010-REV-002 | The validator did not enforce the promised per-document manifest contract. | Added checks that every registered document has a matching `documents/<DOC-SLUG>/document.manifest.yaml` with required structure / fragment fields. |
| LDEI-V010-REV-003 | The validator could pass a `ready` / `ready_with_warnings` package whose `normalized_outputs` files were missing. | Added manifest-driven checks for every listed normalized output path on non-blocked documents. |
| LDEI-V010-REV-004 | The honest-conversion gate was mostly prose; `succeeded` could be paired with `tool: none`. | Added manifest and `conversion-log.md` checks that a successful conversion must name a real tool. |

## Blocking For 9.5

| ID | Finding | Required Change |
| --- | --- | --- |
| LDEI-V010-REV-001 | Three-runtime execution has not yet confirmed intake, macro, legacy-binary, unauthorized-block, and ready-handoff behavior. | Run the five smoke prompts in `docs/runtime-smoke-tests.md` across Codex, Claude Code, and OpenCode and confirm honest-conversion, static macro handling, the authorization block, and the `legacy-flow-context-normalizer` handoff. |

## Verification

```bash
scripts/sync-skills.sh --check --skill legacy-document-evidence-intake
python3 skills/legacy-document-evidence-intake/scripts/validate_document_intake_package.py --help
python3 -m unittest tests/test_document_intake_validator.py
python3 -m unittest discover -s tests
python3 scripts/verify-skill-claims.py
```

Local structural checks, validator unit tests, full unittest discovery, adapter
drift checks, and claim-drift checks passed at review time.
