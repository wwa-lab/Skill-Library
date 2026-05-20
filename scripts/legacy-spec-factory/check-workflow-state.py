#!/usr/bin/env python3
"""Validate a Legacy Spec Factory `workflow-state.yaml` against its contract.

Rules enforced (see docs/workflow-state-contract.md):
  - Required top-level keys: version, project, current_focus, capabilities, history
  - version == 1
  - project.{name, root, last_updated_at, last_updated_by} present
  - project.name matches PPCR convention ^[A-Za-z0-9][A-Za-z0-9-]*$
  - project.root matches `docs/<project.name>/` (with trailing slash)
  - capabilities[].id matches CAP-* or MODULE-* pattern
  - capabilities[].stage_id matches one of the allowed stage IDs from
    references/stage-identification.md
  - capabilities[].blocking has tbds, sme_pending, gates (each a list)
  - capabilities[] has unique `id` values
  - history[] is non-decreasing by `at` timestamp (append-only ordering)
  - history[].skill is non-empty
  - history[].stage_after is allowed, null, or "scan"
  - current_focus.capability_id (if set) references an existing capabilities[].id
  - current_focus.stage_card (if set) points to an existing stage-cards file
  - Cross-check: current_focus.stage_id == capabilities[<current cap>].stage_id

Usage:
  python3 scripts/check-workflow-state.py [--template] [<path>]

Default path: ./workflow-state.yaml

`--template` relaxes PPCR-name and project.root validation so the canonical
template (with `<...>` placeholders) can be checked for structural integrity.

Exit 0 on pass, 1 on validation errors.

Standalone: only depends on PyYAML.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
STAGE_CARDS_DIR = (
    REPO_ROOT
    / "skills"
    / "legacy-modernization-orchestrator"
    / "references"
    / "stage-cards"
)

ALLOWED_STAGE_IDS = {
    "0 Evidence Intake",
    "1 Evidence Ready",
    "2a Inventory In Progress",
    "2b Inventory Blocked",
    "2c Inventory Done",
    "3a Program Analysis In Progress",
    "3b Program Analysis Done",
    "3c Flow Analysis In Progress",
    "3d Flow Analysis Done",
    "3e Module Analysis In Progress",
    "3f Module Analysis Done",
    "4a Static Analysis Partial",
    "4b Static Analysis Complete",
    "5 Runtime Evidence Mined",
    "6 Business Rules Drafted",
    "7 Capabilities Mapped",
    "8a Spec Drafted",
    "8b Spec In Review",
    "8c Spec Approved",
    "9 Equivalence Pack Ready",
    "10 Forward Handoff Ready",
}

ALLOWED_STAGE_AFTER_EXTRA = {None, "scan"}

ID_PATTERN = re.compile(r"^(CAP|MODULE)-[A-Z0-9-]+$")
PROJECT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")


def fail(findings: list[str], msg: str) -> None:
    findings.append(msg)


def validate(state_path: Path, template_mode: bool = False) -> list[str]:
    findings: list[str] = []

    if not state_path.exists():
        return [f"workflow-state.yaml not found at {state_path}"]

    with state_path.open("r", encoding="utf-8") as fh:
        try:
            data = yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            return [f"YAML parse error: {exc}"]

    if not isinstance(data, dict):
        return ["workflow-state.yaml is not a YAML mapping"]

    # Top-level keys
    required_top = ["version", "project", "current_focus", "capabilities", "history"]
    for key in required_top:
        if key not in data:
            fail(findings, f"missing top-level key: {key}")

    # version
    if data.get("version") != 1:
        fail(
            findings,
            f"version must be 1; got {data.get('version')!r}",
        )

    # project
    project = data.get("project") or {}
    if not isinstance(project, dict):
        fail(findings, "project must be a mapping")
    else:
        for key in ("name", "root", "last_updated_at", "last_updated_by"):
            if not project.get(key):
                fail(findings, f"project.{key} is required and non-empty")
        name = project.get("name")
        if not template_mode and isinstance(name, str) and not PROJECT_NAME_PATTERN.match(name):
            fail(
                findings,
                f"project.name {name!r} must match PPCR convention "
                f"^[A-Za-z0-9][A-Za-z0-9-]*$ (e.g. XXX260004-demo)",
            )
        root = project.get("root")
        if not template_mode and isinstance(root, str) and isinstance(name, str):
            expected = f"docs/{name}/"
            if root != expected:
                fail(
                    findings,
                    f"project.root {root!r} must equal {expected!r} "
                    f"(derived from project.name)",
                )

    # capabilities
    caps = data.get("capabilities") or []
    if not isinstance(caps, list):
        fail(findings, "capabilities must be a list")
        caps = []

    seen_ids: set[str] = set()
    cap_index: dict[str, dict] = {}
    for i, cap in enumerate(caps):
        if not isinstance(cap, dict):
            fail(findings, f"capabilities[{i}] must be a mapping")
            continue
        cap_id = cap.get("id")
        if not cap_id or not isinstance(cap_id, str):
            fail(findings, f"capabilities[{i}].id missing or not a string")
            continue
        if not ID_PATTERN.match(cap_id):
            fail(
                findings,
                f"capabilities[{i}].id {cap_id!r} must match CAP-* or MODULE-*",
            )
        if cap_id in seen_ids:
            fail(findings, f"capabilities[].id duplicate: {cap_id}")
        seen_ids.add(cap_id)
        cap_index[cap_id] = cap

        stage_id = cap.get("stage_id")
        if stage_id not in ALLOWED_STAGE_IDS:
            fail(
                findings,
                f"capabilities[{cap_id}].stage_id {stage_id!r} not in allowed set "
                f"(see references/stage-identification.md)",
            )

        blocking = cap.get("blocking") or {}
        if not isinstance(blocking, dict):
            fail(findings, f"capabilities[{cap_id}].blocking must be a mapping")
        else:
            for sub in ("tbds", "sme_pending", "gates"):
                val = blocking.get(sub)
                if val is None:
                    fail(
                        findings,
                        f"capabilities[{cap_id}].blocking.{sub} missing "
                        f"(use [] for empty)",
                    )
                elif not isinstance(val, list):
                    fail(
                        findings,
                        f"capabilities[{cap_id}].blocking.{sub} must be a list",
                    )

    # current_focus
    focus = data.get("current_focus") or {}
    if not isinstance(focus, dict):
        fail(findings, "current_focus must be a mapping")
    else:
        focus_cap = focus.get("capability_id")
        focus_stage = focus.get("stage_id")
        focus_card = focus.get("stage_card")

        if focus_cap is not None:
            if not isinstance(focus_cap, str) or not ID_PATTERN.match(focus_cap):
                fail(
                    findings,
                    f"current_focus.capability_id {focus_cap!r} must match CAP-* / MODULE-*",
                )
            elif focus_cap not in cap_index:
                fail(
                    findings,
                    f"current_focus.capability_id {focus_cap} not present in capabilities[]",
                )
            else:
                cap_stage = cap_index[focus_cap].get("stage_id")
                if focus_stage and focus_stage != cap_stage:
                    fail(
                        findings,
                        f"current_focus.stage_id ({focus_stage!r}) disagrees with "
                        f"capabilities[{focus_cap}].stage_id ({cap_stage!r}); "
                        f"trust the artifact and rewrite state",
                    )

        if focus_stage is not None and focus_stage not in ALLOWED_STAGE_IDS:
            fail(
                findings,
                f"current_focus.stage_id {focus_stage!r} not in allowed set",
            )

        if focus_card is not None and isinstance(focus_card, str):
            # Resolve relative to repo root
            card_path = REPO_ROOT / focus_card
            if not card_path.exists():
                # Also try resolving as orchestrator-relative
                alt = STAGE_CARDS_DIR.parent / focus_card.split("references/")[-1]
                if not alt.exists():
                    fail(
                        findings,
                        f"current_focus.stage_card {focus_card!r} does not resolve "
                        f"(tried {card_path} and {alt})",
                    )

    # history
    history = data.get("history") or []
    if not isinstance(history, list):
        fail(findings, "history must be a list")
        history = []

    prev_at: str | None = None
    for i, entry in enumerate(history):
        if not isinstance(entry, dict):
            fail(findings, f"history[{i}] must be a mapping")
            continue
        skill = entry.get("skill")
        if not skill or not isinstance(skill, str):
            fail(findings, f"history[{i}].skill missing or not a string")
        stage_after = entry.get("stage_after")
        if (
            stage_after is not None
            and stage_after not in ALLOWED_STAGE_IDS
            and stage_after not in ALLOWED_STAGE_AFTER_EXTRA
        ):
            fail(
                findings,
                f"history[{i}].stage_after {stage_after!r} not in allowed set "
                f"(or null or 'scan')",
            )
        at = entry.get("at")
        if not at:
            fail(findings, f"history[{i}].at missing (ISO 8601 timestamp required)")
        elif prev_at is not None and at < prev_at:
            fail(
                findings,
                f"history[{i}].at {at!r} is earlier than previous {prev_at!r} "
                f"(history must be append-only / non-decreasing)",
            )
        if at:
            prev_at = at

    return findings


def main() -> int:
    args = sys.argv[1:]
    template_mode = False
    if args and args[0] == "--template":
        template_mode = True
        args = args[1:]
    if len(args) > 1:
        print("Usage: python3 scripts/check-workflow-state.py [--template] [<path>]")
        return 2
    path = Path(args[0]) if args else Path("workflow-state.yaml")
    findings = validate(path, template_mode=template_mode)
    if not findings:
        print(f"OK: {path} conforms to workflow-state contract.")
        return 0
    print(f"FAIL: {len(findings)} finding(s) in {path}")
    for f in findings:
        print(f"  - {f}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
