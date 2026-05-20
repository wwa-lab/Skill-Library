# Naming Conventions

This repository uses domain-first naming.

## Domains

Domains live under `skills/`:

```text
skills/common/
skills/ibm-i/
skills/java/
```

Domain names must be lowercase kebab-case:

```text
ibm-i
java
common
```

## Skill Directories

Skill directories must be lowercase kebab-case:

```text
skills/java/spring-boot-api-review/
skills/ibm-i/rpg-modernization/
```

Internal example or fixture directories may start with `_`:

```text
skills/common/_example/
```

The installer skips underscore-prefixed skill directories by default.

## Frontmatter Names

By default, the `name` in `SKILL.md` must be:

```text
<domain>-<skill-directory-name>
```

For underscore-prefixed example directories, remove the leading underscore:

```text
skills/common/_example/ -> common-example
```

Examples:

```yaml
name: common-example
name: ibm-i-rpg-modernization
name: java-spring-boot-api-review
```

## Preserved Skill Names

Some imported skill families already use stable, globally namespaced skill names.
For those domains, add `skills/<domain>/domain.json`:

```json
{
  "nameStrategy": "preserve"
}
```

With `preserve`, the `name` in `SKILL.md` must match the skill directory name:

```text
skills/legacy-spec-factory/legacy-spec-writer/ -> legacy-spec-writer
```

Use this only for mature imported families whose existing names are already clear
in a flat OpenCode runtime. New internal domains should use the default
domain-prefixed strategy.

## Descriptions

Descriptions should explain trigger conditions, not marketing value.

Prefer:

```yaml
description: Use when debugging Maven or Gradle build failures in Java projects, especially dependency conflicts, plugin errors, test failures, or CI-only build issues.
```

Avoid:

```yaml
description: A powerful Java helper skill.
```
