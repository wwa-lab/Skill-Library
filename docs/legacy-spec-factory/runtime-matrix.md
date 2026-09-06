# Runtime Matrix

Track where each canonical skill has been synced and tested across Codex,
Claude Code, and OpenCode.

**Single source of truth**: [`docs/skill-status-truth-table.md`](skill-status-truth-table.md).
This file is the runtime-status view of that table. Run
`scripts/verify-skill-claims.py` to confirm they agree.

Any change to `skills/` must update this matrix in the same PR or commit.

## Schema

| Column | Meaning |
| --- | --- |
| Skill | Canonical skill name |
| Version | Canonical version under test |
| Codex / Claude Code / OpenCode | Status enum: `not tested`, `synced`, `loaded`, `executed`, `passed`, `failed` |
| Evidence | Path to current scorecard with smoke-test record |
| Last Verified | Most recent date the runtime status was confirmed |
| Notes | Free-text outcome summary |

## Status Values

| Status | Meaning |
| --- | --- |
| `not tested` | adapter sync not yet attempted |
| `synced` | adapter folder exists, content matches canonical |
| `loaded` | runtime discovered the skill but did not complete the scenario |
| `executed` | runtime completed the scenario with the right shape |
| `passed` | runtime completed the scenario and met every pass criterion |
| `failed` | runtime could not discover the skill or violated a hard gate |

A skill is **field-pilot ready** only when all three runtimes are at `passed`
AND the scorecard records sign-off. Any non-`passed` row caps the published
score at 9.0.

## Models Used

| Runtime | Model |
| --- | --- |
| Codex CLI | `gpt-5.4-mini` (read-only ephemeral) |
| Claude Code | `haiku` (Read-only tools) |
| OpenCode | `minimax-m2.5-free` |

## Matrix

