# Negative Case Expected Output: Portability Blocker

This demonstrates what the legacy-runtime-matrix-tester skill should do when
a runtime is unavailable due to environment/credential issues.

## Analysis

**Issue Detected:** Claude Code runtime unavailable for testing

```
[fail] Claude Code runtime check failed:
  Error: "Not logged in - run claude auth login or sign in through the app"
  Blocked by: Missing authentication
  Severity: Cannot test; blocks field-pilot eligibility
```

## Recommendation

**Do NOT mark Claude Code as `passed` or `executed`.**

Reasons:
1. **Mandatory stop condition:** All three target runtimes must be tested for
   a skill to be marked field-pilot ready (see skill-review-gate.md)
2. **Incomplete picture:** Codex passing does not guarantee Claude Code
   compatibility (runtimes have different constraint levels, model biases, and
   behavior)
3. **Field-pilot risk:** If Claude Code fails in field pilot, you lose time and
   credibility

## Matrix Entry Recommendation

Mark the skill row as:

```markdown
| `legacy-spec-writer` | v0.2.0 | passed | synced | passed | Positive/negative smoke passed on Codex (gpt-5.4-mini) and OpenCode (minimax-m2.5-free) on 2026-05-16. Claude Code testing blocked: local CLI not logged in (env issue, not skill issue). See docs/reviews/legacy-spec-writer-v0.2.0-scorecard.md. |
```

Key points:
- Codex: `passed` (you tested it)
- Claude Code: `synced` (adapter created but not tested)
- OpenCode: `passed` (you tested it)
- Notes: Explain blocker, clarify it's environmental not a skill defect

## Scorecard Decision

```
Decision: blocked (NOT field-pilot ready)

Reason:
- Two of three runtimes passed (Codex, OpenCode)
- Claude Code could not be tested due to CLI auth issue
- All three runtimes must pass before field-pilot eligibility
- Issue is environmental (user must log in); the smoke run is blocked until
  retry

Blocking For 9.5: Yes
  - Cannot lift "portability not tested" cap until all three runtimes pass
  - Recommend: "Fix Claude auth, re-run discovery/trigger for Claude Code,
    update matrix and scorecard"
```

## Next Steps

1. **Fix the environment:**
   ```bash
   claude auth login
   # or: check ~/.claude/credentials if local CLI is not paired
   ```

2. **Re-run Claude Code tests:**
   - Just discovery and trigger phases (not full re-test of other runtimes)
   - Update `docs/reviews/legacy-spec-writer-v0.2.0-scorecard.md` with Claude
     Code results
   - Update matrix entry: change Claude Code from `synced` to `passed`

3. **Bump scorecard decision:**
   - Once all three runtimes reach `passed`, update decision to `field-pilot ready`
   - Version the scorecard update (e.g., add a "Updates" section with date)
   - Commit scorecard and matrix updates together

## Key Learning

This skill's job is to **block premature field pilots.** If a critical runtime
is untested, the answer is "not ready yet" - not "let's hope it works." The
runtime matrix is a contract: field-pilot ready means all three runtimes passed.
