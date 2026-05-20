# Batch AR Reconciliation Happy Path

A compact **synthetic batch fixture** for IBM i modernization pilot work.

## Scenario

This fixture models a nightly accounts-receivable reconciliation batch:

- scheduler submits a CLLE wrapper
- the wrapper launches a fixed-format `SQLRPGLE` driver
- the driver reads staged transactions, writes reconciliation exceptions, and
  updates a checkpoint/control structure
- an exception spool report is reviewed by Finance the next morning

This is designed to exercise the repository's batch-oriented understanding
skills without requiring a large synthetic estate.

## Why This Fixture Exists

Batch-heavy IBM i modernization is usually where reverse-engineering gets more
interesting:

- triggers are indirect (`scheduler -> SBMJOB -> CLLE -> RPGLE`)
- restart/recovery rules matter
- runtime evidence can be as important as source
- spool reports are part of the business control loop

That makes batch a high-value fixture family for this repository.

## Included Assets

```text
batch-ar-reconciliation/
  README.md
  source/
    ARRECONCL.CLLE
    ARRECON.SQLRPGLE
  dds/
    ARTXN.PF
    ARCTRL.PF
    ARERRRPT.PRTF
  runtime/
    sample-joblog.txt
    sample-spool.txt
  sme/
    sme-notes.md
  expected/
    inventory-assertions.md
    runtime-evidence-assertions.md
    program-analysis-assertions.md
    flow-assertions.md
```

## Intended Skill Coverage

- `legacy-modernization-orchestrator`
- `legacy-ibmi-evidence-intake`
- `legacy-ibmi-inventory`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-runtime-evidence-miner`
- `legacy-ibmi-flow-analyzer`

Secondarily, it can support:

- `legacy-ibmi-module-analyzer`
- `legacy-spec-writer`
- `legacy-golden-master-test-planner`

## Expected Reverse-Engineering Themes

- scheduler-driven nightly trigger
- CLLE operational wrapper
- fixed-format `SQLRPGLE` batch loop
- control/checkpoint record usage
- exception-only report generation
- restart awareness after failure or partial completion

## What Good Output Should Notice

- `ARRECONCL` is the batch trigger/control wrapper
- `ARRECON` owns the main reconciliation business logic
- the control file is operationally important, not just incidental plumbing
- exceptions are first-class business outputs, not debug traces
- runtime evidence helps confirm cut-off time and restart procedure

## Suggested Next Sibling

Add a blocked sibling later with:

- missing PRTF or missing checkpoint semantics
- conflicting SME note about rerun scope
- expected result: blocked flow or blocked decision package
