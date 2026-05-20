# Synthesis Rules: How to Aggregate Across Flows and Programs

This document defines the aggregation rules for each of the four views.
The module-analyzer does not re-analyze code or flows; it composes
existing analyses. These rules tell it how.

---

## General Synthesis Principles

1. **Inputs are authoritative.** If a flow analysis says X, the module
   analysis must not say not-X without explicit SME override (and an
   `EV-` link to the override).
2. **Aggregation is union, not intersection.** Every object touched by any
   flow appears in View 4. Every actor referenced in any flow appears
   in View 1. Coverage is broader at the module level.
3. **Deduplicate by stable ID.** Same OBJ-* in two flows → one row in
   View 4 with both flows listed.
4. **Preserve evidence chains.** Every aggregated fact must retain
   pointers to the source flow / program / SME note.
5. **TBDs propagate up.** A blocking TBD in any flow becomes a blocking
   TBD at the module level (unless resolved during module synthesis).

---

## View 1 — Operation Flow / Business Background

### Inputs
- All in-scope `flow-<FLOW-SLUG>.md` (specifically their Trigger Context,
  Business Capability Seeds, Error Propagation operational notes)
- SME-provided BAU notes
- SME interview transcripts (if available)
- Business documentation, ops manuals

### Aggregation Rules

| Field | Source | Rule |
| --- | --- | --- |
| Business Actors | SME notes; not from code | Union; deduplicate by role |
| Business Events | Each in-scope flow contributes one event (its business event name) | One row per flow |
| BAU Rhythm | SME notes; cross-checked against scheduler entries in flows | Cadence comes from SME; scheduler entries confirm |
| Manual Intervention Points | SME notes; cross-checked against operational outcomes in each flow's Error Propagation | Union |
| Exception Lifecycle | SME description; cross-checked against error paths in flows | SME-led |
| Business Rule Seeds | Union of all flows' SEED-* | Deduplicate by candidate-rule wording; combine references |

### Anti-Hallucination

- **No actor inferred from code.** A program named "MGRAPPRV" does not
  imply a "manager" actor unless SME confirms.
- **No BAU rhythm from log file inspection.** Cut-off times must come
  from SME or scheduler entry, not from observed timestamps.
- **No exception procedure from comments in code.** Comments rot; SME
  is authoritative.

---

## View 2 — System Flow

### Inputs
- Each flow's Trigger Context (for inbound systems) and External Calls
  (for outbound systems / interfaces)
- Architecture diagrams, integration specifications, SME

### Aggregation Rules

| Field | Source | Rule |
| --- | --- | --- |
| Upstream Systems | Trigger Context of API/Remote and Menu flows | One per distinct source system |
| Downstream Systems | Flow nodes that write external interface files / send remote calls | One per distinct target system |
| Integration Patterns | Each upstream/downstream relationship has one pattern | Capture per relationship |
| SLA | SME / integration spec | Per interface |
| Auth | SME / integration spec | Per interface |
| Security Boundaries | Architecture diagram + SME | Document at module level |

### Anti-Hallucination

- **No "system" inferred from a CALL** unless the called program is
  outside this module and at the boundary (e.g., a CALL to GLINTERFACE
  is a system call; a CALL to ORDVAL inside the same module is not).
- **No SLA assumed from "the program runs fast"** — must come from a
  documented contract or SME assertion.

---

## View 3 — Program Flow

### Inputs
- All in-scope flow analyses
- Programs are referenced by ID; not re-analyzed

### Aggregation Rules

| Field | Source | Rule |
| --- | --- | --- |
| Flow Inventory | One row per `flow-<FLOW-SLUG>.md` | direct copy of metadata |
| Cross-Flow Dependencies | Computed by scanning each flow's Cross-Program Data Flow section for shared carriers (files / DTAARAs / DTAQs / MSGQs / spool / IFS / external handoffs) | Where producer flow ≠ consumer flow, that's a cross-flow dependency |
| Shared Sub-Programs | Computed by scanning each flow's Nodes; any program appearing in ≥2 flows is shared | Sort by number of containing flows |
| Overall Call Topology | Top-level synthesis (often an ASCII diagram showing flows side-by-side) | Manual / SME-reviewed |

### Computing Cross-Flow Dependencies (Algorithm)

