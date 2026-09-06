# Quality Gates

Gate rubric and required fields for `legacy-document-evidence-intake`. The
package-level gate in `intake.manifest.yaml` is the single source of truth for
handoff; per-document gates roll up into it.

## Gate Definitions

| Gate | Meaning | Handoff |
| --- | --- | --- |
| `ready` | Every document extracted cleanly; no macro/security flags; no unresolved authorization or sensitivity issues. | `legacy-flow-context-normalizer` |
| `ready_with_warnings` | Usable output exists, but some documents carry warnings (macros statically extracted, low-confidence OCR, visual review needed, partial conversion). Warnings travel forward. | `legacy-flow-context-normalizer` |
| `blocked` | At least one hard issue: unauthorized / unknown sensitivity, required redaction missing, no tooling and no usable extraction, or no document could be opened. | `legacy-ibmi-evidence-intake` (auth/sensitivity) or request better export/tooling |

## Roll-Up Rule

- Any document with `document_gate: blocked` for an authorization or sensitivity
  reason ⇒ package `gate: blocked`, route to `legacy-ibmi-evidence-intake`.
- Any document with `security_review_required: true` ⇒ package `gate` capped at
  `ready_with_warnings` until a named reviewer signs off.
- Any warning (OCR, visual-review, partial conversion) on an otherwise usable
  document ⇒ package `gate: ready_with_warnings`.
- Only when every document is `ready` with no warnings ⇒ package `gate: ready`.

## Required Fields (mechanical check)

`intake.manifest.yaml` must declare:

- `package_type: document_evidence_intake`
- `gate` ∈ {`ready`, `ready_with_warnings`, `blocked`}
- `module_slug`, `docset_slug`
- at least one `documents[]` entry, each with `doc_id`, `path`, `family`,
  `file_type`, `size_bytes`, `sha256`, `sensitivity`, `authorization_status`,
  and `document_gate`
- an `outputs` index listing every package-level file present on disk

Each `documents/<DOC-SLUG>/document.manifest.yaml` must declare its `doc_id`,
`structure` block for its family, `fragments[]` with coordinates, and
`document_gate`. Macro-enabled files must carry a `macro_findings` block with
`executed: false`.

For `ready` / `ready_with_warnings` documents, every path listed in
`normalized_outputs` must exist under the package directory.

## Forbidden In `ready` / `ready_with_warnings`

- Any document with `sensitivity: unknown` or `authorization_status: unauthorized`.
- Any conversion recorded `succeeded` without a tool having run.
- Any macro-enabled file missing a security flag.
- Any flow-view classification, business rule, or BRD/spec content.
