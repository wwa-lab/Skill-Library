# Manual Fallback Reference

The MVP reverse chain now has implemented skills for the core IBM i path:

- `legacy-ibmi-inventory`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-flow-analyzer`
- `legacy-ibmi-module-analyzer`
- `legacy-spec-writer`

Use this fallback reference only when the recommended route is genuinely
planned, future, deferred from MVP, or unavailable in the local runtime. Do not
send users to manual fallback for implemented MVP skills unless the runtime
cannot load that skill and the user explicitly accepts a manual workaround.

## Principle

For every planned or unavailable skill, produce the **same artifact shape** the
implemented version would produce, following:

- the artifact's defined output contract (see the README artifact chain)
- the schema in `schemas/spec.schema.yaml` for any spec-shaped output
- the ID conventions in `docs/id-conventions.md`
- the taxonomy in `docs/evidence-and-knowledge-taxonomy.md`

This way, downstream skills can consume the manually produced artifact without
rework once the missing skill or runtime becomes available.

## Per-Skill Fallback

### Implemented MVP Skills

Do not use manual fallback in normal routing for:

- `legacy-ibmi-inventory`
- `legacy-ibmi-program-analyzer`
- `legacy-ibmi-flow-analyzer`
- `legacy-ibmi-module-analyzer`
- `legacy-spec-writer`

Route directly to the implemented skill. If an air-gapped runtime cannot load
one of these skills, follow that skill's `SKILL.md`, templates, and examples
verbatim and record the workaround in the review notes.

### Folded Supplemental Analysis (manual only when explicitly requested)

The former standalone Program Call Map, CRUD matrix, DDS/schema, business-rule, and
capability-mapping tasks are folded into the MVP analyzers. Only use these
manual workflows when a user specifically asks for the standalone supplemental
view.

#### Program Call Map View

1. For each in-scope program, read the source with the team
2. Extract internal routine definitions plus `EXSR` / `CALL` / `CALLP` / `SBMJOB`
3. Build an RDi-style call map plus edge table showing routine and program edges
4. Tag each edge with confidence and evidence
5. Mark unresolved calls (target program not in inventory) as
   `TBD-<SLUG>-<NNN>` and update the inventory's `coverage_gaps`

#### CRUD Matrix View

1. For each program, list each file with the access kind: `reads | writes |
   updates | deletes`
2. Produce a markdown table: rows = programs, columns = files, cells = CRUD
3. Tag each row with evidence IDs

#### DDS / Screen Schema View

1. Read each `PF`, `LF`, `DSPF`, `PRTF` source
2. Produce `data-dictionary.md` (PF/LF fields with type, length, decimals,
   keys) and `screen-map.md` (DSPF/PRTF formats, indicators, function keys)
3. Note CCSID and packed/zoned decimal semantics where relevant
4. Tag inferred semantics with `needs_sme_review`

### `legacy-ibmi-runtime-evidence-miner` (Planned)

**Manual workflow:**

1. Collect redacted job log, spool, and sample transactions per
   `docs/data-collection-and-redaction.md`
2. Build `runtime-evidence.jsonl`, one event per line, with fields:
   `id`, `source_type`, `location`, `summary`, `evidence_strength:
   observed_in_runtime`, `linked_objects: [OBJ-*]`
3. Reference these from program-analysis or business-rules artifacts

### Business Rule Notes (folded into module/spec writer)

**Manual workflow:**

1. For each significant behavior found in program analysis or runtime
   evidence, ask: is this a **business rule** or a **technical workaround**?
2. For business rules, write a `BR-<SLUG>-<NNN>` entry with:
   - `knowledge_type: inferred_business_rule` (or `observed_behavior` if it
     is purely behavior with no inference)
   - linked `evidence_ids`
   - `linked_behaviors`
   - `confidence` and `review_status: needs_sme_review`
3. Reject anything that cannot be tied to evidence

### Capability Notes (folded into module/spec writer)

**Manual workflow:**

1. Group rules with common business intent into capabilities
2. Produce `capability-map.md` listing each capability with its constituent
   `BR-*` IDs and its `CAP-<SLUG>-<NNN>` ID
3. Capabilities do not have to align with program boundaries — that is the
   point

### `legacy-spec-reviewer` (Planned)

**Manual workflow:**

1. Run the spec through the gate criteria in
   [references/gates.md](gates.md), Gate 3 + Gate 4 criteria
2. Produce `review-report.md` listing pass / blocking findings per criterion
3. Update `spec.yaml.status: in_review` and add review_notes

### `legacy-equivalence-test-generator` (Planned)

**Manual workflow:**

1. For every business-critical rule, design at least one golden master test
   case
2. Test inputs and expected outputs must come from runtime evidence, not
   guesses
3. Save under `06_quality/golden-master-tests.md` with `TC-*` IDs traceable
   back to `BR-*` IDs

## When to Stop Using a Manual Fallback

Switch back to the orchestrator-recommended skill the moment it becomes
implemented (status moves from `Planned` to `Implemented` in repository
`README.md#target-skill-family`). The manual artifact, if it followed the
contract, drops in unchanged.

If the artifact does not follow the contract, treat the implemented skill as
authoritative and regenerate — do not patch the manual artifact to look like
it came from the skill.
