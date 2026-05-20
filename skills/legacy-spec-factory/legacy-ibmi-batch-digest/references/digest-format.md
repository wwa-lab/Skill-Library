# Programs Batch Digest — Format Spec

The canonical layout for `02_programs/<MODULE-SLUG>/programs-batch-digest.md`.
This is the file the SME opens when they want a single-page view of every
program in the module, sorted by where their attention is most needed.

## Layout

```markdown
# Programs Batch Digest — <MODULE-SLUG>

**Generated:** <YYYY-MM-DD> by `legacy-ibmi-batch-digest` v<X.Y.Z>
**Source:** <count> `program-analysis.md` files in `02_programs/<MODULE-SLUG>/`
**Inventory:** [`01_inventory/inventory.yaml`](../../01_inventory/inventory.yaml)
  · criticality confirmed <YYYY-MM-DD> by <SME name>

## At a glance

| Bucket | Count | SME effort |
| --- | --- | --- |
| Critical | <N>  | full review per program (~20 min each) |
| Standard | <M>  | spot-check (sample <S> of <M>) |
| Low-risk | <K>  | batch confirm if spot-check passes |
| Not yet analyzed | <L> | route to `legacy-ibmi-program-analyzer` |

Estimated SME time: <approx hours>  ·  (vs. <baseline> if every file were
opened individually)

---

## Critical (<N>) — full SME review per program

| OBJ | Role (1 line) | Key pending decisions | TBDs | Status | Detail |
| --- | --- | --- | --- | --- | --- |
| OBJ-<MOD>-<NAME> | one-sentence role from Metadata | top 3 `needs_sme_review` rows, comma-separated | <count> | draft / approved | [`<MOD>/<NAME>/program-analysis.md`](<MOD>/<NAME>/program-analysis.md) |
| ...

---

## Standard (<M>) — spot-check sample

(Pick <S> rows to verify. If all your picks confirm, the remaining
<M-S> are batch-approved.)

| OBJ | Role | Key decisions | TBDs | Status | Detail |
| --- | --- | --- | --- | --- | --- |
| ...

---

## Low-risk (<K>) — batch confirm

(Scan for anything that doesn't look truly low-risk. If nothing stands
out, batch-confirm the bucket.)

| OBJ | Role | Notes | Status | Detail |
| --- | --- | --- | --- | --- |
| ...

---

## Not yet analyzed (<L>)

These programs are in inventory but have no `program-analysis.md` yet.
Route to `legacy-ibmi-program-analyzer` (or defer with SME approval).

| OBJ | Source member | Criticality | Why pending |
| --- | --- | --- | --- |
| ...

---

## SME signoff

Tick when you finish each bucket. Detailed rejections / corrections go in
`08_business-understanding/<CAP-*>/sme-review-<YYYY-MM-DD>.md` (see
`legacy-sme-review-facilitator`).

- **Critical bucket** ({{n_critical}} programs)
  - Reviewed by: _________________
  - Date: _________
  - Result: ☐ all approved   ☐ <N> rejected → see review log

- **Standard bucket** ({{n_standard}} programs)
  - Spot-check sample size: _____  /  {{n_standard}}
  - Reviewed by: _________________
  - Date: _________
  - Sample result: ☐ all picks passed → batch-approve rest
                    ☐ <N> picks failed → expand sample or full review

- **Low-risk bucket** ({{n_low_risk}} programs)
  - Reviewed by: _________________
  - Date: _________
  - Result: ☐ batch confirmed   ☐ <N> flagged for re-classify → see review log

- **Not-yet-analyzed bucket** ({{n_unanalyzed}} programs)
  - Decision: ☐ analyze before flow-analyzer   ☐ defer (reason: _____)

---

## Re-render

This digest is regenerated on every run of `legacy-ibmi-batch-digest`.
Do NOT hand-edit table rows; edit the source `program-analysis.md` or
`inventory.yaml` and re-run:

```bash
# (manual; orchestrator can also drive)
# Re-run when programs change or after new program-analysis files land
```
```

## Field extraction rules

### `OBJ id`

Take verbatim from `inventory.yaml.objects[].id`. Never abbreviate.

### `Role (1 line)`

Priority order:

1. The first line of `program-analysis.md` → `Metadata.role` (if a `role:` field is present in Metadata)
2. Else, the first non-empty sentence of the program's Metadata block
3. Else, `inventory.yaml.objects[].role`
4. Else, `(role unstated — see detail)`

Strip line breaks; cap at 80 characters; append `…` if truncated.

### `Key pending decisions`

For analyzed programs only. Take rows in `program-analysis.md` where
`review_status: needs_sme_review`. Pick **top 3** by significance:

1. Rows whose table is "Control Flow" or "Error Handling" AND touch
   money / posting / compliance / customer-status (look at the
   Description column for keywords: `posting`, `credit`, `compliance`,
   `customer status`, `inventory`, `price`, `discount`, `payment`)
2. Rows in "External Calls" with `TBD-*` IDs
3. Any other `needs_sme_review` row

Format: `<short-description-from-description-column>` — no `Step ID`,
no row reference. Comma-separated. Cap each at 60 characters.

If no `needs_sme_review` rows: write `(none)`.

### `TBDs`

Count of rows in the "Open Questions" table whose `Resolution` column is
empty (or absent). For not-yet-analyzed programs: blank.

### `Status`

For analyzed programs: read `program-analysis.md` →
`Metadata.review_status`. Render as one of:

- `draft` — `review_status: draft`
- `approved` — `review_status: approved` or
  `approved_with_non_blocking_tbd`
- `blocked` — `review_status: needs_sme_review` AND blocking gate exists
- `(unknown)` — no `review_status` field

### `Detail`

Markdown link to the `program-analysis.md` path, relative to the digest
file's own location. Format: `[<MOD>/<NAME>/program-analysis.md](<path>)`.

If the file does not exist (not-yet-analyzed): no link; that program
appears in the "Not yet analyzed" table instead.

## Counts in "At a glance"

- `Critical` = count of inventory programs with `criticality: critical`
  AND a `program-analysis.md` file
- `Standard` = same with `criticality: standard`
- `Low-risk` = same with `criticality: low_risk`
- `Not yet analyzed` = inventory programs without a corresponding
  `program-analysis.md`

`Estimated SME time` heuristic:

- Critical: 20 min × N
- Standard: spot-check sample of `min(M, max(5, ceil(M × 0.2)))`, 15 min × sample size
- Low-risk: 30 min flat for the whole batch
- Add 10 min buffer

Render as a rough hour range (e.g. "2.5–3.5 hours total"), not a precise
number. The baseline comparison ("vs. 5+ hours if every file were
opened") uses `total_programs × 5 min` for the per-file open
cost (rough heuristic; SMEs typically take 5 minutes minimum just to
load context per file).

## Anti-patterns

- Do NOT add columns beyond what the spec defines. The SME's eye is
  trained on this layout; new columns slow them down.
- Do NOT show `TBDs` as a list of TBD-IDs. Just the count. Detail is in
  the linked file.
- Do NOT highlight rows with colors / emoji / markers. Keep the digest
  monochrome and grep-friendly.
- Do NOT include the digest's own "SME signoff" block in any other
  file. Signoff happens here, once, per module.
