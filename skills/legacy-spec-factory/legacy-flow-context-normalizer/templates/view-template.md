# View N: <View Name> - <Module Name>

## Normalization Status
- status: draft_needs_sme_review # draft_needs_sme_review | triage_needs_source_enrichment | ready_for_context_intake | ready_with_warnings | blocked
- source_state: extracted_documents
- primary_sources:
  - DOC-<MODULE-SLUG>-001

## Summary
<Concise normalized view. No invented facts.>

## Mermaid Flow Diagram
```mermaid
flowchart TD
  STEP_<MODULE-SLUG>_001["<Draft flow step>"]
```

Diagram rules:
- Use `flowchart TD` unless the source order is explicitly left-to-right.
- Use node IDs that mirror `STEP-*`, replacing hyphens with underscores.
- Keep node labels business-readable for View 1; put technical names in
  parentheses only when needed.
- For View 3, draw substantive flow nodes only when AS400 / IBM i program,
  job, service program, CL/RPG object, or explicit API/menu-to-program mapping
  is evidenced. API IDs, journey IDs, menu IDs, and screen IDs may appear as
  trigger/boundary context only; if no IBM i program anchor exists, use a
  `TBD-*` placeholder node and request source supplements.
- For View 4, draw substantive flow nodes only when AS400 / IBM i files,
  tables, PF/LF objects, SQL tables, data areas, data queues,
  display/printer files, DDS/DDL objects, File Specs, CRUD/File I/O maps, or
  explicit business-data-to-file mappings are evidenced. Business data labels
  may describe a node but must not replace the concrete file/table/object name;
  if no data anchor exists, use a `TBD-*` placeholder node and request source
  supplements.
- Annotate low-confidence or SME-pending nodes with `(needs SME review)`.
- Do not add nodes or edges that are not backed by evidence rows below.

## Evidence-Linked Flow Steps
| Step ID | Sequence | Statement | Evidence Basis | Confidence | Review Status |
| --- | ---: | --- | --- | --- | --- |
| STEP-<MODULE-SLUG>-001 | 1 | <Draft flow step in view-appropriate language.> | DOC-<MODULE-SLUG>-001; FRAG-<MODULE-SLUG>-001 | medium | needs_sme_review |

<!--
Evidence Basis field guidance:
- View 1 (Operation/Business): cite DOC-* and FRAG-* only; keep technical names in parentheses.
- View 2 (System): may also cite SYS-<MODULE-SLUG>-NNN for system nodes extracted from diagrams or
  inventory lists. Example: DOC-<MODULE-SLUG>-001; SYS-<MODULE-SLUG>-001 (HOST-CREDITCHECK).
- View 3 (Program): may also cite PGM-<MODULE-SLUG>-NNN for programs/jobs extracted from documents.
  Example: DOC-<MODULE-SLUG>-001; PGM-<MODULE-SLUG>-001 (CCHK100).
  Do not cite API IDs, menu IDs, journey IDs, screen IDs, or service names as
  PGM-* unless a source maps them to IBM i programs/jobs/objects.
- View 4 (Data): may also cite DATA-<MODULE-SLUG>-NNN for data objects extracted from data
  dictionaries or CRUD tables. Example: DOC-<MODULE-SLUG>-002; DATA-<MODULE-SLUG>-001 (APPLICPF).
  Do not cite business labels such as request data, customer profile, or card
  account status as DATA-* unless a source maps them to IBM i files/tables/data
  objects.
SYS-*, PGM-*, and DATA-* IDs are draft identifiers; they must appear in evidence-map.md
Extracted Fragments section the same way FRAG-* IDs do.
-->

## Candidate Seeds
| Candidate ID | Candidate Statement | Business Signal | Evidence Basis | Required Review |
| --- | --- | --- | --- | --- |
| CAND-<MODULE-SLUG>-001 | <Candidate to confirm, not a rule.> | <Business decision, control, SLA, ownership, exception, or capability affected.> | DOC-<MODULE-SLUG>-001; FRAG-<MODULE-SLUG>-001 | SME confirm / reject |

## Gaps For SME Review
| TBD ID | Category | Question | Evidence | Owner | Blocking |
| --- | --- | --- | --- | --- | --- |
| TBD-<MODULE-SLUG>-001 | pending_sme_judgment | <Question that must be answered before context intake or can be carried forward.> | DOC-<MODULE-SLUG>-001 | <Owner> | yes |
| TBD-<MODULE-SLUG>-002 | source_supplement_required | <For View 3, ask for API/menu-to-program mapping, IBM i inventory, ARCAD export, DSPPGMREF/call graph, program spec, or SME-confirmed entry program. For View 4, ask for File Specs, DDS/DDL, data dictionary, CRUD matrix, File I/O map, or SME-confirmed file mapping.> | DOC-<MODULE-SLUG>-001 | <Application SME or Data owner> | yes |
