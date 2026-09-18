# Security implementation map

The normative policy is [SECURITY.md](../SECURITY.md). Do not duplicate or weaken it in workflow prompts.

- Input contracts: `assets/contracts.json`, `scripts/contracts.py`, `assets/theme.js`, `assets/model.js`, `scripts/build.py`.
- Office container boundary: `scripts/ooxml_package.py`; relationship reports: `scripts/ooxml.py`.
- Browser content: `assets/render.js` uses DOM text nodes; editor mutations are validated immutable model commits.
- Runtime dependency: `scripts/vendor_offline.py` and `assets/vendor/manifest.json`; pristine reference is `.txt`, never runtime.
- HTML boundary: `scripts/build.py` escapes JSON, embeds only fixed source and computes CSP hashes. HTML save retains those fixed scripts; data remains data.
- Audit: `scripts/security_audit.py`; exceptions list exact inert URLs with reasons.
- Adversarial regression: `tests/test_security.py`, `tests/test_theme.mjs`; browser tests cover actual CSP, literal malicious text and saved-file reopen.

Run source + final HTML audit after rebuilding and before packaging. A source audit Pass does not certify unscanned HTML artifacts. Regenerate all shipped examples after runtime changes. Do not change allowlists to hide a live network/code path.
