---
name: legacy-html-exporter
description: "Export stakeholder-facing Markdown artifacts into standalone HTML companions for easier reading in pilot reviews, SME walkthroughs, and business sign-off sessions. Use when the user asks for HTML versions of BRDs, specs, review packs, question packs, traceability pages, STATUS pages, or other user / SME-facing docs. Supplemental skill only: Markdown remains the canonical source, and this skill generates `.html` companions plus optional directory `index.html` pages without redefining the underlying artifact contract."
license: Apache-2.0
metadata:
  author: Leo L Zhang
  maintainer: platform-engineering
  source: https://github.com/wwa-lab/legacy-spec-factory
  source_commit: 8871a6b
  domain: legacy-spec-factory
---

<!--
Legacy Spec Factory
Copyright 2026 Leo L Zhang

Original author: Leo L Zhang
License: Apache License 2.0

This skill is part of the Legacy Spec Factory project.
Retain this notice in substantial copies or derived versions.
-->

# Legacy HTML Exporter

Convert human-facing Markdown artifacts into standalone HTML so SMEs,
business users, and pilot reviewers can read the same content in a browser
without changing the canonical source format.

## Purpose

The Legacy Spec Factory deliberately keeps reviewable artifacts in Markdown:
portable across Codex, Claude Code, and OpenCode; diffable in git; easy to
validate; and stable as the source of truth. That is still the right default.

But pilot reviews often involve readers who are more comfortable with:

- browser scrolling instead of raw Markdown
- wider table layouts
- printable pages
- a single click-open `index.html` for a capability package

This skill adds that convenience layer without changing the artifact contract.
It creates HTML companions for docs such as:

- `brd.md`
- `spec.md`
- `sdd-handoff.md`
- `*-review.md`
- `traceability.md`
- `question-pack.md`
- `STATUS.md`
- `programs-batch-digest.md`
- `object-map.md`

## When to Use

Trigger on any of these signals:

- The user asks for "HTML", "web view", "browser-readable", "给 SME 看更方便",
  "导出成 html", or similar
- A capability package already exists in Markdown and needs a more convenient
  review surface for user / SME walkthroughs
- A pilot review is blocked by "these docs are hard to read as raw Markdown"
- The user wants a whole folder of human-facing artifacts exported at once

## When NOT to Use

Do NOT trigger when:

- The user needs the canonical artifact itself rewritten or regenerated
  (route to the producing skill instead)
- The user is asking for machine-readable structured output
  (`spec.yaml`, `sdd-handoff.yaml`, JSON bundles, manifests)
- The caller wants HTML to become the source of truth
- The source Markdown is still unstable, incomplete, or blocked and should be
  fixed first
- The request is really about publishing a full external website rather than
  internal review convenience

This skill is a companion-rendering step, not a replacement for BRD/spec/review
generation and not a web publishing pipeline.

## Non-Negotiable Guardrail

If a caller asks to make HTML the new source of truth, overwrite Markdown with
HTML, or ignore the Markdown after export, block that request.

The correct policy is always:

- Markdown remains canonical
- HTML is a companion view only
- if content is wrong, fix Markdown first and regenerate HTML

When this guardrail is triggered, prefer an explicit answer shape:

```text
- action: blocked
- reason: HTML companion export does not replace the Markdown source of truth
- canonical source of truth: <original .md path>
```

Do not soften, reinterpret, or partially comply with this guardrail. If the
caller asks to promote `.html` above `.md`, the answer must stay blocked.

If the caller both asks for HTML export and tries to replace the source of
truth, the source-of-truth guardrail wins. Do not "split the difference".

## Layer Position

Supplemental rendering skill. It does not advance the linear legacy-analysis
stage and does not alter review status, approvals, IDs, or evidence strength.

Use it after a human-facing Markdown artifact already exists.

## Inputs

Accept:

- One Markdown file path to export
- One directory containing Markdown files to export
- Optional `--recursive` intent when the user wants a whole capability or demo
  tree rendered
- Optional target subset if only specific files in a directory should be
  exported

Input readiness scoring:

- `0-5 blocked`: no readable Markdown source exists; path is ambiguous; the
  caller actually wants canonical content rewritten; source file is not
  Markdown.
- `6 minimum_pass`: one stable Markdown file or one clear directory exists.
- `7-8 usable`: the caller has identified the target package or audience
  (e.g. SME, pilot review, business user).
- `9-10 strong`: the export scope is explicit (single file vs package), and
  the human-facing docs are already complete enough for review.

Stop conditions:

- Source path does not exist
- Source is not `.md`
- Caller asks to overwrite the source with HTML
- Markdown is still blocked and should be fixed upstream before packaging

If a stop condition is hit, do not continue into "best effort" export advice
that violates the contract.

## Output Contract

By default, write HTML companions beside the Markdown source:

- `foo.md` → `foo.html`
- directory mode also writes `index.html` at the supplied directory root

The HTML output must:

- remain standalone with no network dependency
- preserve headings, tables, lists, checklists, links, quotes, and code blocks
- keep the underlying Markdown path visible so reviewers know the canonical
  source
