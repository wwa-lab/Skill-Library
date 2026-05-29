# Legacy Modernization RAG Setup Detail

本文用于和团队对齐 AI retrieval / external RAG / code knowledge graph 的
建设边界、索引设计、知识图谱关系、数据字典接入方式，以及它如何支撑
Legacy Spec Factory 生成 BRD + Validation Package。

## 1. 定位

这里的 RAG 不要求一定自研成独立产品。第一版可以接 OpenAI / 现成搜索检索 /
客户已有 code knowledge graph；关键是形成面向 Legacy Modernization 的
**代码知识图谱 + 数据字典语义层 + 证据检索层**，并输出稳定的 evidence bundle。

它负责：

- 基于全量 source、ARCAD REF、表/文件元数据、全域数据字典建立可检索的 legacy knowledge layer。
- 支持字段、表、程序、调用链、上下游、代码片段、影响范围查询。
- 围绕人工确认的四条 flow 或历史 Function Spec / Technical Design /
  Program Spec / File Spec 等资料补充证据和上下文。
- 输出 Markdown 为主、YAML index 为辅的 evidence bundle，供 Legacy Spec Factory 消费。

它不负责：

- 直接生成最终 BRD 或正式测试用例。
- 自动批准业务规则。
- 替代 SME 判断。
- 替代全域数据字典中心。
- 把 RAG 检索结果当成最终事实。

核心原则：

```text
RAG retrieval is evidence context, not final truth.
Source code is observed behavior.
Data dictionary is approved business meaning.
ARCAD REF is relationship seed.
Human-confirmed four-view context is the preferred BRD skeleton.
Historical specs and scattered documents can be normalized into that skeleton
when reviewed flows are not yet available.
BRD-stage VAL scenarios are review seeds, not final TC cases.
SME approval remains the rule and test promotion gate.
```

## 2. 输入来源

### 2.1 全量 Source

范围包括：

- RPG / RPGLE
- CL / CLLE
- COBOL, if present
- DDS PF / LF / DSPF / PRTF
- SQL, copybooks, service program references, job control material

用途：

- 提供 observed behavior。
- 抽取 program call、file I/O、field usage、branch snippets。
- 支撑代码片段引用和行号级 evidence。

### 2.2 全域数据字典

数据字典是业务语义主干，不是普通文档附件。

最小字段包建议：

```yaml
standard_field_id: DD-CUSTOMER-CREDIT-LIMIT
canonical_name: Credit Limit
business_domain: Customer Credit
field_definition: Approved maximum receivable exposure for a customer.
legacy_aliases:
  - CRLMT
  - CREDLIM
physical_fields:
  - table: ARCUST
    field: CRLMT
  - table: ARHIST
    field: OLDCRLMT
data_type: packed_decimal
precision: "11,2"
visibility_class: internal_user
display_policy: currency_2dp
owner: Credit Operations
dictionary_version: dict-v34
status: approved
```

用途：

- 把 legacy 字段翻译成业务字段。
- 反查同一标准字段的所有 physical aliases。
- 支撑字段影响面分析。
- 支撑 BRD 中的业务语言表达。
- 发现 dictionary 定义和 code behavior 的冲突。

详细贯穿规则见
[`dictionary-center-integration-contract.md`](dictionary-center-integration-contract.md)。

### 2.3 ARCAD REF

ARCAD REF 是关系图谱的种子，不只是普通检索材料。

用途：

- program caller / callee seed
- program-file relation seed
- field reference seed
- impact reference seed
- 和 source parser 结果做交叉校验

如果 ARCAD REF 和 source parser 不一致，不要静默合并。应输出 contradiction / needs review。

示例：

```yaml
contradiction:
  id: RAG-CONFLICT-CUE64-001
  type: arcad_source_mismatch
  arcad_ref: "CUE64 writes ARBAL"
  source_observation: "No write operation to ARBAL found in parsed source"
  severity: needs_review
  next_owner: IT SME
```

## 3. 核心数据层

RAG 至少应有四类逻辑索引。

### 3.1 Artifact Registry

记录每个原始对象的来源、版本、路径、敏感级别和可引用范围。

```yaml
artifact_id: SRC-CUE64-001
artifact_type: rpgle_source
library: ARLIB
object_name: CUE64
member: CUE64
source_path: source/ARLIB/CUE64.RPGLE
snapshot_id: ibmi-export-2026-05-21
line_start: 1
line_end: 2400
sensitivity: internal
source_path_verified: true
```

### 3.2 Entity Catalog

把 legacy 世界里的对象标准化成实体。

实体类型：

