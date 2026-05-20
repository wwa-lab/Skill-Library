#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SKILL_DIR="$ROOT/skills/legacy-modernization-decision-writer"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

require_file() {
  [[ -f "$SKILL_DIR/$1" ]] || fail "missing $1"
}

require_file "SKILL.md"
require_file "references/decision-rules.md"
require_file "references/anti-hallucination.md"
require_file "templates/modernization-decisions.yaml"
require_file "templates/decision-record.md"
require_file "templates/decision-review.md"
require_file "templates/traceability.md"
require_file "examples/decision-positive-ORDERS-001.md"
require_file "examples/decision-negative-ORDERS-ANTI.md"

if grep -R --exclude 'smoke-test.sh' "needs_arch_review" "$SKILL_DIR" >/dev/null; then
  fail "unregistered review_status found: needs_arch_review"
fi

if grep -R "DECPKG-" "$SKILL_DIR/templates" "$SKILL_DIR/examples" "$SKILL_DIR/references" >/dev/null; then
  fail "unregistered ID prefix found: DECPKG-*"
fi

if grep -R --exclude 'smoke-test.sh' "review_status: .*needs_sme_review .*needs_arch_review" "$SKILL_DIR" >/dev/null; then
  fail "template still advertises removed review status"
fi

if grep -n '^---$' "$SKILL_DIR/templates/modernization-decisions.yaml" >/dev/null; then
  fail "YAML template contains Markdown document separators"
fi

if ! grep -q "may mint \`DEC-\\*\`, \`TBD-\\*\`, and \`STEP-\\*\`" "$SKILL_DIR/SKILL.md"; then
  fail "SKILL.md missing explicit ID minting policy"
fi

if ! grep -q "decision-writer does not mint AC-\\*" "$SKILL_DIR/templates/decision-record.md"; then
  fail "decision-record template must state AC-* is not minted here"
fi

echo "PASS: legacy-modernization-decision-writer smoke checks"
