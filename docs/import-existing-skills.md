# Importing Existing Skills

Use this process when a team already has a stable skill or skill family and wants to bring it into this repository.

## Import Steps

1. Identify every source skill directory that contains a `SKILL.md`.
2. Choose the target domain, such as `common`, `ibm-i`, or `java`.
3. Copy each skill into `skills/<domain>/<short-skill-name>/`.
4. Keep the frontmatter `name` as `<domain>-<short-skill-name>`.
5. Preserve useful `references/`, `scripts/`, `assets/`, `examples/`, and `tests/`.
6. Remove local noise such as `.DS_Store`, temporary files, and stale `tests/results/*` output.
7. Add `license` and `metadata` to every imported `SKILL.md`.
8. Keep source-family license files beside the imported family when relevant.
9. Run validation and install dry-run.
10. Commit the import separately from unrelated framework or tooling changes.

## Path Mapping

The repository is domain-first, while OpenCode installs skills into a flat directory.

Example:

```text
source repo:
.claude/ibm-i-code-generator/SKILL.md

this repo:
skills/ibm-i/code-generator/SKILL.md

installed into OpenCode:
~/.config/opencode/skills/ibm-i-code-generator/SKILL.md
```

The `name` field should match the installed OpenCode folder:

```yaml
---
name: ibm-i-code-generator
description: >
  Generates controlled IBM i RPGLE or CLLE source code from an approved Program Spec.
  Use this skill whenever a user provides an IBM i Program Spec and asks to implement it.
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/build-agent-skill
  source_commit: 479a427
  domain: ibm-i
---
```

## Verification

Run:

```bash
node scripts/validate-skills.mjs
node scripts/install-opencode-skills.mjs --domain <domain> --dry-run
```

For a safer install check, install into a temporary directory:

```bash
node scripts/install-opencode-skills.mjs \
  --domain <domain> \
  --dest /private/tmp/opencode-skills-import-test
```

If the imported skills include harnesses, run dry-run or list modes when available before executing model-backed tests.

## Using Placeholders

For internal pilot skills that are known but not ready to import, create the final target directory with a `README.md` only. Do not add `SKILL.md` until the real skill content is ready.

Example:

```text
skills/ibm-i/requirement-intake/README.md
skills/ibm-i/ut-plan-to-xml/README.md
```

This reserves the destination path without making the installer publish an incomplete skill. When the internal skill is ready, copy in `SKILL.md`, add resources, remove any obsolete placeholder notes, and run validation.

## Commit Shape

Prefer separate commits:

```text
chore: update skill import docs
feat: import <domain> skill family
```

For large imports, keep generated result files out of git. Test cases and runners are useful; stale reports are usually not.