```text
PROGRAM
TABLE_OR_FILE
FIELD
STANDARD_FIELD
COPYBOOK
SCREEN
REPORT
JOB
MESSAGE_QUEUE
DATA_AREA
FLOW
MODULE
```

示例：

```yaml
entity_id: PROGRAM-CUE64
entity_type: PROGRAM
name: CUE64
aliases:
  - CUE64R
library: ARLIB
source_artifact_id: SRC-CUE64-001
```

### 3.3 Relationship Graph

这是 impact scope 和 program flow 的核心。

必须支持的关系：

```text
PROGRAM -> calls -> PROGRAM
PROGRAM -> called_by -> PROGRAM
PROGRAM -> reads -> TABLE_OR_FILE
PROGRAM -> writes -> TABLE_OR_FILE
PROGRAM -> updates -> TABLE_OR_FILE.FIELD
PROGRAM -> validates -> TABLE_OR_FILE.FIELD
PROGRAM -> uses -> COPYBOOK
PROGRAM -> runs_in -> JOB
JOB -> runs -> PROGRAM
SCREEN -> displays -> TABLE_OR_FILE.FIELD
REPORT -> prints -> TABLE_OR_FILE.FIELD
TABLE_OR_FILE -> contains -> FIELD
FIELD -> maps_to -> STANDARD_FIELD
STANDARD_FIELD -> belongs_to -> BUSINESS_DOMAIN
STANDARD_FIELD -> owned_by -> DATA_OWNER
FLOW -> contains -> PROGRAM
MODULE -> contains -> FLOW
```

每条关系需要记录 provenance：

```yaml
edge_id: EDGE-CUE64-ARCUST-CRLMT-001
from: PROGRAM-CUE64
relation: updates
to: FIELD-ARCUST-CRLMT
evidence:
  source: source_parser
  artifact_id: SRC-CUE64-001
  snippet_id: SNP-CUE64-042
  line_start: 320
  line_end: 356
confidence: confirmed_from_code
```

### 3.4 Snippet Index

代码片段必须可引用、可回溯、可和关系图绑定。

```yaml
snippet_id: SNP-CUE64-042
artifact_id: SRC-CUE64-001
program: CUE64
line_start: 320
line_end: 356
summary: Updates customer credit limit after validation.
relations:
  - EDGE-CUE64-ARCUST-CRLMT-001
fields:
  - ARCUST.CRLMT
standard_field_ids:
  - DD-CUSTOMER-CREDIT-LIMIT
evidence_strength: confirmed_from_code
```

## 4. 索引策略

### 4.1 不只做向量索引

Legacy modernization 场景里，metadata recall 往往比 semantic similarity 更重要。

建议组合：

```text
keyword / exact index
  program name, table name, field name, library/member, ARCAD object id

vector index
  source comments, business docs, SME notes, dictionary definition, flow prose

relationship graph
  caller/callee, read/write, field mapping, job/program, screen/report usage

snippet index
  line-range-level source evidence
```

### 4.2 Chunking 建议

Source chunk 不要只按固定 token 切。优先按 legacy 结构切：

- program header / F-spec / D-spec / C-spec blocks
- subroutine / procedure
- file I/O block
- validation branch
- update/write block
- error handling block
- screen/report field block

每个 chunk 必须保留：

```yaml
artifact_id
program
library
member
line_start
line_end
tables_read
tables_written
fields_used
standard_field_ids
call_targets
evidence_strength
snapshot_id
```

## 5. 必备查询能力

### 5.1 `program_flow(program_name)`

目标：输入一个 program，例如 `CUE64`，输出上下游和关键证据。

输入：

```yaml
program: CUE64
depth:
  upstream: 2
  downstream: 2
include:
  snippets: true
  table_io: true
  dictionary_mapping: true
  arcad_ref: true
```

输出：

```text
Program Flow: CUE64

Upstream:
- CUE60 -> CUE64
- CUE62 -> CUE64

Current Program:
- Reads ARCUST
- Validates DD-CUSTOMER-CREDIT-LIMIT via ARCUST.CRLMT
- Updates ARCUST.CRLMT
- Writes audit record to ARAUD

Downstream:
- CUE64 -> CUE71
- CUE64 -> ERRMSG

Evidence snippets:
- SNP-CUE64-018, lines 220-260: read customer record
- SNP-CUE64-042, lines 320-356: update credit limit
- SNP-CUE64-051, lines 410-438: write audit trail
```

### 5.2 `field_impact(field_name | standard_field_id)`

目标：输入 legacy 字段或标准字段，输出影响范围。

