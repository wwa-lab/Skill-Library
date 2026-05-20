# Getting Started With OpenCode

Use this guide when you want to start using the shared skill library quickly.

## 10-Minute Path

Choose one installation path:

- Script install: fastest when Node is available.
- Manual copy: use when you do not want to run Node.

### Option A: Script Install

1. Preview what will be installed:

   ```bash
   node scripts/install-opencode-skills.mjs --dry-run
   ```

2. Install the shared skills into OpenCode:

   ```bash
   node scripts/install-opencode-skills.mjs
   ```

### Option B: Manual Copy

OpenCode reads skills from:

```text
~/.config/opencode/skills
```

Copy each skill folder there using the `name` field in `SKILL.md` as the
destination folder name.

Examples:

```text
skills/ibm-i-skill-family/ibm-i-code-generator/ -> ~/.config/opencode/skills/ibm-i-code-generator/
skills/legacy-spec-factory/legacy-spec-writer/ -> ~/.config/opencode/skills/legacy-spec-writer/
```

For detailed manual-copy steps and copy-ready folder examples, open the local
browser guide from the repo root:

```bash
open docs/index.html
```

The Markdown source is `docs/manual-copy-opencode.md`.

### Start Using Skills

1. Pick the right starting skill:

   - Not sure which skill to use: open `docs/index.html` and use the Choose A Skill section.
   - IBM i forward delivery work: start with `ibm-i-workflow-orchestrator`.
   - Legacy reverse-modernization work: start with `legacy-modernization-orchestrator`.

2. Ask OpenCode directly with the skill name and your artifact.

## Recommended First Prompts

For IBM i forward delivery:

```text
Use ibm-i-workflow-orchestrator.
I have this requirement/change request and need help choosing the next skill.
```

For legacy reverse engineering:

```text
Use legacy-modernization-orchestrator.
I have IBM i / AS400 source, DDS, job logs, or SME notes and need to understand the system.
```

For messy business input:

```text
Use ibm-i-requirement-normalizer.
Please normalize this email/ticket/note into a structured requirement package.
```

For a known approved spec:

```text
Use ibm-i-program-spec.
Please turn this approved technical design into an implementation-ready Program Spec.
```

## Install Only One Family

IBM i delivery skills:

```bash
node scripts/install-opencode-skills.mjs --domain ibm-i
```

Legacy Spec Factory skills:

```bash
node scripts/install-opencode-skills.mjs --domain legacy-spec-factory
```

## What Gets Installed

OpenCode receives flat skill folders under:

```text
~/.config/opencode/skills
```

Examples:

```text
ibm-i-code-generator
ibm-i-workflow-orchestrator
legacy-ibmi-inventory
legacy-modernization-orchestrator
legacy-spec-writer
```

## If You Are Stuck

Use an orchestrator skill instead of guessing:

```text
Use ibm-i-workflow-orchestrator.
Here is what I have. Tell me the next best skill and what input it needs.
```

```text
Use legacy-modernization-orchestrator.
Here is my current legacy modernization artifact. Tell me where I am in the pipeline.
```
