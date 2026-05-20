# Expected Review Outcome: Incomplete Evidence Negative Case

## Scenario

**Input:** Incomplete DSPF source fragment for ORDER-LINES-SCR
- DDS member was truncated during extraction
- Partial fields visible (LINENO, ITEMNO, QTY, PRICE)
- Missing: subfile definition, function keys, error handling, complete record format
- Missing: runtime evidence (no spool sample, no screenshot)

**Expected Skill Behavior:** STOP and escalate to inventory/evidence gate

## Proper Handling (What the Skill Should Do)

### Step 1: Detect Incompleteness

When extracting fields and indicators from the DDS fragment:
- Observe that some fields have indicator associations (#01, #02) but no DDS keyword explaining them
- Observe that the DDS file ends abruptly with "... rest of DDS cut off ..."
- Detect missing common elements (function key definitions, error message setup)

### Step 2: Document What Is Present and What Is Missing

**Fields extracted (visible):**
- LINENO (3S 0 input)
- ITEMNO (5A mandatory input)
- QTY (5S 0 input, protected by indicator #01)
- PRICE (8S 2 output, edit code A)

**Fields/structures NOT found:**
- No subfile definition (SFL, SFLPAG, SFLSIZ keywords)
- No function key definitions (CA/CF keywords)
- No error message setup (ERRMSG, ERRSFL keywords)
- No complete record-format / field-role context (input, output, both, hidden)

**Coverage gaps:**
- Uncertain if this is a complete screen or part of a subfile
- Indicator #01, #02 purpose unknown (PROTECT keyword visible, but no explanation)
- No evidence of what this screen is used for

### Step 3: Create TBDs for Missing Evidence

```yaml
TBD-ORDER-LINES-001:
  Issue: DDS source truncated; subfile definition not available
  Category: pending_source
  Blocking: YES (cannot analyze subfile behavior without SFLPAG, SFLSIZ, SFLDROP keywords)
  Resolution: Obtain complete DDS member from source library or file recovery
  Owner: Inventory/evidence intake

TBD-ORDER-LINES-002:
  Issue: Function key definitions missing from DDS fragment
  Category: pending_source
  Blocking: YES (cannot map F-key behavior without CA/CF keyword definitions)
  Resolution: Locate complete SKILL.md member including function key section
  Owner: Inventory/evidence intake

TBD-ORDER-LINES-003:
  Issue: Indicator #01, #02 purpose: only PROTECT keyword visible; no keyword explaining set/clear logic
  Category: pending_program_context
  Blocking: YES (cannot understand when protection is applied without program analysis)
  Resolution: Obtain program analysis that references this DSPF to understand indicator flow
  Owner: Program analyzer

TBD-ORDER-LINES-004:
  Issue: No runtime evidence available (no spool sample, no screenshot, no job log)
  Category: pending_source
  Blocking: YES (cannot confirm DDS matches runtime behavior without evidence)
  Resolution: Obtain screenshot of this screen during normal operation and/or job log showing EXFMT sequence
  Owner: Evidence intake
```

### Step 4: Check Against Inventory

If the object is in the inventory:
- Confirm OBJ-* ID
- Check if inventory marks object as "blocked" due to missing evidence
- Do not edit inventory from this skill. Emit a blocking finding or TBD routing
  the object back to `legacy-ibmi-evidence-intake` / `legacy-ibmi-inventory`.

If the object is NOT in the inventory:
- This is a more serious issue: the object should have been inventoried before analysis
- Return to inventory step; flag for complete evidence collection

### Step 5: Emit Analysis Result

**Status:** `blocked`

**Analysis Recommendation:**
```
Analysis of ORDER-LINES-SCR cannot proceed.

Evidence gaps prevent complete analysis:
1. DDS source is truncated (subfile definition missing)
2. Function key definitions missing
3. No runtime evidence available (screenshot, spool, job log)
4. Indicator usage unclear (only PROTECT keyword visible; set/clear logic unknown)

Blocking TBDs:
- TBD-ORDER-LINES-001 (missing DDS subfile section)
- TBD-ORDER-LINES-002 (missing DDS function key section)
- TBD-ORDER-LINES-003 (indicator logic unclear without program analysis)
- TBD-ORDER-LINES-004 (no runtime evidence)

REQUIRED ACTION:
1. Obtain complete DDS source for ORDERLINES DSPF
2. Obtain runtime evidence: screenshot of screen, job log showing EXFMT, or spool output
3. Once evidence is complete, analysis can proceed

DO NOT proceed to downstream skills (program analyzer, flow analyzer) until:
- Complete DDS source is obtained
- Blocking TBDs are resolved
- Inventory marks this object as "approved" or "approved_with_non_blocking_tbd"
```

## Why This Is a Negative Case

### ❌ What NOT to Do

**WRONG: Proceeding with incomplete analysis**
- Inventing missing subfile behavior
- Guessing at function key meanings
- Inferring indicator purposes from field names alone
- Creating analysis that downstream skills cannot use

**WRONG: Marking analysis as "approved"**
- Incomplete evidence cannot support approval
- Downstream program analyzer would waste effort trying to cross-reference
- Flow analyzer would build models on uncertain foundation

**WRONG: Creating analysis artifacts without blocking status**
- Analysis with blocking TBDs should not be used
- Blocking TBDs should be explicitly listed in output
- Handoff status should be "blocked" not "approved_with_non_blocking_tbd"

### ✅ What This Example Should Teach

**Correct approach:**
1. **Detect incomplete evidence** early (missing DDS sections, no runtime samples)
2. **Document what is missing** specifically (subfile definition, function keys, etc.)
3. **Mark as blocking** if gaps prevent analysis of key features
4. **Stop and escalate** to evidence intake, not proceed with guesses
5. **Create clear TBDs** with resolution paths so work can resume when evidence arrives

## Key Lessons

### Lesson 1: Evidence-First Analysis

**Principle:** Do not infer details that are not present in evidence.

**Example:**
- DDS fragment shows fields but no function key definitions
- ❌ WRONG: "Assume F1 = ACCEPT, F2 = CANCEL based on convention"
- ✅ RIGHT: "Function keys undefined; TBD-* pending complete DDS or job log"

### Lesson 2: Blocking vs. Non-Blocking TBDs

**Blocking TBDs** prevent handoff:
- Missing DDS section that describes core feature (subfile, function keys)
- Missing runtime evidence that would validate assumptions
- Indicator logic unclear and affects downstream analysis

**Non-Blocking TBDs** allow handoff with notes:
- Question about business meaning (resolved later with SME review)
- Detail about calculation logic (resolved during program analysis)
- Multi-page behavior (doesn't affect single-screen analysis)

### Lesson 3: Stop vs. Proceed Decision

**STOP (escalate to evidence intake):**
- Core DDS sections missing (subfile, function key, record format)
- No runtime evidence to cross-check static DDS
- Indicator logic cannot be understood from available evidence
- Object marked "blocked" in inventory

**PROCEED (with non-blocking TBDs):**
- DDS is complete but some program logic is unclear
- Runtime evidence partially available (screenshot but no spool)
- Indicator purposes mostly clear, but edge cases need SME review
- Object is marked "approved_with_non_blocking_tbd" in inventory

## How to Avoid This Case

**Evidence Intake Checklist (Before analysis):**
- [ ] Complete DDS source obtained (not truncated, all sections present)
- [ ] Runtime evidence available (screenshot or spool sample)
- [ ] Object is in approved inventory with `decision: approved` or `decision: approved_with_non_blocking_tbd`
- [ ] Evidence is redacted and safety-assessed
- [ ] No TBDs are marked "blocking" in inventory

**Quality Gate:**
- Analysis artifact with blocking TBDs cannot be merged to main branch
- Blocking TBDs must be resolved or escalated before handoff
- Do not allow downstream skills to depend on incomplete analysis

## Skill Behavior on Negative Case

When the skill encounters this scenario, the proper output is:

1. **Reject the analysis request** (or start analysis but immediately flag as blocked)
2. **List specific evidence gaps** (not vague "something missing")
3. **Create blocking TBDs** with clear resolution path
4. **Recommend escalation** to evidence intake, inventory, or program analyzer
5. **Mark handoff status** as `blocked` with reason

**Example output snippet:**

```markdown
# Screen Analysis: OBJ-ORDER-LINES-SCR [BLOCKED]

## Status: ANALYSIS BLOCKED

Evidence is insufficient to complete analysis. Complete DDS source is required.

### Blocking Issues

- DDS source is truncated (comments indicate subfile definition is missing)
- Function key definitions not found in provided fragment
- No runtime evidence available (no screenshot, spool, or job log)

### Action Required

**Do not use this partial analysis for downstream work.** Evidence must be complete before analysis can proceed.

1. Inventory: Mark OBJ-ORDER-LINES-SCR as "blocked" due to incomplete source
2. Evidence Intake: Request complete DDS member from source library
3. Evidence Intake: Request runtime evidence (screenshot during user interaction)
4. After evidence arrival: Re-run analysis
```

---

## Summary

This negative example demonstrates what happens when the skill encounters incomplete evidence. The correct behavior is to:
- **Detect the gap** (truncated DDS, missing sections)
- **Create blocking TBDs** (specific, not vague)
- **Escalate** (do not proceed with guesses)
- **Provide clear next steps** (how to obtain missing evidence)

This protects downstream skills from building analysis on uncertain foundations and ensures that evidence completeness is enforced before any artifact is marked ready for handoff.
