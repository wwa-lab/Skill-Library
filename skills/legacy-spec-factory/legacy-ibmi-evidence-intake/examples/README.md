# Evidence Intake Examples

This directory contains worked examples of evidence collection and redaction
workflows for IBM i modernization.

---

## Example 1: customer-credit-intake (Worked Example)

**Scenario:** Collecting evidence for a customer credit check capability.

**Files:**
- `evidence-manifest.yaml` — Minimal approved registry for a source-only intake
- `redaction-log.md` — Redaction-owner audit trail
- `evidence-intake-review-checklist.md` — SME assessment and sign-off

**Learning objectives:**
- See how to collect and organize source (RPGLE, CLLE, DSPF)
- Understand redaction of account numbers and financial thresholds
- See spot-check procedure and SME review
- Learn how to preserve business logic while removing PII

**Key decisions:**
- Treats source-only evidence as inventory-ready because approvals are complete.
- Uses `package_state: approved_for_inventory` and `intake_decision.status: pass`.
- Leaves `unresolved_items` empty for the minimal example.

---

## Example 2: inventory-system-partial-intake (Negative Case)

**Scenario:** Incomplete evidence with redaction challenges.

**Files:**
- `evidence-manifest.yaml` — Partial collection with blocking gaps
- `redaction-log.md` — Blocked redaction audit trail
- `evidence-intake-review-checklist.md` — SME rejection and rework plan
- `expected-review-notes.md` — Compact expected behavior for smoke-style review

**Learning objectives:**
- See what happens when evidence is incomplete
- Understand how to document gaps as TBDs
- Learn how unknown sensitivity blocks downstream inventory
- See SME feedback loop and rework workflow

**Key issues:**
- PRTF (printer file) not provided; needed for report structure
- Transaction sample sensitivity is unknown
- Redaction owner is unassigned
- SME requested rework before downstream inventory
- `package_state: blocked` and `intake_decision.status: blocked`

---

## Using These Examples

### As a Template

1. Copy `evidence-manifest.yaml` as a starting point
2. Adapt field names, item counts, and descriptions for your capability
3. Adjust evidence types and redaction strategies as needed
4. Follow the same structure for manifest, redaction log, and checklist

### To Understand the Workflow

1. Read the manifest first to see the full evidence registry
2. Read the redaction log to understand what was redacted and why
3. Read the review checklist to see how SME validates quality
4. Compare worked example (positive) with negative case

### For Training

- Use credit-check example to show best practices
- Use inventory-system example to show common pitfalls
- Walk through spot-check procedure step-by-step
- Discuss strategic redaction decisions (preserve vs. remove)

---

## Quick Checklist for Your First Intake

1. **Intake Phase**
   - [ ] Data owner approved evidence export
   - [ ] All evidence items collected and listed
   - [ ] Capability scope is narrow (one capability, not whole app)

2. **Sensitivity Assessment Phase**
   - [ ] Every item has a sensitivity level (no `unknown`)
   - [ ] Intake reviewer assigned
   - [ ] Redaction owner assigned when redaction is required
   - [ ] SME owner assigned only when Step 0 needs SME judgment

3. **Source Authorization / Redaction Phase**
   - [ ] Source path authorization documented for internal source review
   - [ ] Redaction plan documented when masking is required
   - [ ] Redaction executed for items with `redaction_required: true`
   - [ ] Log records every source authorization or redaction change (no raw values)

4. **Spot-Check Phase**
   - [ ] All files parse without errors
   - [ ] Business logic is understandable
   - [ ] No missed PII patterns
   - [ ] Calculations still valid

5. **Review Phase**
   - [ ] Intake reviewer assesses evidence completeness
   - [ ] SME assesses evidence completeness/redaction quality only when required
   - [ ] Reviewer approves or requests rework

6. **Final Sign-Off Phase**
   - [ ] Manifest is complete
   - [ ] Redaction log is signed
   - [ ] Review checklist is signed
   - [ ] Ready for downstream skills

---

## Common Questions

**Q: What if I don't have all the evidence types?**  
A: Document gaps as TBDs. Mark whether they're blocking or informational. You
can proceed only when the manifest is `approved_for_inventory` and every open
TBD is non-blocking for inventory.

**Q: What if redaction is too complex or removes too much?**  
A: Work with the redaction owner and SME to find a middle ground. Preserve
business-critical information (amounts for thresholds, error messages for
logic). Redact identifiers and secrets.

**Q: What if I only have internal source paths and no SME yet?**  
A: Use `intake_mode: internal_source_review`, record `source_path_verified:
true`, assign the developer/reviewer as the intake owner, and set
`sme_required: false` unless Step 0 depends on business judgment.

**Q: How long does evidence intake take?**  
A: Internal source review can be much shorter because it records source paths
and reviewer approval. Governed redaction still depends on evidence volume,
redaction complexity, and SME availability.

**Q: Can I automate redaction?**  
A: Partially. Use regex to find PII patterns. Always manually verify in
context before replacing. Human judgment is essential.

**Q: What if evidence is contradictory?**  
A: Document both versions in the manifest. Create a TBD requiring SME
resolution. Do not choose one over the other without SME approval.

---

## Next Steps

After completing evidence intake:

1. Use `legacy-ibmi-inventory` to analyze the evidence
2. Reference evidence IDs (EV-SLUG-001, etc.) in all downstream artifacts
3. If new evidence is discovered, use same intake workflow and append to
   manifest
4. Route contradictions or gaps to SME for approval
