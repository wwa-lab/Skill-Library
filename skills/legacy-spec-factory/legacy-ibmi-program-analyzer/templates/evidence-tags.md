# Evidence Strength Quick Reference

Use this card when tagging each behavior in the program analysis.

---

## The Five Evidence Strengths

### ✅ confirmed_from_code
**When:** Source code directly shows the behavior.

```
— Procedure spec (RPGLE BEGPR, COBOL ENTRY)
— File spec (RPGLE F-spec, COBOL FILE-CONTROL)
— I/O statement (SETLL, READE, CHAIN, WRITE, READ)
— CALL statement (CALL, CALLP, PERFORM)
— Error handler (MONITOR, MONMSG, ON ERROR)
— Explicit IF/SELECT condition
```

**Example:** "Entry point MAIN with parameters (CustID, Amount) — confirmed in RPGLE procedure spec."

**Use:** Always for specs, I/O, and visible statements.

---

### 🟡 medium_confidence
**When:** Behavior inferred from code logic but not explicitly declared.

```
— Conditional logic implies validation
— Field assignment suggests purpose
— Indicator logic implies condition
— Control structure implies behavior
— No explicit documentation found
```

**Example:** "CustID is validated before CHAIN — inferred from if/else structure, but no explicit validation rule documented."

**Use:** When code shows the behavior but doesn't state the rule.

---

### 🟠 strongly_inferred
**When:** Multiple evidence points converge on the same conclusion.

```
— Pattern repeats across multiple code paths
— Same check appears in multiple places
— Consistent call-site behavior
— Multiple assignments to same field
```

**Example:** "Both CREDFILE and LIMITTBL must exist before proceeding — both have %found() checks with same error path."

**Use:** When evidence points are consistent and repeating.

---

### 🔴 needs_sme_review
**When:** Evidence is present but interpretation is ambiguous.

```
— Undocumented external call
— Unclear error codes or return values
— Unknown parameter contracts
— Context-dependent behavior
— Multiple valid interpretations
```

**Example:** "External program CHECKEXPOSE returns codes — visible in call, but meanings undocumented."

**Use:** When SME must clarify intent.

---

### ⚠️ missing
**When:** Required evidence is not available. Usually → creates TBD.

```
— DDS not provided for file
— External program documentation missing
— Copybook not included
— Required source not provided
```

**Example:** "CUSTFILE DDS missing — field definitions not available."

**Use:** When you cannot tag without inventing. Create TBD instead.

---

## Decision Tree

```
Does source code directly show this?
(spec, I/O statement, CALL, MONITOR, explicit condition)

├─ YES
│  └─→ confirmed_from_code
│
└─ NO: Is behavior inferred from pattern?
   ├─ Single point
   │  └─→ medium_confidence
   │
   ├─ Multiple points, consistent
   │  └─→ strongly_inferred
   │
   ├─ Ambiguous / undocumented
   │  └─→ needs_sme_review
   │
   └─ Evidence missing entirely
      └─→ missing (create TBD)
```

---

## Common Tags

### Entry Points
- ✅ confirmed_from_code — procedure spec visible
- 🟡 medium_confidence — inferred from calls
- ⚠️ missing — called from external program, spec not visible

### File I/O
- ✅ confirmed_from_code — F-spec / FILE-CONTROL visible
- 🟡 medium_confidence — field access inferred from statements
- ⚠️ missing — DDS not provided

### External Calls
- ✅ confirmed_from_code — CALL statement visible
- 🔴 needs_sme_review — parameters undocumented
- ⚠️ missing — called program documentation missing

### Control Flow
- ✅ confirmed_from_code — IF/SELECT explicit
- 🟡 medium_confidence — inferred from assignment pattern
- 🟠 strongly_inferred — pattern repeats consistently

### Error Handling
- ✅ confirmed_from_code — MONITOR / MONMSG / ON ERROR visible
- 🟠 strongly_inferred — error path observed in multiple branches
- 🔴 needs_sme_review — error codes unclear
- ⚠️ missing — no error handling observed

---

## Bad Tags to Avoid

| ❌ WRONG | ✅ RIGHT |
| --- | --- |
| "probably does this" (no tag) | medium_confidence with explanation |
| "I assume this" (no tag) | needs_sme_review + TBD |
| "likely calls this" (confirmed) | medium_confidence or needs_sme_review |
| "must be file" (no evidence) | missing + TBD |
| "obviously" (no tag) | confirmed_from_code + quote source |

---

## Tagging Template

When documenting each behavior, use:

```
[Behavior description]
[evidence_strength: TAG]

Link: [EV-SLUG-NNN or TBD-SLUG-NNN]
Explanation: [Why this tag? What's the evidence?]
```

**Example:**

```
File I/O: CHAIN on CREDFILE with key CUSTID
evidence_strength: confirmed_from_code

Link: EV-CREDIT-CHECK-002
Explanation: F-spec shows CREDFILE; CHAIN statement on line 145 uses CUSTID as key.
```

---

## When in Doubt

- **Explicit in source?** → confirmed_from_code
- **Pattern repeats?** → strongly_inferred
- **Pattern inferred?** → medium_confidence
- **Ambiguous?** → needs_sme_review
- **Missing?** → missing + TBD-SLUG-NNN

**Never tag "likely" or "probably" without a strength level.**

