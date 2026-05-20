# Skill Selection Guide

Use this guide to quickly choose the right skill for the artifact or question in
front of you.

## Fastest Rule

If you do not know which skill to use, start with an orchestrator:

| Situation | Start With |
|-----------|------------|
| IBM i forward delivery from requirement to code/test | `ibm-i-workflow-orchestrator` |
| Legacy reverse-modernization from old system evidence to specs | `legacy-modernization-orchestrator` |

## IBM i Forward Delivery

Use these skills when the team already has a requirement, change request, spec,
or implementation task and needs to move forward through the delivery chain.

| You Have | Start With | Output Direction |
|----------|------------|------------------|
| Messy email, ticket, notes, or unclear requirement | `ibm-i-requirement-normalizer` | Structured requirement package |
| Requirement or change request | `ibm-i-functional-spec` | Business-functional spec |
| Functional spec or approved requirement | `ibm-i-technical-design` | Technical design |
| Technical design for RPGLE/CLLE work | `ibm-i-program-spec` | Implementation-ready Program Spec |
| Technical design for PF/LF/PRTF/DSPF work | `ibm-i-file-spec` | DDS-focused File Spec |
| Approved Program Spec | `ibm-i-code-generator` | RPGLE/CLLE source |
| Approved File Spec | `ibm-i-dds-generator` | DDS source |
| Generated or changed RPGLE/CLLE source | `ibm-i-compile-precheck` | Compile-safety findings |
| Source plus spec alignment review | `ibm-i-code-reviewer` | Code review report |
| Spec quality gate | `ibm-i-spec-reviewer` | Spec review report |
| DDS quality gate | `ibm-i-dds-reviewer` | DDS review report |
| Requirement, CR, or spec needing developer tests | `ibm-i-ut-plan-generator` | Unit test plan |
| UT plan needing executable setup/run/check scripts | `ibm-i-test-scaffold` | SQL/CL test scaffold |
| Existing RPGLE/CLLE source to understand | `ibm-i-program-analyzer` | Source analysis |
| Existing source plus change request | `ibm-i-impact-analyzer` | Impact/risk analysis |

## Legacy Reverse-Modernization

Use these skills when the team is trying to understand an existing IBM i /
AS400 system and turn legacy behavior into evidence-backed specs.

| You Have | Start With | Output Direction |
|----------|------------|------------------|
| Raw IBM i / AS400 source, DDS, logs, reports, screens, or SME notes | `legacy-modernization-orchestrator` | Routing decision and next step |
| Unclassified evidence or unclear authorization/redaction state | `legacy-ibmi-evidence-intake` | Evidence manifest and redaction log |
| Approved evidence bundle | `legacy-ibmi-inventory` | Inventory and object map |
| One RPGLE, CLLE, or COBOL program | `legacy-ibmi-program-analyzer` | Program analysis |
| One business transaction across programs | `legacy-ibmi-flow-analyzer` | Flow analysis |
| Multiple flows in one business module | `legacy-ibmi-module-analyzer` | Module-level four-view analysis |
| DDS / DB2 metadata needing data model recovery | `legacy-ibmi-data-model-analyzer` | Data dictionary, access paths, CRUD matrix |
| DSPF, PRTF, screens, subfiles, menus, or spool samples | `legacy-ibmi-screen-report-analyzer` | Screen/report analysis |
| Approved job logs or spool/report files | `legacy-ibmi-runtime-evidence-miner` | Runtime evidence observations |
| Many program analyses needing SME review | `legacy-ibmi-batch-digest` | SME-friendly digest |
| Approved module analysis needing business-facing docs | `legacy-brd-writer` | BRD |
| Approved analyses needing source-of-truth specs | `legacy-spec-writer` | `spec.yaml`, `spec.md`, traceability |
| Risky or large modernization choices | `legacy-modernization-decision-writer` | Decision records |
| Artifact needing SME validation | `legacy-sme-review-facilitator` | Review package, decisions, sign-off |
| Approved spec needing old-vs-new validation plan | `legacy-golden-master-test-planner` | Golden master test plan |
| Capability package needing traceability audit | `legacy-traceability-packager` | Traceability package |
| Approved BRD/spec moving to Atlas or forward SDLC | `legacy-brd-to-sdd-handoff` | SDD handoff package |
| Markdown artifacts needing stakeholder HTML | `legacy-html-exporter` | HTML companion files |
| Step output needing mechanical/semantic validation | `legacy-step-validator` | Validation report |
| Skill or artifact process needing shared quality contract | `legacy-step-contract` | Step contract guidance |
| Skill portability check across runtimes | `legacy-runtime-matrix-tester` | Runtime matrix findings |

## Choosing Between Similar Skills

`ibm-i-program-analyzer` vs `legacy-ibmi-program-analyzer`:

- Use `ibm-i-program-analyzer` when the goal is IBM i delivery impact,
  enhancement work, or forward-chain handoff.
- Use `legacy-ibmi-program-analyzer` when the goal is reverse-modernization,
  evidence-backed business recovery, and eventual `spec.yaml` generation.

`ibm-i-ut-plan-generator` vs `legacy-golden-master-test-planner`:

- Use `ibm-i-ut-plan-generator` for developer-level unit test planning.
- Use `legacy-golden-master-test-planner` for old-vs-new behavior equivalence
  planning after reverse-modernization specs are approved.

`ibm-i-functional-spec` vs `legacy-spec-writer`:

- Use `ibm-i-functional-spec` when starting from a requirement/change request.
- Use `legacy-spec-writer` when starting from approved reverse-engineering
  analysis and producing an evidence-backed capability spec.
