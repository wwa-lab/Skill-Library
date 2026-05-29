# Legacy System Modernization Pipeline Alignment

本文档对标老板提出的IBM i旧系统现代化流程，与Legacy Spec Factory repo的skills进行对应分析。

> 边界更新：公司内部正在建设全字典中心。Legacy Spec Factory 不重复建设全域字段主数据平台，而是消费全字典中心的标准字段、视图边界和口径版本，并负责把 legacy 代码、运行时证据、SME 判断反推成可审计的 spec、traceability 和 handoff。对接契约见
> [`dictionary-center-integration-contract.md`](dictionary-center-integration-contract.md)。

## 老板提出的现代化流程

```
数据字典搭建 → 业务字段切片 → 客户&内部用户视图划分
    ↓
Program Flow 逐字段梳理计算取信逻辑错误
    ↓
依托视图 + 字典 + 算法 还原全系统业务程序流程
    ↓
数据实测 + 经验整合 + 冗余清理
    ↓
已知推未知 → 未知反噯已知 (2-3轮螺旋迭代)
    ↓
业务SME + 运营SME + IT SME 三方联合评审定稿
    ↓
全域标准统一固化，全场景落地使用
```

## 我们的Pipeline对应关系

| 老板的步骤 | 描述 | 我们的Skills | 输出物 | 是否已实现 |
|-----------|------|-------------|--------|----------|
| **Step 1: 数据字典搭建** | 全字典中心承接标准字段、字段口径、视图边界；repo 负责消费字典并绑定 legacy 证据 | 公司全字典中心（外部平台）<br>`legacy-ibmi-evidence-intake` (evidence gate)<br>`legacy-ibmi-inventory` (程序/文件列表)<br>`legacy-ibmi-data-model-analyzer` (legacy字段/数据关系证据) | 字典中心字段包<br>`evidence/manifest.yaml`<br>`01_inventory/inventory.yaml`<br>`03_data_models/<DATA-SLUG>/` | ✅ 边界明确<br>repo侧需按实际字段包补贯穿 |
| **Step 2: Program Flow逐字段梳理** | 对程序级计算逻辑、取信规则、变量流进行证据化分析；字段级八类逻辑矩阵后续增强 | `legacy-ibmi-program-analyzer` (单程序深度分析)<br>`legacy-ibmi-screen-report-analyzer` (屏幕/报表逻辑) | `02_programs/<CAP>/program-analysis-<OBJ-ID>.md`<br>`03_screen_reports/<OBJECT-SLUG>/` | ✅ 程序级已实现<br>八类矩阵暂缓 |
| **Step 3: 还原全系统业务流程** | 通过视图 + 字典 + 算法还原业务流程全貌 | `legacy-ibmi-flow-analyzer` (事务流跨程序分析)<br>`legacy-ibmi-module-analyzer` (4视图综合分析) | `03_flows/<CAP>/flow-<FLOW-SLUG>.md`<br>`04_modules/<MODULE-SLUG>/` (Operation/System/Program/Data 4视图) | ✅ 已实现<br>repo-ready (9.0-9.6) |
| **Step 4: 数据实测 + 经验整合** | 基于运行时证据、SME经验、代码验证进行清理 | `legacy-ibmi-runtime-evidence-miner` (job log/spool evidence)<br>`legacy-ibmi-flow-analyzer` (runtime evidence)<br>`legacy-ibmi-module-analyzer` (synthesize views)<br>`legacy-sme-review-facilitator` (SME确认) | `runtime-evidence.jsonl`<br>Flow + Module分析中的`evidence_tags`<br>TBD和假设列表 | ✅ 已实现<br>runtime miner field-pilot ready |
| **Step 5: 2-3轮螺旋迭代** | 已知推未知，未知反噯已知，循环验证 | `legacy-modernization-orchestrator` (routing)<br>`legacy-sme-review-facilitator` (决策记录)<br>`legacy-step-validator` (质量检查) | 迭代的版本控制<br>决策日志<br>验证报告 | ✅ 已实现<br>routing + governance |
| **Step 6: 三方SME评审定稿** | 业务SME + 运营SME + IT SME联合评审 | `legacy-sme-review-facilitator` (评审包准备)<br>`legacy-brd-writer` (BRD文档)<br>`legacy-spec-writer` (Spec定稿) | `07_sme_reviews/<CAP>/<REVIEW>/`<br>`05_brds/<CAPABILITY>/brd.md`<br>`05_specs/<CAPABILITY>/spec.yaml` | ✅ 已实现<br>field-pilot ready (9.55-9.63) |
| **Step 7: 标准统一固化，落地使用** | 标准化、冻结spec、交付给下游系统 | `legacy-traceability-packager` (追踪)<br>`legacy-brd-to-sdd-handoff` (交付)<br>`legacy-golden-master-test-planner` (等价性测试) | `06_traceability_packages/`<br>`06_sdd_handoffs/<CAP>/`<br>`06_quality/<CAP>/golden-master-tests.yaml` | ✅ 已实现<br>field-pilot ready (9.51-9.59) |

