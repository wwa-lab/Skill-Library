# Placeholder: IBM i UT Plan to XML

Author: Kevin

This directory is reserved for the internal pilot skill:

```text
ibm-i-ut-plan-to-xml
```

## Intended Position

This skill runs after `ibm-i-ut-plan-generator` creates the UT Plan.

Expected output from the internal pilot:

- XML generated from the IBM i UT Plan.
- XML shaped for internal JUICE-based unit testing.
- A handoff path for testing iSeries programs with the internal JUICE workflow.

## Import Steps

1. Copy the internal pilot skill's `SKILL.md` into this directory.
2. Ensure the frontmatter `name` is:

   ```yaml
   name: ibm-i-ut-plan-to-xml
   ```

3. Add or preserve provenance metadata:

   ```yaml
   license: Internal
   metadata:
     author: Kevin
     maintainer: platform-engineering
     source: internal-pilot-run
     domain: ibm-i
   ```

4. Copy any supporting `references/`, `scripts/`, `assets/`, `examples/`, or `tests/`.
5. Run:

   ```bash
   node scripts/validate-skills.mjs --strict
   node scripts/install-opencode-skills.mjs --domain ibm-i --dry-run
   ```

This placeholder intentionally does not include `SKILL.md`, so it is not installed into OpenCode yet.
