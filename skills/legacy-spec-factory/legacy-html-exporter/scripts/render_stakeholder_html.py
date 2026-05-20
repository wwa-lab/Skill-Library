#!/usr/bin/env python3
"""Render Markdown docs into standalone HTML for SME / stakeholder review.

This keeps Markdown as the canonical source while producing a more convenient
HTML view for internal pilot reviews, SME walkthroughs, and status sharing.

Usage:
  python3 scripts/render_stakeholder_html.py path/to/doc.md
  python3 scripts/render_stakeholder_html.py docs/EXAMPLE-tutorial --recursive
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


INLINE_CODE_TOKEN = "\u0000CODE{index}\u0000"
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ORDERED_ITEM_RE = re.compile(r"^\d+\.\s+(.*)$")
UNORDERED_ITEM_RE = re.compile(r"^[-*]\s+(.*)$")
CHECKBOX_RE = re.compile(r"^\[( |x|X)\]\s+(.*)$")
TABLE_SEPARATOR_RE = re.compile(r"^\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
STRONG_RE = re.compile(r"\*\*(.+?)\*\*")
EM_RE = re.compile(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")


@dataclass
class Heading:
    level: int
    text: str
    anchor: str


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    slug = re.sub(r"[\s-]+", "-", slug)
    return slug or "section"


def extract_title(markdown_text: str, source_name: str) -> str:
    for raw_line in markdown_text.splitlines():
        match = HEADING_RE.match(raw_line.strip())
        if match and len(match.group(1)) == 1:
            return match.group(2).strip("` ").strip() or source_name
    return source_name


def preserve_code_spans(text: str) -> tuple[str, list[str]]:
    tokens: list[str] = []

    def replacer(match: re.Match[str]) -> str:
        content = match.group(1)
        tokens.append(f"<code>{html.escape(content)}</code>")
        return INLINE_CODE_TOKEN.format(index=len(tokens) - 1)

    return CODE_SPAN_RE.sub(replacer, text), tokens


def restore_code_spans(text: str, tokens: list[str]) -> str:
    for index, replacement in enumerate(tokens):
        text = text.replace(INLINE_CODE_TOKEN.format(index=index), replacement)
    return text


def render_inline(text: str) -> str:
    escaped, code_tokens = preserve_code_spans(html.escape(text, quote=True))
    escaped = LINK_RE.sub(
        lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{m.group(1)}</a>',
        escaped,
    )
    escaped = STRONG_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = EM_RE.sub(r"<em>\1</em>", escaped)
    return restore_code_spans(escaped, code_tokens)


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    return lines[index].lstrip().startswith("|") and bool(
        TABLE_SEPARATOR_RE.match(lines[index + 1].strip())
    )


def parse_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def build_toc(headings: list[Heading]) -> str:
    if len(headings) < 2:
        return ""
    items = "\n".join(
        f'<li class="toc-level-{heading.level}"><a href="#{heading.anchor}">{html.escape(heading.text)}</a></li>'
        for heading in headings
        if heading.level <= 3
    )
    return (
        '<nav class="toc">'
        "<h2>Contents</h2>"
        f"<ul>{items}</ul>"
        "</nav>"
    )


def render_markdown_body(markdown_text: str) -> tuple[str, list[Heading]]:
    lines = markdown_text.splitlines()
    index = 0
    blocks: list[str] = []
    headings: list[Heading] = []
    used_anchors: dict[str, int] = {}

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped.startswith("```"):
            fence = stripped[:3]
            language = stripped[3:].strip() or "text"
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith(fence):
                code_lines.append(lines[index])
                index += 1
            index += 1
            code_body = "\n".join(code_lines)
            blocks.append(
                f'<pre><code class="language-{html.escape(language)}">{html.escape(code_body)}</code></pre>'
            )
            continue

        heading_match = HEADING_RE.match(stripped)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            anchor_base = slugify(text.strip("`"))
            suffix = used_anchors.get(anchor_base, 0)
            used_anchors[anchor_base] = suffix + 1
            anchor = anchor_base if suffix == 0 else f"{anchor_base}-{suffix + 1}"
            headings.append(Heading(level=level, text=text.strip("`"), anchor=anchor))
            blocks.append(
                f'<h{level} id="{anchor}">{render_inline(text)}</h{level}>'
            )
            index += 1
            continue

        if stripped in {"---", "***"}:
            blocks.append("<hr>")
            index += 1
            continue

        if is_table_start(lines, index):
            header_cells = parse_table_row(lines[index])
            table_rows: list[list[str]] = []
            index += 2
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                table_rows.append(parse_table_row(lines[index]))
                index += 1
            header_html = "".join(
                f"<th>{render_inline(cell)}</th>" for cell in header_cells
            )
            body_html = "\n".join(
                "<tr>"
                + "".join(f"<td>{render_inline(cell)}</td>" for cell in row)
                + "</tr>"
                for row in table_rows
            )
            blocks.append(
                "<table>"
                f"<thead><tr>{header_html}</tr></thead>"
                f"<tbody>{body_html}</tbody>"
                "</table>"
            )
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while index < len(lines) and lines[index].strip().startswith(">"):
                quote_lines.append(lines[index].strip()[1:].lstrip())
                index += 1
            blocks.append(f"<blockquote><p>{render_inline(' '.join(quote_lines))}</p></blockquote>")
            continue

        ordered_match = ORDERED_ITEM_RE.match(stripped)
        unordered_match = UNORDERED_ITEM_RE.match(stripped)
        if ordered_match or unordered_match:
            tag = "ol" if ordered_match else "ul"
            items: list[str] = []
            while index < len(lines):
                current = lines[index].strip()
                match = ORDERED_ITEM_RE.match(current) if tag == "ol" else UNORDERED_ITEM_RE.match(current)
                if not match:
                    break
                content = match.group(1).strip()
                checkbox_match = CHECKBOX_RE.match(content)
                if checkbox_match:
                    checked = checkbox_match.group(1).lower() == "x"
                    checkbox_html = (
                        f'<input type="checkbox"{" checked" if checked else ""} disabled>'
                    )
                    item_html = f'{checkbox_html}<span>{render_inline(checkbox_match.group(2))}</span>'
                    items.append(f'<li class="checklist-item">{item_html}</li>')
                else:
                    items.append(f"<li>{render_inline(content)}</li>")
                index += 1
            blocks.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            upcoming = lines[index].strip()
            if not upcoming:
                index += 1
                break
            if (
                upcoming.startswith("```")
                or HEADING_RE.match(upcoming)
                or upcoming in {"---", "***"}
                or is_table_start(lines, index)
                or upcoming.startswith(">")
                or ORDERED_ITEM_RE.match(upcoming)
                or UNORDERED_ITEM_RE.match(upcoming)
            ):
                break
            paragraph_lines.append(upcoming)
            index += 1
        blocks.append(f"<p>{render_inline(' '.join(paragraph_lines))}</p>")

    return "\n".join(blocks), headings


def render_markdown(markdown_text: str, source_name: str) -> str:
    title = extract_title(markdown_text, source_name)
    body_html, headings = render_markdown_body(markdown_text)
    toc_html = build_toc(headings)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #f4efe7;
      --panel: #fffdf8;
      --text: #1f2933;
      --muted: #52606d;
      --line: #d9d1c4;
      --accent: #8f4e22;
      --accent-soft: #f6e3cf;
      --code-bg: #f3f4f6;
      --quote: #f8f1e7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "Iowan Old Style", "Palatino Linotype", "Book Antiqua", Georgia, serif;
      color: var(--text);
      background:
        radial-gradient(circle at top left, #f9e6d2 0, transparent 28rem),
        linear-gradient(180deg, #fcfaf6 0%, var(--bg) 100%);
      line-height: 1.65;
    }}
    .shell {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 20px 64px;
    }}
    .hero {{
      padding: 28px 30px;
      border: 1px solid var(--line);
      border-radius: 24px;
      background: linear-gradient(135deg, rgba(255,255,255,0.96), rgba(250,241,229,0.96));
      box-shadow: 0 18px 50px rgba(92, 66, 37, 0.08);
    }}
    .hero p {{
      margin: 10px 0 0;
      color: var(--muted);
      font-size: 0.98rem;
    }}
    .layout {{
      display: grid;
      grid-template-columns: minmax(0, 1fr);
      gap: 22px;
      margin-top: 24px;
    }}
    .toc, .content {{
      border: 1px solid var(--line);
      border-radius: 24px;
      background: var(--panel);
      box-shadow: 0 16px 40px rgba(92, 66, 37, 0.06);
    }}
    .toc {{
      padding: 20px 22px;
    }}
    .toc h2 {{
      margin: 0 0 10px;
      font-size: 1.05rem;
    }}
    .toc ul {{
      margin: 0;
      padding-left: 18px;
    }}
    .toc li {{
      margin: 6px 0;
    }}
    .toc-level-3 {{
      color: var(--muted);
    }}
    .toc a {{
      color: inherit;
      text-decoration: none;
    }}
    .content {{
      padding: 28px 30px;
    }}
    h1, h2, h3, h4, h5, h6 {{
      line-height: 1.25;
      margin: 1.4em 0 0.6em;
      scroll-margin-top: 24px;
    }}
    h1:first-child {{
      margin-top: 0;
    }}
    h1 {{
      font-size: 2.15rem;
    }}
    h2 {{
      font-size: 1.45rem;
      border-top: 1px solid var(--line);
      padding-top: 18px;
    }}
    h3 {{
      font-size: 1.12rem;
    }}
    p, ul, ol, table, pre, blockquote {{
      margin: 0 0 16px;
    }}
    ul, ol {{
      padding-left: 24px;
    }}
    li {{
      margin: 7px 0;
    }}
    .checklist-item {{
      list-style: none;
      margin-left: -24px;
      display: flex;
      gap: 10px;
      align-items: flex-start;
    }}
    .checklist-item input {{
      margin-top: 0.3rem;
      accent-color: var(--accent);
    }}
    code {{
      font-family: "SFMono-Regular", "SF Mono", Consolas, "Liberation Mono", monospace;
      background: var(--code-bg);
      border-radius: 6px;
      padding: 0.1rem 0.35rem;
      font-size: 0.92em;
    }}
    pre {{
      overflow-x: auto;
      padding: 16px 18px;
      background: #18212b;
      color: #f8fafc;
      border-radius: 16px;
    }}
    pre code {{
      background: transparent;
      color: inherit;
      padding: 0;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      display: block;
      overflow-x: auto;
    }}
    th, td {{
      border: 1px solid var(--line);
      padding: 10px 12px;
      vertical-align: top;
      text-align: left;
    }}
    thead th {{
      background: var(--accent-soft);
    }}
    blockquote {{
      border-left: 4px solid var(--accent);
      margin-left: 0;
      padding: 12px 16px;
      background: var(--quote);
      border-radius: 0 12px 12px 0;
    }}
    a {{
      color: var(--accent);
    }}
    hr {{
      border: 0;
      border-top: 1px solid var(--line);
      margin: 22px 0;
    }}
    .footer {{
      margin-top: 20px;
      color: var(--muted);
      font-size: 0.94rem;
    }}
    @media (min-width: 980px) {{
      .layout.with-toc {{
        grid-template-columns: 280px minmax(0, 1fr);
        align-items: start;
      }}
      .toc {{
        position: sticky;
        top: 20px;
      }}
    }}
    @media (max-width: 700px) {{
      .shell {{
        padding: 18px 12px 32px;
      }}
      .hero, .content, .toc {{
        border-radius: 18px;
        padding: 20px 18px;
      }}
      h1 {{
        font-size: 1.75rem;
      }}
    }}
  </style>
</head>
<body>
  <div class="shell">
    <section class="hero">
      <h1>{html.escape(title)}</h1>
      <p>Standalone HTML view generated from <code>{html.escape(source_name)}</code>. Markdown remains the canonical source.</p>
    </section>
    <div class="layout{' with-toc' if toc_html else ''}">
      {toc_html}
      <article class="content">
        {body_html}
        <p class="footer">Rendered by <code>scripts/render_stakeholder_html.py</code>.</p>
      </article>
    </div>
  </div>
</body>
</html>
"""


