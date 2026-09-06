# Legacy Spec Factory: Evidence-Backed Legacy Modernization Playbook

> Bilingual sync note: This Chinese draft is maintained in lockstep with the English version: [`confluence-legacy-spec-factory-playbook-draft.en.md`](confluence-legacy-spec-factory-playbook-draft.en.md). Any future change to structure, wording, tables, action plan, or Definition of Done must be applied to both versions in the same update.

## Purpose

Legacy Spec Factory 是一套面向 IBM i / AS400 现代化的证据驱动方法论。

它的目标不是把 RPGLE、CLLE、COBOL、DDS 代码直接翻译成 Java，而是从遗留系统中恢复真实业务意图，形成可审计、可评审、可交付给现代云平台 SDLC 的规格说明。

核心产物是经过 SME 审核的业务能力规格包，包括：

- `observed_behavior`：遗留系统已经被证据证明的行为
- `inferred_business_rule`：从代码、数据、运行证据中推导出的业务规则
- `modernization_decision`：面向目标系统的现代化设计决策
- `spec.yaml` / `spec.md`：下游工程和 AI agent 可消费的规格源
- `traceability_package`：从证据、规则、验收标准到测试和交付的追踪链路

## Operating Model

Legacy Spec Factory 支持两条路径。

### Default Path: RAG-Assisted Module-First

```text
RAG / Code Knowledge Graph / ARCAD / Data Dictionary
  -> Four-view Module Context
  -> Module Analysis
  -> BRD + Validation Package
  -> SME Review
  -> spec.yaml / spec.md
  -> Traceability + SDLC Handoff
```

默认企业落地路径是 **module-first**。当团队已经有模块边界、四类流程图、RAG 检索结果或代码知识图谱时，不需要从全量源码重新挖一遍。

### Verification Path: Source-First Evidence Repair

```text
Raw IBM i Evidence
  -> Evidence Intake
  -> Inventory
  -> Program / Flow / Data / Screen / Report Analysis
  -> Evidence Repair
  -> Module / BRD / Spec Synthesis
```

源码级分析主要用于补证、查冲突、验证高风险规则和修复不确定项。

## Page Tree

```text
01 | Method, Principles & Delivery Process
02 | Scope, Non-Goals & Assumptions
03 | Evidence Model, SME Review & Traceability
04 | System Context & Architecture
05 | As-Is Business Processes
06 | Functional Requirements Catalogue
07 | Business Rules Catalogue
08 | Data Model & Data Dictionary
09 | Integrations, Batch Jobs & Scheduling
10 | NFRs, Controls & Observability
11 | Delivery Packaging, Gates & Handoff
```

## Standard Page Contract

每个页面建议保持同一个结构：

```text
Purpose
Scope
Inputs
Outputs
Evidence Required
Open Questions / TBDs
Review Owner
Approval Gate
Examples / Templates
```

## 01 | Method, Principles & Delivery Process

说明这套方法为什么存在、解决什么问题、总体交付链路是什么。

重点写清楚：

- 这不是 code conversion，而是 business intent recovery。
- `spec.yaml` 是结构化 source of truth，`spec.md` 是人类评审视图。
- RAG 是 evidence context，不是 final truth。
- SME 是遗留理解的控制点。
- 每一步都必须保留证据、置信度、TBD 和审批状态。

## 02 | Scope, Non-Goals & Assumptions

定义当前现代化范围、明确不做什么、记录关键假设。

建议包含：

- In scope：业务模块、程序、文件、报表、批处理、接口。
- Out of scope：暂不迁移模块、历史数据清洗、非核心报表等。
- Assumptions：业务规则沿用、目标平台约束、数据可用性、SME 可用性。
- Risk：证据缺失、规则冲突、隐式依赖、人工操作未记录。

## 03 | Evidence Model, SME Review & Traceability

这是核心页面，建议单独放前面。

重点定义四类内容：

```text
observed_behavior
inferred_business_rule
modernization_decision
unknown_tbd
```

证据强度建议统一为：

```text
confirmed_from_code
observed_in_runtime
confirmed_by_sme
strongly_inferred
weakly_inferred
needs_sme_review
contradictory
missing
```

审批规则：

- 没有证据的内容不能升级为需求。
- 推断规则必须经过 SME 确认。
- 现代化决策必须经过架构或产品审批。
- 所有 `TBD-*` 必须被解决，或由 SME 标记为 non-blocking。

## 04 | System Context & Architecture

描述当前遗留系统和目标系统之间的上下文。

建议包含：

- 当前 IBM i / AS400 系统边界
- 上下游系统
- 人工参与角色
- 外部接口
- 批处理和调度依赖
- 数据主从关系
- 目标系统拆分原则

这一页回答：“这个能力在企业系统版图里处于什么位置？”

## 05 | As-Is Business Processes