## 详细能力对标

### 数据字典和业务字段切片 (Step 1)

**老板需求**: 完整的数据字典、字段定义、客户视图 vs 内部用户视图。

**边界定位**: 全域标准字段、字段口径、字段 owner、客户/内部/后台视图边界由公司全字典中心承接。Legacy Spec Factory 只保留 legacy 侧字段证据、DDS/DB2 映射、屏幕/报表出现位置、程序读写证据和后续 `spec.yaml` 追踪，不在本 repo 内重复建设完整字段主数据平台。

**我们的实现**:
- `legacy-ibmi-inventory` → 程序、文件、表、屏幕、报表全量发现
- `legacy-ibmi-data-model-analyzer` → PF/LF/DDS 数据模型分析，字段语义，访问路径，CRUD生命周期
- `legacy-ibmi-screen-report-analyzer` → DSPF/PRTF 屏幕字段和报表字段映射（用户视图）
- `legacy-ibmi-evidence-intake` → 证据源合法性审查，敏感数据脱敏
- 对接契约 → `docs/dictionary-center-integration-contract.md` 定义 `standard_field_id`、字段包版本、视图分类、drift 处理和贯穿规则

**输出**: 字典中心字段包（外部） + `inventory.yaml`, `03_data_models/`, `03_screen_reports/`

---

### 逐字段梳理计算取信逻辑 (Step 2)

**老板需求**: 对每个Program的计算逻辑、指标取信规则、变量转换链进行字段级分析。

**当前取舍**: 先用 program/screen/report/flow/module 分析覆盖程序级证据和关键字段链路；暂不新增 `legacy-ibmi-field-logic-analyzer`。文章中的八类逻辑矩阵（数据来源、基础赋值、算术计算、业务联动、数据转换、汇总统计、条件判断、结果回写）保留为后续增强项，等全字典中心输入格式和真实项目样本稳定后再做。

**我们的实现**:
- `legacy-ibmi-program-analyzer` 提供:
  - 调用图 (call graph)
  - 文件I/O操作 (CRUD matrix)
  - 数据流 (variable tracking)
  - 指标逻辑 (business logic)
  - 错误处理 (error paths)

**输出**: `02_programs/<CAP>/program-analysis-<OBJ-ID>.md`

**限制**: 程序分析仍以源码为主；运行时证据可通过 `legacy-ibmi-runtime-evidence-miner` 补充，但需要用户先提供已审批、已脱敏的 job log / spool evidence。字段级八类逻辑矩阵暂不作为当前 skill 交付物。

---

### 还原全系统业务程序流程 (Step 3)

**老板需求**: 通过视图 + 字典 + 算法把单个程序的理解聚合成端到端的业务流程

**我们的实现**:
- `legacy-ibmi-flow-analyzer` → 跨程序事务流分析 (one flow per transaction)
- `legacy-ibmi-module-analyzer` → 4视图综合分析:
  1. **Operation Flow** - 业务操作流程，BAU (Business-as-Usual)
  2. **System Flow** - 系统级数据流，调度，消息队列
  3. **Program Flow** - 程序级调用链和CRUD
  4. **Data Flow** - 数据模型和关系

**输出**:
- `03_flows/<CAP>/flow-<FLOW-SLUG>.md` (事务级)
- `04_modules/<MODULE-SLUG>/` (模块级4视图)

---

### 数据实测 + 经验整合 + 冗余清理 (Step 4)

**老板需求**: 用运行时证据验证代码分析，整合SME经验，清理历史技术债

**我们的实现**:
- `legacy-ibmi-flow-analyzer` 收集:
  - `confirmed_from_code` - 代码确认
  - `observed_in_runtime` - 运行时日志/spool
  - `confirmed_by_sme` - SME确认
  - `strongly_inferred` - 强推断
  - `needs_sme_review` - 需要评审的假设

