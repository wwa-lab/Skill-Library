# SQLRPGLE Credit Check Happy Path

A compact **synthetic** fixture for fixed-format `SQLRPGLE`-heavy pilot work.

## Scenario

Customer service enters an order amount. A CLLE command wrapper calls a
fixed-format SQLRPGLE program that:

- looks up the customer's active credit profile
- rejects inactive or missing customers
- compares requested amount to available credit
- returns an approval flag and approved amount

This fixture is designed to resemble the kind of narrow, business-relevant
legacy slice we can realistically use for internal pilot testing.

## Why This Fixture First

This repository's likely real-world starting point is:

- mostly fixed-format RPG / SQLRPGLE
- business logic encoded in DB2 access plus status flags
- a small CLLE entry wrapper
- enough runtime evidence to validate behavior

So this fixture is a good seed for the main reverse-engineering path without
requiring a huge synthetic estate.

## Included Assets

```text
sqlrpgle-credit-check-happy/
  README.md
  source/
    CREDITCHK.SQLRPGLE
    CRDTCMD.CLLE
  dds/
    CUSTMAST.PF
    CREDITVW.LF
  runtime/
    sample-joblog.txt
    sample-spool.txt
  sme/
    sme-notes.md
  expected/
    inventory-assertions.md
    program-analysis-assertions.md
    flow-assertions.md
```

## Intended Skill Coverage

- `legacy-modernization-orchestrator`
- `legacy-ibmi-evidence-intake`
- `legacy-ibmi-inventory`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-flow-analyzer`

Secondarily, it can support:

- `legacy-ibmi-module-analyzer`
- `legacy-spec-writer`
- `legacy-golden-master-test-planner`

## Expected Reverse-Engineering Themes

- fixed-format F-specs and D-specs
- embedded SQL in `SQLRPGLE`
- keyed DB2 lookup through a logical file
- returned business decision code (`A` or `D`)
- status-driven business rule extraction
- CLLE wrapper as the entry trigger

## What Good Output Should Notice

- `CRDTCMD` is a control wrapper, not the business rules owner
- `CREDITCHK` holds the key business decision
- inactive customers are denied even if credit exists
- approved amount is capped to available credit
- the logical file shapes the effective read path
- SQLCODE / not-found handling affects decision outcomes

## Suggested Next Fixture

Add a sibling blocked scenario next:

- same business domain
- missing LF or conflicting SME note
- expected result: inventory or program-analysis should stop and record a
  blocking gap instead of inventing behavior
