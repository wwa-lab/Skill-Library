# Skill Authoring Guide

Skills are compact operating instructions for OpenCode. They should teach the agent how to perform a specific internal workflow without loading unnecessary context.

## Required Shape

```text
skills/<domain>/<skill-name>/
  SKILL.md
  references/
  scripts/
  assets/
  examples/
  tests/
```

Only `SKILL.md` is required. The other folders are optional, but the template includes them so authors know where supporting material belongs.

## SKILL.md

Every skill starts with YAML frontmatter:

```yaml
---
name: java-spring-boot-api-review
description: Use when reviewing Java Spring Boot REST APIs for correctness, validation, error handling, observability, and test coverage.
---
```

The body should include only the core workflow:

- What the skill is for.
- When to use it.
- The sequence of steps to follow.
- What files or references to read when needed.
- What verification should be performed.

Keep the body concise. If a section becomes long, move it to `references/` and link to it from `SKILL.md`.

## Progressive Disclosure

Use three levels of context:

1. Frontmatter: short trigger metadata.
2. `SKILL.md`: the essential workflow.
3. Resources: detailed material loaded only when relevant.

This keeps common agent sessions fast and focused.

## Resource Folders

Use `references/` for detailed domain knowledge, API notes, examples, schemas, checklists, and long procedures.

Use `scripts/` for deterministic helpers, validators, converters, or repeatable automation that should not be rewritten each time.

Use `assets/` for templates, sample files, images, or other resources the skill uses as input or output material.

Use `examples/` for representative inputs and outputs that show the skill's expected behavior.

Use `tests/` for harnesses that validate deterministic or fragile generation behavior. This is most useful for mature skills that generate code, DDS, SQL, or other structured artifacts.

## Good Skill Boundaries

A good skill has one clear job. Prefer:

```text
ibm-i-rpg-business-rule-extraction
java-maven-build-debugging
common-technical-design-review
```

Avoid broad catch-all skills:

```text
java-helper
ibm-i-all
engineering
```

## Author Checklist

- The skill name matches `<domain>-<skill-name>`.
- The description says when to use the skill.
- The body gives a concrete workflow.
- Long background material is in `references/`.
- Scripts are executable or clearly documented.
- `node scripts/validate-skills.mjs` passes.