沉淀当前业务流程，不急着写目标方案。

建议按四视图组织：

```text
Operation / Business Flow
System Flow
Program Flow
Data Flow
```

每个流程至少记录：

- 触发条件
- 参与角色
- 输入和输出
- 主路径
- 异常路径
- 关键程序 / 文件 / 报表
- 证据 ID
- SME 确认状态

## 06 | Functional Requirements Catalogue

从已确认的业务流程和规则中抽取功能需求。

每条需求建议包含：

```text
Requirement ID
Capability
User / Actor
Statement
Acceptance Criteria
Linked Business Rules
Linked Evidence
Review Status
```

注意这里不要混入实现设计。功能需求应该描述业务能力，而不是目标系统怎么写代码。

## 07 | Business Rules Catalogue

集中管理业务规则。

每条规则建议包含：

```text
BR ID
Rule Statement
Rule Type
Source Behavior
Evidence IDs
Confidence
SME Decision
Exceptions
Related Acceptance Criteria
```

规则要区分：

- 遗留系统真实行为
- 从行为推导出的业务含义
- 目标系统保留、调整或废弃的决策

## 08 | Data Model & Data Dictionary

整理数据对象、字段、DDS / DB2 for i 关系和目标数据语义。

建议包含：

- Physical files / logical files
- Key fields
- Field meanings
- Code values
- Referential relationships
- CRUD lifecycle
- Data ownership
- Data quality issues
- Target model implications

这一页要特别避免“看字段名猜含义”。字段语义需要代码、运行样例、字典或 SME 支撑。

## 09 | Integrations, Batch Jobs & Scheduling

沉淀接口、批处理、调度、报表和异步流程。

建议包含：

- Job / scheduler inventory
- Program call-chain evidence (supporting trace, not business narrative)
- Submitted jobs
- Message queues / data queues
- File exchange
- Spool / report outputs
- External systems
- Retry / rerun / recovery behavior
- Cutoff time and period-end behavior

这页通常是现代化风险高发区，尤其是月结、日终、补跑、人工重跑。

## 10 | NFRs, Controls & Observability

沉淀非功能、控制点和可观测性要求。

建议包含：

- Performance
- Availability
- Security
- Auditability
- Data retention
- Operational controls
- Reconciliation
- Error handling
- Logging and monitoring
- Regulatory or internal compliance needs

这里的关键是把“遗留系统隐含控制”转成目标系统显式要求。

## 11 | Delivery Packaging, Gates & Handoff

定义什么时候可以交付给下游工程。

建议的交付门禁：

```text
Input readiness passed
Evidence authorization passed
SME review completed
Business rules approved
TBDs resolved or accepted
spec.yaml / spec.md generated
Traceability package complete
Golden master / validation scenarios prepared
SDLC handoff accepted
```

最终交付包建议包括：

- BRD
- Validation scenarios
- `spec.yaml`
- `spec.md`
- `traceability.md`
- Modernization decisions
- Open questions
- SME sign-off record
- Downstream handoff package

## Action Plan

### Delivery Roadmap

| Phase | Timeline | Objective | Key Actions | Owner | Deliverables | Exit Criteria |
|---|---:|---|---|---|---|---|
| 1. Structure Setup | Week 1 | 建立 Confluence 知识库骨架 | 创建 `Legacy Spec Factory` 首页；建立 11 个核心页面；统一页面模板结构 | Modernization Lead / BA | Confluence 页面树；标准页面模板 | 页面可导航；每页已有 Purpose / Inputs / Outputs / Review Gate |
| 2. Core Methodology | Week 1 | 明确方法论和核心原则 | 写清楚不是 code conversion；定义 business intent recovery；说明 `spec.yaml` / `spec.md`；明确 RAG、SME、evidence 的角色 | Modernization Lead / Architect | 首页方法论；Method 页面；Evidence Model 页面 | 团队能解释这套方法与普通逆向工程的区别 |
| 3. Evidence & Review Model | Week 1-2 | 建立证据、审核和追踪规则 | 定义 observed behavior、inferred business rule、modernization decision、TBD；定义 evidence strength；定义 SME approval 规则 | BA / SME / Architect | Evidence taxonomy；SME review rules；traceability rules | 每条规则知道如何关联证据和审批状态 |
| 4. Template Creation | Week 2 | 建立可复用模板 | 创建 Scope、As-Is Process、Business Rule、Functional Requirement、Data Dictionary、Integration、SME Review、Traceability、Handoff 模板 | BA / Solution Analyst | Confluence 模板集 | 新模块可以直接复制模板启动 |
| 5. Pilot Module Selection | Week 2 | 选择一个试点业务模块 | 选一个范围适中、有 SME 支持、有代表性的模块；确认输入材料和边界 | Modernization Lead / Product Owner / SME | Pilot scope；module owner；input checklist | 试点范围明确，owner 和 SME 已确认 |
| 6. Pilot Content Population | Week 3 | 用真实模块填充知识库 | 填写 scope、as-is process、business rules、data model、batch/jobs、integrations；标记 `TBD-*`；关联 evidence IDs | BA / Engineer / SME | Pilot module pages；initial rule catalogue；open TBD list | 试点模块形成端到端内容草稿 |
| 7. SME Review | Week 3-4 | 让业务和 IBM i SME 审核关键内容 | 组织 SME review；确认 observed behavior；批准或驳回 inferred rules；记录 open questions 和 decisions | SME / BA / Modernization Lead | SME decision log；approved rules；review notes | 高风险规则已审核；关键 TBD 已解决或标记 non-blocking |
| 8. Traceability & Handoff | Week 4 | 建立从证据到交付的链路 | 连接 evidence -> behavior -> business rule -> requirement -> acceptance criteria -> test / handoff item | BA / Architect / Delivery Lead | Traceability matrix；handoff checklist；spec package outline | 至少一条完整 traceability 链路可展示 |
| 9. Governance Setup | Week 4 | 固化质量门禁和页面状态 | 定义 Draft / In Review / Approved / Blocked / Retired；定义 input readiness、evidence approval、SME approval、handoff readiness | Modernization Lead / QA / Architect | Governance rules；quality gate checklist | 文档不会无审核进入交付 |
| 10. Rollout & Continuous Improvement | Ongoing | 推广到更多模块并持续优化 | 为新模块复制模板；复盘 pilot；沉淀好例子和反模式；定期检查 TBD 和 traceability | Modernization Lead / Team Leads | Reusable playbook；example library；lessons learned | 团队能按统一方法启动下一个模块 |

