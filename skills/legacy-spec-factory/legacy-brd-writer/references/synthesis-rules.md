# BRD Synthesis Rules

How to extract observed behaviors, aggregate inferred rules, and surface open
questions when synthesizing a Business Requirements Document from approved
module analysis.

---

## 0. Business-First Translation Gate

Before drafting the BRD body, convert technical evidence into business-process
language. The BRD may be evidence-backed by program / flow analysis, but it
must be reviewable by people who do not know IBM i program names.

### Required Translation

For each capability, identify:

- **Function purpose:** why this business function exists
- **Business scenario / use case:** which real-world case the function supports
- **Business trigger:** what event starts the work
- **Business object:** what customer, account, order, claim, payment, card,
  case, or record is affected
- **Channels:** which entry points, channels, or consumers participate
- **User touchpoints:** screens, notifications, reports, messages, queues, or
  manual review surfaces visible to business users
- **System interfaces:** upstream and downstream systems, APIs, file handoffs,
  external processors, or reporting consumers
- **Business state change:** what becomes pending, approved, rejected,
  fulfilled, reconciled, reported, or exceptioned
- **Business participants:** customer, operations user, partner, processor,
  downstream consumer, or control function
- **Business outcome:** what success / failure means outside the code
- **Control point:** approval, validation, reconciliation, audit, reporting, or
  exception handling point
- **Dependencies:** data, policy, system, operational, or reporting
  dependencies that materially affect the function

When the upstream `module-overview.md` includes a BRD Functional Analysis Input
Crosswalk, use it as the first source map for the SME-required BRD sections.
Do not ignore crosswalk gaps: a required area marked `partial` or `missing`
must become a visible `TBD-*` or a BRD review question.

### Program Chain Anti-Pattern

Do not use the direct runtime chain as the as-is summary.

**Wrong:**

1. `@PGMA` selects records from `FILEA` and calls `@PGMB`.
2. `@PGMB` updates `FILEB`.
3. `@PGMC` copies `FILEC` to an interface library.

**Right:**

1. The capability identifies pending customer requests that are eligible for
   processing.
2. Eligible requests are applied to the customer/account record and staged for
   external validation.
3. External responses are received, normalized, reconciled, and routed into
   normal or exception reporting.

Program names may remain in evidence notes, traceability, or a short appendix
when necessary for auditability. They should not carry the main BRD narrative.

### Problem Statement Anti-Pattern

Do not create a standalone `Problem Statement` section that turns analysis
friction into the business problem. Source-document fragmentation, technical
coupling, unclear program chains, or downstream rework risk are evidence and
delivery concerns, not the capability's business problem.

**Wrong:**

- "Current Card Replacement rules are scattered across functional
  specifications, flow diagrams, and technical design documents."
- "If scope, actors, triggers, and rule boundaries are not clarified first,
  downstream inventory and synthesis work will be prone to repeated rework."

**Right:**

- Put business scope ambiguity in `Scope Clarification Need`, phrased as a
  decision the SME can answer.
- Put unresolved boundary questions in `TBD-*` items with `category:
  sme_questions`.
- Keep evidence-source fragmentation in the evidence index, traceability notes,
  or review-session notes instead of the BRD's business narrative.

### Document Success Criteria Anti-Pattern

Do not add generic `Success Criteria`, `Success Criiteria`, `Document Success
Criteria`, or similar sections to `brd.md`. Statements such as "the BRD clearly
explains the first-phase boundary" or "SMEs can use this BRD to confirm scope"
evaluate the document, not the business capability.

**Wrong:**

- "The BRD clearly explains the business boundary, actors, triggers, key
  states, and major exceptions."
- "Business owners and SMEs can use this BRD to confirm scope and rule
  direction."

**Right:**

- Put artifact-readiness checks in `brd-review.md` under the
  author/synthesizer preflight or handoff readiness sections.
- Put input-package mapping checks in `traceability.md`.
- If the statement is actually a business acceptance criterion, defer it to
  `legacy-spec-writer` as `AC-*`; do not mint it in the BRD.

### Optional Section Invention Anti-Pattern

SME-requested sections 10-12 are useful only when grounded in available
evidence. Do not invent security/authentication rules, sequence diagrams,
workflow descriptions, system design notes, or source document names to make
the BRD look complete.

**Wrong:**

- "Mobile users must use MFA" when no channel/auth evidence says so.
- "Sequence diagram: customer -> API -> core system -> notification service"
  when the source package does not contain that sequence.
- "Source document: legacy-auth-design.docx" when the document was not in the
  input package.

**Right:**

- Include section 10 only when security, authentication, authorization, role,
  audit, or access-control evidence exists.
