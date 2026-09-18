# Security policy — corporate-web-slides v1.1

Security is a release gate. Run `python3 scripts/security_audit.py --html examples/six-slides.html` (Windows: `py -3`). Also run the Python, model and available browser tests recorded in `references/test-record.md`. This tool does not replace the company's security review.

## Goals and threat model

Treat Office ZIP/XML, deck JSON, theme/brand JSON, text, notes, images and editor input as untrusted data. Protect against executable content, external resource loading, archive traversal and unbounded decompression. Input confidentiality and portable offline operation take priority over adding features. Arbitrary existing HTML is not an import format: only open generated HTML from a trusted source.

The user controls local source code and generated files. CSP hashes do not digitally sign a file: a person able to replace the HTML can also replace its CSP. This is not malware scanning or a sandbox for arbitrary third-party HTML. Review the source and distribution hashes before deployment.

## Offline operation and files

No network requests are required for presentation, editing, saving or export. No telemetry, conversion service, cloud storage, update checker or runtime AI is included. Python operates on explicitly selected local files; the optional preview server binds only `127.0.0.1`. The browser reads selected PNG/JPEG files and downloads complete HTML/PPTX/POTX. Local storage is a recovery copy only and may retain presentation content in the browser profile; save the HTML and follow company retention policy.

Generating new content can use the user's approved Agent/model and is separate from offline operation. This package never chooses or calls an AI service.

## Content and theme data

All user text is rendered using DOM/textContent. JSON embedded in HTML escapes `<`; XML export escapes text. No user HTML/CSS/JS, SVG imports, iframe, OLE, macros or plugin runtime are accepted. Internal chart SVG is constructed from validated numeric data using a fixed element vocabulary; it is not imported SVG. Images remain PNG/JPEG data URLs and are subject to size/decode limits.

Brand v2, Theme v1 and Layout v1 use closed schemas in `assets/contracts.json`. Unknown fields fail, colors are six hexadecimal digits, fonts are bounded names, numeric values and enum/array lengths are bounded. Themes cannot carry code, CSS, URLs or asset loaders. Brand logos are local approved raster images, not theme resources. Official HSBC logo asset required / not bundled.

Hyperlinks permit HTTPS, mailto and existing `#slide-id` targets; HTTP, file, data, unknown schemes and control characters are rejected. The renderer never follows links automatically. Internal targets navigate within the deck; external URLs are displayed as data for the user, and exported as native PowerPoint hyperlinks. Following an exported link is an explicit action outside offline generation.

## CSP

Build computes SHA-256 hashes of fixed vendor/application scripts and CSS. Policy includes `default-src 'none'`, `connect-src 'none'`, `object-src 'none'`, `base-uri 'none'`, `frame-src 'none'`, `worker-src 'none'`, `form-action 'none'`. Images permit only data/blob. There is no unsafe-eval, unsafe-inline or script blob allowance. Geometry/style updates use fixed CSSOM property mappings, never CSS from theme JSON. Saving preserves fixed code and CSP while replacing only data and reconstructible UI state. Chrome file/reopen behavior is covered by browser tests; managed Edge policies and Safari remain NOT VERIFIED until executed there.

## Dependencies and integrity

No new third-party runtime dependency is introduced. PptxGenJS 4.0.1 and its bundled JSZip dependency remain pinned. A documented derivative removes historical Babel polyfills, script/iframe scheduler fallbacks, dynamic string compilation, Node dynamic imports and remote/path/SVG media loading. Unsupported paths throw. `scripts/vendor_offline.py` deterministically derives the runtime from the exact original hash. The upstream reference in `references/vendor/*.txt` is inert source evidence and is never embedded or executed. Original copyrights and licenses are retained. See `references/dependencies.md` and `assets/vendor/manifest.json` for provenance.

The audit verifies the actual runtime hash, derivative reproducibility, unexpected vendor JS files, forbidden source constructs, HTML resources, script/CSS hashes and optional package manifest. URL exceptions are exact, documented entries in `assets/security-allowlist.json` for OOXML/SVG namespaces and inert upstream documentation strings. There is no blanket vendor ignore. Text/JSON and license comments are data, so malicious sample text is not mistaken for executable JavaScript. Test fixtures intentionally contain malicious strings and are not production runtime.

## Office input limits

Source ≤64 MiB; ≤4096 ZIP entries; member ≤32 MiB; total uncompressed ≤128 MiB; XML/rels ≤8 MiB; compression ratio ≤250:1; deck ≤200 slides. Reject encrypted members, duplicate names, absolute/drive paths, backslashes and `..` traversal. Reject XML DTD/entity declarations before parsing. Bad ZIP/XML fails clearly. Limits can reject unusually compressible legitimate inputs; split or simplify the source instead of silently weakening protection.

External relationships are recorded in the conversion report and never resolved over HTTP, file URLs or UNC/network shares. Unsupported Office objects remain reported, with extractable text/raw unsupported media retained where possible. Raw unsupported media is for review, never embedded in HTML as executable content.

## Known limits

Static scanning catches the specified source patterns and integrity failures; it is not a complete JavaScript parser or proof against deliberately obfuscated malicious source. Trusted release review is still required. PNG/JPEG decoding and native PowerPoint rendering depend on the installed browser/Office security posture. Fonts are not embedded. No Office or Windows UI acceptance is inferred from XML validity. Use the release test record for actual environment/version evidence.
