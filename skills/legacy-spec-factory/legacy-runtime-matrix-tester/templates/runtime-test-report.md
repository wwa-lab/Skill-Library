# Runtime Test Report Template

Use this template when generating a console or file-based report for test
execution. Fill in sections as the test runs.

---

## Runtime Smoke Test Report

**Skill:** `legacy-SKILL-NAME`
**Version:** vX.Y.Z
**Test Date:** YYYY-MM-DD
**Tester:** [Claude Code / Codex / OpenCode]
**Status:** [In Progress / Passed / Blocked]

---

## Pre-Test Checks

| Check | Result | Details |
|-------|--------|---------|
| Skill exists in canonical source | pass/fail | `skills/legacy-SKILL-NAME/SKILL.md` is present and readable |
| Sync drift | pass/fail | `scripts/sync-skills.sh --skill legacy-SKILL-NAME --target all --check` exit code 0 |
| Contract validation | pass/fail | `python3 scripts/check-spec-contract.py` (if applicable) exit code 0 |
| Canonical SKILL.md is synced | pass/fail | Canonical files match the tested adapter copies |
| Test prompts available | pass/fail | Canonical prompts in `docs/runtime-smoke-tests.md` or `examples/`, or override provided |

**Pre-Test Decision:** [Continue to runtime testing / Block until checks pass]

---

## Runtime: Codex CLI

**Engine:** gpt-5.4-mini
**Discovery:** [Passed / Failed]
**Trigger:** [Passed / Executed / Failed]
**Adversarial:** [Passed / Skipped / N/A]

### Phase 1 - Discovery

- [ ] Runtime adapter exists
- [ ] Runtime invocation confirms the skill loads
- [ ] Skill description is visible
- [ ] No frontmatter errors
- [ ] No path resolution errors

**Notes:** [Details if any check failed]

### Phase 2 - Trigger

**Test Prompt:** [Canonical prompt ID or custom override]

**Output Quality:**
- [ ] Correct skill was invoked (not a sibling skill)
- [ ] Output follows declared output contract
- [ ] All required artifact filenames mentioned
- [ ] All required ID prefixes (BR-, TBD-, OBJ-, etc.) present or correctly absent
- [ ] No files created or edited

**Expected vs. Actual:**

Expected:
```
[What the output contract says should appear]
```

Actual:
```
[What the skill actually produced]
```

**Assessment:** [Passed / Executed / Failed]
**Blocker (if any):** [None / Description]

### Phase 3 - Adversarial (Optional)

**Test Prompt:** [Negative-case prompt ID]

**Block/Refuse Quality:**
- [ ] Skill correctly identifies blocking condition
- [ ] Gate/router explanation is clear
- [ ] No unwanted artifacts created

**Assessment:** [Passed / Skipped / Failed]

---

## Runtime: Claude Code

**Engine:** haiku
**Discovery:** [Passed / Failed]
**Trigger:** [Passed / Executed / Failed]
**Adversarial:** [Passed / Skipped / N/A]

### Phase 1 - Discovery

- [ ] Runtime adapter exists
- [ ] Runtime invocation confirms the skill loads
- [ ] Skill description is visible
- [ ] No frontmatter errors
- [ ] No path resolution errors

**Notes:** [Details if any check failed]

### Phase 2 - Trigger

**Test Prompt:** [Canonical prompt ID or custom override]

**Output Quality:**
- [ ] Correct skill was invoked
- [ ] Output follows declared output contract
- [ ] All required artifact filenames mentioned
- [ ] All required ID prefixes present or correctly absent
- [ ] No files created or edited

**Assessment:** [Passed / Executed / Failed]
**Blocker (if any):** [None / Description]

### Phase 3 - Adversarial (Optional)

**Test Prompt:** [Negative-case prompt ID]

**Assessment:** [Passed / Skipped / Failed]

---

## Runtime: OpenCode

**Engine:** minimax-m2.5-free
**Discovery:** [Passed / Failed]
**Trigger:** [Passed / Executed / Failed]
**Adversarial:** [Passed / Skipped / N/A]

### Phase 1 - Discovery

- [ ] Runtime adapter exists
- [ ] Runtime invocation confirms the skill loads
- [ ] Skill description is visible
- [ ] No frontmatter errors
- [ ] No path resolution errors

**Notes:** [Details if any check failed]

### Phase 2 - Trigger

**Test Prompt:** [Canonical prompt ID or custom override]

**Output Quality:**
- [ ] Correct skill was invoked
- [ ] Output follows declared output contract
- [ ] All required artifact filenames mentioned
- [ ] All required ID prefixes present or correctly absent
- [ ] No files created or edited

**Assessment:** [Passed / Executed / Failed]
**Blocker (if any):** [None / Description]

### Phase 3 - Adversarial (Optional)

**Test Prompt:** [Negative-case prompt ID]

**Assessment:** [Passed / Skipped / Failed]

---

## Summary

| Runtime | Discovery | Trigger | Adversarial | Final Status |
|---------|-----------|---------|-------------|--------------|
| Codex | [Result] | [Result] | [Result] | [Status] |
| Claude Code | [Result] | [Result] | [Result] | [Status] |
| OpenCode | [Result] | [Result] | [Result] | [Status] |

**Overall:** [Passed / Executed / Blocked]

---

## Matrix Update

The following entry was added/updated to `docs/runtime-matrix.md`:

```markdown
| `legacy-SKILL-NAME` | vX.Y.Z | [status] | [status] | [status] | [notes] |
```

---

## Scorecard Update

Created or updated: `docs/reviews/legacy-SKILL-NAME-vX.Y.Z-scorecard.md`

**Decision:** [repo-ready / field-pilot ready / blocked]

---

## Next Actions

- [ ] Merge this test result in the same PR/commit as the skill
- [ ] If blocked, document required remediation
- [ ] If passed, skill is eligible for field pilot
- [ ] If executed, consider re-test after minor fixes

---

## Tester Notes

[Any additional context about the test run, environment issues, assumptions,
or recommendations for the next revision.]
