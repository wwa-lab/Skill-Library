# Review Notes: Interactive Subfile Example

**Example Objective:** Demonstrate positive case analysis for an interactive DSPF screen with subfile, showing:
- Complete extraction of screen layout, fields, and indicators
- Subfile dimensions from DDS keywords, with runtime/program behavior separated
- Proper evidence linking (EV-* to DDS source)
- Realistic TBD handling for ambiguous program logic
- No invented facts; all claims traced to DDS or runtime evidence

## Key Analysis Elements Demonstrated

### 1. Surface Type Classification
- **DSPF (Interactive Display File with Subfile)** clearly identified
- Related objects (programs, files) linked via OBJ-* IDs from inventory
- Presentation purpose documented from source comments and runtime context; business purpose remains SME-reviewable

### 2. Layout Analysis
- Screen dimensions (24 rows × 80 columns) documented
- Record formats identified: MAINSCR (header), ORDDETAIL (subfile detail), ORDCTL (subfile control)
- Visual description maps DDS structure to user view

### 3. Field Extraction
- All fields listed with name, role, type, length, decimal places, edit code/mask
- Field roles come from DDS and runtime evidence; business purpose is noted as TBD/SME-reviewable when needed
- Example: ORDNO marked as conditionally protected because a DDS indicator context is present
- Example: TOTAL marked as currency format (edit code A) from EDTCDE(A) keyword