- Include section 11 only when actual workflow diagrams, sequence diagrams, or
  design notes exist and help explain business behavior.
- Include section 12 only for real source document names, sections, pages, or
  paths in the evidence bundle.
- If optional information is expected but missing, create a `TBD-*` with the
  right resolver instead of filling the gap with plausible text.

### If Business Meaning Is Unknown

If evidence only shows that one program calls another, but does not reveal why
the business cares, create a `TBD-*` instead of padding the BRD with technical
detail:

```yaml
id: TBD-<CAPABILITY-SLUG>-001
category: sme_questions
statement: "What business decision or control is represented by this handoff?"
evidence: "Flow analysis shows the handoff; business purpose is not confirmed."
resolver: SME
blocking: yes
```

---

## 1. Extracting Observed Behaviors (BEH-*)

An **observed behavior** is a factual statement about what the legacy system
demonstrably does. It is derived from approved upstream program / flow
analyses, data-flow evidence, or runtime evidence. BRD writing does not inspect
raw IBM i source directly.

### Sources

**Tier 1 (Strong):**
- Flow analysis **control flow** section (branches, loops, conditions)
- Flow analysis **error handling** section (explicit error paths)
- Program analysis **logic flow** (branch statements, decision logic)
- Runtime evidence (spool output, job logs, transaction samples)

**Tier 2 (Contextual):**
- SME observation of manual procedures (BAU)
- Repeated program usage patterns across the module
- Data model structure and field cardinality

**Tier 3 (Weak):**
- Code comments (unreliable; may be outdated)
- Field names (too speculative without other evidence)

### Extraction Steps

1. **Review the module analysis's business / operation view first** — identify
   the business trigger, parties, state changes, outcomes, and controls
2. **Review the module analysis's View 3 (Program Flow)** only as supporting
   evidence for what the system does
3. **For each major branch or decision point**, ask: "What business-visible
   effect does the system create here?"
4. **Extract as a declarative statement** without interpretation:
   - WRONG: "The system intelligently handles credit limits" (interpretation)
   - RIGHT: "If credit amount exceeds limit, the system rejects the transaction
     and writes error code 42 to the response"
5. **Link to upstream evidence**:
   - If from program analysis: cite line number in `program-analysis-<OBJ-ID>.md`
   - If from flow: cite section in `flow-<FLOW-SLUG>.md`
   - If from runtime: cite evidence ID `EV-...-N`

### Do NOT claim behaviors without evidence

- "The system processes orders sequentially" ← unless you see this in control flow
- "The system validates all inputs" ← unless you see explicit validation code
- "Nightly batch jobs clean up old records" ← unless you see the job definition
  or BAU notes

### Confidence Assessment

- `high`: Directly visible in source code + confirmed by runtime evidence
- `medium`: Visible in source code; no runtime contradictions observed
- `low`: Inferred from naming or structure; no direct code evidence

---

## 2. Aggregating Inferred Rules (BR-*)

An **inferred business rule** is a claim about *why* the system behaves a
certain way or what business policy governs behavior.

### Rules vs. Behaviors

| Type | Example | Can Claim Without Evidence? |
| --- | --- | --- |
| Behavior (BEH) | "If credit amount > limit, reject" | Only if code shows it |
| Rule (BR) | "Company policy requires all credits over $10k to be reviewed" | Only if SME confirms |

The system *might* enforce this policy, but the code alone doesn't tell you the
business *intent*.

### Candidate Rule Handling

1. **Module analysis includes a BR-* seed** → aggregate it with supporting BEH-*
   and EV-*
2. **Multiple behaviors point to the same business logic** → consider whether
   they form a coherent rule, but do not mint a new `BR-*` in the BRD
3. **SME mentions a business constraint** → record it as a `TBD-*` requiring
   module/spec review unless an upstream `BR-*` seed already exists

The BRD writer reuses upstream `BR-*` seeds. New rule IDs are finalized by the
upstream module analysis or downstream spec-writing step, not silently minted
inside the BRD.

### Aggregation Steps

1. **Start with module analysis's BR-* seeds** (`04_modules/<MODULE-SLUG>/module-overview.md`)
2. **Cross-check each seed against flow/program analyses**:
   - Does the control flow show behavior consistent with the rule?
   - Are there counterexamples (flows that violate the rule)?
3. **Gather supporting BEH-* and EV-***:
   - One BR-* typically abstracts 2-4 BEH-*
   - Each BR-* must reference ≥1 EV-*
4. **Assign confidence level**:
   - `high`: 3+ independent behaviors all support the rule
   - `medium` (strongly_inferred): 1-2 behaviors support it; no contradictions
   - `low` (weakly_inferred): only naming / comments suggest it; no direct code
     evidence

### Example: Aggregating a Rule

