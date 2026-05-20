#!/usr/bin/env python3
"""Convenience wrapper for the canonical legacy-html-exporter renderer."""

from __future__ import annotations

import runpy
from pathlib import Path


SKILL_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "legacy-html-exporter"
    / "scripts"
    / "render_stakeholder_html.py"
)


if __name__ == "__main__":
    runpy.run_path(str(SKILL_SCRIPT), run_name="__main__")
