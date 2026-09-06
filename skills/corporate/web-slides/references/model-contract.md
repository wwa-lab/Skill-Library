# Corporate Web Slides model v1

Shared implementation contract. JSON only, no HTML markup; coordinates in 1600×900 CSS design pixels. Native PPTX uses 13.333333×7.5 inches (divide geometry by 120; font px × 0.6 = pt).

```json
{"version":1,"id":"deck-id","title":"演示标题","brand":{"name":"Corporate","accent":"C8102E","background":"FFFFFF","foreground":"171717","muted":"666666","fontFace":"Microsoft YaHei","titleFontFace":"Microsoft YaHei","logo":null},"slides":[{"id":"s1","title":"页面标题","notes":"完整讲稿","layout":"content","elements":[]}],"warnings":[]}
```

- layout: `cover`, `content`, `data`, `imported`. Generated header title at x=100,y=92,w=1400,h=125; fontSize=58 (cover=82). Imported slide title may be empty, with all actual content represented as elements. Footer page number/brand and top red rule are authored chrome, omitted on imported layouts. Title cannot exceed 52 Chinese characters; recommend ≤22; overflow is reported, not silently cropped.
- Each element: unique `id`, `type`, finite `x,y,w,h` within canvas. Order is stacking order. Optional `fontSize` (default 32 CSS px), `color` six hex digits, `align` (`left`,`center`,`right`), `bold`.
- `text`: `text` string, plain text with newlines.
- `image`: `src` embedded data URL (PNG/JPEG only baseline), `alt`, `fit` (`contain` or `cover`), `positionX`, `positionY` normalized 0..1 default .5. Browser and export must apply the same crop. Original embedded image stays independent in PPTX; cropping may be baked into image pixels but no whole-page rasterization.
- `shape`: `shape` (`rect`,`roundRect`,`ellipse`,`arrow`,`line`), `fill` hex, optional `text`, `color`, `fontSize`. Lines use x,y,w,h as nonnegative extents.
- `table`: `rows` rectangular string[][], first row header; optional fontSize default 28, color, accent. Max 12 rows × 8 cols. Equal-width cells and equal-height rows. No merges in v1.
- `chart`: `chartType` (`bar`,`line`,`pie`), `labels` string[], `series` [{name:string,values:number[]}], optional `colors` hex[]. Single series for pie, nonnegative values for bar/pie, line can use negatives. At most 12 categories, 4 series. Native chart workbook exported.
- `brand.logo` optional PNG/JPEG data URL, rendered at x=1340,y=28,w=160,h=48 contain. Logo candidates/template inventories may additionally be kept in brand `source`, `themeColors`, `fonts`, `masters`, `layouts`, `logoCandidates`. Reusable native master uses normalized brand. Arbitrary source masters are analyzed, not byte-for-byte cloned.
- Optional slide `background` six hex digits overrides brand. Optional `titleStyle` {fontSize,color,align}. `warnings` array strings reports all known conversion losses; imports may carry `source` provenance. Unknown elements fail validation, never disappear silently.
- Animation rule: authored elements enter with subtle CSS reveal; PPTX exports fully visible static final state. Build explicit sequential slides if distinct key steps are necessary.
- A single validated JSON model is authoritative. DOM, cache and generated PPTX are derivatives. Save embeds latest JSON and complete CSS/JS/vendor code. Notes/HTML user strings must be textContent/escaped, never executable markup.