**BR-CREDIT-CHECK-001: "Credit limit enforcement"**

**Supporting behaviors:**
- BEH-001: "If CRDAMT > CRDLIM, set RTNCODE=42"
- BEH-002: "On RTNCODE=42, write error message to ERRMSG"
- BEH-003: "CRDLIM is read from customer file CUSTPF at transaction start"

**Supporting evidence:**
- EV-001: Program source, line 150-160 (IF statement checking CRDAMT > CRDLIM)
- EV-002: Flow analysis section 3.2 (error propagation)
- EV-003: Sample transaction (rejection message shown in spool)

**Confidence:** `high` (multiple behaviors, runtime evidence, consistent logic)

---

## 3. Surfacing Open Questions (TBD-*)

An **open question** is something we cannot confirm from evidence or upstream
artifacts. It must be resolved before the BRD can be approved and handed to
spec-writer.

### Categories

| Category | Meaning | Resolver | Example |
| --- | --- | --- | --- |
| `missing_inputs` | Upstream artifact missing or below required status | Source owner, Upstream skill | Flow analysis for Program X not completed |
| `evidence_gaps` | Evidence exists but is missing, unreadable, redacted | Source owner, Redaction team | Spool sample for scenario Y not available |
| `contradictory_evidence` | Two evidence items disagree | SME | Program A allows $0 credit; Program B rejects $0 credit |
| `sme_questions` | Only domain expert can answer | SME | Is credit limit enforced for all customer types? |
| `downstream_handoff_blockers` | Non-blocking for BRD, but spec-writer needs it | Architecture, next step | Is modernization target a microservice or monolith? |

### Surfacing Steps

1. **During extraction, flag any**:
   - Evidence that contradicts other evidence
   - Claims where module analysis says "unclear" or "TBD"
   - Inferred rules with only weak evidence
   - Gaps in flow/program coverage

2. **Create a TBD-* for each item**:
   ```yaml
   id: TBD-<CAPABILITY-SLUG>-001
   category: sme_questions
   statement: "Is rule BR-001 enforced for all customer types?"
   evidence_gap: "Module analysis notes this is unclear for new customers"
   resolver: SME
   blocking: yes (this step)
   ```

3. **Mark blocking vs. non-blocking**:
   - **Blocking for this step**: SME must resolve before BRD can be approved
   - **Non-blocking for this step, blocking for spec-writer**: Spec-writer can
     note it as a TBD in the spec and proceed
   - **Non-blocking for both**: Can be deferred or noted as future work

### Do NOT Hide TBDs in Prose

- WRONG: "The system probably validates credit limits in most cases"
- RIGHT: "The system validates credit limits (BEH-001). TBD-001: Does this apply
  to all customer types?"

---

## 4. Evidence Support Assessment

For each BEH and BR, link to evidence records. Do **not** duplicate
`evidence_strength` on the claim itself; derive support from the linked evidence
records per `docs/evidence-and-knowledge-taxonomy.md`.

| Strength | Meaning | Example |
| --- | --- | --- |
| `confirmed_from_code` | Behavior is directly visible in source code logic | RPGLE IF statement, CLLE command |
| `observed_in_runtime` | Behavior is seen in spool, job log, or sample data | Spool output shows "ACCEPTED" or "REJECTED" |
| `confirmed_by_sme` | SME explicitly states the behavior or rule | "Yes, we do enforce this policy" |
| `strongly_inferred` | Multiple independent evidence points support claim | 3+ programs implement same logic; spool shows it; SME nods |
| `weakly_inferred` | Plausible but under-supported inference | Only one program shows it; naming suggests it; comment hints at it |
| `needs_sme_review` | Cannot determine; requires judgment | Ambiguous code; contradictory evidence |
| `contradictory` | Two evidence items disagree | Program A checks CRDLIM; Program B skips check |
| `missing` | Required evidence has not been collected | Referenced file not extracted |

### Assigning Strength

1. **Start with the strongest evidence source** (e.g., source code > comments)
2. **Stack evidence**:
   - 1 tier-1 evidence → `confirmed_from_code`
   - 1 tier-1 + 1 runtime → `confirmed_from_code` (code + runtime agree)
   - 2+ tier-1 sources → `confirmed_from_code` (multiple code paths)
   - 1 tier-1 + SME confirmation → `confirmed_by_sme`
   - 2+ tier-1 → `strongly_inferred` (code clearly implies a rule)
   - 1 tier-1 + weak tier-2 → `weakly_inferred`
3. **If contradictory evidence exists**, mark `contradictory` and create a TBD

---

## 5. Avoiding Over-Inference

### Red Flags

These situations call for TBDs instead of confident claims:

1. **Only one code path shows a behavior**
   - Claim: "The system validates email format"
   - Reality: One program has email validation; others don't
   - Action: Create TBD-* to ask SME if this is a company-wide rule or program-specific

2. **Code and BAU notes disagree**
   - Claim: Code shows automatic processing, but SME says it's manual
   - Action: Create TBD-* to reconcile (maybe code was bypassed, or SME description
     is outdated)

3. **Naming suggests a rule, but behavior doesn't confirm it**
   - Claim: Variable called `IS_APPROVED` must mean the system tracks approval
   - Reality: Field is always 'Y'; no logic reads it
   - Action: Do NOT claim a rule; create TBD-*

4. **Module analysis has marked something as SEED-* (candidate)**
   - These are explicitly unconfirmed
   - Include them as BR-* `needs_sme_review`, not as confident rules

---

## 6. Template Usage

See `templates/brd.md` for the structure. Fill in:

1. **Function Purpose** (including business value and scope boundary)
2. **Business Scenarios / Use Cases**
3. **Channels**
4. **User Interface / User Touchpoints**
5. **System Interfaces**
6. **Process Flow** (business trigger, phases, states, outcomes, controls)
7. **Validation Rules** (observed `BEH-*` plus inferred `BR-*`, all
   evidence-backed)
8. **Error Handling**
9. **Dependencies**
10. **Security / Authentication Requirements** (optional; evidence-backed only)
11. **Supporting Workflow or Design Notes** (optional; evidence-backed only)
12. **Source Document Mapping** (optional; evidence-backed only)
13. **Open Questions & Gaps** (TBD-* with categories and resolvers)
14. **Validation Scenario Summary**
15. **Traceability Summary**

Do not add a `Success Criteria` section to `brd.md`; keep document-readiness
criteria in `brd-review.md`.

All cross-references must resolve to valid IDs in `docs/id-conventions.md`.

---

## 7. Checklist Before SME Review

- [ ] Every BEH-* statement is factual (no interpretation)
- [ ] Section 6 Process Flow is business-first and not a direct program call chain
- [ ] No standalone `Problem Statement` mixes business scope, evidence gaps,
      and delivery/rework risk
- [ ] No generic `Success Criteria` or document-quality/readiness section
      appears in `brd.md`
- [ ] Required SME sections 1-9 are present and evidence-backed or explicitly
      marked with `TBD-*` where evidence/SME confirmation is missing
- [ ] Optional sections 10-12 are omitted unless evidence-backed or explicitly
      SME-confirmed
- [ ] Every BEH-* links to ≥1 EV-*
- [ ] Every BR-* abstracts ≥1 BEH-* (not invented)
- [ ] Every BR-* links to ≥1 EV-*
- [ ] Every BR-* is marked `needs_sme_review` (never `approved` in BRD)
- [ ] Every TBD-* has a category (not just "unclear")
- [ ] Every TBD-* has an assigned resolver
- [ ] Every TBD-* is marked blocking or non-blocking
- [ ] No invented IBM i facts (object names, fields, programs)
- [ ] Traceability table is complete and consistent
- [ ] All IDs resolve to upstream artifacts

---

## 8. Examples

### Good BRD Synthesis

**Input:**
- Module analysis with BR-* seeds for "Order Amount Validation" and "Customer
  Credit Check"
- Flow analysis showing two programs: ORDER-ENTRY (validates amount) and
  CREDIT-CHECK (checks limit)

**Output BRD:**
- BEH-001: "ORDER-ENTRY validates order amount ≥ $0.01"
- BEH-002: "ORDER-ENTRY rejects orders > $999,999.99"
- BEH-003: "CREDIT-CHECK compares order amount against customer credit limit"
- BEH-004: "If amount > limit, CREDIT-CHECK returns rejection code 42"
- BR-001: "Orders must be between $0.01 and $999,999.99" (from BEH-001/002)
- BR-002: "Order amounts must not exceed customer credit limit" (from
  BEH-003/004)
- All BR-* marked `needs_sme_review`
- TBD-001: "Does BR-002 apply to all customer types or only certain tiers?"
  (sme_questions, blocking)

### Problem: Over-Inference

**Wrong:**
- BR-CREDIT-CHECK-005: "The system automatically declines high-risk customers"
  (invented; not in module analysis)
- BR-CREDIT-CHECK-006: "Credit decisions are made within 2 seconds" (naming
  inference; no evidence of latency requirement)

**Right:**
- Extract only what module and flows document
- If decision logic is unclear, create TBD-*

---

## See Also

- `anti-hallucination.md` — what NOT to do
- `SKILL.md` → Workflow section (step-by-step BRD synthesis)
- `docs/evidence-and-knowledge-taxonomy.md` (global)
- `docs/id-conventions.md` (global)
