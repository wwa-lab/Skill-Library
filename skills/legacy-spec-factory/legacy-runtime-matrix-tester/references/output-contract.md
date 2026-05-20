# Output Contract for legacy-runtime-matrix-tester

This document defines the exact artifacts and structure that the
legacy-runtime-matrix-tester skill must produce.

## Artifacts

### 1. Updated Runtime Matrix: `docs/runtime-matrix.md`

**Type:** Markdown table update
**When:** After all runtime tests complete
**Mutability:** Updates existing skill row; adds new row if skill is new

**Required fields in row:**

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| Skill name | markdown link | `` `legacy-ibmi-inventory` `` | Backtick-quoted, lowercase, hyphenated |
| Canonical version | semver | `v0.1.0` | Must match skill SKILL.md version history entry |
| Codex status | enum | `passed` | One of: not tested, synced, loaded, executed, passed, failed |
| Claude Code status | enum | `passed` | Same enum |
| OpenCode status | enum | `passed` | Same enum |
| Notes | markdown text | "Positive and negative ... passed on 2026-05-16." | See notes format below |

The row must have exactly six cells in this order:

```markdown
| `skill-name` | vX.Y.Z | codex-status | claude-code-status | opencode-status | notes |
```

The skill cell must be backtick-quoted. Do not add an overall status column.
Do not wrap the version or runtime status values in backticks. Runtime status
values must be lowercase exact enum values.

**Notes format:**

```markdown
[Outcome summary]. [Runtime] ([Model]) [Details]. [Link if scorecard created].
```

Example:

```
Positive and negative no-write smoke passed on 2026-05-16. Codex CLI (gpt-5.4-mini,
read-only ephemeral), Claude Code (haiku, Read-only tools), and OpenCode
(minimax-m2.5-free) all invoked `/legacy-ibmi-inventory`. Positive smoke returned
the three required artifacts, confirmed TBD tagging. Negative smoke blocked
missing tier-1 evidence. See docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md.
```

Key elements:
- Test outcome (passed, executed, blocked, etc.)
- Date in YYYY-MM-DD format
- Each runtime listed with model name in parentheses
- One-sentence summary of what passed/failed per runtime (optional)
- Link to scorecard file (if created)

**Decision rule for all-passed evidence:**

If Codex, Claude Code, and OpenCode are all `passed`, the matrix row must show
all three runtime columns as `passed`, and the scorecard decision must be
`field-pilot ready`. Do not preserve a stale prior matrix status when the user
has provided new passing test evidence. Do not downgrade to `repo-ready`
because the scorecard file has not been written yet in a no-write smoke run.

### 2. Review Scorecard: `docs/reviews/<skill>-v<X>.<Y>.<Z>-scorecard.md`

**Type:** Markdown document
**When:** After all runtime tests complete
**Mutability:** Create new file if version-new; update if re-testing same version

**Required sections:**

1. **Frontmatter (or header block)**
   - Skill name
   - Canonical version
   - Test date (YYYY-MM-DD)
   - Tester identity
   - Decision (repo-ready / field-pilot ready / blocked)

2. **Pre-Test Checks Table**
   - Rows for: source exists, sync passes, contract valid, canonical clean, test prompts available
   - Columns: Check | Result | Evidence
   - All checks must be `pass`, or any non-pass result must be documented

3. **Per-Runtime Result Sections**
   - One section per runtime (Codex, Claude Code, OpenCode)
   - Subsections for Phase 1 (Discovery), Phase 2 (Trigger), Phase 3 (Adversarial)
   - For each phase:
     - Checkbox list of pass criteria
     - "Outcome: [passed/executed/failed]"
     - Notes or examples of actual output (if relevant)

4. **Summary Table**
   - Three rows (one per runtime)
   - Columns: Runtime | Final Status
   - Single status per runtime (highest achieved: passed > executed > loaded > failed)

5. **Matrix Update Section**
   - Exact markdown table row that was added/updated
   - Allows tracing scorecard back to matrix

6. **Blocking For Field Pilot? Section**
   - Checklist against mandatory stop conditions from skill-review-gate.md
   - Boolean: "Blocking Found: [Yes/No]"

7. **Lifted Caps Section**
   - Note if this scorecard lifts the "portability not tested" 9.0 cap
   - Rationale for the decision

8. **Recommendation and Next Steps**
   - Decision: repo-ready / field-pilot ready / blocked
   - Rationale
   - Action items for next revision (if any)

9. **Notes for Future Revisions**
   - Free-form section for lessons learned or environment quirks

10. **Sign-Off**
    - Date scorecard was created
    - Tester name/identity

**File name format:**

