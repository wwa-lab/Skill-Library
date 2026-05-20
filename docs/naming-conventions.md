# Naming Conventions

This repository uses family-first layout with copy-ready skill folders.

## Families

Families live under `skills/`:

```text
skills/common/
skills/ibm-i-skill-family/
skills/java/
skills/legacy-spec-factory/
```

Family folder names must be lowercase kebab-case:

```text
ibm-i-skill-family
java
common
```

## Skill Directories

Skill directories must be lowercase kebab-case:

```text
skills/java/spring-boot-api-review/
skills/ibm-i-skill-family/ibm-i-rpg-modernization/
```

Prefer copy-ready skill directory names: the folder containing `SKILL.md`
should usually match the `name` field so a teammate can copy the folder directly
into OpenCode.

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
  "metadataDomain": "ibm-i",
  "nameStrategy": "preserve"
}
```

With `preserve`, the `name` in `SKILL.md` must match the skill directory name.
Use this for copy-ready family folders:

```text
skills/ibm-i-skill-family/ibm-i-code-generator/ -> ibm-i-code-generator
skills/legacy-spec-factory/legacy-spec-writer/ -> legacy-spec-writer
```

Use this only for mature imported families whose existing names are already clear
in a flat OpenCode runtime.

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