- avoid inventing or transforming business content

The HTML output must NOT:

- become the authoritative artifact instead of `.md`
- silently drop sections from the source Markdown
- add new business statements, approvals, or IDs
- rewrite YAML / JSON machine artifacts into fake HTML substitutes unless the
  user explicitly asked for a human-readable companion

If a caller requests any forbidden item above, block instead of partially
complying.

## Canonical Script

Use:

- `scripts/render_stakeholder_html.py` as the stable entrypoint
- `skills/legacy-html-exporter/scripts/render_stakeholder_html.py` as the
  canonical skill-owned implementation
- `skills/legacy-html-exporter/scripts/export_contract_helper.py` for
  deterministic contract-only / no-write smoke responses

The root script exists for convenience and should stay behaviorally aligned
with the skill-owned script.

## Step Contract

## Fast Decision Rules

Apply this decision order exactly:

1. If the prompt says HTML should replace Markdown, answer with the blocked
   template and stop.
2. Else if the prompt is a contract-only / no-write smoke test for one `.md`
   file, use `export_contract_helper.py` or follow its exact logic: infer the
   sibling `.html` path, return the requested labels only, and stop.
3. Else if the prompt is a normal export request for one `.md` file, run the
   renderer and report the emitted `.html` path.
4. Else if the prompt is a directory export request, use directory mode and
   report the relevant `.html` / `index.html` outputs.

Do not inspect more files than the active branch requires.

### Input

- **Required**: one existing Markdown file or one directory containing Markdown
  files
- **Optional**: recursive export intent; a narrowed list of target docs; a
  custom index title
- **Readiness checks**: source exists; source files are human-facing docs
  suitable for browser reading; caller understands Markdown remains canonical
- **Stop conditions**: nonexistent path; non-Markdown source; request to treat
  HTML as the system of record

### Execution

- **Procedure**:
  1. Confirm whether the request is single-file export or package export
  2. Select only the human-facing Markdown docs in scope
  3. If the prompt is a contract-only or no-write smoke test, do not actually
     run the script; infer the sibling `.html` path from the contract
  4. Otherwise run `python3 scripts/render_stakeholder_html.py <path> [--recursive]`
  5. Report generated or expected `.html` paths back to the user
- **Allowed inference**: if the user says "给 SME 看这些文档", infer that the
  relevant Markdown package or capability directory should be exported
- **Forbidden assumptions**: changing source content; exporting YAML/JSON as if
  they were the reviewed source; claiming HTML is canonical; omitting source
  files without noting scope
- **Output discipline**: when the caller says `Return only`, respond with only
  the requested labels / bullets. Do not add extra sections, explanations, or
  permission requests.
- **Smoke-test discipline**: when the prompt says `contract-only no-write smoke
  test` or `do not create or edit files`, never ask to execute the renderer,
  never request approval, and never imply that HTML becomes canonical.
- **Single-file discipline**: for one concrete `.md` path, do not scan large
  directory trees, whole docs folders, or unrelated examples unless the file is
  missing and the prompt explicitly asks you to find alternatives.

### Output

- **Canonical artifacts**: sibling `.html` files and optional directory
  `index.html`
- **Handoff status**: a convenience package for human review only; does not
  change stage gates, approval states, or traceability semantics

### Validation

- **Mechanical**: generated `.html` file exists for every exported `.md`;
  directory export writes `index.html`; links are emitted; no source `.md` is
  overwritten
- **Human-facing**: tables remain readable; checklists render as checkboxes;
  large review docs remain navigable via headings / table of contents
- **Governance**: user / SME can browse the docs more easily, but the canonical
  review source remains Markdown in git

## Workflow

1. Confirm the export scope.
2. Prefer exporting the exact docs the stakeholder will read rather than the
   whole repository.
3. Use the script entrypoint instead of hand-writing HTML.
4. If the user asks for a whole folder, use directory export and keep the
   generated `index.html`.
5. If the user later edits the Markdown source, re-run the export rather than
   editing the HTML directly.

## Response Templates

Positive contract-only answer:

```text
- canonical source path: <path/to/file.md>
- generated HTML path: <path/to/file.html>
- whether Markdown remains canonical: yes
```

Use exactly `yes`, not prose such as "Markdown remains canonical because...".

Negative source-of-truth challenge:

```text
- action: blocked
- reason: HTML companion export does not replace the Markdown source of truth
- canonical source of truth: <path/to/file.md>
```

Use exactly `blocked`, not "convert", "warn", "deprecated", or mixed answers.

## Quick Commands

Single file:

```bash
python3 scripts/render_stakeholder_html.py 05_specs/CAP-PRICE-CALCULATION/spec.md
```

Whole package:

```bash
python3 scripts/render_stakeholder_html.py docs/EXAMPLE-tutorial --recursive
```

## Notes

- This skill is intentionally lightweight and deterministic.
- It exists to reduce review friction, not to introduce a second source of
  truth.
- If a document is wrong, fix the Markdown first, then regenerate the HTML.
