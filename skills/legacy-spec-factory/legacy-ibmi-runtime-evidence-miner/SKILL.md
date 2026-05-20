---
name: legacy-ibmi-runtime-evidence-miner
description: "Use when teams need to extract structured `observed_in_runtime` evidence from approved IBM i job logs and spool/report files into `runtime-evidence.jsonl`. Use after `legacy-ibmi-evidence-intake` has approved the evidence manifest and `legacy-ibmi-inventory` can map runtime artifacts to `OBJ-*` IDs. Blocks on missing approval, unredacted confidential evidence, or missing inventory mappings; never infers business rules or modernization decisions from runtime logs."
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 8871a6b
  domain: legacy-spec-factory
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Legacy IBM i Runtime Evidence Miner

**Version**: 0.1.0  
**Status**: Field-pilot ready (v0.1.0)
**Author**: Leo L Zhang  
**Last Updated**: 2026-05-16

## Purpose

Extract structured evidence observations from IBM i runtime artifacts (job logs, spool/report files) to ground program/flow/module analysis in actual execution behavior. This skill mines `observed_in_runtime` evidence per the evidence taxonomy—a tier-2 evidence strength equal in authority to `confirmed_from_code` when SME-approved.

**Use when**: You have approved evidence manifest with job logs and/or spool files, and want to extract call sequences, error patterns, timing/rhythm, or report structure into machine-consumable `runtime-evidence.jsonl` for downstream analyzers.

**Do not use for**: Raw unredacted evidence, or when evidence manifest is not yet approved.

---

## Layer Position

**Layer**: Layer 1 (platform-specific extraction)  
**Family**: IBM i extraction  
**Sibling skills**:
- `legacy-ibmi-evidence-intake` (gates this skill)
- `legacy-ibmi-inventory` (complements; identifies OBJ-* targets)
- `legacy-ibmi-program-analyzer` (consumes optional `runtime_hints`)
- `legacy-ibmi-flow-analyzer` (consumes optional `bau_notes`)
- `legacy-ibmi-module-analyzer` (feeds View 1: Operation Flow context)

---

## Step Contract

### INPUT

**Evidence Manifest** (required)
- Source: Output of `legacy-ibmi-evidence-intake` v0.1.0
- State: `package_state: approved_for_inventory` or later
- Must include: `evidence[]` array with type `job_log` and/or `spool_or_report`
- All confidential artifacts must be marked `redaction_status: approved` (no raw unredacted logs)
- Example: `evidence/manifest.yaml` after SME approval in evidence-intake

**Inventory** (required for EV-* → OBJ-* mapping)
- Source: Output of `legacy-ibmi-inventory` v0.1.0
- File: `01_inventory/inventory.yaml` or `inventory.md`
- Contains: `objects[]` array with `object_id` (OBJ-*), `object_type`, `object_name`
- Used to: Cross-reference which programs/files appear in runtime logs

**Job Logs** (optional but recommended)
- Format: IBM i JOBLOG000 or exported job log (text)
- Sensitivity: Redacted or marked public (see redaction-log.md from evidence intake)
- Content expectations: CALL statements, timestamps, error messages, I/O wait messages
- Size: Typically 10KB–500KB per run

**Spool/Report Files** (optional)
- Format: Printer output (text), typically from PRTF outputs
- Sensitivity: Redacted or marked public
- Content expectations: Report headers, sections, fields, totals, control breaks
- Size: Typically 5KB–100KB per report

**Inventory and Spool/Job Log Co-location**
- All files should be in the same evidence directory or referenced by path from manifest
- No external network calls allowed (air-gap compatibility)

### EXECUTION

**Workflow**: 9 ordered steps with defined inputs, outputs, and stop conditions

1. **Verify Evidence Manifest & Readiness**
   - Input: `evidence/manifest.yaml`
   - Output: readiness assessment (proceed / blocked)
   - Checks:
     - Evidence manifest is present and approved
     - `package_state` is `approved_for_inventory` or later
     - All job logs / spool files listed with type and sensitivity
     - All confidential artifacts marked `redaction_status: approved` (redacted)
   - Stop condition: Manifest missing, not approved, or contains unredacted confidential data