| Skill | Version | Codex | Claude Code | OpenCode | Evidence | Last Verified | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `legacy-modernization-orchestrator` | v0.2.5 | synced | synced | synced | [scorecard](reviews/legacy-modernization-orchestrator-v0.2.5-scorecard.md) | 2026-05-29 | v0.2.5 routes module analysis to BRD review before spec-writing while preserving the context-view vs canonical module-flow timing rule; expanded-route execution still needed. |
| `legacy-flow-context-normalizer` | v0.1.9 | synced | synced | synced | [scorecard](reviews/legacy-flow-context-normalizer-v0.1.9-scorecard.md) | 2026-05-29 | v0.1.9 adds View 3 / View 4 AS400 technical-anchor gates so API/menu/business labels produce supplement TBDs instead of invented program or file nodes; execution smoke pending. |
| `legacy-module-context-intake` | v0.1.4 | synced | synced | synced | [scorecard](reviews/legacy-module-context-intake-v0.1.4-scorecard.md) | 2026-05-29 | v0.1.4 preserves owner-risk-approved sparse input as low-confidence context and clarifies that intake view files are not canonical module-flow artifacts; execution smoke pending. |
| `legacy-document-evidence-intake` | v0.1.0 | synced | synced | synced | [scorecard](reviews/legacy-document-evidence-intake-v0.1.0-scorecard.md) | not-yet-tested | v0.1.0 pre-normalization format intake: converts Excel/Word/PPT/Visio/PDF/image into Markdown/CSV/PDF/PNG/SVG with manifests and DOC-*/FRAG-* evidence coordinates; static-only macro policy; routes unauthorized/unknown-sensitivity to evidence intake; execution smoke pending. |
| `legacy-ibmi-evidence-intake` | v0.1.0 | passed | passed | passed | [scorecard](reviews/legacy-ibmi-evidence-intake-v0.1.0-scorecard.md) | 2026-05-15 | Full positive and negative smoke rerun. Claude Code initially hung in default Codex sandbox (EPERM on Claude config); rerun with auth/config/network access passed. |
| `legacy-ibmi-inventory` | v0.1.0 | synced | synced | synced | [scorecard](reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md) | not-yet-tested | Runtime copies created with `scripts/sync-skills.sh`; loading/execution not yet verified. |
| `legacy-ibmi-runtime-evidence-miner` | v0.1.0 | passed | passed | passed | [scorecard](reviews/legacy-ibmi-runtime-evidence-miner-v0.1.0-scorecard.md) | 2026-05-16 | Positive and negative no-write smoke passed in Codex CLI (`gpt-5.4-mini`), Claude Code (`haiku`), and OpenCode (`opencode/minimax-m2.5-free`) in a disposable temp copy. Frontmatter/discoverability fixed; single-run runtime evidence stays below high confidence and does not become a schedule claim. |
| `legacy-ibmi-program-analyzer` | v0.1.0 | synced | synced | synced | [scorecard](reviews/legacy-ibmi-program-analyzer-v0.1.0-scorecard.md) | not-yet-tested | All 5 review findings fixed in `99e27f4`; smoke prompts added to `runtime-smoke-tests.md`. Ready for execution. |
| `legacy-ibmi-data-model-analyzer` | v0.1.0 | passed | synced | passed | [scorecard](reviews/legacy-ibmi-data-model-analyzer-v0.1.0-scorecard.md) | 2026-05-16 | Codex and OpenCode passed positive/negative no-write smoke. Claude Code blocked by `Not logged in - Please run /login`; field-pilot remains blocked. |
| `legacy-ibmi-screen-report-analyzer` | v0.1.0 | passed | passed | passed | [scorecard](reviews/legacy-ibmi-screen-report-analyzer-v0.1.0-scorecard.md) | 2026-05-16 | Positive no-write DSPF smoke passed in all three runtimes. Returned canonical artifact `screen-report-analysis-OBJ-ORDER-ENTRY-003.md`; kept `BR-*`/`CAP-*`/`DEC-*` forbidden; handoff non-approved (no SME sign-off evidence). |
| `legacy-ibmi-flow-analyzer` | v0.1.2 | synced | synced | synced | [scorecard](reviews/legacy-ibmi-flow-analyzer-v0.1.2-scorecard.md) | 2026-05-26 | v0.1.2 makes Business Capability Seeds business-readable; three-runtime smoke pending. |
| `legacy-ibmi-module-analyzer` | v0.1.4 | synced | synced | synced | [scorecard](reviews/legacy-ibmi-module-analyzer-v0.1.4-scorecard.md) | 2026-05-29 | v0.1.4 keeps canonical Mermaid-backed four-view module analysis under `04_modules/` but routes standard consumption to BRD writer first; three-runtime smoke pending. |
| `legacy-brd-writer` | v0.1.5 | synced | synced | synced | [scorecard](reviews/legacy-brd-writer-v0.1.5-scorecard.md) | 2026-05-29 | v0.1.5 makes BRD the standard business review gate before spec-writing; three-runtime smoke pending. |
| `legacy-spec-writer` | v0.1.2 | synced | synced | synced | [scorecard](reviews/legacy-spec-writer-v0.1.2-scorecard.md) | 2026-05-29 | v0.1.2 requires an approved BRD Package before standard spec-writing; three-runtime smoke pending. |
| `legacy-modernization-decision-writer` | v0.1.0 | passed | passed | passed | [scorecard](reviews/legacy-modernization-decision-writer-v0.1.0-scorecard.md) | 2026-05-16 | Positive returned canonical `05_decisions/ORDERS/` four-file package, approved DEC. Negative blocked invented PostgreSQL/Kafka DEC with missing BR/BEH/EV grounding. |
| `legacy-sme-review-facilitator` | v0.1.2 | synced | synced | synced | [scorecard](reviews/legacy-sme-review-facilitator-v0.1.2-scorecard.md) | 2026-05-26 | v0.1.2 makes SME questions business-language first; three-runtime chat-review smoke pending. |
| `legacy-brd-to-sdd-handoff` | v0.1.0 | passed | passed | passed | [scorecard](reviews/legacy-brd-to-sdd-handoff-v0.1.0-scorecard.md) | 2026-05-16 | Positive returned five required package files. Negative refused missing `spec.yaml`, routed to `legacy-spec-writer`. |
| `legacy-traceability-packager` | v0.1.1 | passed | passed | passed | [scorecard](reviews/legacy-traceability-packager-v0.1.1-scorecard.md) | 2026-05-16 | Positive returned `pass` with the four required files. Negative blocked dangling `AC-* -> BR-*`, refused to mint missing `BR-*`. |
| `legacy-runtime-matrix-tester` | v0.1.0 | passed | passed | passed | [scorecard](reviews/legacy-runtime-matrix-tester-v0.1.0-scorecard.md) | 2026-05-16 | Positive returned six-cell matrix row with lowercase statuses, `field-pilot ready` decision. Negative refused false `passed`, kept unavailable adapter at `synced`. |
| `legacy-golden-master-test-planner` | v0.1.0 | passed | passed | passed | [scorecard](reviews/legacy-golden-master-test-planner-v0.1.0-scorecard.md) | 2026-05-16 | Positive returned five `06_quality/CREDIT-LIMIT/` files with `TC-*` IDs. Negative blocked missing-customer rejection without observed expected-output evidence. |
| `legacy-step-contract` | v0.1.2 | passed | passed | passed | [scorecard](reviews/legacy-step-contract-v0.1.2-scorecard.md) | 2026-05-29 | Terminology-only update aligns flow-context-normalizer with the four-view context boundary. Prior positive and negative smoke passed across all three runtimes. |
| `legacy-step-validator` | v0.1.1 | passed | passed | passed | [scorecard](reviews/legacy-step-validator-v0.1.1-scorecard.md) | 2026-05-14 | Positive and negative smoke passed across all three runtimes. Scorecard 9.53. |
| `legacy-html-exporter` | v0.1.0 | passed | failed | passed | [scorecard](reviews/legacy-html-exporter-v0.1.0-scorecard.md) | 2026-05-19 | Codex passed positive and negative no-write smoke after quoting the frontmatter description for YAML safety. Claude Code still violates the negative source-of-truth guardrail. OpenCode now passes the positive contract-only smoke by invoking `export_contract_helper.py` and returning the exact sibling `.html` path while keeping Markdown canonical. |

## Verification

Run:

```bash
python3 scripts/verify-skill-claims.py
```

The script checks that:

1. Every row has a current scorecard with frontmatter
2. The runtime status in this table matches the scorecard `runtimes_tested:`
3. The truth table (`docs/skill-status-truth-table.md`) agrees with this matrix
4. README's "Current Skill Scores" table also agrees

The script exits non-zero if drift is detected.
