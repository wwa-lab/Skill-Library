# BRD Validation Scenarios: `<CAPABILITY-NAME>`

**BRD ID:** `BRD-<CAPABILITY-SLUG>-001`
**Capability ID:** `CAP-<CAPABILITY-SLUG>-001`
**Status:** `draft` | `in_review` | `approved`
**Owner:** `<SME Name / Role>`
**Created:** `<YYYY-MM-DD>`
**Last Updated:** `<YYYY-MM-DD>`

---

## Purpose

This file captures SME-reviewable validation scenario seeds for the BRD.
They help reviewers confirm business behavior and help downstream teams plan
acceptance criteria, golden master tests, and SOW scope.

These are **not** formal acceptance criteria and **not** executable test cases.
Do not mint `AC-*` or `TC-*` here. Formal `AC-*` entries are produced by
`legacy-spec-writer`; formal `TC-*` entries are produced by
`legacy-golden-master-test-planner` after spec approval and runtime evidence
review.

---

## Scenario Coverage Summary

| Area | Count | Notes |
| --- | ---: | --- |
| Happy path scenarios | `<N>` | `<Coverage summary>` |
| Exception scenarios | `<N>` | `<Coverage summary>` |
| Boundary scenarios | `<N>` | `<Coverage summary>` |
| Deferred / evidence-missing scenarios | `<N>` | `<Coverage summary>` |

---

## Scenario Seeds

### VAL-<CAPABILITY-SLUG>-001: `<Scenario Title>`

**Scenario Type:** `happy_path` | `exception` | `boundary` | `negative` |
`manual_review`
**Business Goal:** `<What business behavior this scenario helps validate>`
**Related Rules:** `BR-<CAPABILITY-SLUG>-001`
**Related Behaviors:** `BEH-<CAPABILITY-SLUG>-001`
**Evidence:** `EV-<CAPABILITY-SLUG>-001`, `EV-<CAPABILITY-SLUG>-002`
**SME Question:** `<What should the SME confirm or correct?>`
**Expected Business Outcome:** `<Business-level outcome only; do not invent exact outputs>`
**Data Needed Later:** `<Sample transaction, field set, spool sample, or runtime evidence needed for TC-* planning>`
**Readiness:** `ready_for_spec` | `needs_sme_review` | `needs_runtime_evidence` |

**Notes:**

```
<Optional notes for SME / BA / downstream test planner>
```

---

### VAL-<CAPABILITY-SLUG>-002: `<Scenario Title>`

**Scenario Type:** `exception`
**Business Goal:** `<What exception or edge behavior this scenario validates>`
**Related Rules:** `BR-<CAPABILITY-SLUG>-002`
**Related Behaviors:** `BEH-<CAPABILITY-SLUG>-002`
**Evidence:** `EV-<CAPABILITY-SLUG>-003`
**SME Question:** `<What policy or interpretation is unclear?>`
**Expected Business Outcome:** `<Business-level outcome only>`
**Data Needed Later:** `<Runtime sample / expected output evidence needed>`
**Readiness:** `needs_sme_review`

**Notes:**

```
<Optional notes>
```

---

## Deferred Scenarios

Use this section when a useful validation scenario cannot be drafted safely
because evidence is missing or contradictory.

| Deferred Scenario | Related BR/BEH | Blocking Reason | Resolver | Next Step |
| --- | --- | --- | --- | --- |
| `<Scenario idea>` | `BR-<CAPABILITY-SLUG>-003` | `missing_runtime_evidence` | `<SME / Source Owner>` | `<Collect sample transaction / answer TBD>` |

---

## SME Review Checklist

- [ ] Every `VAL-*` scenario maps to at least one `BR-*` or `BEH-*`.
- [ ] No `VAL-*` scenario introduces a new business rule.
- [ ] No scenario contains formal `AC-*`, formal `TC-*`, target architecture,
      implementation detail, or invented exact output.
- [ ] Deferred scenarios are tied to explicit evidence gaps or SME questions.
- [ ] Scenario coverage is sufficient for the SME to review the BRD scope.

---

**Prepared by:** Claude Code / Agent name
**Last reviewed by:** `<SME name>` (date, status)