2. **Map Runtime Artifacts to Inventory**
   - Input: evidence manifest + `01_inventory/inventory.yaml`
   - Output: artifact-to-object mapping list
   - Do:
     - For each job log / spool, identify which OBJ-* (programs/files) it involves
     - Cross-reference against inventory
     - Create EV-* → OBJ-* traceability
   - Create TBD: For programs appearing in logs but not in inventory (pending_source)
   - Stop condition: Inventory missing or incompatible format

3. **Extract Call Sequences from Job Logs**
   - Input: Job logs (JOBLOG000 or equivalent)
   - Output: `call_sequence` observations
   - Do:
     - Parse CALL, CALLP, CALLPRC statements logged by system
     - Document sequence, timing (if timestamps available), conditional calls
     - Extract supporting detail: log line numbers, timestamps, program names
   - Confidence scoring: High if 3+ independent runs show identical sequence; medium if 1–2 runs; low if ambiguous
   - Stop condition: None (missing logs → create low-confidence observations for available data)

4. **Extract Error Patterns from Job Logs**
   - Input: Job logs
   - Output: `error_pattern` observations
   - Do:
     - Identify all error messages (MCH*, CPF*, SQL errors, CPI*, etc.)
     - Document which programs/objects threw errors
     - Track recovery paths if logged (RETRY, ROLLBACK, etc.)
     - Identify unhandled exceptions / crashes
   - Confidence scoring: High if pattern repeats 3+ times; low if single instance
   - Note: Never invent error handling not visible in logs

5. **Extract Timing & Rhythm Observations**
   - Input: Job logs with timestamps
   - Output: `timing_observation`, `batch_window`, `interactive_frequency` observations
   - Do:
     - Calculate execution duration per program or job
     - Identify batch windows (e.g., "job runs 01:00–02:30")
     - Peak hours for interactive transactions (if DSPLY logged)
     - I/O contention patterns (FILE LOCKED, RECORD LOCKED frequency)
   - Confidence scoring: High if 3+ runs; medium if 2 runs; low if single run or timing is variable
   - Note: Timing is inherently variable; never claim high confidence from one run
   - Frequency rule: A single run may support "observed once at <time range>" only. Do not call a batch window "nightly", "typical", "scheduled", or "BAU" unless multiple runs, scheduler evidence, or SME approval explicitly support that frequency.

6. **Extract Structure from Spool Files**
   - Input: Printer output / spool files (PRTF output)
   - Output: `report_structure` observations
   - Do:
     - Parse report headers, section markers, footers
     - Document field positions and formats
     - Identify summary lines, grand totals, control breaks
     - Extract example value ranges (e.g., "AMOUNT: 1000.00–99999.99")
     - Infer data types from field examples (numeric vs. alphanumeric)
   - Confidence scoring: High if multiple report instances show consistent structure; low if structure varies
   - Anti-hallucination: Do not quote actual customer names/amounts; record ranges instead

7. **Correlate Multiple Runs**
   - Input: All extracted observations from steps 3–6
   - Output: Consolidated observations with confidence assessment
   - Do:
     - For each observation type, check how many independent runs confirm it
     - Upgrade confidence from "low" → "medium" → "high" based on frequency
     - Mark observations that contradict across runs as TBDs for SME review
     - Create `contradictory` evidence records (per evidence taxonomy)
   - Rule: Never claim high confidence from a single run
   - Rule: Do not promote one observed runtime occurrence into a recurring operational rhythm. Carry the recurrence question to SME review or `pending_source` instead.

8. **Generate `runtime-evidence.jsonl`**
   - Input: Consolidated observations from step 7
   - Output: `runtime-evidence.jsonl` (line-delimited JSON)
   - Schema: Each line is a valid JSON object per output-contract.md
   - Required fields per observation:
     - `observation_id` (RTE-SLUG-NNN format)
     - `evidence_id` (EV-* back-reference to intake manifest)
     - `observation_type` (call_sequence, error_pattern, timing_observation, report_structure, etc.)
     - `statement` (human-readable summary)
     - `supporting_detail` (raw extraction with log line references)
     - `confidence` (high/medium/low)
     - `knowledge_type` (always observed_behavior for runtime mining)
     - `evidence_strength` (always observed_in_runtime)
     - `sme_review_status` (draft)
   - Validation: Each line must be valid JSON; file must be parseable line-by-line as JSONL
   - Anti-hallucination: Every statement must trace back to a specific log line or spool section number

