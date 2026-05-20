# Happy Path Expected Output

This is what the legacy-runtime-matrix-tester skill should produce when given
the prompt in `prompt.txt`.

## Pre-Test Checks

```
[pass] Skill exists: skills/legacy-ibmi-inventory/SKILL.md
[pass] Sync check: scripts/sync-skills.sh --skill legacy-ibmi-inventory --target all --check exit 0
[pass] Contract validation: python3 scripts/check-spec-contract.py exit 0
[pass] Canonical source synced: adapter copies match canonical source
[pass] Test prompts available: docs/runtime-smoke-tests.md and/or skills/legacy-ibmi-inventory/examples/
```

## Per-Runtime Results

### Codex CLI (gpt-5.4-mini)

#### Phase 1 - Discovery
```
[pass] Codex adapter exists and skill invocation confirms runtime load
[pass] Skill description is visible
[pass] No frontmatter errors
[pass] No path resolution errors
Status: loaded
```

#### Phase 2 - Trigger
```
Invoked: /legacy-ibmi-inventory [pass]
Output Contract Check:
  [pass] inventory.yaml generated
  [pass] object-map.md generated
  [pass] inventory-review-checklist.md generated
  [pass] TBD-CREDIT-CHECK-* IDs present
  [pass] OBJ-* IDs assigned
  [pass] sme_review.decision = "approved" or "approved_with_non_blocking_tbd"
  [pass] No files actually created (ephemeral mode)
Status: passed
```

#### Phase 3 - Adversarial
```
Scenario: Negative case - missing PRTF, inventory.yaml has sme_review.decision: blocked
Invoked: /legacy-ibmi-inventory [pass]
Blocking Check:
  [pass] Skill correctly identified blocking condition
  [pass] Router explanation: "Cannot advance to program analyzer. Missing tier-1 evidence: CRHOLDP (PRTF). Create TBD-CREDIT-CHECK-001 and route back to inventory resume."
  [pass] No downstream outputs (inventory.yaml not marked approved)
Status: passed
```

### Claude Code (haiku)

#### Phase 1 - Discovery
```
[pass] Claude Code adapter exists and skill invocation confirms runtime load
[pass] Skill description is visible
[pass] No frontmatter errors
[pass] No path resolution errors
Status: loaded
```

#### Phase 2 - Trigger
```
Invoked: /legacy-ibmi-inventory [pass]
Output Contract Check:
  [pass] All required artifacts present in output
  [pass] IDs properly tagged
  [pass] SME review gate documented
  [pass] No files written
Status: passed
```

#### Phase 3 - Adversarial
```
Status: passed
```

### OpenCode (minimax-m2.5-free)

#### Phase 1 - Discovery
```
[pass] OpenCode adapter exists and skill invocation confirms runtime load
[pass] Skill description is visible
[pass] No frontmatter errors
[pass] No path resolution errors
Status: loaded
```

#### Phase 2 - Trigger
```
Invoked: /legacy-ibmi-inventory [pass]
Output Contract Check:
  [pass] All required artifacts present
  [pass] IDs properly tagged
  [pass] SME review gate documented
  [pass] No files written
Status: passed
```

#### Phase 3 - Adversarial
```
Status: passed
```

## Summary

| Runtime | Discovery | Trigger | Adversarial | Final Status |
|---------|-----------|---------|-------------|--------------|
| Codex | passed | passed | passed | passed |
| Claude Code | passed | passed | passed | passed |
| OpenCode | passed | passed | passed | passed |

**Overall:** `passed`

## Matrix Update

The following entry was added to `docs/runtime-matrix.md`:

```markdown
| `legacy-ibmi-inventory` | v0.1.0 | passed | passed | passed | Positive and negative no-write smoke passed on 2026-05-16. Codex CLI (gpt-5.4-mini, read-only ephemeral), Claude Code (haiku, Read-only tools), and OpenCode (minimax-m2.5-free) all invoked `/legacy-ibmi-inventory`. Positive smoke returned the three required artifacts (inventory.yaml, object-map.md, inventory-review-checklist.md), confirmed TBD tagging, and preserved SME gate. Negative smoke blocked missing tier-1 evidence. See docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md. |
```

## Scorecard

Created: `docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md`

**Decision:** `field-pilot ready` (eligible for 9.5+ score)

**Rationale:**
- All three target runtimes passed discovery + trigger + adversarial phases
- Output contract verified in all runtimes
- No files created during no-write test
- Negative cases correctly blocked with clear router explanations
- Pre-test checks all passed
- No mandatory stop conditions triggered

## Next Steps

1. [pass] Merge runtime-matrix.md update and scorecard in the same commit
2. [pass] Skill is now eligible for field pilot with real SME / engineering users
3. [pass] If issues arise during field pilot, create a new scorecard with updated notes
