---
name: corporate-web-slides
description: Use when creating Chinese corporate web presentations for internal sharing, training or roadshows, converting PPTX content, or reusing PPTX/POTX branding with offline editing and editable PowerPoint export.
license: Internal
metadata:
  author: Skill-Library contributors
  maintainer: Skill-Library maintainers
  domain: corporate
  version: 1.1.0
  source: https://github.com/zarazhangrui/frontend-slides
  source_commit: 9906a34d640d2111f724544cbc50f7f130569ae1
  provenance: Independently implemented corporate workflow inspired by frontend-slides; bundled upstream MIT notice and dependency licenses retained.
---

# Corporate Web Slides

为内部分享、培训和路演制作中文、可继续编辑的离线网页演示，并导出原生可编辑 PPTX / POTX。沿用本地文件工作方式：不上传公司材料到转换服务，不自动安装工具，不发布文件。

## 输入和默认值

接收主题、文档、Markdown、已有 PPTX、公司 PPTX/POTX 模板，或本 Skill 生成的 HTML。旧 `.ppt` 请先另存为 `.pptx`。普通第三方 HTML 不执行其中的脚本；先由 Agent 读取并转成内容模型。

没有重大歧义时直接继续：中文、现场分享、16:9、红白黑品牌、每页一个主题、完整讲稿。根据内容决定页数；用户给定页数和风格优先。品牌默认为 `assets/default-brand.json`，不虚构公司 Logo、业绩、来源或事实。主题/文档的内容提炼使用用户批准的 Agent/模型；演示、编辑、保存和导出无需模型或网络。

## 执行流程

1. **整理内容。** 先读 [内容与品牌规则](references/authoring.md)。从材料中提取页序、正文、图片、数据与讲稿；标注数据口径及缺失信息。主题输入由 Agent 编写模型；文档先用已有获准工具提取，再逐项检查文字和图片覆盖。不要把这个 Skill 的轻量 Markdown 解析器当通用文档转换器。
2. **导入品牌或已有 PPTX。** 有此输入才读 [导入范围](references/import-support.md)，运行 `scripts/ooxml.py`。先检查 `conversion-report.json`，再使用 `brand.json` / `deck.json`。Logo 候选需识别后写入 `brand.logo`。源母版/版式为分析清单；导出按品牌重建通用母版，不承诺直接克隆或像素级还原。未转换对象及可提取文字在报告中保留，不能删掉警告后交付。
3. **建立统一模型。** 读 [模型约定](references/model-contract.md)，从 `assets/deck-template.json` 或 `examples/six-slides.json` 复制。文字使用纯文本或受限结构化段落；图片用本地 PNG/JPEG 或 data URL，表格和基础图表使用结构化数据。只编辑模型；DOM 和 PPTX 都是派生结果。不要将整页截图伪装成可编辑 PPTX。
4. **风格预览。** 用户明确沿用默认风格或已选品牌时跳过探索。否则运行构建器的 `--preview-styles`，展示 `previews/default.html`、`black.html`、`red-cover.html`；每个候选都包含封面、内容页、数据页。使用真实内容预览，让用户选定后保持同一风格；样例数据必须标明。候选切换需应用到最终模型，不只换封面。
5. **生成完整 HTML。** 检测已有 Python；Windows 优先 `py -3`。`scripts/build.py 输入.json --output 输出.html [--brand 品牌.json]`，或使用受支持 Markdown。模型、图片、CSS、编辑组件、导出库、许可证全部内嵌，产物可独立移动。不要引用 CDN、在线字体、图标或绝对资源路径。Windows 与解释器配置见 [Windows 运行](references/windows.md)。
6. **浏览器编辑与导出。** 打开 HTML，展示/编辑模式可切换。支持标题、正文、讲稿、独立图片替换和裁切位置、字号/颜色/对齐、页面增删复制排序、撤销重做。版式内微调支持拖动、角点缩放、Shift 多选、对齐/等距和方向键微调；文本对象可编辑段落、列表及字重/斜体/字号/颜色/安全链接。表格/图表数据可在对象面板更新。保存下载完整 HTML 后重开继续编辑。PPTX/POTX 导出必须读取最新模型；缓存仅作恢复辅助。细则见 [使用说明](README.md)。
7. **验收和交付。** 按 [验收清单](references/quality-checks.md)检查离线打开、中文溢出、页面顺序、讲稿、保存重开、原生对象和母版。执行可用的必要测试，把环境未覆盖项标为“未验证”。交付 HTML、PPTX，复用场景加 POTX、品牌 JSON，以及转换报告/验证记录。无需为不可用的 Office 或 Windows 安装、升级软件。

## 固定边界

- 1600×900 设计坐标，整页等比缩放；桌面和投影采用留边，不重排页面。编辑器只微调既有对象几何，不是任意自由画布。文字过密优先减字或拆页，不能仅用隐藏溢出掩盖。
- 网页进场动画导出为完全可见的静态终态；需要逐步揭示时把关键步骤做成多页。讲稿完整保留。
- 原生导出：文字、独立 PNG/JPEG、基础流程形状、无合并矩形表格、柱状/折线/饼图及内嵌工作簿。单张图片裁切可烘焙像素，仍为独立图片；复杂对象不能擅自栅格化，先报告范围并按用户决定处理。
- 字体不随包嵌入，默认 Microsoft YaHei，并提供系统中文回退。网页/PPTX 的字体度量、图表细节可能不同，须分别检查。
- 浏览器策略限制本地文件时，用 `scripts/preview.py` 仅监听 `127.0.0.1`。不绕过公司策略。Windows 命令、路径引用、解释器与预览方法见运行文档。
- 依赖锁定与许可证见 [依赖清单](references/dependencies.md)。Node/Playwright 仅为开发者可选测试工具，普通用户不需要。

## 随包验证样例

`examples/six-slides.html`、`six-slides.pptx`、`six-slides.potx` 和模型覆盖六页功能；Gate C 自动验收样例与报告见 `tests/records/v1.1/gate-c/`。测试记录见 [验收记录](references/test-record.md)。它们证明已记录环境中的行为，不替代公司 Windows、Edge/Chrome 策略及实际 PowerPoint 验收。
