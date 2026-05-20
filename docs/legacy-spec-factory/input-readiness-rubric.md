# Input Readiness Rubric

Use this rubric in every Legacy Spec Factory skill before producing the main
artifact. The goal is to tell the user the smallest usable input set, what
blocks execution, what can be safely missing, and which extra inputs improve
the output.

## Required Output

Every skill response should include an `input_readiness` summary before the
main artifact or validation result:

```yaml
input_readiness:
  score: 0-10
  status: blocked | minimum_pass | usable | strong
  minimum_pass_met: true | false
  hard_blockers:
    - ...
  optional_missing:
    - ...
  quality_boosters_available:
    - ...
  quality_ceiling_reason: ...
```

If the user only asks whether the input is enough, return this summary and
do not produce the downstream artifact.

## Score Bands

| Score | Status | Meaning | Action |
| --- | --- | --- | --- |
| 0-5 | `blocked` | A required source, prerequisite gate, authorization, or ID link is missing. | Stop. Explain exactly what is missing and route to the right prior skill. |
| 6 | `minimum_pass` | The smallest safe input set is present. Output may be draft-like and carry TBDs. | Proceed, but state likely blind spots. |
| 7-8 | `usable` | Required inputs plus useful context are present. Most relationships can be traced. | Proceed with normal confidence and record remaining optional gaps. |
| 9-10 | `strong` | Required inputs plus runtime samples, SME notes, edge cases, or downstream review context are present. | Proceed with high confidence and produce richer outputs. |

## Input Categories

### Hard Blockers

Hard blockers must prevent the skill from producing its main artifact:

- Required upstream artifact is missing, below required status, or cannot be
  located.
- Required stable IDs cannot be resolved (`EV-*`, `OBJ-*`, `BEH-*`, `BR-*`,
  `AC-*`, etc. depending on the step).
- Evidence authorization is unresolved: `sensitivity: unknown`, missing
  `source_path_verified`, or `redaction_required: true` without approved
  redaction.
- The requested scope is too broad to review as one slice.
- The user asks the skill to infer facts that only source evidence, runtime
  evidence, or SME approval can establish.

### Minimum Pass

Minimum pass means the skill may run, but should warn that output quality is
limited:

- The canonical required inputs in the skill's `## Inputs` section are present.
- Evidence is authorized for the current environment.
- The scope and slug are stable.
- Missing but expected details are represented as `TBD-*` instead of being
  silently filled in.

### Optional Missing

These inputs do not block execution and should not lower the status below
`minimum_pass` when the required inputs exist:

- Historical notes, spreadsheets, wikis, or vendor documents that are not the
  source of truth.
- SME notes for early developer-led analysis steps where SME judgment is not
  needed to start.
- Runtime samples for static inventory or code-structure extraction.
- Downstream packaging context when the current step only produces an upstream
  analysis artifact.

List these as `optional_missing` so users know they are not being blocked.

### Quality Boosters

These inputs should be actively encouraged because they improve precision,
reduce TBDs, or raise confidence:

- Runtime logs, spool/report samples, screen recordings, or sample
  transactions that show observed behavior.
- SME notes for entry points, hidden dependencies, edge cases, exception paths,
  manual workarounds, and business meaning.
- DDS/copybook definitions, DB metadata, scheduler notes, and job logs linked
  to the analyzed program or flow.
- Negative examples, boundary cases, month-end/period-end cases, and known
  incident examples.
- Prior modernization decisions, downstream constraints, or target SDLC
  expectations when generating specs, BRDs, handoff packages, or traceability
  packs.

Missing quality boosters must not block the step. Instead, report how they
would improve the output and whether their absence caps confidence or leaves
specific TBDs.

## User-Facing Guidance

When inputs are thin but passable, say so directly:

- "Minimum pass is met; I can proceed with a 6/10 input readiness score."
- "Missing runtime samples do not block this step, but they would improve
  exception-path confidence."
- "This must not proceed because source authorization is unresolved."

Prefer actionable guidance over generic requests for "more information".
