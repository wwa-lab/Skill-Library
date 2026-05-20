# IBM i Skill Family

![IBM i Skill Family overview](../../docs/assets/ibm-i-skill-family-overview.svg)

This family contains the internal IBM i skills migrated from `wwa-lab/build-agent-skill` at source commit `479a427`.
The original Apache-2.0 license is retained in `skills/ibm-i-skill-family/LICENSE`.

It supports IBM i (AS/400, iSeries) enterprise delivery across requirement intake, RPGLE/CLLE program analysis, specification, DDS, source generation, review, unit test planning, and executable SQL/CL test scaffold generation.

This family is copy-ready for OpenCode: each real skill folder name matches the
`name` field in `SKILL.md`, so a teammate can copy a folder such as
`ibm-i-code-generator/` directly into `~/.config/opencode/skills/`.

## Chain

```text
Raw Input -> Requirement Normalizer -> Functional Spec -> Technical Design
                                           |                  |
Existing Source -> Program Analyzer -> Impact Analyzer        |
                         (+ CR)                              |
                                                              +-> Program Spec -> Code Generator -> Compile Precheck -> Code Reviewer
                                                              |
                                                              +-> File Spec -> DDS Generator -> DDS Reviewer

Any spec or CR -> UT Plan Generator -> Test Scaffold
Any stage      -> Workflow Orchestrator
```

## Skills

| Skill | Path | Purpose |
|-------|------|---------|
| `ibm-i-requirement-normalizer` | `ibm-i-requirement-normalizer/` | Normalize messy business or technical input into a structured requirement package. |
| `ibm-i-program-analyzer` | `ibm-i-program-analyzer/` | Analyze existing RPGLE/CLLE source for comprehension, flow, interfaces, I/O, and dependencies. |
| `ibm-i-impact-analyzer` | `ibm-i-impact-analyzer/` | Analyze existing source plus a change request to produce impact, risk, and handoff guidance. |
| `ibm-i-functional-spec` | `ibm-i-functional-spec/` | Generate business-functional specifications from requirements or change requests. |
| `ibm-i-technical-design` | `ibm-i-technical-design/` | Generate technical design documents with module allocation, processing flow, object interaction, and impact. |
| `ibm-i-program-spec` | `ibm-i-program-spec/` | Generate implementation-ready Program Specs for RPGLE and CLLE work. |
| `ibm-i-file-spec` | `ibm-i-file-spec/` | Generate DDS-focused File Specs for PF, LF, PRTF, and DSPF objects. |
| `ibm-i-code-generator` | `ibm-i-code-generator/` | Generate RPGLE or CLLE source from an approved Program Spec. |
| `ibm-i-dds-generator` | `ibm-i-dds-generator/` | Generate DDS source from File Spec JSON contracts. |
| `ibm-i-ut-plan-generator` | `ibm-i-ut-plan-generator/` | Generate developer-level unit test plans from specs, CRs, or raw inputs. |
| `ibm-i-test-scaffold` | `ibm-i-test-scaffold/` | Generate executable SQL/CL scripts for setup, compile, execution, verification, and cleanup. |
| `ibm-i-compile-precheck` | `ibm-i-compile-precheck/` | Review RPGLE/CLLE source for compile-safety issues before transport or compile. |
| `ibm-i-spec-reviewer` | `ibm-i-spec-reviewer/` | Review IBM i specs for layer boundary, completeness, traceability, and downstream readiness. |
| `ibm-i-dds-reviewer` | `ibm-i-dds-reviewer/` | Review DDS source against File Specs for correctness, syntax, completeness, and type-specific rules. |
| `ibm-i-code-reviewer` | `ibm-i-code-reviewer/` | Review RPGLE/CLLE source against Program Specs for correctness and enhancement safety. |
| `ibm-i-workflow-orchestrator` | `ibm-i-workflow-orchestrator/` | Route work to the right skill, plan batch `task.md` runs, and execute approved batches. |

## Pending Internal Pilot Imports

These placeholders reserve final paths for internal pilot skills that are not in the public source repo yet. They intentionally do not contain `SKILL.md`, so validation and installation skip them until the internal skill content is copied in.

| Future Skill | Author | Placeholder Path | Notes |
|--------------|--------|------------------|-------|
| `ibm-i-requirement-intake` | Oliver | `ibm-i-requirement-intake/` | Internal legacy name: `as400-requirment-intake`; use corrected spelling and IBM i namespace on import. |
| `ibm-i-ut-plan-to-xml` | Kevin | `ibm-i-ut-plan-to-xml/` | Converts IBM i UT Plan artifacts into XML once internal pilot content is imported. |

## Design Principles

- Layer boundary discipline: each skill stays in its document or artifact layer.
- BR-xx continuity: business rule IDs carry through requirement, spec, design, code, and review.
- Enhancement-first: skills support real IBM i BAU change work, not only greenfield delivery.
- Anti-hallucination: unknown object names, rules, and system details must remain explicit TBDs.
- Tiered output: spec skills scale Lite, Standard, or Full based on change complexity.
- Review gates: specs, DDS, source code, and compile safety each have separate reviewers.

## Installation

Preview installation:

```bash
node scripts/install-opencode-skills.mjs --domain ibm-i --dry-run
```

Install into OpenCode:

```bash
node scripts/install-opencode-skills.mjs --domain ibm-i
```
