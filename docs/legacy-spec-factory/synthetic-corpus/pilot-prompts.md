# Synthetic Corpus Pilot Prompts

Use these prompts for the **first internal pilot run** against the synthetic
fixtures in [`docs/synthetic-corpus/`](README.md).

These prompts are intentionally compact and evaluation-oriented. They are meant
to test routing, gate discipline, and output shape, not to generate final
production artifacts.

Pair this file with:

- [`pilot-execution-checklist.md`](pilot-execution-checklist.md)
- [`pilot-results-template.md`](pilot-results-template.md)

## OpenCode Usage

If your company can only use **OpenCode**, use these prompts there directly.
You do not need to adapt them for Codex or Claude Code. Keep the run style:

- no-write
- compact output
- compare against `expected/`

## Prompt Style

- keep runs **no-write** unless you explicitly want artifact generation
- ask for compact outputs that are easy to compare across runtimes
- compare responses against each fixture's `expected/` files

---

## 1. `sqlrpgle-credit-check-happy`

### Orchestrator

```text
Use /legacy-modernization-orchestrator.

User input:
I have a small synthetic IBM i credit-check slice under docs/synthetic-corpus/sqlrpgle-credit-check-happy/.
It includes:
- fixed-format SQLRPGLE program CREDITCHK
- CLLE wrapper CRDTCMD
- PF CUSTMAST
- LF CREDITVW
- sample joblog
- sample spool output
- SME notes

I want to reverse-engineer this capability safely. This is a no-write pilot check.

Return only:
- current stage
- recommended next skill
- gate check
```

### Evidence Intake

```text
Use /legacy-ibmi-evidence-intake.

User input:
Prepare evidence intake guidance for the synthetic fixture at
docs/synthetic-corpus/sqlrpgle-credit-check-happy/.

Available inputs:
- source/CREDITCHK.SQLRPGLE
- source/CRDTCMD.CLLE
- dds/CUSTMAST.PF
- dds/CREDITVW.LF
- runtime/sample-joblog.txt
- runtime/sample-spool.txt
- sme/sme-notes.md

This is a no-write pilot check. Do not create files.

Return only:
- required output files
- whether downstream inventory may run
- compact status
```

### Inventory

```text
Use /legacy-ibmi-inventory.

User input:
Review the synthetic fixture at docs/synthetic-corpus/sqlrpgle-credit-check-happy/.
Infer the minimum inventory needed for downstream analysis from:
- CLLE wrapper CRDTCMD
- SQLRPGLE program CREDITCHK
- PF CUSTMAST
- LF CREDITVW
- runtime evidence and SME notes

This is a no-write pilot check. Do not create files.

Return only:
- object list
- key relationships
- gate result
```

### Program Analyzer

```text
Use /legacy-ibmi-program-analyzer.

User input:
Analyze docs/synthetic-corpus/sqlrpgle-credit-check-happy/source/CREDITCHK.SQLRPGLE.
Focus on:
- entry point
- embedded SQL access
- decision branches
- message/report output behavior
- what business meaning is directly visible vs SME-confirmed

This is a no-write pilot check. Do not create files.

Return only:
- program type
- key control-flow summary
- key data/file access summary
- blocking status
```

### Flow Analyzer

```text
Use /legacy-ibmi-flow-analyzer.

User input:
Model the business flow for the synthetic fixture at
docs/synthetic-corpus/sqlrpgle-credit-check-happy/.

Available context:
- CRDTCMD is the wrapper entry path
- CREDITCHK performs the credit decision
- CREDITVW and CUSTMAST support status and available credit lookup
- runtime evidence shows over-limit deny behavior
- SME notes confirm active/inactive status meaning

This is a no-write pilot check. Do not create files.

Return only:
- trigger model
- high-level sequence
- capability seed
- blocking status
```

---

## 2. `sqlrpgle-credit-check-blocked`

### Orchestrator