- `legacy-sme-review-facilitator` → 记录SME决策，标记冗余和遗留技术债
- `legacy-ibmi-evidence-intake` → 敏感数据脱敏后保存证据
- `legacy-ibmi-runtime-evidence-miner` → 从已审批的 job logs / spool files 提取 `observed_in_runtime` JSONL 证据

**限制**: 仍需要用户提供实际运行时日志和样本数据；runtime miner 只处理 evidence-intake 已批准且已脱敏的证据。

---

### 2-3轮螺旋迭代 (Step 5)

**老板需求**: 已知推未知 → 未知反噯已知，循环验证，每轮发现新问题并回溯

**我们的实现**:
- `legacy-modernization-orchestrator` v0.2.3:
  - 询问当前阶段 (scope / intake / inventory / analysis / synthesis / approval / handoff)
  - 识别阻塞条件
  - 推荐下一步 skill
  - 对散落文档 / Function Spec / Technical Design / Program Spec / File Spec 等输入做质量分层路由：资料强/部分时进入 flow normalization，资料稀疏但授权可读时进入 source-quality triage；如果 owner 确认无法补料并接受风险，则以 warning/TBD 方式进入 context intake
  - 支持返回前一步重新分析

- `legacy-step-validator` → 质量检查，识别blocking/warning/ok
- `legacy-sme-review-facilitator` → 记录决策日志，追踪疑问
- GitHub PR workflow → 版本控制，评审轨迹

**实现方式**: 用户通过 git branches 迭代，每轮 PR 包含新发现和回复。

---

### 三方SME评审定稿 (Step 6)

**老板需求**: 业务SME + 运营SME + IT SME 联合评审，签署最终版本

**我们的实现**:
- `legacy-sme-review-facilitator` v0.1.0 (field-pilot ready):
  - 准备评审包
  - 记录评审会议决策
  - 捕获签名 (sign-offs)
  - 路由后续发现

- `legacy-brd-writer` v0.1.1 → BRD (Business Requirements Document)，包含:
  - Observed Behavior (观察到的行为)
  - Inferred Business Rules (推断的业务规则)
  - Open Questions (未解决的问题)

- `legacy-spec-writer` v0.1.0 → `spec.yaml` + `spec.md`:
  - 最终需求合同
  - 可追踪的ID (`BR-*`, `AC-*`, `DEC-*`)
  - 证据链接

**输出**:
- `07_sme_reviews/<CAP>/<REVIEW>/` (评审记录)
- `05_brds/<CAPABILITY>/` (BRD文档)
- `05_specs/<CAPABILITY>/` (最终spec)

---

### 标准统一固化，全场景落地 (Step 7)

**老板需求**: 冻结标准，生成下游系统能消费的交付物（SDD、测试、代码线索）

**我们的实现**:
- `legacy-traceability-packager` v0.1.1 → 审计追踪:
  - 证据 → BRD → Spec → 测试 → 代码 的完整链路
  - `06_traceability_packages/`

- `legacy-brd-to-sdd-handoff` v0.1.0 → SDD (Solution Design Document) 交付:
  - 5文件交付包 (`sdd-handoff.yaml`, `sdd-handoff.md`, `atlas-context-pack.json`, etc.)
  - 交付给 Atlas Engineering Delivery Hub (下游Java/cloud SDLC agent)

- `legacy-golden-master-test-planner` v0.1.0 → 等价性测试计划:
  - Golden master tests (`TC-*`)
  - Old-vs-new 对标
  - 6个质量文件 (测试yaml、md、checklist等)

**输出**:
- `06_sdd_handoffs/<CAP>/` (下游交付物)
- `06_quality/<CAP>/golden-master-tests.yaml` (测试计划)

---

## 整体覆盖度评分

