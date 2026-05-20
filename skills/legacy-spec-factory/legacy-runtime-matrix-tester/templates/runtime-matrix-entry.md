# Runtime Matrix Entry Template

Use this template when updating `docs/runtime-matrix.md` after running runtime
smoke tests for a skill.

## Table Row Format

```markdown
| `legacy-SKILL-NAME` | vX.Y.Z | STATUS | STATUS | STATUS | Notes... |
```

Replace:
- `legacy-SKILL-NAME` with the actual skill name
- `vX.Y.Z` with the canonical version tested
- `STATUS` with one of: `passed`, `executed`, `loaded`, `synced`, `failed`, `not tested`
- `Notes...` with details (see below)

## Status Definitions

| Status | Meaning |
|--------|---------|
| `passed` | Skill discovered, loaded, and trigger produced expected output following output contract. No files created/edited. Negative case (if applicable) also blocked correctly. |
| `executed` | Skill discovered, loaded, trigger produced output, but did not fully meet all pass criteria. Retest or refinement needed. |
| `loaded` | Skill discovered and loaded in runtime, but trigger test not yet run or did not produce expected output. |
| `synced` | Skill adapter created by sync script but not yet tested or loaded. Or, test was blocked by runtime unavailability. |
| `failed` | Skill not discovered, failed to load, or critical blocker encountered. |
| `not tested` | Not yet attempted. |

## Notes Cell Format

The Notes cell should include:

1. **Runtime engine + model**: e.g., `Codex CLI (gpt-5.4-mini)`, `Claude Code (haiku)`, `OpenCode (minimax-m2.5-free)`
2. **Test date**: e.g., `2026-05-16`
3. **Test outcome**: One sentence summary of what passed/failed
4. **Blocking issues** (if any): e.g., "Claude Code missing login; cannot test", "Negative case missing; cannot fully validate"
5. **Artifacts**: Reference to the scorecard if created: `See docs/reviews/legacy-SKILL-vX.Y.Z-scorecard.md`

## Example

```markdown
| `legacy-ibmi-inventory` | v0.1.0 | passed | passed | passed | Positive and negative no-write smoke passed on 2026-05-16. Codex CLI (gpt-5.4-mini, read-only ephemeral), Claude Code (haiku, Read-only tools), and OpenCode (minimax-m2.5-free) all invoked `/legacy-ibmi-inventory`. Positive smoke returned the three required artifacts (inventory.yaml, object-map.md, inventory-review-checklist.md), confirmed TBD tagging, and preserved SME gate. Negative smoke blocked missing tier-1 evidence. See docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md. |
```

## Checklist Before Updating Matrix

- [ ] All three target runtimes have been tested (or explicitly marked `synced` with a blocker reason)
- [ ] Status values match actual test outcomes (not aspirational)
- [ ] Notes include date, runtime + model, and one-line outcome
- [ ] If scorecard was created, scorecard path is linked in Notes
- [ ] Matrix syntax is valid (pipe separators, no orphaned cells)
