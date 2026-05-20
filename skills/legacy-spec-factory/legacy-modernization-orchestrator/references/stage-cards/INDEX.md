# Stage Cards Index

One card per pipeline stage. Each card is a single-screen cheat sheet that
tells a first-time user exactly **what to have, what to run, what file to
save, and where to go next**. Cards are deterministic — they do not require
LLM judgement to follow.

The orchestrator should attach the card matching the user's current stage
(from `references/stage-identification.md`) at the end of every routing
decision via the **Quick Card** block in `SKILL.md → Output Structure`.

## Linear Path (8 cards covering the happy path)

| Card | Stage IDs | Title | You arrive here when... |
| --- | --- | --- | --- |
| [00-evidence-intake](00-evidence-intake.md) | 0 | Evidence Intake | You have raw IBM i source / job logs / spool / DDS not yet redacted |
| [01-evidence-ready](01-evidence-ready.md) | 1 | Evidence Ready | All evidence redacted; `evidence-manifest.yaml` approved |
| [02-inventory](02-inventory.md) | 2a–2c | Inventory | You are building or have built `inventory.yaml` |
| [03-program-analysis](03-program-analysis.md) | 3a–3b | Program Analysis | Inventory approved; analyzing one program at a time |
| [04-flow-analysis](04-flow-analysis.md) | 3c–3d | Flow Analysis | Multiple programs analyzed; tracing one business transaction end-to-end |
| [05-module-analysis](05-module-analysis.md) | 3e–3f | Module Analysis | Several flows belong to the same module; need 4-view synthesis |
| [06-spec-writing](06-spec-writing.md) | 8a–8c | Spec Writing | Module approved; producing `spec.yaml` + `spec.md` per capability |
| [07-forward-handoff](07-forward-handoff.md) | 10 | Forward SDLC Handoff | Spec approved + equivalence pack ready; crossing to `build-agent-skill` |

## Optional / Parallel Cards

These do not block the linear path but strengthen evidence quality. The
orchestrator points to them when applicable.

| Skill | When to add | Card |
| --- | --- | --- |
| `legacy-ibmi-runtime-evidence-miner` | Job logs / spool / reports available alongside source | See SKILL.md (no dedicated card yet) |
| `legacy-ibmi-screen-report-analyzer` | DSPF / PRTF / subfile / menu samples available | See SKILL.md |
| `legacy-ibmi-data-model-analyzer` | Domain data model needed before spec-writing | See SKILL.md |
| `legacy-brd-writer` | Stakeholders want a business-facing BRD before spec | See SKILL.md |
| `legacy-modernization-decision-writer` | A modernization decision is large/risky enough to warrant a DEC-* package | See SKILL.md |

## Path Convention

All paths shown in cards are **relative to your project root**
(`docs/<project-name>/`, set by the orchestrator at Step 0.b). A card that
says "Save under `01_inventory/`" means
`docs/<your-project>/01_inventory/`. For project `XXX260004-demo`, that
resolves to `docs/XXX260004-demo/01_inventory/`. The orchestrator's Quick
Card always shows the fully-resolved path.

## How to Use a Card

1. The orchestrator identifies your current stage and points you to one card.
2. Open the card. Check `Need before starting` — you must have every listed file.
3. Run the named skill (or manual fallback if `Planned`).
4. Save the output exactly at the path under `Produce`.
5. Run the `Gate before advancing` check. If it fails, stay on this card.
6. Do the `SME action` if marked **Required**.
7. Move to the card listed under `Next card`.

If a card's `Need before starting` is not satisfied, **do not skip backward**
— ask the orchestrator to re-route you. Skipping a stage breaks traceability.