### Execution Tracker

| Workstream | Task | Priority | Target Date | Status | Dependencies | Notes |
|---|---|---:|---|---|---|---|
| Confluence Setup | Create Legacy Spec Factory homepage | High | Week 1 | Not Started | None | 作为统一入口 |
| Confluence Setup | Create 11 core child pages | High | Week 1 | Not Started | Homepage | 页面标题固定后再建 |
| Methodology | Draft principles and delivery process | High | Week 1 | Not Started | Homepage | 强调 evidence-backed，不是 code conversion |
| Evidence | Define evidence taxonomy | High | Week 1 | Not Started | Methodology draft | 需要 SME 和 architect 对齐 |
| Evidence | Define SME review and approval rules | High | Week 2 | Not Started | Evidence taxonomy | 决定哪些内容可进入 spec |
| Templates | Create business rule template | High | Week 2 | Not Started | ID convention | 必须包含 evidence IDs |
| Templates | Create traceability matrix template | High | Week 2 | Not Started | Evidence model | 用于 handoff 前检查 |
| Pilot | Select pilot module | High | Week 2 | Not Started | Scope criteria | 范围不要太大 |
| Pilot | Populate pilot module pages | High | Week 3 | Not Started | Templates, input materials | 先允许 draft，不追求一次完美 |
| Pilot | Conduct SME review | High | Week 4 | Not Started | Draft pilot pages | 记录 approved / rejected / TBD |
| Delivery | Build handoff checklist | Medium | Week 4 | Not Started | Traceability matrix | 对接下游 SDLC |
| Governance | Define page status and gates | Medium | Week 4 | Not Started | Pilot findings | 用试点经验反推标准 |
| Rollout | Publish pilot example as reference | Medium | Week 4+ | Not Started | SME-reviewed pilot | 成为后续项目样板 |
| Rollout | Schedule recurring review cadence | Medium | Ongoing | Not Started | Governance setup | 关注 TBD、规则审批、traceability |

## Suggested 30-Day Plan

| Week | Focus | Key Outcomes |
|---:|---|---|
| Week 1 | Structure and methodology | 搭建 Confluence 页面树；完成首页、方法论、证据模型三页；确定 ID 规则和页面状态 |
| Week 2 | Templates and pilot selection | 完成核心模板；补齐 Scope、Process、Business Rules、Data Model 页面框架；选定 pilot module |
| Week 3 | Pilot population | 填充 pilot module；记录 observed behavior、business rules、TBDs；准备 SME review 材料 |
| Week 4 | Review and standardization | 完成 SME review；更新规则状态和 traceability；总结 pilot lessons learned；固化团队标准流程 |

## Definition of Done

这套 Confluence 知识库的第一版完成标准：

- 11 个核心页面已建立。
- 每页有明确 purpose、input、output、owner、approval gate。
- Evidence taxonomy 已定义。
- 至少一个 pilot module 已填充。
- 至少一次 SME review 已完成。
- 至少一条从 evidence 到 business rule 到 acceptance criteria 的 traceability 链路可展示。
- 团队知道新模块应该从哪个模板开始。
