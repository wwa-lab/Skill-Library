# Skill-Library Agent Instructions

This repository is the internal source of truth for OpenCode skills.

## Scope

- Manage skills only. Do not add agents, commands, hooks, or platform adapters unless the user explicitly asks for them.
- Keep the repository OpenCode-first.
- Organize skills by domain under `skills/<domain>/<skill>/`.
- Install skills into OpenCode as flat, namespaced folders such as `ibm-i-rpg-modernization`.

## Repository Shape

```text
skills/
  common/
  ibm-i/
  java/
templates/
  skill/
docs/
scripts/
```

Each skill must have a `SKILL.md`. Optional skill resources live beside it:

```text
SKILL.md
references/
scripts/
assets/
examples/
tests/
```

## Skill Authoring Rules

- Use lowercase kebab-case for domains and skill directories.
- The skill frontmatter `name` must match `<domain>-<skill-name>`.
- Directories prefixed with `_`, such as `_example`, are internal examples and skipped by the installer unless requested.
- Keep `SKILL.md` concise. Move long reference material into `references/`.
- Add scripts only when deterministic execution is better than prose instructions.
- Preserve `examples/` and `tests/` for mature imported skills when they document expected outputs or validate fragile generation behavior.
- Avoid broad skills. Each skill should have one clear job and clear trigger conditions.

## Verification

Run this before finishing changes:

```bash
node scripts/validate-skills.mjs
```

If install behavior changed, also run:

```bash
node scripts/install-opencode-skills.mjs --dry-run --include-examples
```