def collect_markdown_files(path: Path, recursive: bool) -> list[Path]:
    if path.is_file():
        if path.suffix.lower() != ".md":
            raise ValueError(f"Expected a Markdown file, got: {path}")
        return [path]
    if not path.is_dir():
        raise ValueError(f"Path does not exist: {path}")
    pattern = "**/*.md" if recursive else "*.md"
    return sorted(p for p in path.glob(pattern) if p.is_file())


def render_markdown_file(source_path: Path, output_path: Path | None = None) -> Path:
    destination = output_path or source_path.with_suffix(".html")
    html_text = render_markdown(
        source_path.read_text(encoding="utf-8"),
        source_name=source_path.name,
    )
    destination.write_text(html_text, encoding="utf-8")
    return destination


def render_index_html(root: Path, rendered_paths: Iterable[Path], index_title: str) -> Path:
    items = []
    for html_path in sorted(rendered_paths):
        if html_path.name == "index.html":
            continue
        relative = html_path.relative_to(root)
        items.append(
            f'<li><a href="{html.escape(relative.as_posix(), quote=True)}">{html.escape(relative.as_posix())}</a></li>'
        )
    body = "\n".join(items) or "<li>No HTML pages were generated.</li>"
    output = root / "index.html"
    output.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(index_title)}</title>
  <style>
    body {{
      margin: 0;
      font-family: Georgia, serif;
      background: linear-gradient(180deg, #fcfaf6, #f4efe7);
      color: #1f2933;
    }}
    main {{
      max-width: 840px;
      margin: 0 auto;
      padding: 32px 18px 48px;
    }}
    section {{
      background: rgba(255,255,255,0.96);
      border: 1px solid #d9d1c4;
      border-radius: 24px;
      padding: 24px 26px;
      box-shadow: 0 16px 40px rgba(92, 66, 37, 0.06);
    }}
    a {{ color: #8f4e22; }}
    li {{ margin: 8px 0; }}
  </style>
</head>
<body>
  <main>
    <section>
      <h1>{html.escape(index_title)}</h1>
      <p>Standalone HTML exports for human-readable project artifacts.</p>
      <ul>{body}</ul>
    </section>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )
    return output


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Markdown file(s) or directories")
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="When a directory is supplied, render Markdown files recursively.",
    )
    parser.add_argument(
        "--index-title",
        default="Stakeholder HTML Export",
        help="Title for directory index pages.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rendered_paths: list[Path] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            markdown_paths = collect_markdown_files(path, recursive=args.recursive)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

        if not markdown_paths:
            print(f"WARNING: no Markdown files found under {path}", file=sys.stderr)
            continue

        start_index = len(rendered_paths)
        for markdown_path in markdown_paths:
            destination = render_markdown_file(markdown_path)
            rendered_paths.append(destination)
            print(destination)

        if path.is_dir():
            index_path = render_index_html(
                path,
                rendered_paths[start_index:],
                args.index_title,
            )
            print(index_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