9. **Prepare for SME Review**
   - Input: `runtime-evidence.jsonl` + observations list
   - Output: SME review package
   - Do:
     - Create `mining-checklist.md` with review questions for SME
     - Highlight high-value observations (likely to affect program/flow analysis)
     - Flag any contradictions between runtime and code analysis
     - Note any gaps (unidentified programs in logs, missing evidence)
     - Summarize confidence distribution (how many high/medium/low)
   - Outcome: Output marked `sme_review_status: draft` pending SME sign-off

### OUTPUT

**Primary Artifact: `runtime-evidence.jsonl`**
- Location: Output directory alongside evidence manifest, or `07_runtime_evidence/runtime-evidence.jsonl`
- Format: Line-delimited JSON (one observation per line)
- Schema: See `references/output-contract.md`
- Consumers:
  - `legacy-ibmi-program-analyzer` (optional `runtime_hints` parameter)
  - `legacy-ibmi-flow-analyzer` (optional `bau_notes` parameter)
  - `legacy-ibmi-module-analyzer` (View 1 Operation Flow context)
  - SME review process

**Review Artifact: `mining-checklist.md`**
- Required whenever runtime mining proceeds beyond readiness checks
- Captures SME review questions, confidence distribution, unresolved TBDs,
  and sign-off prompts from Step 9

**Secondary Artifacts (Optional)**
- `mining-report.md` — Human-readable summary of mining results
- `mining-checklist-completed.md` — SME review checklist + sign-off after SME review

**Observation Types** (see observation-taxonomy.md for full definitions)
- `call_sequence` — CALL/CALLP statements extracted from job logs
- `error_pattern` — Error messages and recovery paths
- `timing_observation` — Execution duration, frequency
- `batch_window` — When batch jobs run, how long they take
- `interactive_frequency` — Peak hours for interactive transactions
- `report_structure` — Spool file section layout, field positions, totals
- `lock_contention` — FILE LOCKED / RECORD LOCKED patterns
- `commit_boundary` — Explicit or inferred commit points (from logs)

**Status**: All observations marked `sme_review_status: draft` until SME approval

### VALIDATION

**Anti-Hallucination Checks**
1. Every observation must trace back to a specific log line number or spool section
2. Never invent program behavior not visible in logs
3. Never quote unredacted sensitive data (customer IDs, amounts, personal info)
4. Never claim high confidence from a single run
5. Contradictions must be documented as TBDs, never suppressed
6. Unidentified programs in logs must become pending_source TBDs

**Format Validation**
1. `runtime-evidence.jsonl` must be line-delimited JSON (each line independently valid)
2. All required fields present in each observation
3. `observation_id` format: RTE-<SLUG>-NNN (stable, unique per capability)
4. `evidence_id` format: EV-<SLUG>-NNN (back-reference to evidence manifest)
5. `confidence` value in {high, medium, low}
6. `evidence_strength` must be "observed_in_runtime" (by definition)
7. `sme_review_status` must be "draft" initially

**Readiness Check**
- [ ] Evidence manifest approved for inventory
- [ ] All job logs / spool files either redacted or marked public
- [ ] Inventory complete (programs and files identified)
- [ ] All 9 workflow steps completed
- [ ] No unredacted sensitive data in output
- [ ] All observations have evidence_id back-references
- [ ] Confidence scoring is justified (1/3+ rule for high)
- [ ] TBDs created for ambiguous or missing observations
- [ ] SME review checklist populated

**Downstream Consumption Check**
- Program analyzer can read `runtime_hints` from JSONL
- Flow analyzer can read `bau_notes` from JSONL
- Module analyzer can use View 1 context from observations
- No downstream skill is blocked by missing or malformed observations

---

## Evidence Minimum

**What makes an observation approvable**:
1. Human-readable statement (summary of the observation)
2. Supporting detail with specific log line references or spool section numbers
3. Confidence score (high/medium/low) with justification
4. Evidence strength: "observed_in_runtime" (tier 2, equal to "confirmed_from_code")
5. Link back to EV-* evidence ID in the intake manifest
6. No unredacted sensitive data quoted in the statement or detail

**What does NOT make it approvable**:
- Statement without source reference ("CALC program must validate amounts" — inferred, not observed)
- Contradictory observations without TBD ("logs show sequence X, but SME says sequence Y")
- Single observation claimed as "high confidence"
- Unredacted customer names, account numbers, or transaction amounts

---

## References