### 4. Indicator Mapping
- Each indicator (#01, #03, #04, #05, #06, #99) listed with purpose
- Set-by and cleared-by source documented only when program/runtime evidence supports it
- Indicator usage patterns:
  - **Protection/display indicators**: #03 (ORDNO), #05 (ORDDATE), #06 (TOTAL) have DDS conditioning context
  - **Validation/message indicators**: #01 and #04 require program context for set/clear timing
  - **Subfile control**: #99 has SFLCLR context and job-log evidence for refresh behavior
- Evidence linked to DDS or job log

### 5. Subfile Behavior Documentation
- Subfile definition extracted: SFLPAG(10), SFLSIZ(100), SFLDROP(05), SFLCLR(99)
- Page-down behavior: observed in screenshot sequence; exact reload/scroll mechanism left to program context
- Selection field (SEL): multi-select via user input; marks items for action
- Clear logic: SFLCLR(99) indicator cleared by program; typically on F5 (REFRESH) or when switching modes

### 6. Function Key & Command Key Documentation
- All F-keys listed: F1 (ACCEPT), F2 (CANCEL), F5 (REFRESH), F6 (DELETE)
- CA/CF distinction: CA01 (command attention) causes exit; CF not used in this example
- DDS labels documented for all keys; program actions are confirmed only where job log or SME evidence supports them

### 7. Validation & Constraints
- CUSTID: MANDATORY keyword documents screen-level entry requirement; lookup behavior remains program/SME evidence
- QTY: No DDS constraints visible; validation moved to TBD (program-level custom logic)
- LINEAMT: Output-only, formula not explicit in DDS → TBD pending program analysis

### 8. Program Touchpoints
- Related program OBJ-ORDER-ENTRY-001 identified
- EXFMT to MAINSCR, WRITE loop for subfile records documented
- Indicator usage correlated only where job log evidence exists; other set/clear paths remain TBDs
- Evidence from job log showing EXFMT sequence

### 9. Observed Behaviors (BEH-*)
Four behaviors documented from runtime evidence:
- **BEH-ORDER-ENTRY-001**: Visible subfile rows change after page-down (runtime observation; mechanism pending program context)
- **BEH-ORDER-ENTRY-002**: Subfile clears on F5 REFRESH (SFLCLR(99) confirmed)
- **BEH-ORDER-ENTRY-003**: Selection plus F6 raises delete-semantics question unless program evidence confirms removal
- **BEH-ORDER-ENTRY-004**: Invalid CUSTID shows error message without clearing order (program control flow)

### 10. Inferred Questions (SEED-*)
Four candidate seeds for downstream analysis:
- **SEED-ORDER-ENTRY-001**: Delete operation mechanics (SEL field + F6 only way, or other modes?)
- **SEED-ORDER-ENTRY-002**: Processing sequence when F1 pressed (deletes, updates, inserts in order?)
- **SEED-ORDER-ENTRY-003**: Whether target UI should preserve the 10-row legacy page size
- **SEED-ORDER-ENTRY-004**: Item status codes / restrictions (some items non-editable?)

### 11. TBD Ledger
Three TBDs identified (all non-blocking):
- **TBD-ORDER-ENTRY-001**: QTY validation constraints (MINVAL, MAXVAL not visible in DDS; stock check mentioned but unclear)
- **TBD-ORDER-ENTRY-002**: SEL + deletion trigger (indicator action vs. F6 code required?)
- **TBD-ORDER-ENTRY-003**: LINEAMT calculation source (program computed or database-derived?)

Each TBD includes:
- Issue description (specific, not vague)
- Category: pending_source (missing DDS), pending_program_context (program logic needed), pending_sme_judgment (business meaning)
- Blocking status: all "no" (non-blocking; analysis can proceed to flow/module level)
- Resolution path: specific next step (e.g., "Review program I-specs and MONITOR block")
- Owner: who should resolve (program analyzer, SME, etc.)

## What This Example Gets Right

✅ **No Invented Facts**
- Only DDS keywords and runtime evidence are cited
- Inferences marked as SEED-* or TBD-*, not presented as facts
- Field business meaning is either source-literal presentation context or marked for SME/program review

✅ **Complete Evidence Linking**
- Every field, indicator, subfile keyword has at least one EV-* link
- DDS source (EV-ORDER-ENTRY-012) is the primary authority
- Screenshots and job log provide runtime corroboration

✅ **Clear Indicator Mapping**
- Each indicator has keyword context and set/clear evidence status
- Indicator patterns documented without turning shop conventions into facts
- Relationship between indicators and keywords explained (e.g., #03 + PROTECT)

✅ **Realistic TBD Handling**
- TBDs are specific, not dismissive ("something unclear")
- Category clarifies resolution type (source, context, judgment)
- Non-blocking TBDs allow analysis to proceed while noting gaps

✅ **Downstream Usability**
- Program analyzer can reference this when analyzing OBJ-ORDER-ENTRY-001
  - TBD-ORDER-ENTRY-001 prompts program analyzer to confirm QTY validation
- BEH-ORDER-ENTRY-001/002 provide context for program paging and refresh handling
- Flow analyzer can understand user actions and screen state transitions
- Module/capability modeler can use BEH-* and SEED-* for business rule mining

## What This Example Avoids

❌ **Not Invented**
- No field labels inferred as business meaning (ITEMDESC is described, not assumed to mean "product name")
- No indicator set/clear behavior guessed (keyword context is separated from program behavior)
- No function key behavior assumed from DDS label alone

❌ **Not Over-Simplified**
- Subfile paging complexity documented without overstating DDS keywords
- Indicator state transitions are explained only when evidenced; otherwise marked TBD
- Error paths explicitly noted (error message display, re-entry behavior)

❌ **Not Under-Evidenced**
- Every major claim linked to DDS or runtime evidence
- Confidence levels recorded (high, medium) where observations support them
- Open questions explicitly marked as TBD, not left implicit

## How to Use This Example

**For Analysts:**
- Follow this template (templates/screen-report-analysis.md) when analyzing your own DSPF
- Use the field inventory table, indicator mapping, and subfile behavior sections as a checklist
- Ensure every BEH-* and SEED-* has corresponding EV-* evidence links

**For Reviewers:**
- Use templates/screen-report-review-checklist.md when reviewing analyses
- Check that:
  - All fields are DDS-sourced (not invented)
  - All indicators have keyword context and evidence status
  - All TBDs have categories and resolution paths
  - All BEH-* have runtime evidence
  - No claims are made without evidence links

**For Downstream Skills:**
- Program analyzer: Use TBD-* to confirm program-level validation, indicator usage, deletion logic
- Flow analyzer: Use BEH-* for user action sequences, state transitions, paging patterns
- Module/capability modeler: Use SEED-* as candidates for business rules (with SME review)

## Next Steps for This Analysis

1. **Obtain SME Review**: IBM i/DSPF expert reviews field names, indicator logic, subfile behavior, validation realism
2. **Forward to Program Analyzer**: TBDs are resolved during program analysis of OBJ-ORDER-ENTRY-001
3. **Use in Flow Analysis**: Screen state transitions and user actions inform ORDER-ENTRY flow model
4. **Reference in Module Synthesis**: BEH-* and SEED-* candidate rules for capability model

## Conformance to Review Gate

This example demonstrates alignment with [docs/skill-review-gate.md](../../docs/skill-review-gate.md):

- ✅ **Purpose and trigger clarity**: Clear when to use (screen/report analysis task, approved inventory required)
- ✅ **Workflow completeness**: 9 ordered steps in SKILL.md; templates and examples provided
- ✅ **IBM i correctness**: DSPF DDS keywords are recorded conservatively; program behavior is not inferred from labels alone
- ✅ **Evidence and anti-hallucination**: All claims linked to EV-*; TBDs explicitly marked; no invented facts
- ✅ **Output contract**: Canonical artifact shape defined; required sections/IDs specified
- ✅ **Progressive disclosure**: SKILL.md concise; references, templates, examples loaded as needed
- ✅ **Portability**: Canonical skill under skills/; portable across Codex, Claude Code, OpenCode
- ✅ **Reviewability and testability**: Review checklist provided; examples show positive and negative cases
- ✅ **Engineering handoff value**: Outputs usable by program analyzer, flow analyzer, module synthesizer
- ✅ **Maintainability**: Clear ID scheme (OBJ-*, EV-*, BEH-*, SEED-*, TBD-*); author/copyright preserved
