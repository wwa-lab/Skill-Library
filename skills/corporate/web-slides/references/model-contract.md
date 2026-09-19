# Corporate Web Slides model v1 / 1.1

Shared implementation contract. JSON only, no HTML markup; coordinates in 1600×900 CSS design pixels. Native PPTX uses 13.333333×7.5 inches (divide geometry by 120; font px × 0.6 = pt).

```json
{"version":1,"modelVersion":"1.1","id":"deck-id","title":"Presentation Title","brand":{"name":"Corporate","accent":"C8102E","background":"FFFFFF","foreground":"171717","muted":"666666","fontFace":"Arial","titleFontFace":"Arial","logo":null},"slides":[{"id":"s1","title":"Slide Title","notes":"Complete speaker notes","layout":"content","section":"Section","elements":[]}],"warnings":[]}
```

- `modelVersion` 可缺省以兼容 v1 输入；新增输出设为 `1.1`。v1.1 使用严格的 Brand / Theme / Layout 契约（见 `assets/contracts.json`），可以有 `theme`。布局包括 `cover`、`content`、`data`、`imported`、`section`、`title-body`、`two-column`、`image-text`、`kpi`、`comparison`、`timeline`、`process`、`closing`、`freeform`。
- Generated header title 默认位于 x=100,y=92,w=1400,h=125；fontSize=58（封面 82）。可选 slide `titleBox` `{x,y,w,h}` 存储被编辑的标题框几何；可选 `layoutOverride` 标记显式版式微调。导入页标题可为空，实际内容以对象表示。页眉页脚是可复用主题，不承诺逐像素复刻源母版。标题硬上限为 52 个字符；英文标题建议保持简短；溢出会报告，不静默裁掉。
- 可选 `section` 为最长 100 字的目录章节标签。页面对象 ID 在一页内唯一，页面 ID 在整个演示中唯一。
- Each element: unique `id`, `type`, finite `x,y,w,h` within canvas. Order is stacking order. Optional `fontSize` (default 32 CSS px), `color` six hex digits, `align` (`left`,`center`,`right`), `bold`.
- `text`: 兼容模式只需 `text` 纯文本（换行分段）。可选 `paragraphs` 启用结构化富文本：每段 `{align?,list?,indent?,runs}`；`list` 为 `none|bullet|number`，`indent` 为 0–5；每个 run `{text,bold?,italic?,fontSize?,color?,hyperlink?}`。最多 50 段、每段 100 个 run，文本总长度最多 20,000 字。`text` 必须等于各段 run 文本拼接并以换行分隔；它作为纯文本兼容回退。链接仅允许 HTTPS、mailto 和指向已有页面 ID 的 `#slide-id`。HTML 将文字作为文本节点渲染，PPTX 将格式、列表和链接输出为原生可编辑文本。
- `image`: `src` embedded data URL (PNG/JPEG only baseline), `alt`, `fit` (`contain` or `cover`), `positionX`, `positionY` normalized 0..1 default .5. Browser and export must apply the same crop. Original embedded image stays independent in PPTX; cropping may be baked into image pixels but no whole-page rasterization.
- `shape`: `shape` (`rect`,`roundRect`,`ellipse`,`arrow`,`line`), `fill` hex, optional `text`, `color`, `fontSize`. Lines use x,y,w,h as nonnegative extents.
- `table`: `rows` rectangular string[][], first row header; optional fontSize default 28, color, accent. Max 12 rows × 8 cols. Equal-width cells and equal-height rows. No merges in v1.
- `chart`: `chartType` (`bar`,`line`,`pie`), `labels` string[], `series` [{name:string,values:number[]}], optional `colors` hex[]. Single series for pie, nonnegative values for bar/pie, line can use negatives. At most 12 categories, 4 series. Native chart workbook exported.
- `brand.logo` optional PNG/JPEG data URL, rendered at x=1340,y=28,w=160,h=48 contain. Logo candidates/template inventories may additionally be kept in brand `source`, `themeColors`, `fonts`, `masters`, `layouts`, `logoCandidates`. Reusable native master uses normalized brand. Arbitrary source masters are analyzed, not byte-for-byte cloned.
- Optional slide `background` six hex digits overrides brand. Optional `titleStyle` {fontSize,color,align}. Object-level `layoutOverride` and slide-level `titleBox` record editor geometry. `warnings` array strings reports all known conversion losses; imports may carry `source` provenance. Unknown elements fail validation, never disappear silently.
- Animation rule: authored elements enter with subtle CSS reveal; PPTX exports fully visible static final state. Build explicit sequential slides if distinct key steps are necessary.
- A single validated JSON model is authoritative. DOM, cache and generated PPTX are derivatives. Save embeds latest JSON and complete CSS/JS/vendor code. Notes/HTML user strings must be textContent/escaped, never executable markup.
