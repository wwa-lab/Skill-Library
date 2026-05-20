#!/usr/bin/env python3
"""Deterministic helper for legacy-html-exporter contract-only decisions."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def sibling_html_path(markdown_path: str) -> str:
    path = Path(markdown_path)
    if path.suffix.lower() != ".md":
      raise ValueError(f"Expected a Markdown path, got: {markdown_path}")
    return str(path.with_suffix(".html").as_posix())


def source_of_truth_challenge(prompt_text: str) -> bool:
    lowered = prompt_text.lower()
    challenge_markers = (
        "source of truth",
        "canonical",
        "ignore the markdown",
        "replace markdown",
        "overwrite markdown",
        "html the source",
    )
    html_markers = ("html", ".html")
    markdown_markers = ("markdown", ".md")
    return (
        any(marker in lowered for marker in challenge_markers)
        and any(marker in lowered for marker in html_markers)
        and any(marker in lowered for marker in markdown_markers)
    )


def format_positive(markdown_path: str) -> str:
    return "\n".join(
        [
            f"- canonical source path: {markdown_path}",
            f"- generated HTML path: {sibling_html_path(markdown_path)}",
            "- whether Markdown remains canonical: yes",
        ]
    )


def format_negative(markdown_path: str) -> str:
    return "\n".join(
        [
            "- action: blocked",
            "- reason: HTML companion export does not replace the Markdown source of truth",
            f"- canonical source of truth: {markdown_path}",
        ]
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown_path", help="Markdown source path")
    parser.add_argument(
        "--prompt-text",
        default="",
        help="Optional raw prompt text to evaluate as a source-of-truth challenge.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        if source_of_truth_challenge(args.prompt_text):
            print(format_negative(args.markdown_path))
        else:
            print(format_positive(args.markdown_path))
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
