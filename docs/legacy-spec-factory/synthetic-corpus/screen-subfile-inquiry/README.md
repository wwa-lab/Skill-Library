# Screen Subfile Inquiry Happy Path

A compact **synthetic interactive-screen fixture** centered on a DSPF subfile
inquiry flow.

## Scenario

Customer service opens a customer inquiry function from a menu, enters a
customer number, and views recent transactions in a paged subfile list.

This fixture emphasizes:

- DSPF screen structure
- subfile control and paging
- function-key navigation
- inquiry-only interaction instead of update-heavy maintenance logic

## Why This Fixture Exists

Many IBM i systems encode important business workflows in green-screen inquiry
surfaces:

- menus define entry context
- DSPF field conditioning reveals operational state
- subfiles expose list semantics and user navigation patterns
- function keys imply downstream branching

That makes a screen-first fixture useful even before full program or module
artifacts exist.

## Included Assets

```text
screen-subfile-inquiry/
  README.md
  source/
    CUSTMENU.MENU.txt
    CUSTINQDSP.DSPF
    CUSTINQ.SQLRPGLE
  runtime/
    sample-screen-notes.md
    sample-joblog.txt
  sme/
    sme-notes.md
  expected/
    screen-analysis-assertions.md
    flow-assertions.md
```

## Intended Skill Coverage

- `legacy-modernization-orchestrator`
- `legacy-ibmi-evidence-intake`
- `legacy-ibmi-inventory`
- `legacy-ibmi-screen-report-analyzer`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-flow-analyzer`

Secondarily, it can support:

- `legacy-ibmi-module-analyzer`
- `legacy-spec-writer`

## Expected Reverse-Engineering Themes

- menu-driven trigger model
- inquiry screen with header plus subfile region
- option field or selection field semantics
- F5 refresh, F12 return, Enter/detail navigation
- display-only business information vs actionable maintenance behavior

## What Good Output Should Notice

- the surface is inquiry-oriented, not order-entry or maintenance-first
- the subfile is a transaction-history presentation surface
- function keys are part of operational navigation
- program logic is needed to confirm some option semantics, but screen intent is
  still strongly visible from DSPF and runtime evidence
