# Placeholder: IBM i Requirement Intake

This directory is reserved for the internal pilot skill currently known as:

```text
as400-requirment-intake
```

Use the corrected library name when importing it:

```text
ibm-i-requirement-intake
```

## Import Steps

1. Copy the internal pilot skill's `SKILL.md` into this directory.
2. Rename or normalize the frontmatter `name` to:

   ```yaml
   name: ibm-i-requirement-intake
   ```

3. Add or preserve provenance metadata:

   ```yaml
   license: Internal
   metadata:
     author: Leo L Zhang
     maintainer: platform-engineering
     source: internal-pilot-run
     legacy_name: as400-requirment-intake
     domain: ibm-i
   ```

4. Copy any supporting `references/`, `scripts/`, `assets/`, `examples/`, or `tests/`.
5. Run:

   ```bash
   node scripts/validate-skills.mjs --strict
   node scripts/install-opencode-skills.mjs --domain ibm-i --dry-run
   ```

This placeholder intentionally does not include `SKILL.md`, so it is not installed into OpenCode yet.

