# Code As Ground Truth

The single most important principle of Legacy Spec Factory.

## The Principle

> **The currently-deployed source code is the authoritative description
> of what the legacy system does.** Comments, source-level headers,
> shop tool outputs, external documentation, wikis, prior specs, and
> SME recollection are supplementary — useful, sometimes essential, but
> never authoritative when they disagree with what code actually does.

## Why This Matters

In every long-lived legacy system, three drifts accumulate:

- **Comment drift.** Comments are written once; code is edited many
  times. After a decade, a non-trivial fraction of comments lie.
- **Documentation drift.** Wiki pages, runbooks, prior modernization
  attempts, vendor specs — all freeze at a moment in time while the
  code keeps moving.
- **Memory drift.** SMEs remember the system as it was when they last
  worked on a given module, not as it is. Senior engineers describe
  intent. Code describes behavior. They diverge.

Modernization projects fail when they model the *intent* instead of the
*behavior*. The target system then ships with confidently-encoded rules
that no production transaction actually follows.

## Evidence Tier Model

When sources disagree, resolve in this order:

| Tier | Source | Authority | Notes |
| --- | --- | --- | --- |
| **1** | Currently-deployed source code (RPGLE, CLLE, COBOL, DDS, SQL DDL) | **Authoritative** for *behavior* (what the system does) | The compiler / runtime executes this; nothing else does |
| **2** | SME confirmation | **Authoritative** for *intent and policy* (why the system does what it does) | Code can never explain "why"; only humans can |
| **3** | Source-level comments / flow headers / DDS descriptions / shop tool exports (F5-OBJREF, etc.) | **Reference** | Useful starting point; verify against tier 1 before relying on |
| **4** | External documentation, wikis, prior modernization specs, vendor manuals, training material | **Suspect** | Treat as hypotheses requiring tier 1 or tier 2 confirmation |

## Conflict Resolution Rules

### Rule 1: Tier 1 wins on behavior

If a comment says "this validates customer status" but the code doesn't,
**the spec records that the code does not validate customer status.**
The comment is stale.

The disagreement itself becomes a TBD asking the SME to confirm whether:
- (a) the comment is stale → update comment, no behavior change, or
- (b) the code drifted from intent → behavior is a bug requiring fix.

Until SME confirms (a) or (b), the spec describes the code's actual
behavior, not the comment's claim.

### Rule 2: Tier 2 wins on why

If SME says "credit limit enforcement is required by regulation"
and the code enforces it, **the spec attributes the rule to the
regulation** (SME provides intent; code provides mechanism).

If SME says "credit limit is required by regulation" but the code
*doesn't* enforce it, **both observations are recorded:**
- BEH (factual): "Credit limit is not enforced for transactions of
  type ATMP" (from code)
- TBD: "SME says credit limit is regulatorily required; code does not
  enforce for ATMP. Bug? Intentional carve-out? Policy change?"

The spec does not silently encode the SME's claim as a BR — that would
codify a rule the legacy system doesn't actually follow.

### Rule 3: Tier 3 is starting point, not endpoint

Use shop tool outputs (F5-OBJREF TREE, source-level flow headers, DDS
descriptions) to **navigate** the code quickly. Then verify each tier-3
claim against tier 1 before promoting it to evidence.

- Source flow header lists `SR110 → SR111 → SR112` but code only has
  `EXSR SR110` and `EXSR SR113` → TBD: comment drift; spec records the
  actual EXSR pattern.
- Shop OBJREF tree lists `HCCDTAR115` as a copybook but the code
  doesn't `/COPY` it → TBD: stale dependency report; spec records the
  code's actual `/COPY` directives.

### Rule 4: Tier 4 is hypothesis only

Wiki pages, prior specs, vendor manuals, training materials — read them
to build hypotheses. Never carry their claims into the spec without
tier-1 or tier-2 confirmation.

## Application Per Skill

### `legacy-ibmi-inventory`

The inventory enumerates **objects that actually exist in the
production library** — from current `WRKOBJ` / `DSPOBJD` / source
member listings. Tier 3 inputs (existing inventory spreadsheets,
shop catalogs) are starting points, not endpoints; every entry is
verified against tier 1.

