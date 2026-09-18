# Brand, Theme and Layout

Brand v2 specifies company identity, preferred font names, approved local logo slot/box, footer, base colors and chart palette. Default: `assets/brands/hsbc/brand.json`. A missing logo is valid and renders nothing; no unofficial logo is supplied.

Theme v1 specifies visual tokens only. Bundled IDs: `hsbc-light`, `hsbc-executive`, `hsbc-dark`. Fonts, colors, typography roles, spacing, cards, table style, chart palette, title decoration and footer appearance are validated against the closed schema in `assets/contracts.json`. Another company can supply a Brand v2 and theme whose `brand` matches its ID. There is no HSBC-specific renderer branch.

Layout v1 is semantic geometry, kept separately in `assets/layouts.json`. Layout IDs: cover, section, title-body, two-column, image-text, kpi, comparison, timeline, process, data, closing, freeform, imported; `content` remains a v1 alias. Reapply Layout explicitly partitions the layout's slots among all existing objects and never drops objects. Dense layouts fail if resulting slots become too small. Freeform/imported preserve geometry.

The canonical model stays version 1 for compatibility; `modelVersion: "1.1"` is additive. Existing complete v1 decks remain valid with their own brand and geometry. Missing brand defaults to HSBC Light. `theme` contains the complete theme JSON, not a URL. `CorporateTheme.resolve/element/title` supply both renderers. A theme switch remaps matching previous brand colors, preserves custom colors and x/y/w/h, and keeps notes, IDs and content unchanged. Explicit element typography remains an override; use semantic `role` and omit explicit styles to fully inherit theme typography.

Manual canvas changes set `layoutOverride: true`. Only the distinct Reapply Layout action resets geometry/that flag. Style switching never calls layout application.

Native exported layouts use `<BRAND_ID>_<LAYOUT>` names (hyphens become underscores). Legacy unthemed decks retain CORPORATE_COVER/CONTENT/DATA/IMPORTED. Semantic layouts contain native title/body placeholders, reusable brand chrome and East Asian fonts. A two-column layout contains two body placeholders. This is normalized generation, not exact cloning of a supplied PowerPoint master. Test package structure and actual Office New Slide behavior separately.