推荐从 `standard_field_id` 开始反查：

```text
STANDARD_FIELD
  -> physical aliases
  -> table/file fields
  -> programs read/write/update/validate
  -> screens/reports display/print
  -> jobs/flows/modules touched
  -> snippets
```

输出分层：

- Direct impact: 直接读写/更新/校验字段的程序。
- Indirect impact: 上游调用者、下游被调用者、关联 job / flow。
- User-visible impact: screen / report / API / interface。
- Data impact: table, file, copybook, archive/history fields。
- Evidence: snippet ids, line ranges, ARCAD refs。
- Confidence: confirmed / inferred / needs review。

### 5.3 `dictionary_lookup(field | table.field | standard_field_id)`

目标：查询字段业务含义、别名、版本、owner。

输出：

```yaml
standard_field_id: DD-CUSTOMER-CREDIT-LIMIT
canonical_name: Credit Limit
definition: Approved maximum receivable exposure for a customer.
legacy_aliases:
  - ARCUST.CRLMT
  - ARHIST.OLDCRLMT
owner: Credit Operations
dictionary_version: dict-v34
status: approved
known_code_usage:
  read_by:
    - CUE64
    - CUE71
  written_by:
    - CUE64
  displayed_by:
    - CUEINQ
```

### 5.4 `hydrate_flows(flow_list)`

目标：输入人工确认的四条 flow，输出 BRD 可用的 evidence bundle。

输入：

```yaml
module_slug: CREDIT-LIMIT
flows:
  operation_business_flow: <markdown or text>
  system_flow: <markdown or text>
  program_flow: <markdown or text>
  data_flow: <markdown or text>
include:
  source_snippets: true
  dictionary_mappings: true
  arcad_refs: true
  contradictions: true
  retrieval_gaps: true
```

输出目录建议：

```text
rag_runs/<MODULE-SLUG>/<RUN-ID>/
├── rag-run-index.yaml
├── flow-hydration-summary.md
├── operation-business-flow-evidence.md
├── system-flow-evidence.md
├── program-flow-evidence.md
├── data-flow-evidence.md
├── source-snippets.md
├── field-dictionary-context.md
├── impact-scope.md
├── contradictions.md
└── retrieval-gaps.md
```

## 6. 输出给 Legacy Spec Factory 的契约

Legacy Spec Factory 不直接读取 RAG 内部数据库。RAG 应输出文件包。

推荐格式：Markdown 为主，YAML index 为辅。

```text
rag_runs/<MODULE-SLUG>/<RUN-ID>/
├── rag-run-index.yaml
├── flow-hydration-summary.md
├── source-snippets.md
├── field-dictionary-context.md
├── impact-scope.md
├── contradictions.md
└── retrieval-gaps.md
```

`rag-run-index.yaml` 示例：

```yaml
rag_run:
  module_slug: CREDIT-LIMIT
  run_id: RAG-20260521-001
  source_snapshot: ibmi-export-2026-05-21
  dictionary_version: dict-v34
  arcad_ref_snapshot: arcad-ref-2026-05-21
  input_flow_source: human_confirmed_four_flows

coverage:
  programs_found: 12
  programs_missing: 1
  tables_found: 8
  fields_mapped: 43
  fields_unmapped: 6
  snippets_returned: 31
  contradictions_found: 3

outputs:
  flow_hydration_summary: flow-hydration-summary.md
  source_snippets: source-snippets.md
  field_dictionary_context: field-dictionary-context.md
  impact_scope: impact-scope.md
  contradictions: contradictions.md
  retrieval_gaps: retrieval-gaps.md

handoff:
  target_repo_path: 00_context_packages/CREDIT-LIMIT/
  next_step: legacy-module-context-intake
  recommended_brd_mode: module_first_rag_hydrated
```

Legacy Spec Factory 整理后的目标结构：

```text
00_context_packages/<MODULE-SLUG>/
├── context-index.yaml
├── 01-operation-business-flow.md
├── 02-system-flow.md
├── 03-program-flow.md
├── 04-data-flow.md
├── rag-evidence-map.md
├── contradiction-log.md
└── open-questions.md
```

可参考一个完整但紧凑的 synthetic 输出样例：
[`docs/rag-output-sample/`](rag-output-sample/)。

## 7. 冲突和缺口处理

RAG 输出必须显式暴露冲突，不能帮用户悄悄合并。

常见冲突：

