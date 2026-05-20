# Program Analyzer Smoke Test Execution Guide

为 `legacy-ibmi-program-analyzer` v0.1.0 运行三个运行时的烟雾测试，从 9.0 升级至 9.5。

## 前置检查

```bash
# 确认适配器已同步
scripts/sync-skills.sh --target all --check
# 期望：所有行返回 OK
```

## Positive Scenario（正面场景）

测试输入：RPGLE CREDITCHK 程序（OBJ-CREDIT-VALIDATION-001）

源代码位置：`skills/legacy-ibmi-program-analyzer/examples/simple-crud-rpgle/input-source.txt`

期望输出：`skills/legacy-ibmi-program-analyzer/examples/simple-crud-rpgle/program-analysis.md`

### Pass Criteria（通过标准）

分析输出必须包含：

- ✅ **Metadata**：Program ID、Program Type (RPGLE)、Entry Points
- ✅ **Entry Points & Parameters**：CreditChk 过程，参数 (CustID, RequestAmount)，返回 Decision Code
- ✅ **Control Flow**：CHAIN on CREDFILE，IF/ELSE 分支在信用限额检查上
- ✅ **File I/O**：CREDFILE 带 CHAIN 操作；CUSTFILE 标记为已声明但未使用
- ✅ **External Calls**：None（正确识别没有外部 CALL）
- ✅ **Evidence Tagging**：所有主要行为标记为 `confirmed_from_code`
- ✅ **Status**：`draft` 或 `needs_sme_review`（不是 `blocked_pending_source`）
- ✅ **No hallucinations**：没有为完整源代码部分创建 TBD

---

## Runtime 1: Codex CLI

```bash
cd /Users/leo/wwa-lab/GitHub/legacy-spec-factory

codex exec -C . -s read-only --ephemeral -m gpt-5.4-mini \
  "Use /legacy-ibmi-program-analyzer.

User input:
I have RPGLE source for CREDITCHK (OBJ-CREDIT-VALIDATION-001). It validates customer credit limits. Analyze its control flow, file I/O, entry points, and external calls.

Provide the analysis in the output contract format."
```

**Record Result:**
- [ ] Discovery: Skill found and loaded
- [ ] Trigger: Execution completed with correct output shape
- [ ] Pass Criteria: All requirements met (see above)
- **Status to record:** `passed` | `executed` | `synced`
- **Date:** YYYY-MM-DD
- **Model used:** gpt-5.4-mini

---

## Runtime 2: Claude Code

```bash
cd /Users/leo/wwa-lab/GitHub/legacy-spec-factory

claude -p --model haiku --permission-mode dontAsk --tools Read --max-budget-usd 0.20 \
  "Use /legacy-ibmi-program-analyzer.

User input:
I have RPGLE source for CREDITCHK (OBJ-CREDIT-VALIDATION-001). It validates customer credit limits. Analyze its control flow, file I/O, entry points, and external calls.

Provide the analysis in the output contract format."
```

**Record Result:**
- [ ] Discovery: Skill found and loaded
- [ ] Trigger: Execution completed with correct output shape
- [ ] Pass Criteria: All requirements met (see above)
- **Status to record:** `passed` | `executed` | `synced`
- **Date:** YYYY-MM-DD
- **Model used:** haiku

---

## Runtime 3: OpenCode

```bash
cd /Users/leo/wwa-lab/GitHub/legacy-spec-factory

opencode run -m opencode/minimax-m2.5-free \
  "Use /legacy-ibmi-program-analyzer.

User input:
I have RPGLE source for CREDITCHK (OBJ-CREDIT-VALIDATION-001). It validates customer credit limits. Analyze its control flow, file I/O, entry points, and external calls.

Provide the analysis in the output contract format."
```

**Record Result:**
- [ ] Discovery: Skill found and loaded
- [ ] Trigger: Execution completed with correct output shape
- [ ] Pass Criteria: All requirements met (see above)
- **Status to record:** `passed` | `executed` | `synced`
- **Date:** YYYY-MM-DD
- **Model used:** opencode/minimax-m2.5-free

---

## Negative Scenario（可选但推荐）

测试输入：不完整的 COBOL 源代码

源代码位置：`skills/legacy-ibmi-program-analyzer/examples/incomplete-source-negative/input-source.txt`

期望输出：`skills/legacy-ibmi-program-analyzer/examples/incomplete-source-negative/expected-review-notes.md`

### Pass Criteria（通过标准）

- ✅ **Status**：`blocked_pending_source`（源代码不完整阻止分析）
- ✅ **Does NOT invent**：没有发明缺失的程序、子程序体或 CALL 语句
- ✅ **Blocking TBDs**：为每个缺失源片段创建了阻塞 TBD
- ✅ **Documents what IS visible**：评论表明 GET-BASE-RATE 调用但代码未显示
- ✅ **Refuses to guess**：没有猜测程序行为而不使用源代码

---

## 更新文档

所有三个运行时都通过后：

### 1. 更新 `docs/runtime-matrix.md`

```markdown
| `legacy-ibmi-program-analyzer` | v0.1.0 | passed | passed | passed | Smoke tests passed on 2026-05-14 (Codex/gpt-5.4-mini, Claude Code/haiku, OpenCode/minimax-m2.5-free). Lifted from 9.0 to 9.5 field-pilot ready. |
```

### 2. 更新 `SKILL.md` Version History

```markdown
- v0.1.0 (2026-05-14): Runtime smoke test passed in Codex CLI (gpt-5.4-mini), Claude Code (haiku), and OpenCode (minimax-m2.5-free). Lifted from 9.0 to 9.5.
```

### 3. 更新 scorecard decision

```markdown
- decision:
  - [ ] reject
  - [ ] revise
  - [ ] repo-ready
  - [x] field-pilot ready

Final score after cap: **9.5 / 10**
```

---

## Commit Changes

```bash
git add docs/runtime-matrix.md skills/legacy-ibmi-program-analyzer/SKILL.md

git commit -m "feat: program-analyzer v0.1.0 smoke tests passed — lifted to field-pilot ready (9.5)

Smoke test execution results:
- Codex CLI (gpt-5.4-mini): passed [date]
- Claude Code (haiku): passed [date]
- OpenCode (minimax-m2.5-free): passed [date]

All pass criteria met for positive scenario.
No files created or edited during execution.

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| Skill not found | 适配器未同步 | 运行 `scripts/sync-skills.sh --target all` |
| Command hangs | 交互式 skill 等待输入 | 尝试在 IDE 中使用 skill，而不是 CLI |
| Output shape mismatch | 模型版本差异 | 检查是否符合基本契约（metadata, entry points, file I/O 等） |
| TBDs created for complete source | Anti-hallucination rule 被触发 | 验证源代码是完整的；如果不完整，使用负面场景 |

---

**准备好后报告结果，我会更新 runtime-matrix.md 和 scorecard。**
