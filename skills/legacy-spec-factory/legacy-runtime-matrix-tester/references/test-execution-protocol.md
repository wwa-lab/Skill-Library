# Test Execution Protocol

This document details the step-by-step procedure for running the runtime smoke
tests and updating the runtime matrix. Use this as your checklist when
executing runtime tests.

## Overview

The goal: confirm that a skill can be discovered, loaded, and executed in all
three target runtimes (Codex, Claude Code, OpenCode) with no side effects
(no files created).

**Success criteria:**
- Runtime adapter is present and the runtime invocation confirms the skill
  can load
- Skill loads without frontmatter or path errors
- Skill correctly fires on its declared trigger prompt
- Skill output follows the declared output contract
- No files are created or edited during test
- Optional: negative-case scenario correctly blocks with explanation

## Pre-Test Setup

### Prerequisites

You will need:
- Access to three runtimes:
  - Codex CLI (requires installation; see `scripts/setup-codex.sh`)
  - Claude Code (requires login via `claude auth login` or in-app)
  - OpenCode (requires agentstack; see project setup docs)
- The skill source under `skills/legacy-SKILL-NAME/SKILL.md`
- The canonical test prompts in `docs/runtime-smoke-tests.md` or
  `skills/legacy-SKILL-NAME/examples/`
- Git access to the project root to run pre-test checks and updates

### 1. Verify Skill Readiness

```bash
# Check that the skill exists
ls -la skills/legacy-SKILL-NAME/SKILL.md

# Verify no syntax errors in frontmatter
head -10 skills/legacy-SKILL-NAME/SKILL.md
```

If the skill does not exist or has invalid frontmatter, stop and report to the
skill author.

### 2. Run Pre-Test Checks

All of these must pass before proceeding:

```bash
# Check for sync drift on the target skill only
scripts/sync-skills.sh --skill legacy-SKILL-NAME --target all --check
# Expected: exit code 0

# Check contract validation (if skill touches spec.yaml)
python3 scripts/check-spec-contract.py
# Expected: exit code 0

# Check the canonical source state
git status --short skills/legacy-SKILL-NAME/
# Expected: any canonical changes under test have already been synced to adapters

# Verify test prompts exist
ls -la skills/legacy-SKILL-NAME/examples/
# Expected: at least one scenario prompt, or a prompt in docs/runtime-smoke-tests.md
```

If any check fails, fix it before testing. Record the results in the scorecard.

### 3. Gather Test Prompts

For each skill, you need:

1. **Canonical positive test prompt**
   - Location: `docs/runtime-smoke-tests.md` or
     `skills/legacy-SKILL-NAME/examples/<SCENARIO>/`
   - Filename: usually `prompt.txt` or similar
   - If missing, ask the skill author or provide your own override

2. **Optional: Canonical negative test prompt**
   - Location: `docs/runtime-smoke-tests.md` or
     `skills/legacy-SKILL-NAME/examples/<SCENARIO>/`
   - Use this only if the skill has blocking gates or router logic
   - If missing, mark Phase 3 as "skipped" in the report

### 4. Create Scorecard Stub

Create a new file: `docs/reviews/legacy-SKILL-NAME-vX.Y.Z-scorecard.md`

Use `templates/review-scorecard-template.md` and fill in:
- Skill name and version
- Test date (today)
- Tester identity (your name or "Claude Code")
- Pre-test check results (from step 2 above)
- Stub entries for per-runtime results (fill in during runtime tests)

Commit or save this stub (do not yet push).

## Per-Runtime Test Execution

Run the following for each runtime in sequence. The goal is to isolate issues
per runtime rather than having all fail at once.

### Runtime 1: Codex CLI

#### Setup

```bash
# Ensure Codex is installed and available
which codex

# Verify you are in the project root
pwd
# Expected: /Users/leo/wwa-lab/GitHub/legacy-spec-factory

# Ensure the skill is synced
scripts/sync-skills.sh --skill legacy-SKILL-NAME --target codex --check
```

#### Phase 1 - Discovery

```bash
# Check that the Codex adapter exists and exposes readable frontmatter
test -f .codex/skills/legacy-SKILL-NAME/SKILL.md
sed -n '1,12p' .codex/skills/legacy-SKILL-NAME/SKILL.md

# If Codex exposes an interactive skill list in the local install, capture it
# as additional evidence. The mandatory proof is adapter presence plus
# successful Phase 2 invocation.
```

**Outcome:** `loaded` if the adapter is readable and Phase 2 does not report a
load/frontmatter/path error; `failed` if the adapter is missing or load errors
are reported.

#### Phase 2 - Trigger (Codex)