- `references/output-contract.md` — Full JSONL schema, field definitions, validation rules
- `references/joblog-parsing-patterns.md` — IBM i JOBLOG000 structure, message types, regex patterns
- `references/spool-parsing-patterns.md` — Report structure, field extraction, control break detection
- `references/observation-taxonomy.md` — Enum of observation types and when to use each
- `references/mining-confidence-rules.md` — Scoring rules for high/medium/low confidence

---

## Integration with Downstream Skills

### Program Analyzer: `runtime_hints` Parameter
```yaml
## Runtime Hints (Optional)
- Source: runtime-evidence.jsonl (EV-CREDIT-CHECK-015)
- Observation: Call sequence MAIN → VALIDATE → CALC confirmed in 5 job runs
- Effect: Program Call Map edge marked `confirmed_from_code + observed_in_runtime`
- Confidence: high (multiple runs, consistent pattern)
```

**Integration rule**: If program-analyzer finds a Program Call Map edge in source code AND runtime mining confirms it in 3+ job logs, tag as `confirmed_from_code + observed_in_runtime`. Confidence upgraded from "source-only" to "code + runtime co-confirmed."

### Flow Analyzer: `bau_notes` Parameter
```yaml
## BAU Notes (from Runtime Mining)
- Observation: Batch job BATCHRECON runs every night 01:00–02:30 (3 observations, high confidence)
- Observation: Typical error FILE LOCKED on CUSTFILE, retry succeeds (2 observations, medium confidence)
- Effect: Trigger model substantiated; error propagation grounded in runtime behavior
```

**Integration rule**: Flow analyzer uses BAU notes to estimate trigger frequency and document error recovery patterns that source code alone cannot supply.

### Module Analyzer: View 1 Context
```yaml
## View 1: Operation Flow / Business Context

### BAU Rhythm (informed by runtime mining)
- Overnight batch window: 01:00–02:30 (confirmed by logs, 5 runs) — RTE-CREDIT-CHECK-008
- Peak interactive usage: 08:00–17:00 (inferred from DSPLY frequency in logs) — RTE-CREDIT-CHECK-009
- Error recovery: Manual retry on file lock; successful 95% of time (from error logs) — RTE-CREDIT-CHECK-010
```

**Integration rule**: Module analyzer uses runtime-mined observations to substantiate View 1 (Operation Flow) without relying purely on SME memory.

---

## Rule Auto-Validation (cross-check inferred rules against runtime)

After mining `runtime-evidence.jsonl`, the skill performs a cross-check
pass against any `inferred_business_rule` entries already present in
`02_programs/<MODULE>/<OBJ>/program-analysis.md` and module View 1.

Goal: promote rules whose code-side inference is corroborated by ≥ N
runtime samples (default N=3) from `review_status: needs_sme_review` to
`review_status: auto_validated_spot_check_only`. SMEs spot-check this
bucket instead of reviewing every rule individually — typically cuts SME
load 30-60% per capability.

The full protocol, eligibility rules, threshold logic, conflict handling,
and audit trail format live in
[`references/rule-auto-validation-protocol.md`](references/rule-auto-validation-protocol.md).
Summary:

| Rule must be | Action |
| --- | --- |
| `inferred_business_rule` + medium/high source confidence + ≥ N matching runtime samples (all outcomes match) | Promote to `auto_validated_spot_check_only`; append runtime `EV-RUN-*` IDs to the rule's `evidence_ids` |
| matching runtime samples but conflicting outcomes | Flag as `runtime_conflict_with_inference`; ESCALATE to SME — do NOT downgrade |
| `critical` criticality + affects money/posting/compliance | Leave at `needs_sme_review` regardless of corroboration (bandwidth-saver, not safety bypass) |
| < N matching samples OR 0 samples OR `low` source confidence | Leave at `needs_sme_review` |

Each promotion appends an audit entry to the rule:

```yaml
auto_validation:
  matched_records: 5
  runtime_evidence_ids: [EV-RUN-014, EV-RUN-027, EV-RUN-041, EV-RUN-053, EV-RUN-061]
  validated_at: 2026-05-16
  validated_by: legacy-ibmi-runtime-evidence-miner
  protocol_version: 1
```

The skill MUST NOT auto-validate when:

- Source-side confidence is `low`
- All matching samples come from a single batch / single day (not
  representative)
- The rule depends on date/time, seasonality, or a configuration value
- The owning capability is `critical` AND the rule touches money,
  posting, or compliance

