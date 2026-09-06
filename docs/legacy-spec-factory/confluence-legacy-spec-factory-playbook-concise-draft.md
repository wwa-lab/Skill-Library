# Legacy Spec Factory 内部知识库草稿

> 同步说明：本中文精简稿与英文精简稿 [`confluence-legacy-spec-factory-playbook-concise-draft.en.md`](confluence-legacy-spec-factory-playbook-concise-draft.en.md) 保持同步。后续任何结构、表格、标题或内容调整，都需要同时更新两份文件。

## 1. 目标

Legacy Spec Factory 是一套面向 IBM i / AS400 现代化的证据驱动方法。它的目标不是把 RPGLE、CLLE、COBOL 或 DDS 代码直接翻译成 Java，而是从遗留系统中恢复真实业务意图，形成可审计、可评审、可交付给下游 SDLC 的规格说明。

核心原则：

- 以业务能力为中心，而不是以程序为中心。
- RAG / 代码知识图谱提供证据上下文，但不是最终真相。
- 遗留系统行为、推导出的业务规则、现代化设计决策必须分开管理。
- 所有关键规则必须有证据或 SME 审核。
- `spec.yaml` / `spec.md` 是下游交付的主要输入。

## 2. 推荐页面结构

| No. | Page | Purpose |
|---:|---|---|
| 01 | Method, Principles & Delivery Process | 说明方法论、核心原则和整体交付流程 |
| 02 | Scope, Non-Goals & Assumptions | 定义范围、不做什么、关键假设和风险 |
| 03 | Evidence Model, SME Review & Traceability | 定义证据模型、SME 审核规则和追踪链路 |
| 04 | System Context & Architecture | 描述遗留系统、目标系统和上下游系统关系 |
| 05 | As-Is Business Processes | 沉淀当前业务流程、系统流程、程序流程和数据流程 |
| 06 | Functional Requirements Catalogue | 汇总可交付给下游团队的功能需求 |
| 07 | Business Rules Catalogue | 管理业务规则、证据、置信度和 SME 决策 |
| 08 | Data Model & Data Dictionary | 整理数据对象、字段含义、关系和数据质量问题 |
| 09 | Integrations, Batch Jobs & Scheduling | 记录接口、批处理、调度、报表和补跑机制 |
| 10 | NFRs, Controls & Observability | 沉淀非功能需求、控制点、审计和监控要求 |
| 11 | Delivery Packaging, Gates & Handoff | 定义交付包、质量门禁和下游 handoff 标准 |

## 3. 页面草稿：01 | Method, Principles & Delivery Process

### Purpose

本页说明 Legacy Spec Factory 为什么存在、解决什么问题，以及一个遗留系统现代化工作如何从原始系统知识推进到可审批、可交付的规格包。

遗留系统现代化不是代码转换。目标不是把 RPGLE、CLLE、COBOL、DDS 或 legacy jobs 直接翻译成 Java 或云服务，而是恢复遗留系统中隐藏的业务意图，区分已被证明的行为和未经确认的假设，并创建一层可信的规格说明，供业务人员、SME、架构师、工程团队和下游 agent 共同使用。

### Why This Method Exists

很多遗留系统现代化失败，是因为团队把旧系统当成源码翻译问题。实际最有价值的知识往往分散在多个地方：

- source code and control flow
- DDS files and DB2 for i tables
- batch jobs, schedulers, job logs, and spool files
- screens, reports, and operational procedures
- SME knowledge that was never fully documented

Legacy Spec Factory 把这些分散知识转化为 evidence-backed business understanding。最终产物不只是文档，而是经过审核、可追踪的规格包，用于指导目标系统设计、开发、测试和 cutover planning。

### Core Principles

| Principle | Meaning |
|---|---|
| Business intent over code conversion | 关注业务能力做什么、为什么存在，而不是机械翻译遗留实现细节。 |
| Evidence over assumptions | 每个重要行为、规则和决策都应关联代码、运行证据、数据、文档或 SME 确认。 |
| RAG as context, not final truth | RAG、ARCAD、代码知识图谱和数据字典可以帮助定位证据，但输出仍然需要验证。 |
| SME as control point | SME 判断推导规则、模糊行为和现代化决策是否足够可信，可以进入下一步。 |
| Separate observed, inferred, and decided | 遗留行为、推导出的业务规则和目标系统决策必须分开管理。 |
| Traceability by default | Evidence、behavior、rule、requirement、acceptance criteria、test 和 handoff item 应通过稳定 ID 连接。 |
| TBDs stay visible | 未知、冲突和缺失证据必须显式记录，不能静默补齐。 |

