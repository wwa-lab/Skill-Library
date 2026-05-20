# Review Scorecard Template

Use this template to create or update `docs/reviews/legacy-SKILL-NAME-vX.Y.Z-scorecard.md`
after completing runtime smoke tests.

---

# Review Scorecard: `legacy-SKILL-NAME` v0.1.0

**Test Date:** 2026-05-16
**Tester:** [Claude Code / Codex / OpenCode]
**Review Gate Version:** See `docs/skill-review-gate.md`
**Decision:** [repo-ready / field-pilot ready / blocked]

---

## Pre-Test Checks

| Check | Result | Evidence |
|-------|--------|----------|
| Canonical source exists | pass | `skills/legacy-SKILL-NAME/SKILL.md` |
| Skill not already at `passed` in all runtimes | pass | Prior matrix entry shows `synced` or `loaded` |
| Sync check passes | pass | `scripts/sync-skills.sh --skill legacy-SKILL-NAME --target all --check` exit 0 |
| Contract validation passes (if applicable) | pass | `python3 scripts/check-spec-contract.py` exit 0 |
| Canonical source is synced | pass | Canonical files match the tested adapter copies |
| Test prompts available | pass | `docs/runtime-smoke-tests.md` or `examples/` contains canonical prompt(s) |

---

## Per-Runtime Results

### Codex CLI

**Runtime:** gpt-5.4-mini
**Date:** 2026-05-16

| Phase | Status | Notes |
|-------|--------|-------|
| Discovery | passed | Adapter exists; runtime invocation confirms load; description visible; no frontmatter errors |
| Trigger | passed | Correct skill invoked; output follows contract; all required artifacts named |
| Adversarial | passed | Negative case blocked correctly with clear gate explanation |

**Outcome:** `passed`

### Claude Code

**Runtime:** haiku
**Date:** 2026-05-16

| Phase | Status | Notes |
|-------|--------|-------|
| Discovery | passed | Adapter exists; runtime invocation confirms load; description visible; no errors |
| Trigger | passed | Correct skill invoked; output meets contract |
| Adversarial | passed | Negative case blocked correctly |

**Outcome:** `passed`

### OpenCode

**Runtime:** minimax-m2.5-free
**Date:** 2026-05-16

| Phase | Status | Notes |
|-------|--------|-------|
| Discovery | passed | Adapter exists; runtime invocation confirms load; description visible; no errors |
| Trigger | passed | Correct skill invoked; output follows contract |
| Adversarial | passed | Negative case blocked correctly |

**Outcome:** `passed`

---

## Summary

| Runtime | Final Status |
|---------|--------------|
| Codex | `passed` |
| Claude Code | `passed` |
| OpenCode | `passed` |

**All Required Runtimes Tested:** Yes

**Blocker Found:** No

---

## Runtime Matrix Update

Updated `docs/runtime-matrix.md` with:

```markdown
| `legacy-SKILL-NAME` | v0.1.0 | passed | passed | passed | Positive and negative no-write smoke passed on 2026-05-16. Codex CLI (gpt-5.4-mini, read-only ephemeral), Claude Code (haiku, Read-only tools), and OpenCode (minimax-m2.5-free) all invoked `/legacy-SKILL-NAME`. All phases completed successfully. See docs/reviews/legacy-SKILL-NAME-v0.1.0-scorecard.md. |
```

---

## Blocking For Field Pilot?

Check the `docs/skill-review-gate.md` mandatory stop conditions:

- [x] Valid `SKILL.md` with strong frontmatter
- [x] Copyright and authorship notice
- [x] Portable across Codex, Claude Code, OpenCode
- [x] No runtime-specific assumptions mixed in
- [x] Clear trigger conditions
- [x] Clear output contract
- [x] SME review gates (if IBM i skill)
- [x] Anti-hallucination rules documented

**Blocking Found:** No - all mandatory conditions met

---

## Lifted Caps

Previous scorecard (if any) may have noted:

> "Portability has been considered but not tested" - capped at 9.0

**This scorecard lifts the cap:** All three runtimes passed discovery and trigger
phases. No portability blockers found.

---

## Recommendation

**Decision:** `field-pilot ready` (eligible for 9.5+ score)

**Rationale:**
- All three target runtimes passed phase 1 and phase 2
- Output contract verified in all runtimes
- No files created during no-write test
- Negative cases passed (where applicable)
- Pre-test checks all passed

**Next Steps:**
1. Merge runtime-matrix.md update and this scorecard in the same PR/commit
2. Skill is now eligible for field pilot with real SME / engineering users
3. If any issues arise during field pilot, create a new scorecard with issue notes

---

## Notes for Future Revisions

[Any lessons learned, environment quirks, assumptions, or recommendations
for the next version of this skill or the next round of testing.]

---

**Scorecard Created:** 2026-05-16
**Scorecard Author:** [Tester Name/Claude Code]
