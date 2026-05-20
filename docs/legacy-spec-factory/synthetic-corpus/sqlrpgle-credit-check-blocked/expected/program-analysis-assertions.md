# Expected Program Analysis Assertions

Program analysis should be able to describe visible source structure, but it
must remain **blocked for approved interpretation**.

## What The Analysis Can State

- fixed-format `SQLRPGLE`
- embedded SQL references `CREDITVW`
- source includes a distinct `Status = 'H'` branch
- deny-style outcomes are returned for missing, hold, inactive, or over-limit
  paths

## What The Analysis Must Not State As Approved Fact

- how `AVAIL_CREDIT` is derived without `CREDITVW.LF`
- the business meaning of `Status = 'H'` without SME confirmation
- whether hold means compliance, collections, or manual review

## Gate Expectation

- emit blocking TBDs instead of producing an approved business rule set
