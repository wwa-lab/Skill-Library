# Synthetic Legacy Corpus

This folder holds **synthetic IBM i modernization test fixtures** for Legacy
Spec Factory.

The goal is not to mimic one customer's codebase line-for-line. The goal is to
create a reusable, non-sensitive corpus that exercises the repository's
critical skills against the patterns we expect in real pilot work:

- mostly **fixed-format** RPG / SQLRPGLE
- some **free-format** RPGLE
- CLLE wrappers and submitted-job control flow
- DDS PF/LF, DSPF, and PRTF assets
- runtime evidence such as job logs, spool samples, and sample transactions
- SME notes that confirm or reject inferred business meaning

## Why This Exists

External pilot work is limited by code access and redaction constraints. A
synthetic corpus lets the team:

- test the end-to-end reverse-modernization chain without customer data
- reproduce regressions in a stable fixture set
- compare runtime behavior across Codex, Claude Code, and OpenCode
- demonstrate the methodology to internal stakeholders
- harden anti-hallucination and blocking-gate behavior

## Design Principles

- **Reality-shaped, not toy-shaped**: use idioms common in IBM i shops,
  especially fixed-format SQLRPGLE.
- **Small but complete**: each fixture should be narrow enough to understand in
  one sitting, but complete enough to drive multiple downstream skills.
- **Gate-aware**: every positive fixture should have a sibling negative or
  blocked scenario.
- **Traceable**: each fixture should say which skills it is meant to test and
  what successful output should contain.
- **Portable**: fixtures are plain repository files, not tied to one runtime.

## Recommended Fixture Mix

Start with these four families:

1. `sqlrpgle-credit-check-happy`
   Fixed-format SQLRPGLE happy path with PF/LF, CLLE wrapper, runtime evidence,
   and clear SME rule confirmation.
2. `sqlrpgle-credit-check-blocked`
   Same domain, but with missing DDS or conflicting evidence so the chain must
   stop cleanly.
3. `batch-ar-reconciliation`
   Submitted-job / report-heavy flow with spool and joblog evidence.
4. `screen-subfile-inquiry`
   DSPF + subfile + F-key navigation for inquiry screens.

## Coverage Goals

For the current repository, the highest-value synthetic coverage is:

- `legacy-modernization-orchestrator`
- `legacy-ibmi-evidence-intake`
- `legacy-ibmi-inventory`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-flow-analyzer`
- `legacy-ibmi-module-analyzer`
- `legacy-spec-writer`

That is the main path we most need to harden.

## Fixture Contract

Each fixture should include some or all of:

```text
<fixture-name>/
  README.md
  source/
  dds/
  runtime/
  sme/
  expected/
```

Where:

- `source/` contains RPGLE, SQLRPGLE, CLLE, COBOL, or SQL snippets
- `dds/` contains PF/LF/DSPF/PRTF members when relevant
- `runtime/` contains job logs, spool samples, or sample transactions
- `sme/` contains simulated SME confirmations or open questions
- `expected/` contains compact assertions or exemplar outputs for downstream
  skills

## Current Fixtures

The current starter set is:

- [`sqlrpgle-credit-check-happy`](sqlrpgle-credit-check-happy/README.md)
- [`sqlrpgle-credit-check-blocked`](sqlrpgle-credit-check-blocked/README.md)
- [`batch-ar-reconciliation`](batch-ar-reconciliation/README.md)
- [`screen-subfile-inquiry`](screen-subfile-inquiry/README.md)

Together, these fixtures cover fixed-format `SQLRPGLE`, blocked-source
behavior, batch/runtime evidence, and DSPF subfile inquiry screens.

## How To Run A Pilot

Use [`pilot-execution-checklist.md`](pilot-execution-checklist.md) to run a
consistent internal pilot across the current synthetic fixtures.
Use [`pilot-results-template.md`](pilot-results-template.md) to record results
in a consistent format.
Use [`pilot-prompts.md`](pilot-prompts.md) for copy-paste prompts in the first
pilot round.

If your environment only permits **OpenCode**, this synthetic pilot still
works. Treat the current materials as OpenCode-first and use them to validate
skill triggering, gate discipline, and output shape in that one runtime.