`legacy-sme-review-facilitator` consumes the resulting partition to
generate three-bucket review packages (full review / spot-check / batch
confirm) — see that skill's SME Communication Package section.

## Workflow State Write-Back

At the end of a mining run, update `<project-root>/workflow-state.yaml`
per [`docs/workflow-state-contract.md`](../../../docs/legacy-spec-factory/workflow-state-contract.md).
Template: [`skills/legacy-modernization-orchestrator/references/state-writeback-snippet.md`](../legacy-modernization-orchestrator/references/state-writeback-snippet.md).

**Stage this skill produces:**

- `5 Runtime Evidence Mined` when `runtime-evidence.jsonl` is complete and
  every record links back to an `OBJ-*` from inventory and an `EV-*` from
  the approved evidence manifest
- No advancement when any record has unresolved redaction or missing
  inventory mapping; record blockers in `blocking.gates: ["redaction"]` or
  `blocking.tbds`

**Last artifact path pattern:** `07_runtime-evidence/runtime-evidence.jsonl`
(plus referenced sample files under `07_runtime-evidence/samples/`)

**Capability scoping:** Runtime mining typically runs per-module rather
than per-capability. Two cases:

- If `current_focus.capability_id` is set, overwrite that
  `capabilities[]` entry's `stage_id` and `last_artifact`.
- If `current_focus` is module-scoped only (no `CAP-*` yet), append
  `history[]` only with `capability_id: null` and the module slug in
  `note`. Do not invent a `CAP-*`.

**Writes per run:**

1. (When CAP-* is scoped) Overwrite `capabilities[<CAP-*>]` with stage id,
   the JSONL path, `last_skill: legacy-ibmi-runtime-evidence-miner`, and
   blocking IDs.
2. Append one `history[]` entry with the run's record count and any
   redaction findings.
3. Overwrite `project.last_updated_at` / `project.last_updated_by`.

Never touch `current_focus`, other capabilities' entries, or past
`history[]` rows. Stage `5` is parallel to the linear program/flow/module
chain — re-running this skill does NOT regress those stages.

## SME Review Questions

After mining is complete, present SME with these questions before approving output:

1. **Call Sequences** — Do the observed call sequences match your understanding of how programs interact? Are there sequences you expected but did not see in logs (dead code, or logs incomplete)?

2. **Error Patterns** — Are the error messages and recovery paths typical or exceptional? Which errors are expected BAU vs. unhandled exceptions that should be TBDs?

3. **Timing & Rhythm** — Are the batch windows and peak hours accurate? Does the job run every night or sporadically? Is one-run-per-week typical or a backlog exception?

4. **Report Structure** — Do the extracted field positions and summary lines match what you expect the system to produce? Any control breaks or subtotals we missed?

5. **Contradictions** — Where runtime logs conflict with code analysis or SME expectation, should we investigate (e.g., "VALIDATE is called in code but never appears in logs"), or mark it as TBD?

6. **Gaps** — Are there programs or data flows in logs that are NOT in inventory? Should we expand scope or stay focused?

7. **Confidence Scores** — Are the confidence assignments reasonable (high: 3+ runs; medium: 1–2; low: ambiguous)?

8. **Sensitive Data** — Has redaction been applied correctly? Any values in output that should not be there?

**Sign-off**: SME approval upgrade `sme_review_status` from "draft" to "approved" and record decision date.

---

## Known Limitations

1. **Job log parsing is pattern-based, not exhaustive** — Semi-structured IBM i logs require regex pattern matching; unrecognized message formats are skipped gracefully.

2. **Incomplete logs are handled gracefully** — If a job log is truncated, mining continues for available data; confidence scores are adjusted downward.

3. **Transaction sample mining deferred to Phase 2** — This skill focuses on job logs and spool files; mining CSV or fixed-width transaction records is a separate Phase 2 effort.

4. **Data model / DB extract mining deferred to Phase 2** — Field ranges and special codes from transaction data are deferred to a future `legacy-ibmi-data-miner` skill focused on DB2 and sample data.

5. **Real-time or online transaction logs may be sparse** — If the system does not log DSPLY or EXFMT statements for interactive flows, interactive frequency observations will be low-confidence or absent.

6. **Timing observations require timestamps in logs** — If the job log does not include timestamps, timing observations cannot be extracted.

---

## Field-Pilot Readiness