```
For each pair of flows (A, B):
    For each data exchange in A's Cross-Program Data Flow section:
        If exchange mechanism is "Shared file" / "Shared DTAARA" /
           "Shared DTAQ" / "Shared work file":
            Look for matching object in B's Cross-Program Data Flow.
            If found and roles complement (A produces, B consumes):
                Record cross-flow dependency A→B via that object.
```

### Anti-Hallucination

- **No dependency inferred** beyond what data-flow sections explicitly
  show. If A writes X and B reads X but the flows don't note it, do not
  invent the dependency — confirm with SME or treat as TBD.
- **No "shared utility"** inferred just because two programs have similar
  names. Must appear as a node in both flows.

---

## View 4 — Data Flow

### Inputs
- Every flow's Cross-Program Data Flow section
- Every program's Data Touch Map and Object Dependencies sections (from
  each `program-analysis-<OBJ-ID>.md`)
- inventory.yaml (for cross-reference)

### Aggregation Rules

| Field | Source | Rule |
| --- | --- | --- |
| Data Objects in Scope | Union of every flow `DATA-*` carrier plus every program Data Touch Map / Object Dependencies entry | One row per meaningful data object / carrier |
| Producer Flows / Consumer Flows | Determined by each flow's Cross-Program Data Flow section | Producer = flow with writer/sender/creator node; Consumer = flow with reader/receiver node |
| Coupling Score | Number of flows touching the object | Integer |
| Data Lifecycle | Union of all flow `State Impact` values and program Data Touch operations | Created (first write) / Updated (subsequent writes) / Read / Archived / Purged |
| Critical Data Trails | Flow critical trails plus SME review; trace key business records end-to-end | Evidence-backed, SME-confirmed for business meaning |
| DB Table Relationships | From DDS / SQL definitions in inventory | Direct mapping |
| Cross-Module Data Dependencies | Objects in this view owned by another module OR consumed by another module | Boundary detection |

### Computing Coupling Score

```
For each object O in scope:
    coupling[O] = number of distinct flows that touch O (read or write)

Coupling thresholds:
    1     - low (single-flow private object)
    2     - moderate (shared between 2 flows)
    3-5   - high (module-level shared)
    6+    - very high (hot path; modernization risk)
```

### Computing Data Lifecycle Stages

```
For each object O:
    Created: earliest-running flow that has a WRITE/INSERT to O without
             a prior CHAIN/SELECT (creation, not update)
    Updated: any flow with UPDATE on O
    Read:    any flow with CHAIN/READE/SELECT on O
    Archived: typically a separate archival job/flow (often out of module)
    Purged:  typically a separate purge job (often out of module)
```

Archived and Purged are often "out of module" → mark as `external` and
create a non-blocking TBD if not in scope of this module.

### Anti-Hallucination

- **No archival/purge** assumed without SME confirmation or a visible
  archive job in inventory.
- **No DB relationship** asserted without DDS / SQL evidence.
- **No coupling-hotspot mitigation** prescribed without SME consultation.

---

## Cross-View Consistency Check

After all four views are built, run these checks:

| Check | Rule |
| --- | --- |
| Actor → Code Path | Every ACTOR-* in View 1 must map to at least one entry node in View 3 OR be tagged `manual_actor: yes`. |
| System → Flow | Every SYS-* in View 2 must appear in View 3 as the source/target of at least one flow. |
| Rule Seed → Program | Every BR-* in View 1 must reference at least one program from View 3 or one object from View 4. |
| Data Object → Flow | Every object row in View 4 must reference at least one flow in View 3. |
| Flow → Data | Every flow in View 3 should touch at least one object in View 4 (otherwise the flow is pure compute — possible but unusual). |

Mismatches create cross-view TBDs that must be resolved (or explicitly
waived by SME) before the module is approved.

---

## How to Handle BAU That Has No Code Trace

Some BAU procedures exist only in human practice — e.g., "Finance reviews
the spool every morning before 09:00 and emails the auth team if exceptions
are found." This has no code path.

**Rule:** Document it in View 1 (manual intervention point) with
`evidence_strength: confirmed_by_sme` and link to a named SME note.
Do not try to map it to View 3 (no code). Tag the associated business
rule seed as "BAU-driven, not enforced by code" — this is critical
information for spec-writer to decide whether the target system should
encode this rule programmatically or preserve the manual process.