### Delivery Process

```text
RAG / Source Evidence / SME Knowledge
  -> Module Context
  -> As-Is Business Processes
  -> Observed Behaviors
  -> Business Rules
  -> Functional Requirements
  -> SME Review
  -> spec.yaml / spec.md
  -> Traceability Package
  -> SDLC Handoff
```

### Key Artifacts

| Artifact | Purpose |
|---|---|
| Module Context | 定义业务能力、系统边界、参与者、流程和可用证据。 |
| As-Is Process | 描述遗留流程今天如何运行，包括 business、system、program 和 data views。 |
| Business Rules Catalogue | 记录规则、证据、置信度、SME 决策和例外情况。 |
| Functional Requirements Catalogue | 把已审批的业务理解转化为下游需求。 |
| `spec.yaml` | 面向自动化、工程 agent 和下游 SDLC 的结构化 source of truth。 |
| `spec.md` | 面向 SME、架构师、分析师和交付团队的人类评审视图。 |
| Traceability Package | 连接 evidence、behavior、rule、requirement、acceptance criteria、test 和 handoff item。 |

### Approval Expectations

页面或产物进入下一步前，应满足：

- 关键 claim 已关联 evidence。
- 推导出的 business rule 有 SME review status。
- open questions 已记录为 `TBD-*`。
- confidence level 可见。
- modernization decisions 与 legacy behavior 分开记录。
- approval status 清晰：Draft、In Review、Approved、Blocked 或 Retired。

### Output of This Page

读完本页后，团队应理解：

- 为什么需要这套方法。
- 它和 code conversion 有什么不同。
- evidence 和 SME 分别扮演什么角色。
- 工作如何从 legacy understanding 推进到 approved specifications。
- downstream handoff 前需要达到什么质量标准。

## 4. 页面草稿：02-11

### 02 | Scope, Non-Goals & Assumptions

**Purpose:** 定义当前现代化工作的边界，避免团队把一个模块试点扩散成无限范围的系统重写。

**What to Capture**

| Area | Content |
|---|---|
| In Scope | 业务能力、程序、文件、报表、批处理、接口和数据对象。 |
| Non-Goals | 当前阶段不迁移、不分析、不重构或不负责的内容。 |
| Assumptions | 业务规则沿用、目标平台约束、SME 可用性、数据可用性等假设。 |
| Risks | 证据缺失、规则冲突、隐藏依赖、人工操作未记录、范围过大。 |
| Open Questions | 需要产品、架构、SME 或交付负责人确认的问题。 |

**Outputs:** scope statement、non-goals list、assumptions log、risk / TBD list。

**Approval Gate:** scope owner 和 SME 已确认边界；所有 out-of-scope 项目不会被静默带入交付。

### 03 | Evidence Model, SME Review & Traceability

**Purpose:** 定义团队如何判断“什么是事实、什么是推断、什么是目标系统决策”，并确保每个关键 claim 可追踪。

**What to Capture**

| Area | Content |
|---|---|
| Knowledge Types | `observed_behavior`、`inferred_business_rule`、`modernization_decision`、`unknown_tbd`。 |
| Evidence Strength | `confirmed_from_code`、`observed_in_runtime`、`confirmed_by_sme`、`strongly_inferred`、`weakly_inferred`、`contradictory`、`missing`。 |
| Evidence IDs | 每个证据项的 ID、来源、路径、敏感级别和可用性。 |
| SME Decisions | 确认、驳回、修改、标记 non-blocking 或要求补证。 |
| Traceability Links | evidence -> behavior -> rule -> requirement -> acceptance criteria -> test / handoff item。 |

**Outputs:** evidence taxonomy、SME decision log、traceability rules、TBD policy。

**Approval Gate:** 没有证据的内容不能成为需求；推导规则必须有 SME review status。

### 04 | System Context & Architecture

**Purpose:** 说明当前能力在企业系统版图中的位置，以及遗留系统和目标系统之间的上下文关系。