**v0.1.0 Status**: Field-pilot ready (9.57)

**Smoke Test Evidence**:
1. **Positive path**: Approved job log + spool evidence produced the expected `runtime-evidence.jsonl` / `mining-checklist.md` contract shape in Codex CLI, Claude Code, and OpenCode.
2. **Negative path**: Draft confidential job log with pending redaction blocked in all three runtimes before mining.
3. **Single-run guard**: Smoke confirmed one runtime occurrence stays below high confidence and is not promoted to nightly, typical, scheduled, or BAU rhythm.

**Optional integration follow-up**:
- Verify program-analyzer consumes `runtime_hints` from `runtime-evidence.jsonl`
- Verify flow-analyzer consumes `bau_notes`
- Verify module-analyzer grounds View 1 in runtime observations

---

## How to Use This Skill

### Quick Start
1. Ensure `legacy-ibmi-evidence-intake` has produced approved `evidence/manifest.yaml`
2. Confirm job logs and/or spool files are listed with sensitivity status
3. Provide this skill with the evidence manifest path and inventory
4. Run through 9-step workflow
5. Review output `runtime-evidence.jsonl` and SME checklist
6. Share with IBM i SME for review and sign-off

### Typical Call Context
```
orchestrator → "stage: analysis; next: legacy-ibmi-program-analyzer"
       (but also run in parallel or before program-analyzer)
→ legacy-ibmi-runtime-evidence-miner
       + optional runtime_hints fed into program-analyzer
       + optional bau_notes fed into flow-analyzer
       + optional View 1 context fed into module-analyzer
```

### Output Consumption Examples

**Program Analyzer**:
```
/legacy-ibmi-program-analyzer
  --program OBJ-CREDIT-CHECK-001
  --inventory 01_inventory/inventory.yaml
  --runtime_hints runtime-evidence.jsonl
  → output: program-analysis-OBJ-CREDIT-CHECK-001.md
     (with enhanced evidence_strength tags for runtime-confirmed behaviors)
```

**Flow Analyzer**:
```
/legacy-ibmi-flow-analyzer
  --flow BATCH-RECON
  --program_analyses 02_programs/*/program-analysis-*.md
  --bau_notes runtime-evidence.jsonl
  → output: flow-BATCH-RECON.md
     (with BAU timing and error patterns grounded in logs)
```

---

## Skill Portability

This skill is portable across Codex, Claude Code, and OpenCode. All runtime references are to file paths relative to the evidence directory; no IDE-specific or site-specific assumptions.

**Adapter folders** (synced from canonical):
- `.claude/skills/legacy-ibmi-runtime-evidence-miner/SKILL.md`
- `.codex/skills/legacy-ibmi-runtime-evidence-miner/SKILL.md`
- `.opencode/skills/legacy-ibmi-runtime-evidence-miner/SKILL.md`
- `.agents/skills/legacy-ibmi-runtime-evidence-miner/SKILL.md`

Use `scripts/sync-skills.sh --target all` to keep them synchronized.

---

## Authorship & Maintenance

**Original author**: Leo L Zhang  
**Copyright**: 2026 Leo L Zhang  
**License**: Apache License 2.0

This skill is part of the Legacy Spec Factory project. See LICENSE and NOTICE files in the project root for full terms.

**Version History**:

- v0.2.0 (2026-05-16): Added Rule Auto-Validation pass. After mining,
  cross-checks any `inferred_business_rule` against runtime samples and
  promotes corroborated rules from `needs_sme_review` to
  `auto_validated_spot_check_only`. Default threshold N=3 matching
  samples; conflicting samples flag `runtime_conflict_with_inference`
  and escalate. Critical-criticality rules touching money/posting/
  compliance never auto-validate. Full protocol with eligibility,
  threshold logic, conflict handling, audit trail, and anti-patterns
  in `references/rule-auto-validation-protocol.md`. Together with the
  inventory criticality field this reduces typical SME review load by
  ~30–60% per capability.
- v0.1.0 (2026-05-16): Initial runtime evidence miner. Frontmatter,
  confidence rules, `job_log` artifact typing, single-run frequency guard,
  and `mining-checklist.md` output contract validated by positive and
  negative no-write smoke in Codex CLI (`gpt-5.4-mini`), Claude Code
  (`haiku`), and OpenCode (`opencode/minimax-m2.5-free`).

**Maintenance**: Update version number and this section when the skill is revised.