```text
Use /legacy-modernization-orchestrator.

User input:
I have a synthetic IBM i credit-check slice under
docs/synthetic-corpus/sqlrpgle-credit-check-blocked/.
It includes CREDITCHK.SQLRPGLE, CRDTCMD.CLLE, CUSTMAST.PF, runtime notes, and SME notes.
But CREDITVW.LF is missing, and SME has not confirmed the meaning of STATUS = 'H'.

This is a no-write pilot check.

Return only:
- current stage
- gate status
- next skill (or stop)
```

### Inventory

```text
Use /legacy-ibmi-inventory.

User input:
Review the synthetic blocked fixture at
docs/synthetic-corpus/sqlrpgle-credit-check-blocked/.
Known issue:
- program references CREDITVW but the LF source is missing
- SME has not confirmed the business meaning of STATUS = 'H'

This is a no-write pilot check. Do not create files.

Return only:
- object list
- unresolved gaps
- gate result
```

### Program Analyzer

```text
Use /legacy-ibmi-program-analyzer.

User input:
Analyze docs/synthetic-corpus/sqlrpgle-credit-check-blocked/source/CREDITCHK.SQLRPGLE.
Important constraints:
- CREDITVW.LF source is missing
- SME has not yet confirmed the meaning of STATUS = 'H'

This is a no-write pilot check. Do not create files.

Return only:
- visible structure summary
- what remains unconfirmed
- blocking TBDs
- blocking status
```

### Flow Gate Check

```text
Use /legacy-ibmi-flow-analyzer.

User input:
Can the synthetic blocked fixture at
docs/synthetic-corpus/sqlrpgle-credit-check-blocked/
advance to flow analysis if CREDITVW.LF is missing and STATUS='H' is not SME-confirmed?

This is a no-write pilot check. Do not create files.

Return only:
- should flow analysis proceed
- blocking reasons
- next required upstream action
```

---

## 3. `batch-ar-reconciliation`

### Orchestrator

```text
Use /legacy-modernization-orchestrator.

User input:
I have a synthetic IBM i batch reconciliation slice under
docs/synthetic-corpus/batch-ar-reconciliation/.
It includes:
- CLLE submission wrapper ARRECONCL
- fixed-format SQLRPGLE batch driver ARRECON
- PF files ARTXN and ARCTRL
- PRTF ARERRRPT
- sample joblog
- sample spool report
- SME notes

This is a no-write pilot check.

Return only:
- current stage
- recommended next skill
- gate check
```

### Evidence Intake

```text
Use /legacy-ibmi-evidence-intake.

User input:
Prepare evidence intake guidance for the synthetic fixture at
docs/synthetic-corpus/batch-ar-reconciliation/.

Available inputs:
- source/ARRECONCL.CLLE
- source/ARRECON.SQLRPGLE
- dds/ARTXN.PF
- dds/ARCTRL.PF
- dds/ARERRRPT.PRTF
- runtime/sample-joblog.txt
- runtime/sample-spool.txt
- sme/sme-notes.md

This is a no-write pilot check. Do not create files.

Return only:
- required output files
- whether downstream inventory may run
- compact status
```

### Inventory

```text
Use /legacy-ibmi-inventory.

User input:
Review the synthetic batch fixture at
docs/synthetic-corpus/batch-ar-reconciliation/.
Infer the minimum inventory needed for downstream analysis from the source,
runtime evidence, and SME notes.

This is a no-write pilot check. Do not create files.

Return only:
- object list
- key relationships
- gate result
```

### Program Analyzer

```text
Use /legacy-ibmi-program-analyzer.

User input:
Analyze docs/synthetic-corpus/batch-ar-reconciliation/source/ARRECON.SQLRPGLE.
Focus on:
- batch trigger context
- checkpoint / restart control
- main loop behavior
- exception-report generation
- completion-state update

This is a no-write pilot check. Do not create files.

Return only:
- program type
- key control-flow summary
- key data/file access summary
- blocking status
```

### Runtime Evidence Miner

