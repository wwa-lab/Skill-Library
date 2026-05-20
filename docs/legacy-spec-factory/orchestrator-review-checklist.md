# Orchestrator Review Checklist

Use this checklist to evaluate whether
`legacy-modernization-orchestrator` is strong enough to act as the single
front door for Legacy Spec Factory.

This is an **OpenCode-first** review aid. The review can be reused for other
runtimes later, but the internal pilot should answer one practical question:

> Can users who only remember `legacy-modernization-orchestrator` still move
> safely through the reverse-modernization chain in OpenCode?

## Why This Matters

Legacy Spec Factory has many specialized skills. Real users should not need to
memorize that map. They should be able to start from one routing skill, describe
what they have, and receive the safest next step.

That means the orchestrator is not just another skill. It is the product
surface for the whole workflow.

## Review Outcomes

| Outcome | Meaning |
| --- | --- |
| `field-pilot ready` | OpenCode routes reliably across happy, blocked, batch, and screen scenarios |
| `repo-ready` | Structurally sound, but one or more route families need hardening |
| `revise` | Unsafe routing, weak gate discipline, or unclear next steps |
| `blocked` | Recommends unsafe advancement, invents missing state, or skips hard gates |

## Capability Rubric

Score each capability from 0 to 3.

| Score | Meaning |
| ---: | --- |
| 3 | Reliable in the tested OpenCode scenarios |
| 2 | Mostly correct, with minor gaps or wording issues |
| 1 | Partially works, but needs review before pilot use |
| 0 | Missing, unsafe, or misleading |

### 1. Stage Recognition

The orchestrator can identify where the user is in the chain.

Check that it recognizes:

- raw evidence only
- evidence intake ready
- inventory blocked
- inventory approved
- program analysis partial or complete
- flow-ready state
- module-ready state
- spec draft, review, or approved state

Evidence to inspect:

- whether it names the current stage clearly
- whether it avoids jumping straight to spec or handoff
- whether it uses artifact state when paths are provided

### 2. Gap Recognition

The orchestrator can identify what is missing before the next stage.

Check that it catches:

- missing source member
- missing DDS, LF, DSPF, or PRTF
- missing runtime evidence when runtime behavior is needed
- missing SME confirmation
- missing approval status
- incomplete program-analysis coverage before flow analysis

Evidence to inspect:

- whether gaps are concrete
- whether gaps are tied to the next required action
- whether it avoids vague "needs more context" answers when the missing item is
  visible

### 3. Gate Discipline

The orchestrator stops at hard gates.

Check that it blocks:

- unredacted or unapproved evidence
- inventory with blocking coverage gaps
- flow analysis when required program analyses are missing
- spec generation when flow/module evidence is incomplete
- handoff when `spec.yaml` is missing or not approved

Evidence to inspect:

- whether it says `stop` or equivalent when advancement is unsafe
- whether it names the blocking gate
- whether it refuses deadline-pressure bypasses unless an explicit waiver path
  exists in project rules

### 4. Next-Step Clarity

The orchestrator tells the user exactly what to do next.

Good output should include:

- current stage
- recommended next skill
- reason for the recommendation
- expected output artifact
- gate status
- SME action when needed

Evidence to inspect:

- whether a user could act on the answer without knowing the skill family
- whether output is compact enough to be useful in OpenCode
- whether it separates "run next" from "read for background"

### 5. Main-Path Priority

The orchestrator keeps users on the main reverse-modernization path before
introducing optional skills.

Main path:

- `legacy-ibmi-evidence-intake`
- `legacy-ibmi-inventory`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-flow-analyzer`
- `legacy-ibmi-module-analyzer`
- `legacy-spec-writer`

Evidence to inspect:

- whether it avoids routing to helper skills too early
- whether optional skills are presented as optional
- whether it does not replace downstream extraction skills with its own
  analysis

### 6. Recovery And Resume

The orchestrator helps users resume without re-explaining the whole project.

Check that it can use:

- `docs/<project>/workflow-state.yaml`
- named project path
- named capability or module
- existing artifact directories
- blocked findings or open gates

Evidence to inspect:

- whether it chooses the right project when one is named
- whether it asks when multiple projects match
- whether it corrects stale state from artifacts instead of trusting stale
  state blindly

### 7. OpenCode Fit

The orchestrator works naturally in the runtime the company actually uses.

Check that OpenCode responses:

- trigger the orchestrator when users ask "what next?"
- preserve no-write behavior when requested
- produce compact routing output
- do not depend on Codex-only or Claude-only affordances
- keep file paths portable and repository-relative where appropriate

Evidence to inspect:

- whether prompts from `docs/synthetic-corpus/pilot-prompts.md` trigger the
  expected skill
- whether output can be pasted into the pilot results template without cleanup

## Synthetic Pilot Scenarios

Use the synthetic corpus to review the orchestrator in OpenCode.

| Fixture | Expected Orchestrator Behavior |
| --- | --- |
| `sqlrpgle-credit-check-happy` | route to intake or inventory; do not jump to spec |
| `sqlrpgle-credit-check-blocked` | stop on missing `CREDITVW.LF` and unconfirmed `STATUS = 'H'` |
| `batch-ar-reconciliation` | recognize scheduler/batch path and runtime evidence value |
| `screen-subfile-inquiry` | recognize menu-driven inquiry and route toward screen/program/flow analysis |

References:

- [`docs/synthetic-corpus/pilot-prompts.md`](synthetic-corpus/pilot-prompts.md)
- [`docs/synthetic-corpus/pilot-execution-checklist.md`](synthetic-corpus/pilot-execution-checklist.md)
- [`docs/synthetic-corpus/pilot-results-template.md`](synthetic-corpus/pilot-results-template.md)

## Scoring Sheet

| Capability | Score 0-3 | Evidence / Notes |
| --- | ---: | --- |
| Stage recognition | | |
| Gap recognition | | |
| Gate discipline | | |
| Next-step clarity | | |
| Main-path priority | | |
| Recovery and resume | | |
| OpenCode fit | | |

Maximum score: 21.

## Decision Guide

| Total | Decision | Meaning |
| ---: | --- | --- |
| 19-21 | `field-pilot ready` | Safe enough for OpenCode internal pilot use |
| 16-18 | `repo-ready` | Good foundation, but harden weak scenarios first |
| 11-15 | `revise` | Routing quality is not yet reliable enough |
| 0-10 | `blocked` | Unsafe as a single front door |

Any critical gate failure caps the decision at `revise`, even if the numeric
score is high.

Any unsafe recommendation to proceed past missing source, missing SME approval,
or unapproved `spec.yaml` caps the decision at `blocked`.

## Review Record Template

```markdown
# Orchestrator Review Record

Date:
Reviewer:
Runtime: OpenCode
Model:
Repository commit:

## Scores

| Capability | Score | Evidence |
| --- | ---: | --- |
| Stage recognition | | |
| Gap recognition | | |
| Gate discipline | | |
| Next-step clarity | | |
| Main-path priority | | |
| Recovery and resume | | |
| OpenCode fit | | |

Total:
Decision:

## Critical Findings

-

## Required Fixes Before Next Pilot

1.
2.
3.
```