**What to Capture**

| Area | Content |
|---|---|
| Legacy Boundary | 当前 IBM i / AS400 子系统、程序组、文件组和运行环境边界。 |
| Actors | 业务用户、操作人员、支持团队、外部系统和自动任务。 |
| Upstream / Downstream | 调用方、被调用方、数据来源、数据消费者、报表接收方。 |
| Target Context | 目标服务、API、数据库、事件流、批处理或平台约束。 |
| Architecture Decisions | 需要保留、拆分、替换或重新设计的架构点。 |

**Outputs:** context diagram、system inventory、integration map、architecture assumptions。

**Approval Gate:** 关键上下游系统和 owner 已识别；目标架构假设已由架构负责人确认或标记为 TBD。

### 05 | As-Is Business Processes

**Purpose:** 记录遗留流程今天如何真实运行，不急着写目标方案。

**What to Capture**

| Area | Content |
|---|---|
| Business Flow | 业务触发、参与角色、主路径、例外路径和业务结果。 |
| System Flow | 系统交互、接口调用、批处理触发和外部依赖。 |
| Program Flow | 支撑性技术追踪：入口点、关键分支、错误路径和调用链证据；不要把它当作主业务流程叙事。 |
| Data Flow | 输入、输出、文件读写、关键字段和数据状态变化。 |
| Controls / Workarounds | 人工检查、补跑、对账、报表核验和操作惯例。 |

**Outputs:** as-is process map、flow notes、observed behavior list、open questions。

**Approval Gate:** 关键路径和高风险例外路径已由 SME 审核，未确认内容已记录为 `TBD-*`。

### 06 | Functional Requirements Catalogue

**Purpose:** 把已确认的业务流程和规则转化为可交付给下游团队的功能需求。

**What to Capture**

| Area | Content |
|---|---|
| Requirement ID | 稳定 ID，便于追踪和引用。 |
| Actor / User | 谁触发或使用该能力。 |
| Requirement Statement | 业务能力需要做什么，避免描述技术实现。 |
| Linked Rules | 关联的 `BR-*` business rules。 |
| Acceptance Criteria | 可验证的验收条件。 |
| Evidence Links | 支撑需求的 evidence、behavior 或 SME decision。 |
| Status | Draft、In Review、Approved、Blocked 或 Retired。 |

**Outputs:** functional requirements catalogue、acceptance criteria seeds、open requirement TBDs。

**Approval Gate:** 每条需求都能追溯到已确认行为、业务规则或明确的现代化决策。

### 07 | Business Rules Catalogue

**Purpose:** 集中管理业务规则，避免规则散落在流程图、会议纪要、代码注释和需求文档中。

**What to Capture**

| Area | Content |
|---|---|
| BR ID | 稳定 business rule ID。 |
| Rule Statement | 清晰、可验证的规则表述。 |
| Rule Type | 计算、校验、资格、路由、状态转换、控制或例外规则。 |
| Source Behavior | 规则对应的遗留行为或运行现象。 |
| Evidence IDs | 代码、运行日志、报表、数据样例或 SME 确认。 |
| Confidence / Status | 置信度和审批状态。 |
| Exceptions | 边界条件、特殊客户、期间处理、补跑或人工处理。 |
| Modernization Implication | 目标系统中保留、调整、废弃或重新设计。 |

**Outputs:** business rules catalogue、exception list、SME decision log。

**Approval Gate:** 推导规则未经 SME 确认不得标记为 Approved；冲突规则必须记录 resolution 或 TBD。

### 08 | Data Model & Data Dictionary

**Purpose:** 整理遗留数据对象、字段语义、关系和数据质量问题，为目标数据模型提供可信输入。

**What to Capture**

| Area | Content |
|---|---|
| Data Objects | PF、LF、DB2 for i table、view、data area、work file。 |
| Field Meaning | 字段业务含义、格式、长度、取值范围和 code values。 |
| Keys / Relationships | 主键、访问路径、逻辑文件、跨表关系和引用规则。 |
| CRUD Lifecycle | 哪些程序创建、读取、更新、删除或归档数据。 |
| Ownership | 数据 owner、source of record、下游消费者。 |
| Quality Issues | 缺失值、重复值、历史脏数据、隐式编码、特殊值。 |
| Target Implications | 目标字段映射、拆分、合并、清洗和迁移注意事项。 |

