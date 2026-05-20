# OpenCode Installation

This repository stores skills by domain. OpenCode reads skills from a flat skills directory.

The install script maps:

```text
skills/java/spring-boot-api-review/
```

to:

```text
~/.config/opencode/skills/java-spring-boot-api-review/
```

The installed name comes from the `name` field in `SKILL.md`.

## Validate First

```bash
node scripts/validate-skills.mjs
```

## Preview Installation

```bash
node scripts/install-opencode-skills.mjs --dry-run --include-examples
```

## Install All Real Skills

```bash
node scripts/install-opencode-skills.mjs
```

Directories that start with `_` are skipped by default.

## Manual Copy Without Node

You can also copy skills manually. OpenCode only needs each skill folder under
the flat runtime directory:

```text
~/.config/opencode/skills/<skill-name>/
```

The `<skill-name>` must match the `name` field in `SKILL.md`.

Examples:

```text
skills/ibm-i-skill-family/ibm-i-code-generator/ -> ~/.config/opencode/skills/ibm-i-code-generator/
skills/legacy-spec-factory/legacy-spec-writer/ -> ~/.config/opencode/skills/legacy-spec-writer/
```

See `docs/manual-copy-opencode.md` for the full manual-copy guide and
copy-ready folder examples.

## Install One Family Or Domain Alias

```bash
node scripts/install-opencode-skills.mjs --domain java
```

Install the IBM i skill family:

```bash
node scripts/install-opencode-skills.mjs --domain ibm-i
```

`ibm-i` is an alias for the copy-ready family folder
`skills/ibm-i-skill-family/`.

You can pass `--domain` multiple times:

```bash
node scripts/install-opencode-skills.mjs --domain common --domain ibm-i
```

## Custom Destination

```bash
node scripts/install-opencode-skills.mjs --dest /tmp/opencode-skills
```

## Existing Destination Folders

The installer writes a `.skill-library-source.json` marker into each installed skill folder.

If a destination skill folder already exists and has this marker, the installer may replace it.

If a destination skill folder exists without this marker, the installer refuses to overwrite it unless `--force` is used.

Use `--force` carefully:

```bash
node scripts/install-opencode-skills.mjs --domain java --force
```