```text
Use /legacy-ibmi-runtime-evidence-miner.

User input:
Mine runtime evidence from:
- docs/synthetic-corpus/batch-ar-reconciliation/runtime/sample-joblog.txt
- docs/synthetic-corpus/batch-ar-reconciliation/runtime/sample-spool.txt

Focus on:
- batch submission
- restart behavior
- exception events
- completion event
- report structure

This is a no-write pilot check. Do not create files.

Return only:
- observations found
- confidence summary
- blocking status
```

### Flow Analyzer

```text
Use /legacy-ibmi-flow-analyzer.

User input:
Model the business flow for the synthetic fixture at
docs/synthetic-corpus/batch-ar-reconciliation/.

Available context:
- scheduler submits ARRECONCL
- ARRECONCL submits ARRECON
- ARRECON reads ARTXN and ARCTRL
- ARRECON writes exception output to ARERRRPT
- runtime evidence shows restart, exception, and completion signals
- SME notes confirm nightly reconciliation and next-morning finance review

This is a no-write pilot check. Do not create files.

Return only:
- trigger model
- high-level sequence
- capability seed
- blocking status
```

---

## 4. `screen-subfile-inquiry`

### Orchestrator

```text
Use /legacy-modernization-orchestrator.

User input:
I have a synthetic IBM i inquiry slice under
docs/synthetic-corpus/screen-subfile-inquiry/.
It includes:
- menu entry text for Customer Inquiry
- DSPF with header and transaction-history subfile
- SQLRPGLE inquiry program skeleton
- runtime screen notes
- sample joblog
- SME notes

This is a no-write pilot check.

Return only:
- current stage
- recommended next skill
- gate check
```

### Evidence Intake

```text
Use /legacy-ibmi-evidence-intake.

User input:
Prepare evidence intake guidance for the synthetic fixture at
docs/synthetic-corpus/screen-subfile-inquiry/.

Available inputs:
- source/CUSTMENU.MENU.txt
- source/CUSTINQDSP.DSPF
- source/CUSTINQ.SQLRPGLE
- runtime/sample-screen-notes.md
- runtime/sample-joblog.txt
- sme/sme-notes.md

This is a no-write pilot check. Do not create files.

Return only:
- required output files
- whether downstream inventory may run
- compact status
```

### Inventory

```text
Use /legacy-ibmi-inventory.

User input:
Review the synthetic inquiry fixture at
docs/synthetic-corpus/screen-subfile-inquiry/.
Infer the minimum inventory needed for downstream analysis from the menu entry,
DSPF, SQLRPGLE program skeleton, runtime notes, and SME notes.

This is a no-write pilot check. Do not create files.

Return only:
- object list
- key relationships
- gate result
```

### Screen Analyzer

```text
Use /legacy-ibmi-screen-report-analyzer.

User input:
Analyze docs/synthetic-corpus/screen-subfile-inquiry/source/CUSTINQDSP.DSPF.
Focus on:
- overall screen purpose
- subfile structure
- function key behavior
- what is clearly inquiry behavior vs what needs program confirmation

This is a no-write pilot check. Do not create files.

Return only:
- surface classification
- key fields and regions
- key function-key behaviors
- blocking status
```

### Program Analyzer

```text
Use /legacy-ibmi-program-analyzer.

User input:
Analyze docs/synthetic-corpus/screen-subfile-inquiry/source/CUSTINQ.SQLRPGLE.
Focus on:
- inquiry loop behavior
- EXFMT usage
- refresh path
- return-to-menu path

This is a no-write pilot check. Do not create files.

Return only:
- program type
- key control-flow summary
- key screen interaction summary
- blocking status
```

### Flow Analyzer

```text
Use /legacy-ibmi-flow-analyzer.

User input:
Model the business flow for the synthetic fixture at
docs/synthetic-corpus/screen-subfile-inquiry/.

Available context:
- user selects option 5 from customer-service menu
- inquiry program displays customer inquiry header and transaction subfile
- runtime notes confirm F5 refresh and F12 back behavior
- SME notes confirm inquiry-only usage

This is a no-write pilot check. Do not create files.

Return only:
- trigger model
- high-level sequence
- capability seed
- blocking status
```