### `legacy-ibmi-program-analyzer`

- Call graph: source-level "Main flow control" headers (tier 3) are
  reproduced verbatim *because* they reflect the author's intent. But
  the analyzer also derives a call graph from `EXSR / CALL / CALLP /
  PERFORM` statements (tier 1). When they disagree, **the tier-1
  graph is authoritative**, and the disagreement becomes a TBD.
- Object dependencies: F5-OBJREF TREE output (tier 3) is matched
  against `F-spec`, `D-spec`, `/COPY`, and `CALL` statements (tier 1).
  Tier-1 wins on disagreement.
- Error handling: comments labeling a block as "error recovery" do not
  make it error recovery — `MONITOR`, `MONMSG`, `ON ERROR`, indicator
  flags in code do.

### `legacy-ibmi-flow-analyzer`

- Edges between nodes must trace to a tier-1 CALL/CALLP/CALLPRC/SBMJOB/
  trigger-registration statement. Shop documentation describing the
  flow (tier 3-4) is a navigation aid, not evidence.
- Trigger model is identified from tier 1 (CL source, menu definition,
  trigger registration, scheduler entry, MQ config) — tier 2 (SME)
  fills in *why* the flow exists, not *that* it exists.
- Cross-program data flow (DTAARA, DTAQ, shared files) must trace to
  tier-1 statements in some program; SME claims about hidden data
  exchanges require tier-1 corroboration or a TBD.

### `legacy-ibmi-module-analyzer`

The 4-view model has a per-view authority pattern:

| View | Primary Tier | Why |
| --- | --- | --- |
| 1. Operation Flow | Tier 2 (SME) | Business context is irreducibly human |
| 2. System Flow | Tier 2 + Tier 3 (architecture docs, integration specs) | Architectural intent lives outside code |
| 3. Program Flow | Tier 1 (via aggregated flow / program analyses) | Programs and calls are code facts |
| 4. Data Flow | Tier 1 (via aggregated object dependencies and DDS) | File structure is a code fact |

**However**, even in View 1 and View 2, **tier 1 contradicts tier 2 when
they disagree about behavior**:
- SME says "we always log every transaction" but TXNLOGPF write is
  inside an IF block in NODE-04 → BEH records the conditional log;
  TBD asks SME to confirm whether the IF-guarded behavior is intent
  or bug.
- SME says "we no longer use the ATMP path" but flow-analyzer found
  references to it → TBD asks SME whether the path is dead code or
  the SME's recollection is wrong.

### `legacy-spec-writer`

The rule-extraction protocol in `references/rule-extraction-protocol.md`
already classifies rule sources:

- **Class A** (code-encoded + SME approved) — tier 1 + tier 2
- **Class B** (SME-only) — tier 2 (operational policy)
- **Class C** (inferred from patterns) — weakest, requires explicit SME
- **Class D** (speculative) — never becomes a BR

A BR can be `approved` when class A or B is met. Class C requires SME
to explicitly say "yes, the inference is correct" — without that the
BR stays `needs_sme_review`.

## What This Rules Out

This principle rules out three common modernization-project failure
modes:

1. **"The comments say X, so the system does X."** Wrong if the code
   says otherwise. The spec records what code does; the comment becomes
   a TBD about which is correct.
2. **"The SME told me the rule is X, so the BR is X."** Wrong if the
   code doesn't implement X. The spec records both observations and
   blocks until SME reconciles them.
3. **"The old spec said X, so we'll just re-confirm X."** Wrong; the
   old spec is tier 4. Start from tier 1 + tier 2; the old spec
   contributes hypotheses, not facts.

## What This Does Not Rule Out

- SME interviews — essential for tier 2 (the *why*).
- Shop tool outputs — useful for tier 3 (fast navigation).
- Prior documentation — useful for tier 4 (hypothesis generation).

The principle is about **resolution**, not exclusion. Use every source;
when they disagree, code wins on behavior, SME wins on policy, and the
disagreement itself becomes a TBD.

## The Cardinal Rule

> If you cannot point to a line of currently-deployed source code, a
> named SME with a date-stamped confirmation, or both, you are
> describing intent rather than behavior. Mark it as a TBD or as
> `needs_sme_review`. The spec only describes what runs.
