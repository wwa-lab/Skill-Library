# Manual Copy Into OpenCode

Use this guide when you do not want to run the Node installer.

OpenCode reads skills from a flat folder:

```text
~/.config/opencode/skills
```

Each installed skill folder name must match the `name` field in that skill's
`SKILL.md`.

## Manual Copy Rules

1. Create the OpenCode skills folder if it does not exist.
2. Pick a source skill folder that contains `SKILL.md`.
3. Copy the whole folder into `~/.config/opencode/skills/<skill-name>/`.
4. Use the `name` field from `SKILL.md` as `<skill-name>`.
5. Skip placeholder folders that only have `README.md`.
6. Skip `_example` unless you intentionally want example skills installed.

Create the destination folder:

```bash
mkdir -p ~/.config/opencode/skills
```

## Finder Copy

For one skill:

1. Open the source folder, for example `skills/ibm-i-skill-family/ibm-i-code-generator/`.
2. Open `SKILL.md` and read the frontmatter `name`.
3. Copy the whole source folder to `~/.config/opencode/skills/`.
4. Rename the copied folder to the `name`, for example
   `ibm-i-code-generator`.

For a clean replacement, delete or archive the old destination folder first.

## Terminal Copy Without Node

Copy one IBM i skill:

```bash
mkdir -p ~/.config/opencode/skills/ibm-i-code-generator
cp -R skills/ibm-i-skill-family/ibm-i-code-generator/. ~/.config/opencode/skills/ibm-i-code-generator/
```

Copy multiple IBM i skills by selecting the `ibm-i-*` folders that contain
`SKILL.md` and copying them into `~/.config/opencode/skills/`. Skip placeholder
folders until their `SKILL.md` files are added.

Copy one Legacy Spec Factory skill:

```bash
mkdir -p ~/.config/opencode/skills/legacy-spec-writer
cp -R skills/legacy-spec-factory/legacy-spec-writer/. ~/.config/opencode/skills/legacy-spec-writer/
```

Copy all Legacy Spec Factory skills. This works because that domain preserves
the original `legacy-*` folder names:

```bash
cp -R skills/legacy-spec-factory/legacy-* ~/.config/opencode/skills/
```

## IBM i Copy-Ready Folders

IBM i source folders are copy-ready. The source folder name already matches the
OpenCode folder name.

| Source Folder | OpenCode Folder |
|---------------|-----------------|
| `skills/ibm-i-skill-family/ibm-i-code-generator/` | `~/.config/opencode/skills/ibm-i-code-generator/` |
| `skills/ibm-i-skill-family/ibm-i-code-reviewer/` | `~/.config/opencode/skills/ibm-i-code-reviewer/` |
| `skills/ibm-i-skill-family/ibm-i-compile-precheck/` | `~/.config/opencode/skills/ibm-i-compile-precheck/` |
| `skills/ibm-i-skill-family/ibm-i-dds-generator/` | `~/.config/opencode/skills/ibm-i-dds-generator/` |
| `skills/ibm-i-skill-family/ibm-i-dds-reviewer/` | `~/.config/opencode/skills/ibm-i-dds-reviewer/` |
| `skills/ibm-i-skill-family/ibm-i-file-spec/` | `~/.config/opencode/skills/ibm-i-file-spec/` |
| `skills/ibm-i-skill-family/ibm-i-functional-spec/` | `~/.config/opencode/skills/ibm-i-functional-spec/` |
| `skills/ibm-i-skill-family/ibm-i-impact-analyzer/` | `~/.config/opencode/skills/ibm-i-impact-analyzer/` |
| `skills/ibm-i-skill-family/ibm-i-program-analyzer/` | `~/.config/opencode/skills/ibm-i-program-analyzer/` |
| `skills/ibm-i-skill-family/ibm-i-program-spec/` | `~/.config/opencode/skills/ibm-i-program-spec/` |
| `skills/ibm-i-skill-family/ibm-i-requirement-normalizer/` | `~/.config/opencode/skills/ibm-i-requirement-normalizer/` |
| `skills/ibm-i-skill-family/ibm-i-spec-reviewer/` | `~/.config/opencode/skills/ibm-i-spec-reviewer/` |
| `skills/ibm-i-skill-family/ibm-i-technical-design/` | `~/.config/opencode/skills/ibm-i-technical-design/` |
| `skills/ibm-i-skill-family/ibm-i-test-scaffold/` | `~/.config/opencode/skills/ibm-i-test-scaffold/` |
| `skills/ibm-i-skill-family/ibm-i-ut-plan-generator/` | `~/.config/opencode/skills/ibm-i-ut-plan-generator/` |
| `skills/ibm-i-skill-family/ibm-i-workflow-orchestrator/` | `~/.config/opencode/skills/ibm-i-workflow-orchestrator/` |

## Legacy Spec Factory Copy-Ready Folders

Legacy Spec Factory uses preserved names. The source folder is already the
OpenCode folder name.

Examples:

| Source Folder | OpenCode Folder |
|---------------|-----------------|
| `skills/legacy-spec-factory/legacy-modernization-orchestrator/` | `~/.config/opencode/skills/legacy-modernization-orchestrator/` |
| `skills/legacy-spec-factory/legacy-ibmi-inventory/` | `~/.config/opencode/skills/legacy-ibmi-inventory/` |
| `skills/legacy-spec-factory/legacy-spec-writer/` | `~/.config/opencode/skills/legacy-spec-writer/` |

## Quick Check

After copying, the destination should look like this:

```text
~/.config/opencode/skills/
  ibm-i-workflow-orchestrator/
    SKILL.md
  legacy-modernization-orchestrator/
    SKILL.md
```

Then ask OpenCode with the installed skill name:

```text
Use ibm-i-workflow-orchestrator.
Here is what I have. Tell me the next best skill and what input it needs.
```
