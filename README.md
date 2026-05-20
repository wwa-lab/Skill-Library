# Internal OpenCode Skills Library

This repository manages reusable OpenCode skills for internal engineering work.

The library is intentionally simple:

- Skills are grouped by domain in this repository.
- Skills are installed into OpenCode as flat, namespaced folders.
- The repository manages skills only, not agents or commands.

## Repository Layout

```text
skills/
  common/       Shared skills that apply across domains
  ibm-i/        IBM i skill family for requirements, specs, DDS, code, review, and tests
  java/         Java, Spring, Maven, Gradle, JVM, and testing skills
templates/
  skill/        Starter template for new skills
docs/           Authoring, naming, and installation guidance
scripts/        Validation and OpenCode installation utilities
```

## Included Skill Families

### IBM i

The IBM i family was migrated from `wwa-lab/build-agent-skill` after stabilization. It contains 16 skills covering the full IBM i delivery chain:

- Requirement intake and normalization.
- Existing RPGLE/CLLE source analysis.
- Impact analysis for enhancement work.
- Functional specs, technical designs, program specs, and file specs.
- RPGLE/CLLE and DDS generation.
- Spec, DDS, code, and compile-safety review.
- Unit test planning and executable SQL/CL test scaffold generation.
- Workflow orchestration for routing and batch `task.md` execution.

See `skills/ibm-i/README.md` for the full map.

## Quick Start

Validate the library:

```bash
node scripts/validate-skills.mjs
```

Preview OpenCode installation:

```bash
node scripts/install-opencode-skills.mjs --dry-run --include-examples
```

Install all real skills into the default OpenCode skills directory:

```bash
node scripts/install-opencode-skills.mjs
```

Install only one domain:

```bash
node scripts/install-opencode-skills.mjs --domain java
```

Install the IBM i family:

```bash
node scripts/install-opencode-skills.mjs --domain ibm-i
```

The default destination is:

```text
~/.config/opencode/skills
```

Use `--dest <path>` to install elsewhere.

## Creating a Skill

1. Copy `templates/skill` into `skills/<domain>/<skill-name>`.
2. Update `SKILL.md` frontmatter.
3. Keep the `name` field in the form `<domain>-<skill-name>`.
4. Put long details in `references/`, deterministic helpers in `scripts/`, reusable files in `assets/`, samples in `examples/`, and fragile behavior checks in `tests/`.
5. Run `node scripts/validate-skills.mjs`.

Example:

```text
skills/ibm-i/rpg-modernization/SKILL.md
```

```yaml
---
name: ibm-i-rpg-modernization
description: Use when modernizing IBM i RPG applications, analyzing RPG code, extracting business rules, or planning RPG refactors.
---
```

## Docs

- `docs/skill-authoring.md`
- `docs/import-existing-skills.md`
- `docs/naming-conventions.md`
- `docs/opencode-installation.md`
