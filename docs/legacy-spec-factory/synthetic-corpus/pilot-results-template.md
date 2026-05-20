# Synthetic Corpus Pilot Results Template

Use this template to record one internal pilot pass against the synthetic
fixtures.

Pair this with
[`pilot-execution-checklist.md`](pilot-execution-checklist.md).

---

## Pilot Metadata

| Field | Value |
| --- | --- |
| Pilot Name | |
| Date | |
| Reviewer | |
| Runtime | OpenCode |
| Model | |
| Repository Commit | |
| Scope | full pilot / partial rerun / targeted skill check |

## Overall Summary

| Fixture | Overall Judgment | Short Note |
| --- | --- | --- |
| `sqlrpgle-credit-check-happy` | pass / executed / blocked / failed | |
| `sqlrpgle-credit-check-blocked` | pass / executed / blocked / failed | |
| `batch-ar-reconciliation` | pass / executed / blocked / failed | |
| `screen-subfile-inquiry` | pass / executed / blocked / failed | |

## Findings Summary

### What Worked

- 

### What Failed

- 

### Hallucination Risks Observed

- 

### Gate / Blocking Mistakes Observed

- 

### Highest-Value Next Fixes

1. 
2. 
3. 

---

## Fixture Results

### 1. `sqlrpgle-credit-check-happy`

| Phase / Skill | Judgment | Notes |
| --- | --- | --- |
| Orchestrator | | |
| Evidence Intake | | |
| Inventory | | |
| Program Analyzer | | |
| Flow Analyzer | | |

**Expected References**

- `expected/inventory-assertions.md`
- `expected/program-analysis-assertions.md`
- `expected/flow-assertions.md`

**Prompts Used**

```text
<paste prompt(s) here>
```

**Observed Strengths**

- 

**Observed Gaps**

- 

**Action Items**

- 

### 2. `sqlrpgle-credit-check-blocked`

| Phase / Skill | Judgment | Notes |
| --- | --- | --- |
| Orchestrator | | |
| Evidence Intake | | |
| Inventory | | |
| Program Analyzer | | |
| Flow Gate Check | | |

**Expected References**

- `expected/expected-review-notes.md`
- `expected/inventory-assertions.md`
- `expected/program-analysis-assertions.md`

**Prompts Used**

```text
<paste prompt(s) here>
```

**Did The System Stop Correctly?**

- yes / no

**If No, What Did It Invent Or Skip?**

- 

**Action Items**

- 

### 3. `batch-ar-reconciliation`

| Phase / Skill | Judgment | Notes |
| --- | --- | --- |
| Orchestrator | | |
| Evidence Intake | | |
| Inventory | | |
| Program Analyzer | | |
| Runtime Evidence Miner | | |
| Flow Analyzer | | |

**Expected References**

- `expected/inventory-assertions.md`
- `expected/runtime-evidence-assertions.md`
- `expected/program-analysis-assertions.md`
- `expected/flow-assertions.md`

**Prompts Used**

```text
<paste prompt(s) here>
```

**Observed Strengths**

- 

**Observed Gaps**

- 

**Action Items**

- 

### 4. `screen-subfile-inquiry`

| Phase / Skill | Judgment | Notes |
| --- | --- | --- |
| Orchestrator | | |
| Evidence Intake | | |
| Inventory | | |
| Screen Analyzer | | |
| Program Analyzer | | |
| Flow Analyzer | | |

**Expected References**

- `expected/screen-analysis-assertions.md`
- `expected/flow-assertions.md`

**Prompts Used**

```text
<paste prompt(s) here>
```

**Observed Strengths**

- 

**Observed Gaps**

- 

**Action Items**

- 

---

## Cross-Fixture Patterns

### Skills That Performed Reliably

- 

### Skills That Need Hardening

- 

### Common False Positives / Hallucinations

- 

### Common Missed Signals

- 

---

## Decision

### Pilot Outcome

- proceed
- proceed with caveats
- rerun after fixes
- blocked until critical issues fixed

### Reason

- 

### Follow-Up Owner

- 

## OpenCode-Specific Notes

- Did the correct skill trigger in OpenCode?
- Did OpenCode keep blocked cases blocked?
- Did OpenCode invent business meaning or missing source details?
- Did OpenCode preserve the expected no-write behavior?