```
docs/reviews/legacy-<SKILL-NAME>-v<MAJOR>.<MINOR>.<PATCH>-scorecard.md
```

Example: `docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md`

### 3. Test Report (Console or File)

**Type:** Text/Markdown summary
**When:** Generated at end of test run (optional; for logging/audit)
**Mutability:** Not committed to repo; informational only

**Produced by:** The runtime tester (Claude Code, Codex, or human)

**Contains:**
- Skill name and version
- Per-runtime discovery/trigger/adversarial results
- Pass/fail checklist with reasoning
- Link to scorecard
- Recommended next actions
- Blocker summary (if any)

Use `templates/runtime-test-report.md` to structure.

---

## Output Validation Rules

### Structural Rules

- Runtime matrix row syntax must be valid Markdown (pipe-delimited columns)
- Scorecard file must be valid Markdown with clear section headers
- All file paths must be relative to project root
- No hardcoded absolute paths (e.g., `/Users/leo/...`)

### Semantic Rules

- Status values must be one of: `not tested`, `synced`, `loaded`, `executed`, `passed`, `failed`
- Version numbers must match the canonical skill version (from SKILL.md history)
- Test date must be in YYYY-MM-DD format
- Scorecard decision must be one of: `repo-ready`, `field-pilot ready`, `blocked`
- Scorecard decision must not be `pass`, `passed`, `executed`, `loaded`, or
  any runtime status value
- All pre-test checks must be documented (not assumed)
- Scorecard location must point to
  `docs/reviews/<skill>-v<X>.<Y>.<Z>-scorecard.md`, not to this skill's
  templates

### Consistency Rules

- Skill name in matrix row must match the directory name (`legacy-SKILL-NAME`)
- Version in matrix must match scorecard filename
- Scorecard decision must align with actual test results (not aspirational)
- If a runtime is `failed`, decision must be `blocked` (not field-pilot ready)
- If a required negative case exists but was not run, decision cannot exceed `executed`
- Runtime-unavailable environment issues with a synced adapter must be recorded
  as runtime status `synced`, not as a non-enum `blocked`
- If a requested target runtime is blocked by credentials, login, network, or
  missing local runtime, keep the runtime status at `synced` when the adapter
  is present, set the smoke-run scorecard decision to `blocked`, and state
  that field-pilot readiness is blocked until that runtime is tested

### Immutability Rules

- Do not edit or delete existing matrix rows for other skills
- Do not edit scorecard decisions after initial sign-off (create new version if re-testing)
- Do not backfill test results after the fact (only record live test outcomes)

---

## Example Output

### Matrix Row (Before)

```markdown
| `legacy-ibmi-inventory` | not tested | not tested | not tested | not tested | Not yet tested. |
```

### Matrix Row (After)

```markdown
| `legacy-ibmi-inventory` | v0.1.0 | passed | passed | passed | Positive and negative no-write smoke passed on 2026-05-16. Codex CLI (gpt-5.4-mini, read-only ephemeral), Claude Code (haiku, Read-only tools), and OpenCode (minimax-m2.5-free) all invoked `/legacy-ibmi-inventory`. Positive smoke returned the three required artifacts (inventory.yaml, object-map.md, inventory-review-checklist.md), confirmed TBD tagging. Negative smoke blocked missing tier-1 evidence. See docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md. |
```

### Scorecard (Excerpt)

```markdown
# Review Scorecard: `legacy-ibmi-inventory` v0.1.0

**Test Date:** 2026-05-16
**Tester:** Claude Code
**Decision:** `field-pilot ready`

## Per-Runtime Results

### Codex CLI
- [x] Skill discovered
- [x] Output follows contract
- [x] Negative case blocked correctly
**Outcome:** `passed`

### Claude Code
- [x] Skill discovered
- [x] Output follows contract
- [x] Negative case blocked correctly
**Outcome:** `passed`

### OpenCode
- [x] Skill discovered
- [x] Output follows contract
- [x] Negative case blocked correctly
**Outcome:** `passed`

## Recommendation

**Decision:** `field-pilot ready` (eligible for 9.5+ score)

**Rationale:** All three target runtimes passed all phases. Output contract
verified. No side effects.
```

---

## Handoff to Orchestrator

When this skill completes, the orchestrator (`legacy-modernization-orchestrator`)
receives:

- Status of the skill's runtime matrix entry (all runtimes at `passed` or not)
- Whether the skill is eligible for field pilot (decision = field-pilot ready)
- Link to scorecard for reference

The orchestrator uses this to decide whether to advance the skill to the next
stage of validation or flag it for remediation.

---

## Version History

- v0.1.0 (2026-05-16): Initial output contract definition.
