# BRD Review Checklist: `<CAPABILITY-NAME>`

**BRD ID:** `BRD-<CAPABILITY-SLUG>-001`  
**Capability Owner (SME):** `<Name / Role>`  
**Review Date:** `<YYYY-MM-DD>`  
**Status:** `in_review` | `approved` | `needs_revision` | `rejected`

---

## Reviewer Guidance

This checklist is completed by the **capability owner SME**. The reviewer must
validate that the BRD is accurate, complete, and safe to forward to the
specification phase.

**What to check:**

1. Are the **observed behaviors** accurate to legacy system reality?
2. Are the **inferred business rules** actually business rules (not
   implementation artifacts)?
3. Is the **scope and boundary** correct?
4. Are there **unspoken rules** the code doesn't show (BAU, manual procedures)?
5. Are the **TBDs** correctly categorized and achievable?
6. Is the BRD ready for **spec-writing** without re-interrogating you?

---

## Observed Behaviors

### `BEH-<CAPABILITY-SLUG>-001`: Does this match legacy system behavior?

- [ ] **Yes** — accurate, can forward to spec-writer
- [ ] **Partial** — mostly correct, but needs clarification (see notes)
- [ ] **No** — inaccurate or missing key behavior (block until revised)

**Reviewer Notes:**

```
<Space for SME feedback>
```

---

### `BEH-<CAPABILITY-SLUG>-002`: Does this match legacy system behavior?

- [ ] **Yes**
- [ ] **Partial**
- [ ] **No**

**Reviewer Notes:**

```
<Space for SME feedback>
```

---

## Inferred Business Rules

### `BR-<CAPABILITY-SLUG>-001`: Is this a real business rule?

- [ ] **Yes** — this is a business rule; mark for promotion in spec phase
- [ ] **No** — this is implementation artifact, not a rule (remove or clarify)
- [ ] **Unclear** — needs more evidence or discussion (block until resolved)

**Reviewer Decision:** `approve` | `reject` | `needs_evidence`

**Reviewer Notes:**

```
<Space for SME feedback>
```

---

### `BR-<CAPABILITY-SLUG>-002`: Is this a real business rule?

- [ ] **Yes**
- [ ] **No**
- [ ] **Unclear**

**Reviewer Decision:** `approve` | `reject` | `needs_evidence`

**Reviewer Notes:**

```
<Space for SME feedback>
```

---

## Scope & Boundaries

### Is the capability scope correct?

- [ ] **Yes** — in_scope and out_of_scope are accurate
- [ ] **Partial** — some items are mis-categorized (see notes)
- [ ] **No** — boundary is wrong or contested

**Reviewer Notes:**

```
<Space for SME feedback>
```

---

### Are there unspoken business rules or BAU procedures not captured in the BRD?

- [ ] **No** — everything material is captured
- [ ] **Yes** — there are gaps (describe below)

**Gaps Identified:**

```
<Space for SME to list missing business context>
```

---

## Open Questions (TBDs)

### Are the TBDs correctly categorized and achievable?

- [ ] **All TBDs are valid** — correctly categorized, achievable, appropriately
      blocking/non-blocking
- [ ] **Some TBDs need refinement** — description or resolver needs clarity
      (see notes)
- [ ] **TBD handling is blocked** — cannot move forward until resolved

**Reviewer Notes:**

```
<Space for SME feedback on TBDs>
```

---

## Completeness & Handoff Readiness

### Is the BRD ready to forward to the specification phase?

- [ ] **Yes** — all facts validated, no silent gaps, spec-writer can proceed
      without re-interrogating SME
- [ ] **Almost** — minor gaps (see notes); recommend minor revision before
      forwarding
- [ ] **No** — major issues (see notes); block until resolved

**Readiness Assessment:**

```
<Space for overall SME judgment>
```

---

## Final Decision

### BRD Status Transition

**Current Status:** `in_review`

**Final Status:**

- [ ] `approved` — Forward to spec-writer with confidence
- [ ] `approved_with_non_blocking_tbd` — Forward to spec-writer; carry
      non-blocking TBDs listed below
- [ ] `needs_revision` — Return to author with specific feedback
- [ ] `rejected` — Do not forward to spec-writer

**Non-Blocking TBDs (if approved_with_non_blocking_tbd):**

```
<List any non-blocking TBDs that spec-writer should carry forward>
```

---

## Sign-Off

**Capability Owner (SME):**

- **Name:** `<Full name>`
- **Role:** `<Title>`
- **Date:** `<YYYY-MM-DD>`
- **Signature / Approval:** `<Electronic or written sign-off>`

**Author/Synthesizer:**

- **Name:** `<Claude Code or Agent name>`
- **Date:** `<YYYY-MM-DD>`

---

## Next Steps

If `approved` or `approved_with_non_blocking_tbd`:
- Forward BRD to `legacy-spec-writer` along with module analysis
- Spec-writer may promote BR-* from `needs_sme_review` to `approved` in
  `spec.yaml` using your explicit decisions recorded above
- Spec-writer will generate acceptance criteria and modernization decisions

If `needs_revision`:
- Author revises BRD based on feedback
- SME re-reviews before approval

If `rejected`:
- Escalate to product/architecture leadership for path forward
