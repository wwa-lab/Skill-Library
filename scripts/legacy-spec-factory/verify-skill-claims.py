#!/usr/bin/env python3
"""
Verify that skill status claims agree across:
  - Scorecard frontmatter (docs/reviews/*-scorecard.md)
  - docs/skill-status-truth-table.md
  - docs/runtime-matrix.md
  - README.md "Current Skill Scores" table

Exits 0 if no drift, non-zero with a report otherwise.

Run from project root:
    python3 scripts/verify-skill-claims.py
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEWS = ROOT / "docs" / "reviews"
TRUTH_TABLE = ROOT / "docs" / "skill-status-truth-table.md"
RUNTIME_MATRIX = ROOT / "docs" / "runtime-matrix.md"
SKILL_FAMILIES = ROOT / "docs" / "skill-families.md"
README = ROOT / "README.md"

VALID_STATUSES = {"not tested", "synced", "loaded", "executed", "passed", "failed"}
VALID_DECISIONS = {"field-pilot ready", "repo-ready", "repo-ready (provisional)", "revise", "reject", "unknown"}
RUNTIMES = ("codex", "claude_code", "opencode")


@dataclass
class Claim:
    """One skill's status as claimed by one source."""
    source: str
    skill: str
    version: str = ""
    static_score: float | None = None
    decision: str | None = None
    runtimes: dict[str, str] = field(default_factory=dict)  # codex/claude_code/opencode -> status
    last_verified: str | None = None


def parse_scorecard_frontmatter(path: Path) -> Claim | None:
    text = path.read_text()
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    body = text[3:end]
    fm: dict[str, str] = {}
    for line in body.splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()

    skill = fm.get("skill", "")
    if fm.get("status") == "superseded":
        return None  # ignore superseded scorecards

    claim = Claim(source=f"scorecard:{path.name}", skill=skill)
    claim.version = fm.get("scorecard_version", "")
    if "static_score" in fm and fm["static_score"] not in ("unknown", ""):
        try:
            claim.static_score = float(fm["static_score"])
        except ValueError:
            pass
    claim.decision = fm.get("decision")
    claim.last_verified = fm.get("last_verified")

    # Parse inline-table runtimes (look for `runtime: { status: X, ... }` lines)
    for rt in RUNTIMES:
        m = re.search(rf"^\s*{rt}:\s*\{{\s*status:\s*([a-z _]+?)\s*,", body, re.M)
        if m:
            claim.runtimes[rt] = m.group(1).strip()
    return claim


def parse_truth_table() -> list[Claim]:
    text = TRUTH_TABLE.read_text()
    claims = []
    for line in text.splitlines():
        # Match table rows: | `legacy-x` | vX.Y.Z | 9.NN | decision | rt | rt | rt | date | [link] |
        m = re.match(
            r"^\|\s*`(legacy-[a-z0-9-]+)`\s*\|\s*(v\d+\.\d+\.\d+)\s*\|\s*([\d.]+|n/a)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|",
            line,
        )
        if not m:
            continue
        skill, ver, score_s, decision, codex, claude, opencode, last_v = m.groups()
        claim = Claim(source="truth-table", skill=skill, version=ver, decision=decision.strip())
        try:
            claim.static_score = float(score_s)
        except ValueError:
            pass
        claim.runtimes = {"codex": codex.strip(), "claude_code": claude.strip(), "opencode": opencode.strip()}
        claim.last_verified = last_v.strip()
        claims.append(claim)
    return claims


def parse_runtime_matrix() -> list[Claim]:
    text = RUNTIME_MATRIX.read_text()
    claims = []
    for line in text.splitlines():
        # Match: | `skill` | vX.Y.Z | codex | claude | opencode | [scorecard](...) | date | notes |
        m = re.match(
            r"^\|\s*`(legacy-[a-z0-9-]+)`\s*\|\s*(v\d+\.\d+\.\d+)\s*\|\s*([a-z _]+?)\s*\|\s*([a-z _]+?)\s*\|\s*([a-z _]+?)\s*\|\s*[^|]*\|\s*([^|]+?)\s*\|",
            line,
        )
        if not m:
            continue
        skill, ver, codex, claude, opencode, last_v = m.groups()
        claim = Claim(source="runtime-matrix", skill=skill, version=ver)
        claim.runtimes = {"codex": codex.strip(), "claude_code": claude.strip(), "opencode": opencode.strip()}
        claim.last_verified = last_v.strip()
        claims.append(claim)
    return claims


def parse_readme_scores() -> list[Claim]:
    text = README.read_text()
    in_section = False
    claims = []
    for line in text.splitlines():
        if "### Current Skill Scores" in line:
            in_section = True
            continue
        if in_section and line.startswith("### "):
            break
        if not in_section:
            continue
        # Match: | `skill` | [v0.1.0 scorecard](...) | static | current | status | reason |
        m = re.match(
            r"^\|\s*`(legacy-[a-z0-9-]+)`\s*\|\s*\[v[\d.]+[^\]]*\]\([^)]+\)\s*\|\s*([\d.]+|[\d.]+ expected)\s*\|\s*([\d.]+)\s*\|\s*([^|]+?)\s*\|",
            line,
        )
        if not m:
            continue
        skill, static_s, current_s, status = m.groups()
        claim = Claim(source="readme", skill=skill)
        try:
            claim.static_score = float(static_s.split()[0])
        except ValueError:
            pass
        claim.decision = status.strip().lower().replace("repo-ready;", "repo-ready").split(";")[0].strip()
        claims.append(claim)
    return claims