```bash
# Run the canonical test prompt
# Example (adjust for your skill):

codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini "
Use /legacy-SKILL-NAME.

User input:
[CANONICAL TEST PROMPT CONTENT HERE]

Return only:
- [Expected output fields from SKILL.md output contract]
"
```

**Evaluation checklist:**
- [ ] Correct skill was invoked (response mentions the skill name or output)
- [ ] Output follows the declared output contract
- [ ] All required artifact filenames are mentioned
- [ ] All required ID prefixes (BR-, TBD-, OBJ-, AC-, etc.) are present or
      correctly absent
- [ ] No files were created or edited (should be in ephemeral mode)
- [ ] Response includes any expected gate information (e.g., "approval required",
      "blocked by missing evidence")

**Outcome:**
- `passed` if all checks pass
- `executed` if output was produced but some checks failed
- `failed` if skill did not run or produced no output

Record the actual response in the scorecard under "Codex CLI > Phase 2".

#### Phase 3 - Adversarial (Codex, Optional)

If a negative-case prompt exists in `docs/runtime-smoke-tests.md` or the target
skill's `examples/`:

```bash
codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini "
Use /legacy-SKILL-NAME.

User input:
[NEGATIVE TEST PROMPT CONTENT HERE]

Return only:
- gate status (blocked / approved / needs_review)
- reason
- next step
"
```

**Evaluation checklist:**
- [ ] Skill correctly identifies the blocking condition
- [ ] Explanation mentions the specific gate or rule that blocks the input
- [ ] Routing (e.g., "go back to X skill") is clear
- [ ] No files were created despite the negative input

**Outcome:** `passed` if all checks pass; `skipped` if no negative case exists.

Record outcome in scorecard under "Codex CLI > Phase 3".

### Runtime 2: Claude Code

#### Setup

```bash
# Verify login
claude auth status
# Expected: "Logged in"

# Verify skill is synced
scripts/sync-skills.sh --skill legacy-SKILL-NAME --target claude --check
```

#### Phase 1 - Discovery

Run this from within Claude Code when using an interactive session:

```
/skills
```

This lists all available skills. Look for `legacy-SKILL-NAME`. If found, you
are at `loaded`. For non-interactive `claude -p` runs, use the adapter check
above and the Phase 2 invocation as discovery evidence.

#### Phase 2 - Trigger (Claude Code)

Within Claude Code, run:

```
Use /legacy-SKILL-NAME.

[CANONICAL TEST PROMPT CONTENT HERE]

Return only:
- [Expected output fields from SKILL.md output contract]
```

**Evaluation checklist:** (same as Codex above)

**Outcome:** `passed`, `executed`, or `failed`.

Record response in scorecard.

#### Phase 3 - Adversarial (Claude Code, Optional)

```
Use /legacy-SKILL-NAME.

[NEGATIVE TEST PROMPT CONTENT HERE]

Return only:
- gate status
- reason
- next step
```

**Outcome:** `passed` or `skipped`.

Record in scorecard.

### Runtime 3: OpenCode

#### Setup

```bash
# Verify OpenCode is available
which opencode

# Ensure skill is synced
scripts/sync-skills.sh --skill legacy-SKILL-NAME --target opencode --check
```

#### Phase 1 - Discovery

```bash
# Check that the OpenCode adapter exists and exposes readable frontmatter
test -f .opencode/skills/legacy-SKILL-NAME/SKILL.md
sed -n '1,12p' .opencode/skills/legacy-SKILL-NAME/SKILL.md

# If the local OpenCode install exposes a skill list, capture it as additional
# evidence. The mandatory proof is adapter presence plus Phase 2 invocation.
```

**Outcome:** `loaded` or `failed`.

#### Phase 2 - Trigger (OpenCode)

```bash
# Run the canonical test prompt
opencode run -m opencode/minimax-m2.5-free "
Use /legacy-SKILL-NAME.

[CANONICAL TEST PROMPT HERE]

Return only:
- [Expected output from contract]
"
```

**Evaluation checklist:** (same as above)

**Outcome:** `passed`, `executed`, or `failed`.

Record response.

#### Phase 3 - Adversarial (OpenCode, Optional)

```bash
opencode run -m opencode/minimax-m2.5-free "
Use /legacy-SKILL-NAME.

[NEGATIVE TEST PROMPT HERE]

Return only:
- gate status
- reason
- next step
"
```

**Outcome:** `passed` or `skipped`.

## Post-Test Steps

### 1. Complete Scorecard

Fill in all per-runtime results with actual outcomes and notes. Calculate the
final decision:

- **field-pilot ready**: All three runtimes at `passed`
- **repo-ready**: All three runtimes at `loaded` or better, but not all at
  `passed`
- **blocked**: Any runtime at `failed`, or required negative case not run

### 2. Update Runtime Matrix

Edit `docs/runtime-matrix.md`:

1. Find or create the row for `legacy-SKILL-NAME`
2. Update the canonical version column to vX.Y.Z
3. Update the three runtime columns with the final status
4. Add a Notes cell with:
   - Runtimes and models used (e.g., "Codex (gpt-5.4-mini), Claude Code (haiku), OpenCode (minimax-m2.5-free)")
   - Test date (e.g., "2026-05-16")
   - One-line outcome (e.g., "All phases passed; skill ready for field pilot")
   - Link to scorecard (e.g., "See docs/reviews/legacy-SKILL-NAME-vX.Y.Z-scorecard.md")

### 3. Commit and Push

```bash
# Stage both files
git add docs/runtime-matrix.md docs/reviews/legacy-SKILL-NAME-vX.Y.Z-scorecard.md

# Commit with message linking the skill version
git commit -m "
test: runtime smoke tests for legacy-SKILL-NAME v0.1.0

All three runtimes (Codex, Claude Code, OpenCode) passed discovery and
trigger phases. Output follows declared contract. No side effects.

Lifted from 9.0 (portability not tested) to eligible for 9.5+.

See docs/runtime-matrix.md and docs/reviews/ for full results.
"

# Push (use -u if new branch)
git push
```

### 4. Close Out

If the skill is now at `passed` in all runtimes:
- It is eligible for field pilot
- Notify the skill author and project leads
- Link to the scorecard in any comms

If any runtime is below `passed`:
- Document the blocker in the scorecard
- Route back to the skill author with specific recommendations for fixes
- Re-test after remediation

## Troubleshooting

### Issue: Skill Does Not Appear in Runtime List

**Cause:** Sync failed or skill folder structure is invalid.

**Fix:**
1. Check that `skills/legacy-SKILL-NAME/SKILL.md` exists and has valid YAML
   frontmatter
2. Run `scripts/sync-skills.sh --skill legacy-SKILL-NAME --target codex` to
   refresh that adapter, then rerun the per-skill `--check`
3. If sync fails, fix the canonical source and retry

### Issue: Skill Invoked But Output Does Not Match Contract

**Cause:** Skill implementation or output contract mismatch.

**Fix:**
1. Compare the skill's declared output contract in `SKILL.md` with actual
   output
2. If the output looks reasonable but contract is unclear, route back to skill
   author to clarify the contract
3. Do not force-mark as `passed` if contract is unclear; mark as `executed`

### Issue: Negative Case Did Not Block

**Cause:** Skill routing logic may be incorrect.

**Fix:**
1. Check that the negative test prompt is actually triggering the blocking
   condition (e.g., missing required input, invalid evidence)
2. If the skill should have blocked but didn't, route back to skill author
3. Mark as `executed` (positive case only) if negative case is missing or
   needs work

### Issue: Timeout or Runtime Unavailable

**Cause:** Environment setup issue, credentials missing, or runtime not
installed.

**Fix:**
1. Check runtime installation and PATH: `which codex`, `which opencode`,
   `claude auth status`
2. If runtime is unavailable, leave it at `synced` with blocker notes in
   scorecard
3. Do not force-mark as `passed`; retry when environment is ready

## Reporting

After completing all runtimes, you have:

1. Updated `docs/runtime-matrix.md` with results
2. Created/updated `docs/reviews/legacy-SKILL-NAME-vX.Y.Z-scorecard.md`
3. Git commit ready to merge

Use these artifacts to report back to the project:

- **For automation/CI:** Parse `docs/runtime-matrix.md` to check status
- **For humans:** Link to the scorecard in PR/commit message
- **For skill author:** Point to specific failures and recommended fixes

## Sign-Off

This protocol is complete when:

- [ ] Pre-test checks pass
- [ ] All three runtimes complete phases 1 and 2
- [ ] Negative cases (if any) are tested
- [ ] Scorecard is complete and reviewed
- [ ] Runtime matrix is updated
- [ ] Changes are committed and documented

Example final commit message:

```
test: runtime smoke tests for legacy-ibmi-inventory v0.1.0

Tested against:
- Codex CLI (gpt-5.4-mini): passed
- Claude Code (haiku): passed
- OpenCode (minimax-m2.5-free): passed

All phases (discovery, trigger, adversarial) completed successfully.
Output follows declared contract. Ready for field pilot.

See docs/runtime-matrix.md and docs/reviews/legacy-ibmi-inventory-v0.1.0-scorecard.md
```
