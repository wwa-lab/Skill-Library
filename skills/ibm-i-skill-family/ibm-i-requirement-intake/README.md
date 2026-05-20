# Placeholder: IBM i Requirement Intake

Author: Oliver

This directory is reserved for the internal pilot skill currently known as:

```text
as400-requirment-intake
```

Use the corrected library name when importing it:

```text
ibm-i-requirement-intake
```

## Intended Position

This is the first skill in the IBM i skill family. It prepares the request
intake material before requirement normalization.

Expected output from the internal pilot:

- A CSV request-intake document.
- CSV columns aligned so users can copy the data into the Excel request
  template.
- A collection aid for users to gather enough requirement material before the
  main IBM i delivery chain starts.

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
     author: Oliver
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