**Outputs:** data dictionary、relationship map、CRUD matrix、data quality notes。

**Approval Gate:** 关键字段含义不能只靠字段名猜测；必须有代码、数据字典、样例或 SME 支撑。

### 09 | Integrations, Batch Jobs & Scheduling

**Purpose:** 记录接口、批处理、调度、报表和异步流程，避免现代化时遗漏运行链路。

**What to Capture**

| Area | Content |
|---|---|
| Jobs / Schedules | job 名称、触发方式、频率、窗口期、依赖和 owner。 |
| Program Chain | job 调用的 CL、RPGLE、SQL、report 或 utility。 |
| External Interfaces | 文件交换、消息队列、data queue、API、FTP、第三方系统。 |
| Reports / Spool | 报表、spool 输出、接收方、用途和保留要求。 |
| Retry / Rerun | 失败处理、补跑步骤、幂等性、人工干预和恢复流程。 |
| Cutoff / Period-End | 日终、月结、年结、冻结窗口和特殊业务日。 |

**Outputs:** integration inventory、batch calendar、job dependency map、recovery notes。

**Approval Gate:** 关键 job 的运行条件、失败处理和 owner 已明确；未知依赖已记录为 TBD。

### 10 | NFRs, Controls & Observability

**Purpose:** 把遗留系统中的隐性控制和运行期望转化为目标系统的显式非功能需求。

**What to Capture**

| Area | Content |
|---|---|
| Performance | 响应时间、吞吐量、批处理窗口、峰值和容量假设。 |
| Availability | 可用性目标、维护窗口、恢复时间和业务连续性要求。 |
| Security | 认证、授权、敏感数据、职责分离和访问控制。 |
| Auditability | 审计日志、操作记录、审批轨迹和监管要求。 |
| Reconciliation | 对账、控制总数、报表核验、差异处理。 |
| Error Handling | 错误分类、重试、告警、人工处理和用户提示。 |
| Observability | 日志、指标、trace、dashboard、alert 和 runbook。 |

**Outputs:** NFR catalogue、controls matrix、observability requirements、operational acceptance criteria。

**Approval Gate:** 高风险控制点必须有 owner、验收方式和下游实现责任。

### 11 | Delivery Packaging, Gates & Handoff

**Purpose:** 定义什么情况下规格包可以交付给下游工程、测试、架构或 AI-native SDLC。

**What to Capture**

| Area | Content |
|---|---|
| Required Artifacts | BRD、validation scenarios、`spec.yaml`、`spec.md`、traceability、decision log。 |
| Quality Gates | input readiness、evidence approval、SME approval、traceability completeness、handoff readiness。 |
| Open TBDs | 未关闭问题、owner、目标日期、是否 blocking。 |
| Approvals | SME、product、architecture、delivery 和 QA sign-off。 |
| Handoff Consumers | 下游团队、agent、系统、测试或迁移负责人。 |
| Validation Plan | golden master、parallel run、acceptance tests 或 manual validation。 |

**Outputs:** handoff checklist、approved spec package、traceability package、delivery notes。

**Approval Gate:** `spec.yaml` / `spec.md` 已批准；blocking TBD 已关闭；traceability 足够支持下游实现和测试。

## 5. 标准页面模板

每个页面建议使用同一套结构：

| Section | Content |
|---|---|
| Purpose | 这个页面解决什么问题 |
| Scope | 覆盖和不覆盖的范围 |
| Inputs | 需要哪些输入材料 |
| Outputs | 该页面应产出什么内容 |
| Evidence Required | 需要关联哪些证据 |
| Open Questions / TBDs | 尚未确认的问题 |
| Review Owner | 谁负责审核 |
| Approval Gate | 什么条件下可以进入下一步 |

## 6. 证据与审核模型

知识类型：

| Type | Meaning |
|---|---|
| `observed_behavior` | 遗留系统被代码、运行日志、报表或样例证明的真实行为 |
| `inferred_business_rule` | 从行为、代码或数据中推导出的业务规则 |
| `modernization_decision` | 面向目标系统的设计或取舍决策 |
| `unknown_tbd` | 证据不足、含义不清或存在冲突的问题 |

