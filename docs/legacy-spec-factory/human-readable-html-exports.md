# Human-Readable HTML Exports

This repository keeps Markdown as the canonical source for human-facing
artifacts, but internal pilot reviews may prefer standalone HTML for easier
reading, scrolling, printing, and link sharing.

Use `scripts/render_stakeholder_html.py` to export any Markdown file or a whole
directory tree into HTML companions.

## Why

- SMEs and business users usually read HTML more comfortably than raw Markdown.
- Large tables, checklists, and traceability matrices are easier to scan in a
  browser.
- HTML exports keep the source portable across Codex, Claude Code, and
  OpenCode because the canonical artifacts stay `.md`.

## Usage

Render one file:

```bash
python3 scripts/render_stakeholder_html.py path/to/spec.md
```

Render one folder:

```bash
python3 scripts/render_stakeholder_html.py 05_specs/CAP-PRICE-CALCULATION
```

Render a whole project tree:

```bash
python3 scripts/render_stakeholder_html.py docs/EXAMPLE-tutorial --recursive
```

## Output Behavior

- Each Markdown file becomes a sibling `.html` file.
- Directory mode also writes `index.html` at the directory root.
- The HTML is standalone: no external CSS, JS, or network dependency.
- Markdown remains the source of truth. Regenerate HTML after editing the `.md`
  source.

## Good Candidates

- `brd.md`
- `spec.md`
- `sdd-handoff.md`
- `brd-review.md`
- `spec-review.md`
- `handoff-review.md`
- `traceability.md`
- `question-pack.md`
- `STATUS.md`
- `programs-batch-digest.md`
- `object-map.md`

## Notes

- The renderer is intentionally lightweight and only depends on Python's
  standard library.
- It is optimized for the Markdown structures used in this repository:
  headings, tables, lists, checklists, links, blockquotes, code blocks, and
  section-heavy review documents.
