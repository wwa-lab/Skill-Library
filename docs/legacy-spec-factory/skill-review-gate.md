# Skill Review Gate

This document defines the quality gate for skills generated for Legacy Spec
Factory.

Claude Code may generate or revise a skill. Codex reviews the skill before it
is accepted. A skill must score at least **9.0 / 10** to be merged into the
repository and at least **9.5 / 10** before it is used in an internal field
pilot.

## Gate Levels

| Score | Meaning | Decision |
| --- | --- | --- |
| 9.5-10.0 | Field-pilot ready | May be used with real SME / engineering users |
| 9.0-9.4 | Repo-ready but not field-ready | May be merged, but needs one more hardening pass before pilot |
| 8.0-8.9 | Promising draft | Return to Claude Code for revision |
| 7.0-7.9 | Structurally incomplete | Rewrite or split the skill |
| < 7.0 | Not acceptable | Restart from the skill brief |

## Mandatory Stop Conditions

Any of the following caps the score at **8.0**, even if the rest of the skill
looks good:

- no valid `SKILL.md`
- missing or weak `name` / `description` frontmatter
- no copyright / author notice
- not portable across Codex, Claude Code, and OpenCode
- runtime-specific assumptions are mixed into the canonical skill without an
  adapter strategy
- no clear trigger conditions
- no clear output contract
- no SME review or evidence governance where legacy IBM i understanding is
  involved
- hallucination-prone instructions that encourage inventing object names,
  business rules, interfaces, or source evidence

Any of the following caps the score at **9.0**:

- examples are missing or too generic
- references are useful but not linked clearly from `SKILL.md`
- validation steps are described but not enforceable
- portability has been considered but not tested in all target runtimes — see
  [docs/runtime-smoke-tests.md](runtime-smoke-tests.md) for the reusable
  protocol that lifts this cap
- review checklist exists but does not map to measurable outputs

## Scoring Rubric

Score each category from 0 to 10. The final score is the weighted average.

| Category | Weight | What Good Looks Like |
| --- | ---: | --- |
| Purpose and trigger clarity | 10% | The description makes it obvious when the skill should and should not activate |
| Workflow completeness | 12% | The skill gives a complete, ordered procedure with clear inputs, outputs, and stop points |
| IBM i / domain correctness | 14% | The skill respects RPGLE, CLLE, DDS, DB2 for i, PRTF, DSPF, jobs, and SME realities |
| Evidence and anti-hallucination | 12% | The skill requires evidence tags, confidence levels, TBD handling, and no invented facts |
| Output contract | 10% | The generated artifact shape is structured, stable-ID based, and downstream-agent friendly |
| Progressive disclosure | 8% | `SKILL.md` stays lean; references, templates, and scripts are loaded only when needed |
| Runtime portability | 10% | The skill can run in Codex, Claude Code, and OpenCode with a canonical source plus adapters |
| Reviewability and testability | 10% | The skill includes review gates, acceptance checks, examples, and negative cases |
| Engineering handoff value | 8% | Outputs are specific enough for developers, SMEs, and automation to use with minimal rework |
| Maintainability | 6% | Versioning, authorship, references, and file layout are clean and easy to evolve |

## Review Protocol

1. **Structural pass**
   Confirm the skill folder contains only necessary files:

   ```text
   SKILL.md
   references/
   templates/
   scripts/
   assets/
   agents/openai.yaml
   ```

   Do not accept skill-local `README.md`, `INSTALLATION_GUIDE.md`,
   `CHANGELOG.md`, or other clutter unless there is a specific runtime reason.

2. **Frontmatter pass**
   Check `name`, `description`, and any metadata. The description must include
   both what the skill does and when to use it.

3. **Workflow pass**
   Verify the skill gives an executable procedure, not just principles.

4. **SME pass**
   For IBM i reverse-engineering skills, check whether an IBM i SME could use
   the instructions to reject bad output. The skill must make room for SME
   judgment instead of treating model output as truth.

5. **Portability pass**
   Check that the canonical source lives under `skills/<skill-name>/` and that
   runtime copies or adapters are treated as derived artifacts.

6. **Artifact contract pass**
   Verify the skill defines the shape of its output, required IDs, evidence
   fields, review status, and handoff conditions.

7. **Adversarial pass**
   Ask how the skill behaves with incomplete source, missing DDS, contradictory
   evidence, unknown subroutines, weak business context, and runtime-specific
   folder differences.

8. **Score and disposition**
   Fill in `templates/skill-review-scorecard.md`. If the score is below 9.0,
   return revision instructions to Claude Code. If the score is between 9.0 and
   9.4, allow repo integration but block field pilot. If the score is 9.5 or
   higher, mark it field-pilot ready.

## Iteration Contract

Claude Code and Codex should iterate until the target score is reached.

Each iteration must include:

- skill version or revision ID
- reviewer score
- top three defects blocking the next score band
- exact requested changes
- whether the issue affects portability, SME correctness, evidence integrity,
  or downstream automation

Do not approve a skill because it "sounds good." Approve it because the workflow
is executable, auditable, portable, and strong enough for SME-led modernization.

