#!/bin/bash
# Smoke test runner for legacy-ibmi-module-analyzer v0.1.4
# Runs positive case across all three runtimes
# Usage: ./scripts/smoke-test-module-analyzer.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

POSITIVE_PROMPT="Use /legacy-ibmi-module-analyzer. Contract-only no-write smoke test. Do not create or edit files. Do not inspect or rely on the actual workspace filesystem; use only the scenario text below and the skill contract. User input: I have three approved flow analyses (FLOW-AUTH-001, FLOW-BATCH-001, FLOW-MANUAL-001), approved program analyses for all programs, an approved inventory with the AUTH-MODULE scope confirmed, and BAU notes from the Module Owner. Module slug is AUTH-MODULE, business name is \"Authorization Processing\". Help me synthesize the four-view module analysis. Return the module-overview.md and all four views (01-operation-flow.md through 04-data-flow.md) following the output contract format. Each view must include ## Mermaid Flow Diagram with a fenced Mermaid flowchart before evidence or traceability tables; do not return table-only flow views."

passes_positive_contract() {
  local result_file="$1"
  local mermaid_sections
  local flowchart_blocks

  mermaid_sections=$(grep -c "## Mermaid Flow Diagram" "$result_file" || true)
  flowchart_blocks=$(grep -c "flowchart" "$result_file" || true)

  grep -q "MODULE-AUTH-MODULE-001" "$result_file" &&
    grep -q "module-overview" "$result_file" &&
    grep -q "01-operation-flow" "$result_file" &&
    grep -q "02-system-flow" "$result_file" &&
    grep -q "03-program-flow" "$result_file" &&
    grep -q "04-data-flow" "$result_file" &&
    [ "$mermaid_sections" -ge 4 ] &&
    [ "$flowchart_blocks" -ge 4 ]
}

echo -e "${BLUE}=== legacy-ibmi-module-analyzer v0.1.4 Smoke Test ===${NC}\n"

# Pre-test checks
echo -e "${BLUE}Pre-Test Checks:${NC}"
echo "Checking drift..."
scripts/sync-skills.sh --target all --check || {
  echo "Drift detected. Running sync..."
  scripts/sync-skills.sh --target all
}
echo -e "${GREEN}✓ Drift check passed${NC}\n"

# Test 1: Codex CLI
echo -e "${BLUE}Test 1: Codex CLI (gpt-5.4-mini)${NC}"
echo "Running: codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini"
if codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini "$POSITIVE_PROMPT" > /tmp/codex-result.txt 2>&1; then
  echo -e "${GREEN}✓ Codex CLI: executed${NC}"
  CODEX_STATUS="executed"
  if passes_positive_contract /tmp/codex-result.txt; then
    CODEX_STATUS="passed"
    echo -e "${GREEN}✓ Codex CLI: passed (output structure + Mermaid diagrams correct)${NC}"
  fi
else
  echo "✗ Codex CLI: failed or not available"
  CODEX_STATUS="synced"
fi
echo ""

# Test 2: Claude Code (local via skill)
echo -e "${BLUE}Test 2: Claude Code (haiku, Read-only)${NC}"
echo "Running: claude -p --model haiku --permission-mode dontAsk --tools Read"
if claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 "$POSITIVE_PROMPT" > /tmp/claude-result.txt 2>&1; then
  echo -e "${GREEN}✓ Claude Code: executed${NC}"
  CLAUDE_STATUS="executed"
  if passes_positive_contract /tmp/claude-result.txt; then
    CLAUDE_STATUS="passed"
    echo -e "${GREEN}✓ Claude Code: passed (output structure + Mermaid diagrams correct)${NC}"
  fi
else
  echo "✗ Claude Code: failed or not available"
  CLAUDE_STATUS="synced"
fi
echo ""

# Test 3: OpenCode
echo -e "${BLUE}Test 3: OpenCode (minimax-m2.5-free)${NC}"
echo "Running: opencode run -m opencode/minimax-m2.5-free"
if command -v opencode &> /dev/null; then
  if opencode run -m opencode/minimax-m2.5-free "$POSITIVE_PROMPT" > /tmp/opencode-result.txt 2>&1; then
    echo -e "${GREEN}✓ OpenCode: executed${NC}"
    OPENCODE_STATUS="executed"
    if passes_positive_contract /tmp/opencode-result.txt; then
      OPENCODE_STATUS="passed"
      echo -e "${GREEN}✓ OpenCode: passed (output structure + Mermaid diagrams correct)${NC}"
    fi
  else
    echo "✗ OpenCode: failed"
    OPENCODE_STATUS="synced"
  fi
else
  echo "⚠ OpenCode: not installed or not in PATH"
  OPENCODE_STATUS="synced"
fi
echo ""

# Summary
echo -e "${BLUE}=== Smoke Test Results ===${NC}"
echo "Codex CLI:    $CODEX_STATUS"
echo "Claude Code:  $CLAUDE_STATUS"
echo "OpenCode:     $OPENCODE_STATUS"
echo ""

if [ "$CODEX_STATUS" = "passed" ] && [ "$CLAUDE_STATUS" = "passed" ] && [ "$OPENCODE_STATUS" = "passed" ]; then
  echo -e "${GREEN}✓ All tests PASSED - ready for v0.1.4 scorecard${NC}"
  exit 0
else
  echo -e "${BLUE}⚠ Some tests did not reach 'passed' status (see above for details)${NC}"
  echo "Next step: Review results and update docs/runtime-matrix.md manually"
  exit 1
fi