| 冲突类型 | 示例 | 处理 |
| --- | --- | --- |
| ARCAD vs source | ARCAD says CUE64 writes ARBAL, source parser did not find it | contradiction, IT SME review |
| dictionary vs source | Dictionary says CRLMT is approved credit limit, code uses it as temporary exposure cap | contradiction, data owner + SME review |
| human flow vs RAG flow | Human flow says CUE64 calls CUE71, graph only finds CUE64 -> ERRMSG | flow comparison note |
| table metadata vs source | Table field exists but no code reads/writes it | dormant/zombie candidate |
| source usage without dictionary mapping | Code uses field not in dictionary | field mapping TBD |

`contradictions.md` 每条记录建议包含：

```yaml
id: RAG-CONFLICT-<MODULE>-<NNN>
type: dictionary_source_mismatch
summary: Short human-readable statement.
observed_from_code:
  snippet_id: SNP-CUE64-042
  line_start: 320
  line_end: 356
dictionary_claim:
  standard_field_id: DD-CUSTOMER-CREDIT-LIMIT
  dictionary_version: dict-v34
impact:
  affected_flows:
    - 03-program-flow.md
  affected_outputs:
    - BRD rules
next_owner: Data Owner / Business SME / IT SME
status: needs_review
```

## 8. MVP 建设顺序

### MVP 1: Metadata-heavy Hybrid Retrieval

目标：

- source / ARCAD / dictionary / table metadata 可导入。
- 能按 program、table、field、standard_field_id 精准召回。
- 每个结果有 artifact id、snapshot、line range、source path。

完成标准：

- 输入 `CUE64` 能返回 source artifact、ARCAD refs、相关 tables、candidate snippets。
- 输入 `ARCUST.CRLMT` 能映射到标准字段或标记 unmapped。

### MVP 2: Program Flow Query

目标：

- 支持 `program_flow(program_name)`。
- 能输出 upstream / current / downstream / table I/O / snippets。

完成标准：

- 对 CUE64 类 program，能给出上下游、读写表、关键代码片段。
- 输出可被人工校正。

### MVP 3: Field Impact Query

目标：

- 支持 `field_impact(field_name | standard_field_id)`。
- 以标准字段为中心反查所有 legacy aliases 和程序影响面。

完成标准：

- 改一个字段时，能看到 direct impact、indirect impact、screen/report impact、snippet evidence。

### MVP 4: Flow Hydration

目标：

- 输入四条人工确认 flow。
- RAG 围绕四条 flow 补证据。

完成标准：

- 输出 `rag_runs/<MODULE>/<RUN-ID>/` evidence bundle。
- 包含 contradictions 和 retrieval gaps。

### MVP 5: Legacy Spec Factory Integration

目标：

- `legacy-module-context-intake` 将 RAG bundle 归一化进入
  `00_context_packages/<MODULE>/`。
- module analyzer / BRD writer 可以基于 module-first + RAG evidence 生成
  reviewable downstream package。
- RAG / AI retrieval 不是 source of truth，只是 context candidate generator。
  source of truth 是 SME-reviewed context package，以及有 evidence 支撑的
  BRD / spec / validation artifacts。

完成标准：

- 输入四条 flow + RAG output。
- 输出 BRD + Validation Package：

```text
05_brds/<MODULE-or-CAPABILITY>/
├── brd.md
├── brd-review.md
├── validation-scenarios.md
├── traceability.md
├── source-evidence-map.md
├── flow-comparison-notes.md
└── open-questions.md
```

其中 `validation-scenarios.md` 只产出 BRD 阶段的 `VAL-*` 业务验证场景种子，
用于 SME 验证、SOW 讨论和后续测试计划输入；不提前生成正式 `AC-*`
acceptance criteria，也不提前生成正式 `TC-*` golden master test cases。

## 9. 会议对齐建议

下午对齐建议重点确认这些问题：

1. RAG 第一版是否只承诺 `program_flow`、`field_impact`、`dictionary_lookup`、`hydrate_flows` 四个查询。
2. ARCAD REF 的关系数据能否稳定导出 caller/callee、program-file、field reference。
3. 数据字典能否提供 `standard_field_id`、aliases、definition、owner、version、status。
4. Source parser 是否能产出 line-range snippets 和 file I/O / field usage。
5. RAG 输出是否统一采用 Markdown bundle + `rag-run-index.yaml`。
6. Legacy Spec Factory 是否只消费 RAG output package，不直接耦合 RAG 内部数据库。
7. 冲突处理是否按 `contradictions.md` 显式输出，而不是自动合并。

推荐达成的结论：

```text
RAG builds the evidence and relationship layer.
Legacy Spec Factory builds the reviewed business artifact layer.
The handoff between them is a file-based RAG evidence bundle.
```