证据强度：

| Strength | Meaning |
|---|---|
| `confirmed_from_code` | 源代码直接证明 |
| `observed_in_runtime` | 运行日志、spool、样例交易或报表证明 |
| `confirmed_by_sme` | SME 明确确认 |
| `strongly_inferred` | 多个证据点强推断，但仍需审核 |
| `weakly_inferred` | 弱推断，不能直接进入需求 |
| `contradictory` | 证据之间存在冲突 |
| `missing` | 关键证据缺失 |

审批规则：

- 没有证据的内容不能成为正式需求。
- 推导出的业务规则必须经过 SME 确认。
- 现代化决策需要产品、架构或交付负责人确认。
- 所有 `TBD-*` 必须被解决，或被明确标记为 non-blocking。

## 7. 推荐落地路径

```text
RAG / Code Knowledge Graph / Source Evidence
  -> Module Context
  -> As-Is Process
  -> Business Rules
  -> Functional Requirements
  -> spec.yaml / spec.md
  -> Traceability Package
  -> SDLC Handoff
```

默认从模块视角开始。如果模块边界、流程和 RAG 证据已经具备，不需要先做全量源码挖掘。源码级分析主要用于补证、查冲突、验证高风险规则和解决 TBD。

## 8. Action Plan

| Phase | Timeline | Objective | Key Actions | Deliverables |
|---|---:|---|---|---|
| 1. Build Structure | Week 1 | 建立 Confluence 页面骨架 | 创建首页和 11 个子页面；套用标准页面模板 | 页面树和空白模板 |
| 2. Align Methodology | Week 1 | 形成方法论共识 | 写清楚目标、原则、证据模型、SME 角色和交付路径 | 方法论首页和证据模型页面 |
| 3. Create Templates | Week 2 | 让团队可以按模板执行 | 建立 Scope、Process、Rule、Requirement、Data、Integration、Traceability、Handoff 模板 | 可复制的页面模板 |
| 4. Select Pilot Module | Week 2 | 选择一个真实模块试点 | 确认模块边界、输入材料、owner 和 SME | 试点范围和输入清单 |
| 5. Populate Pilot | Week 3 | 用真实内容验证结构 | 填充流程、规则、数据、接口、批处理和 TBD | 试点模块草稿 |
| 6. Run SME Review | Week 3-4 | 审核高风险规则和不确定项 | 组织 SME review；确认、驳回或标记规则 | SME 决策记录和 approved rules |
| 7. Build Traceability | Week 4 | 建立从证据到交付的链路 | 连接 evidence -> behavior -> rule -> requirement -> acceptance criteria | Traceability matrix |
| 8. Standardize & Roll Out | Ongoing | 固化为团队工作方式 | 复盘试点；沉淀好例子和反模式；推广到更多模块 | 团队 playbook 和样例库 |

## 9. Execution Tracker

| Task | Priority | Owner | Target | Status |
|---|---:|---|---|---|
| Create Confluence homepage | High | Modernization Lead | Week 1 | Not Started |
| Create 11 child pages | High | BA | Week 1 | Not Started |
| Draft methodology summary | High | Modernization Lead / Architect | Week 1 | Not Started |
| Define evidence taxonomy | High | BA / SME / Architect | Week 1 | Not Started |
| Create business rule template | High | BA | Week 2 | Not Started |
| Create traceability template | High | BA / Architect | Week 2 | Not Started |
| Select pilot module | High | Product Owner / SME | Week 2 | Not Started |
| Populate pilot pages | High | BA / Engineer | Week 3 | Not Started |
| Run SME review | High | SME / BA | Week 4 | Not Started |
| Finalize handoff checklist | Medium | Delivery Lead / Architect | Week 4 | Not Started |
| Publish pilot as reference | Medium | Modernization Lead | Week 4+ | Not Started |

## 10. Definition of Done

第一版知识库完成标准：

- 11 个核心页面已创建。
- 每页都有 purpose、inputs、outputs、owner 和 approval gate。
- 证据模型和 SME 审核规则已定义。
- 至少一个试点模块已填充。
- 至少完成一次 SME review。
- 至少能展示一条完整链路：evidence -> behavior -> business rule -> requirement -> acceptance criteria。
- 团队知道下一个模块应该从哪个模板开始。