| 维度 | 覆盖度 | 状态 | 备注 |
|-----|-------|------|-----|
| **Step 1: 数据字典** | 90% | ✅ 分工明确 | 全字典中心承接标准字段；repo 侧已补对接契约，后续按实际字段包贯穿 `standard_field_id` |
| **Step 2: 程序分析** | 85% | ✅ 程序级已实现 | 八类字段逻辑矩阵暂缓；需要smoke测试完成 |
| **Step 3: 流程还原** | 85% | ✅ 已实现 | module-analyzer需完成smoke和strict-pass |
| **Step 4: 实测+整合** | 85% | ✅ 已实现 | runtime-evidence-miner 已实现；仍需用户提供已脱敏样本 |
| **Step 5: 螺旋迭代** | 95% | ✅ 已实现 | orchestrator v0.2.0 + step-validator |
| **Step 6: 三方评审** | 95% | ✅ 已实现 | sme-review-facilitator, brd-writer, spec-writer都field-pilot ready |
| **Step 7: 交付落地** | 100% | ✅ 已实现 | handoff, traceability, golden-master-tester都field-pilot ready |
| **总体** | **90%** | ✅ **MVP+ ready（字段中心外置）** | repo 负责反推、证据、SME、spec/handoff；全字典中心负责标准字段治理 |

---

## 未来优化点 (Planned but not MVP)

1. **Runtime evidence integration smoke** → 验证 program/flow/module analyzer 对 `runtime-evidence.jsonl` 的消费链路
2. **Dictionary center ID propagation** → 在真实字段包格式稳定后，把 `standard_field_id` 贯穿 data/screen/program/flow/module/spec/traceability
3. **`legacy-equivalence-test-generator`** → 从golden master test plan生成可执行的old-vs-new对标测试
4. **Cross-module spec synthesis** → 多个模块的规范聚合
5. **Field eight-logic matrix** → 暂缓新增 `legacy-ibmi-field-logic-analyzer`，待全字典中心和样本项目稳定后再评估

---

## 与老板期望的对应检查清单

- [x] 数据字典搭建 → 公司全字典中心 + repo legacy证据映射（`inventory.yaml` + `data-model-analyzer`）
- [x] 业务字段切片 → 字典中心标准字段 + `program-analyzer` / `screen-report-analyzer` 补 legacy 出现位置
- [x] 客户&内部视图划分 → 字典中心提供视图边界，repo 通过 screen/report/runtime 证据校验实际展示
- [x] Program Flow逐字段梳理 → `program-analyzer` 详细的CRUD/flow/error矩阵
- [x] 计算取信逻辑 → `program-analyzer` 的business logic和data flow小节；八类字段逻辑矩阵暂缓
- [x] 依托视图+字典还原 → `flow-analyzer` + `module-analyzer` 的4视图综合
- [x] 数据实测 → `evidence-intake` + `sme-review-facilitator` 记录的证据源
- [x] 经验整合 → `sme-review-facilitator` 的decision log
- [x] 冗余清理 → `brd-writer` 过滤掉技术债，保留业务规则
- [x] 2-3轮螺旋迭代 → `modernization-orchestrator` routing + git PR workflow
- [x] 已知推未知 → `flow-analyzer` 的TBD标记和cross-reference
- [x] 未知反噯已知 → `sme-review-facilitator` 决策日志记录反馈
- [x] 三方SME评审 → `sme-review-facilitator` 的评审包和sign-off
- [x] 全域标准统一 → `spec.yaml` 作为唯一source of truth
- [x] 全场景落地使用 → `brd-to-sdd-handoff` + downstream Java/cloud agents

---

## 建议的使用流程

对于客户要运行的一个业务能力（如Credit Check、Order Entry）：

```
1. 初始化scope + evidence intake
   $ /legacy-modernization-orchestrator
   → "stage: scope; next: evidence-intake"

2. 收集并合法化evidence
   $ /legacy-ibmi-evidence-intake
   → evidence/manifest.yaml

3. 发现程序/文件/表全景
   $ /legacy-ibmi-inventory
   → 01_inventory/inventory.yaml

4. 并行分析（可同时执行）
   $ /legacy-ibmi-program-analyzer (per program)
   $ /legacy-ibmi-data-model-analyzer
   $ /legacy-ibmi-screen-report-analyzer

5. 聚合成事务级流程
   $ /legacy-ibmi-flow-analyzer (per transaction)

6. 综合4视图
   $ /legacy-ibmi-module-analyzer

7. 准备评审（需要SME）
   $ /legacy-sme-review-facilitator

8. 生成BRD + Spec
   $ /legacy-brd-writer
   $ /legacy-spec-writer

9. 生成test plan + traceability + handoff
   $ /legacy-golden-master-test-planner
   $ /legacy-traceability-packager
   $ /legacy-brd-to-sdd-handoff

10. 交付给Atlas进行downstream Java生成
```

每一步都支持iterate和SME review。
