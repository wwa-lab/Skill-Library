# Program Criticality Classifier

A heuristic for tagging every program object in `inventory.yaml` with one
of `critical | standard | low_risk` so downstream skills can route SME
review effort proportionally to risk.

**Why this matters.** A 200-program module produces 200
`program-analysis.md` files. Asking the SME to deep-review all 200 is
unrealistic — most are CRUD, display, or queries. The criticality field
lets the SME spend bandwidth where it matters (money / inventory /
compliance / customer-status / posting paths) and batch-approve the rest.

## The three buckets

| Bucket | Review intensity | Rough % of typical module |
| --- | --- | --- |
| `critical` | Deep, per-program SME review | 15–25% |
| `standard` | Spot-check (review N out of all) | 30–50% |
| `low_risk` | Batch confirm (one signoff for the group) | 30–50% |

The percentages are typical only — your specific module will vary. Tag
honestly; do NOT inflate counts to reach these ratios.

## Heuristics for auto-classification

Inventory skill applies these rules in order. The first matching rule
wins; otherwise default to `standard`.

### Promote to `critical` when ANY of:

| Signal | Source |
| --- | --- |
| Writes (`OUTPUT`, `WRITE`, `UPDATE`, `DELETE`) to a file whose name contains `ARMAST`, `APMAST`, `GLMAST`, `POSTHIST`, `LEDGER`, `JOURNAL`, `CRDLINE`, `INVMAST`, `STKQTY`, `ONHAND`, `ALLOC` | program-analysis File I/O table |
| Modifies customer status fields (`CUSTAT`, `STATCODE`, `HOLD`, `SUSPEND`, `BLOCKED`) | program-analysis Control Flow + File I/O |
| Validates credit limits, compliance flags, KYC, AML, sanctioned-party lists | program-analysis Control Flow (uses such fields in conditions) |
| Calls programs whose own criticality is `critical` (transitive) | inventory call graph |
| SME explicitly flagged as critical during evidence walkthrough | `EV-SME-*` notes |

### Promote to `low_risk` when ALL of:

| Signal | Source |
| --- | --- |
| File I/O contains only `CHAIN` / `READ` / `READE` / `READP` (no write operations) | program-analysis File I/O table |
| No external `CALL` to a critical program | inventory call graph |
| Program purpose (from name + source-comment header) is one of: display, query, report, lookup, browse, list | program member + DDS analysis |
| No conditions involve money fields (`AMT*`, `PRICE*`, `BAL*`, `TOT*`) or status changes | program-analysis Control Flow |

### Otherwise

Default to `standard`. These are programs with business logic that
doesn't directly touch money / inventory / compliance but still warrant
spot-check review.

## SME confirmation

**The SME confirms the classification ONCE for the whole inventory**, not
per program. The inventory skill emits a single confirmation prompt:

```
Found 47 programs total:
  critical:  12 programs  (need deep SME review)
  standard:  21 programs  (spot-check)
  low_risk:  14 programs  (batch confirm)

Do these counts match your understanding of the module? Please flag any
program where the bucket looks wrong before we proceed to analysis.
```

SME's response:

- **Confirm** all → proceed
- **Reclassify N programs** → SME names which programs move buckets and why; updates `inventory.yaml.objects[].criticality` + `criticality_reason: "SME reclassified — <why>"`
- **Cannot confirm without more info** → log as a blocking gap

Record the SME's confirmation in `inventory.yaml.sme_review.criticality_confirmed_at`.

## How downstream skills consume `criticality`

| Skill | Behavior by criticality |
| --- | --- |
| `legacy-ibmi-program-analyzer` | Same depth for all; LLM does the work uniformly |
| `legacy-ibmi-flow-analyzer` | Flows that touch ≥1 critical program inherit critical priority |
| `legacy-ibmi-module-analyzer` | View 1 BR seeds tagged `critical` if rooted in critical programs |
| `legacy-sme-review-facilitator` | Routes review batches by bucket — critical: per-program; standard: 30% sample; low_risk: batch digest |
| `legacy-spec-writer` | Acceptance criteria depth scales with criticality (critical: explicit per-case; low_risk: shape-only) |
| `legacy-golden-master-test-planner` | Test coverage thresholds scale with criticality |

## Anti-patterns (do NOT do these)

- **Don't auto-classify `critical` and then skip SME confirmation.** The
  whole point is that SME confirms the partitioning once. Skipping that
  step trades 200 reviews for 0 reviews and hopes the AI got it right.
- **Don't lower a `critical` to `standard` without SME approval.** SME
  may upgrade or downgrade; AI may only propose initial classification.
- **Don't use criticality to skip program analysis** for `low_risk`
  programs. Run the analysis at full depth — only the SME review effort
  is dialed down, not the artifact production.
- **Don't conflate criticality with confidence.** A `low_risk` program
  whose analysis the AI is uncertain about still needs flagging via
  `TBD-*` or `confidence: low` on the analysis row.
