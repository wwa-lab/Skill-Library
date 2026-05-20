# SME Review Session

**Session ID:** REVIEW-`<CAPABILITY-SLUG>`-`<NNN>`

**Artifact Under Review:** `<path/to/artifact.md or .yaml>`  
**Artifact Status:** `draft` / `in_review` / `approved_with_non_blocking_tbd` / `approved`

## Participants

**SME Reviewer:**
- Name: `<SME name>`
- Role/Title: `<role, e.g., "Accounts Payable Team Lead">`
- Organization: `<org>`
- Email/Contact: `<contact>`
- Availability: `<sync/async, preferred dates/times>`

**Review Facilitator:**
- Name: `<facilitator name>`
- Role: `<role, e.g., "Legacy Spec Factory Agent">`

## Scope Statement

**Capability:** `<CAPABILITY-SLUG>`

**Review Focus:** (select one or more)
- [ ] Confirm observed behaviors (`BEH-*`)
- [ ] Validate inferred business rules (`BR-*` seeds)
- [ ] Clarify contradictory evidence
- [ ] Resolve open TBDs (`TBD-*`)
- [ ] Record SME acceptance or rejection of modernization decisions (`DEC-*`)
- [ ] Validate evidence strength assessments
- [ ] Record SME sign-off conditions for downstream advancement

**Specific Items in Scope:**
```
- TBD-<CAPABILITY>-NNN: <brief description>
- BR-<CAPABILITY>-NNN: <brief description>
- ...
```

**Out of Scope:**
(list any items explicitly not reviewed in this session)

## Session Structure

1. **Setup** (5-10 min)
   - Confirm scope and expectations
   - Review artifacts and evidence summaries
   - Check that all materials are available

2. **Question Review** (30-60 min, depends on scope)
   - Present each question (TBD, inferred rule, contradiction, etc.)
   - Record SME answer verbatim
   - Capture decision outcome

3. **Escalation Handling** (as needed)
   - If SME defers: record owner, target date, next step
   - If contradiction needs more time: propose follow-up

4. **Sign-Off** (5-10 min)
   - Confirm all decisions are recorded accurately
   - Request SME approval for advancement

## Materials Prepared

- [ ] Question pack (`sme-question-pack.md`)
- [ ] Evidence summaries (linked `EV-*` with strength assessment)
- [ ] Evidence manifest (redaction status for all linked items)
- [ ] Related artifacts (BRD, spec, module analysis, etc.)
- [ ] Scope boundaries (what is / is not being reviewed)

## Session Status

**Scheduled Date:** `YYYY-MM-DD`  
**Actual Date:** `YYYY-MM-DD` (if completed)  
**Status:** `pending` / `in_progress` / `completed` / `blocked`

**Stop Reason (if blocked):**
```
- No SME owner assigned
- Artifact below required status
- Evidence sensitivity unknown
- Other: <explain>
```

## Session Notes

(Record any context, scheduling notes, or SME availability constraints)

## Next Steps

After sign-off:
1. Route decision log and follow-up findings to downstream owners
2. Ask the owning skill to update artifact status when the recorded decisions
   permit it
3. Escalate unresolved items per follow-up-findings.yaml