def parse_skill_families() -> set[str]:
    """Return set of skill names that appear in docs/skill-families.md table rows."""
    text = SKILL_FAMILIES.read_text()
    skills = set()
    # Match `legacy-foo` occurrences in markdown link targets pointing to skills/
    for m in re.finditer(r"\[`(legacy-[a-z0-9-]+)`\]\(\.\./skills/", text):
        skills.add(m.group(1))
    return skills


def collect_scorecards() -> list[Claim]:
    out = []
    for path in sorted(REVIEWS.glob("legacy-*-scorecard.md")):
        c = parse_scorecard_frontmatter(path)
        if c:
            out.append(c)
    return out


def check_drift() -> list[str]:
    issues: list[str] = []
    scorecards = collect_scorecards()
    truth = parse_truth_table()
    matrix = parse_runtime_matrix()
    readme = parse_readme_scores()
    families = parse_skill_families()

    # Index by skill (current versions only)
    sc_by_skill = {c.skill: c for c in scorecards}
    truth_by_skill = {c.skill: c for c in truth}
    matrix_by_skill = {c.skill: c for c in matrix}
    readme_by_skill = {c.skill: c for c in readme}

    all_skills = set(sc_by_skill) | set(truth_by_skill) | set(matrix_by_skill) | set(readme_by_skill)

    for skill in sorted(all_skills):
        sc = sc_by_skill.get(skill)
        tt = truth_by_skill.get(skill)
        mx = matrix_by_skill.get(skill)
        rm = readme_by_skill.get(skill)

        # Check 1: every skill must have a current scorecard
        if not sc:
            issues.append(f"[{skill}] no current scorecard found in docs/reviews/")
            continue

        # Check 2: scorecard frontmatter must have valid decision
        if sc.decision and sc.decision not in VALID_DECISIONS:
            issues.append(f"[{skill}] scorecard decision '{sc.decision}' not in {VALID_DECISIONS}")

        # Check 3: scorecard runtime statuses must be valid
        for rt, st in sc.runtimes.items():
            if st not in VALID_STATUSES:
                issues.append(f"[{skill}] scorecard {rt} status '{st}' not in {VALID_STATUSES}")

        # Check 4: field-pilot ready requires all three runtimes at passed
        if sc.decision == "field-pilot ready":
            non_passed = [rt for rt, st in sc.runtimes.items() if st != "passed"]
            if non_passed:
                issues.append(
                    f"[{skill}] scorecard claims 'field-pilot ready' but runtimes not all passed: {non_passed} ({sc.runtimes})"
                )

        # Check 5: matrix vs scorecard runtime status
        if mx:
            if mx.version != sc.version:
                issues.append(f"[{skill}] matrix version {mx.version} != scorecard version {sc.version}")
            for rt in RUNTIMES:
                sc_st = sc.runtimes.get(rt)
                mx_st = mx.runtimes.get(rt)
                if sc_st and mx_st and sc_st != mx_st:
                    issues.append(f"[{skill}] runtime {rt} mismatch: scorecard={sc_st} matrix={mx_st}")
        else:
            issues.append(f"[{skill}] missing from runtime-matrix.md")

        # Check 6: truth table vs scorecard
        if tt:
            if tt.version != sc.version:
                issues.append(f"[{skill}] truth-table version {tt.version} != scorecard version {sc.version}")
            if sc.static_score is not None and tt.static_score is not None and abs(tt.static_score - sc.static_score) > 0.01:
                issues.append(f"[{skill}] static_score mismatch: scorecard={sc.static_score} truth-table={tt.static_score}")
            for rt in RUNTIMES:
                sc_st = sc.runtimes.get(rt)
                tt_st = tt.runtimes.get(rt)
                if sc_st and tt_st and sc_st != tt_st:
                    issues.append(f"[{skill}] runtime {rt} mismatch: scorecard={sc_st} truth-table={tt_st}")
        else:
            issues.append(f"[{skill}] missing from skill-status-truth-table.md")

        # Check 7: README static score vs scorecard
        if rm and sc.static_score is not None and rm.static_score is not None:
            if abs(rm.static_score - sc.static_score) > 0.01:
                issues.append(f"[{skill}] static_score mismatch: scorecard={sc.static_score} README={rm.static_score}")

        # Check 8: skill must appear in skill-families.md
        if skill not in families:
            issues.append(f"[{skill}] missing from docs/skill-families.md")

    # Check 9: skill-families.md should not list a skill that has no scorecard
    sc_skills = {c.skill for c in scorecards}
    for fam_skill in sorted(families - sc_skills):
        issues.append(f"[{fam_skill}] listed in skill-families.md but no current scorecard exists")

    return issues


def main():
    issues = check_drift()
    if not issues:
        print("OK: all skill claims agree across scorecards, truth table, runtime matrix, and README.")
        return 0
    print(f"DRIFT DETECTED: {len(issues)} issue(s)\n")
    for i, msg in enumerate(issues, 1):
        print(f"  {i}. {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
