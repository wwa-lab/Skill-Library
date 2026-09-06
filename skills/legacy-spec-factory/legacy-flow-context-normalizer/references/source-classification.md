# Source Classification Guide

Use this guide to inventory historical documents without confusing document
shape with proof of current behavior.

## Document Role Classification

Record both:

- `format`: the physical file type, such as `docx`, `xlsx`, `pdf`, `pptx`, or
  `vsdx`.
- `source_type`: the document role, such as `function_spec`,
  `technical_design`, `program_spec`, `file_spec`, `interface_spec`,
  `data_dictionary`, `mixed_spec_workbook`, `flow_diagram`, `runbook`, or
  `sme_note`.

The source set does **not** need to contain all roles below. Use whatever the
team has, preserve gaps as `TBD-*`, and avoid treating a design document as
proof of current production behavior without SME or source/runtime evidence.

| Source Type | Usually Helps With | Notes |
| --- | --- | --- |
| `function_spec` / `functional_spec` | Operation / Business Flow, candidate business events, user actions, expected outcomes, exception intent | Good for business intent, but may describe intended behavior rather than current IBM i behavior. |
| `technical_design` | System Flow, integration boundaries, batch timing, security/SLA assumptions, technical exception handling | Treat as architecture/design evidence until corroborated by source, runtime, or SME. |
| `program_spec` | Program Flow, menus, jobs, reports, entry points, technical branching, program-to-program relationships | Candidate execution detail only; do not infer business meaning from program names alone. |
| `file_spec` / `record_layout` | Data Flow, file/table ownership, fields, record formats, read/write/update direction | Strong for structure; business meaning still needs dictionary or SME confirmation. |
| `interface_spec` / `batch_layout` / `api_spec` | System Flow and Data Flow across upstream/downstream systems | Preserve message/file direction and timing separately from business approval logic. |
| `data_dictionary` | Data Flow and business vocabulary | Prefer approved enterprise dictionary terms when they exist. |
| `mixed_spec_workbook` | Any view, depending on sheet names and headers | Use for multi-sheet Excel where each sheet may represent a different spec or inventory role. |
| `flow_diagram` / `process_deck` | Operation / Business Flow, System Flow, cross-view hints | Diagram arrows can be ambiguous; carry uncertain directions as SME questions. |
| `runbook` / `procedure` | Operation / Business Flow, manual steps, controls, workarounds | Often captures actual operations; confirm whether it is current. |
| `rag_summary` / `code_knowledge_summary` | Cross-view candidate evidence and retrieval gaps | Keep as candidate context, not approved truth. |
| `sme_note` | Any view, especially unresolved gaps | Record owner/date; SME notes can approve meaning only when clearly framed as a decision. |

## Format Handling

| Format | Preferred Extraction | Notes |
| --- | --- | --- |
| `.docx` | OOXML text, headings, tables | Preserve heading path and table row locators. |
| `.xlsx` / `.csv` | Workbook sheets, table rows | Record sheet name, header row, and row number. |
| `.pptx` | Slide text, speaker notes, embedded tables | Record slide number and shape or table label. |
| `.pdf` | Text extraction, page images when needed | Record page number; low-confidence OCR must be marked. |
| `.vsdx` | Diagram XML text, page names, connectors; exported PDF/SVG/PNG if XML is insufficient | Request an export when connector direction or labels are unreadable. |
| `.md` / `.txt` | Plain text sections | Preserve section headings and line or paragraph locators when available. |
| image / screenshot | OCR or manual transcription with page/region locator | Low confidence unless SME confirms. |
| RAG summary | Existing RAG IDs and snippet links | Keep RAG candidates as candidates; do not promote. |
| SME notes | Named note, date, owner, meeting reference | SME note is evidence, but not source-code proof. |
| ARCAD inventory CSV | Library, object-type, and description columns | Record library, object type (`*PGM`, `*FILE`, etc.), and object name. Use for View 3 (Program Flow) and View 4 (Data Flow) candidate seeds. Names are 10-character IBM i conventions; do not infer business meaning from them. |
| Skyview EA / Stingray call-graph export | Caller/callee node pairs, edge type, module label | Edges are static-analysis candidates only; runtime call order requires SME or source-code confirmation. |
| IBM i ACS object report (`DSPOBJ` / `DSPOBJD` spool) | Object name, library, type, text description | Text description is often short or blank. Treat as candidate seed, not confirmed business description. |
| iDoctor / IBM i Code Review HTML/CSV | Program, procedure, reference map | Cross-reference candidate; do not treat as runtime proof without source analysis. |

## Evidence Strength

Use these values in view tables and `evidence-map.md`:

| Strength | Meaning |
| --- | --- |
| high | Current, authoritative source or SME-confirmed artifact with clear locator. |
| medium | Clear historical document evidence but current-state confirmation missing. |
| low | OCR, screenshot, old diagram, inferred connector direction, or ambiguous table row. |
| blocked | Source exists but cannot be read or authorization is unresolved. |

## View Classification Heuristics

For `.xlsx` files, prefer:

```bash
python3 skills/legacy-flow-context-normalizer/scripts/extract_excel_fragments.py \
  <workbook>.xlsx \
  --module-slug <MODULE-SLUG> \
  --output 00_context_packages/<MODULE-SLUG>/flow-normalization/source-document-index.yaml
```

The helper reads every sheet in the workbook. It uses the first non-empty row
as headers and emits one `FRAG-*` per non-empty data row with locators like
`Interfaces row 4` or `Data Dictionary row 12`.

Sheet names such as `Function Spec`, `Technical Design`, `Program Spec`, and
`File Spec` are useful signals. They should guide candidate view
classification, but they do not make any view mandatory.

Classify by the question the fragment answers:

| Fragment answers... | View |
| --- | --- |
| Who does what, when, why, and what business outcome changes? | Operation / Business Flow |
| Which systems exchange work, messages, files, or scheduled batches? | System Flow |
| Which applications, jobs, menus, programs, or reports execute? | Program Flow |
| Which data objects are read, changed, derived, retained, or owned? | Data Flow |

When one fragment fits multiple views, cite the same `FRAG-*` in each view but
write a view-specific statement. Do not clone the same sentence into all four
views.

## Confidence Traps

- Old diagrams often show intended architecture, not actual operations.
- Function Specs and Technical Designs often show intended or target behavior,
  not necessarily the current legacy implementation.
- Excel application inventories may list ownership but not runtime sequence.
- A PowerPoint process arrow may mean a business handoff, a system call, or a
  reporting dependency. Keep it ambiguous until another source or SME resolves
  it.
- File names and table names are not business data meanings.
- A missing exception path in a diagram does not prove the exception does not
  exist.
- A Visio swimlane can be an organization, role, application, or batch
  responsibility. Preserve the original label and ask SME to classify it.

## SME Review Routing

Route questions to the owner most likely to answer:

| Question Type | Preferred Reviewer |
| --- | --- |
| Business sequence, manual work, exception handling | Business SME / operations lead |
| System boundary, interface timing, upstream/downstream ownership | Integration architect / application owner |
| Program/job/menu execution detail | IBM i technical lead / application developer |
| Data meaning, lifecycle, retention, lineage | Data owner / data analyst |
| Obsolete vs current document conflict | Module owner plus source document owner |
