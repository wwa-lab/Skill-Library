# corporate-web-slides

用于公司内部分享、培训和路演的英文优先网页演示 Skill。默认红、白、黑风格；可在浏览器编辑，保存完整 HTML，并导出原生可编辑 PPTX 或可复用 POTX。用户可以指定中文或其他目标语言。

## 快速体验

直接用 Edge / Chrome 打开 `examples/six-slides.html`。样例六页包含文字、图片、流程、表格、图表和讲稿；所有统计数字均为演示数据。无需 Node.js、Python、联网或模型即可展示、编辑、保存和导出。

随包六页验证样例保留中文内容；新建演示默认使用英文，也可按请求使用其他语言。

1. 点击“编辑”，选择正文或左侧目录页面。输入后移出输入框即生效。
2. 在面板修改标题/讲稿，选择独立对象修改正文、字号、颜色、对齐；文字对象可拆分段落并设置项目符号、编号、缩进、字重、斜体、局部字号/颜色和安全链接。画布上拖动对象可移动，拖动选框角点可缩放；按住 Shift 多选，可对齐/等距，方向键微调（Shift+方向键每次 10 单位）。图片可替换、切换完整显示/裁切填充、调整横纵裁切位置。数据对象有 JSON 编辑框及“应用数据”。
3. 增加、复制、删除页面；拖动目录排序或用上移/下移按钮。最多撤销 30 次；删除可撤销，至少保留一页。
4. 点击“保存 HTML”，保留下载的完整文件。重开该文件可继续编辑。模型、富文本、图片和页面顺序会嵌入完整文件；不要仅保留浏览器缓存。
5. 点击“导出 PPTX”；需要复用主题时点击“导出 POTX”。在 PowerPoint 中继续编辑文字、图片、表格、图表或形状。PowerPoint 修改不会自动同步回 HTML。

展示快捷键：左右箭头、空格、PageUp/PageDown 翻页；Home/End 跳转；E 编辑；N 讲稿；F 全屏。编辑面板聚焦时不截获普通翻页键。Ctrl/Cmd+S 保存；面板外 Ctrl/Cmd+Z 撤销，Ctrl/Cmd+Shift+Z / Ctrl+Y 重做。“减少动态”与系统减少动态设置均受支持。浏览器下载受公司策略限制时，不能以缓存替代保存。

## 安装 Skill

分发时复制整个目录，勿只复制 SKILL.md。仓库内路径为 `skills/corporate/web-slides`，安装后为平铺命名 `corporate-web-slides`。

OpenCode 项目级安装：在目标项目下创建 `.opencode/skills/corporate-web-slides/`，将本目录内容放进去。仓库安装器的全局默认是用户目录 `.config/opencode/skills/corporate-web-slides/`。手动复制无需 Node、管理员权限或更改 PATH。其他获准 Agent 可直接读取 SKILL.md 及同目录资源；本包不增加平台适配器。

给 Agent 的示例请求：

> 用 corporate-web-slides，把这份培训材料做成 12 页英文演示，沿用默认红白黑风格，配完整英文讲稿，输出离线 HTML 和可编辑 PPTX。

> 分析公司模板.potx，复用颜色、字体和 Logo。将已有培训.pptx 转为网页，先检查并保留所有转换警告。

## 从源文件构建

生成新内容需要用户批准的 Agent/模型，将内容写成 JSON；确定性封装只需要已有 Python 3.9+ 标准库。从 Skill 根目录运行，Windows 优先：

```bat
py -3 scripts/build.py "examples\six-slides.json" --output "输出\演示.html"
py -3 scripts/build.py "examples\starter.md" --output "输出\入门.html" --preview-styles
py -3 scripts/ooxml.py "C:\公司资料\公司 模板.potx" --out "输出\品牌" --brand-only
py -3 scripts/ooxml.py "C:\公司资料\已有 培训.pptx" --out "输出\导入"
py -3 scripts/build.py "输出\导入\deck.json" --brand "输出\品牌\brand.json" --output "输出\培训.html"
```

转换后先查看 `conversion-report.json`，不支持对象会列出位置、原因和可提取内容；原 PPTX 请保留。品牌里的 `logoCandidates` 需要核对后将所选 `src` 写入 `logo`。母版和布局被分析并规范化重建，不能承诺完整复刻源模板。

需要指定 Python 时使用 `scripts\run.cmd --python "C:\工具\Python\python.exe" build.py ...`，或 `CORPORATE_SLIDES_PYTHON`；详见 [Windows 指南](references/windows.md)。macOS/Linux 使用已检测到的 `python3` 或绝对解释器路径。

公司浏览器限制本地 HTML 时：

```bat
py -3 scripts/preview.py "输出" --port 8765
```

打开本机 `http://127.0.0.1:8765/演示.html`；按 Ctrl+C 停止。服务拒绝目录浏览、路径穿越、符号链接，不向局域网开放。

## 文件与支持范围

| 位置 | 用途 |
| --- | --- |
| `SKILL.md` | Agent 的触发及执行规范 |
| `assets/deck-template.json` / `default-brand.json` | 可复制的三页内容模板与品牌配置 |
| `assets/shell.html` / `style.css` / `*.js` | 单文件生成模板、模型、渲染、编辑、导出组件 |
| `assets/vendor/` | 锁定的前端库、校验和、许可证 |
| `scripts/` | 标准库构建、PPTX/POTX 提取、解释器发现、本机预览 |
| `examples/` | 六页 JSON / HTML / PPTX / POTX、Markdown、风格预览 |
| `references/` | 输入与品牌、支持边界、依赖、验收记录 |
| `tests/` | Python、模型及可选浏览器集成测试 |

采用固定版式内微调，不是自由画布。支持最多 200 页、每页 100 个对象；文本最多 50 段、每段 100 个文本片段；表格最多 12 行×8 列、无合并；柱状/折线/饼图最多 12 类别、4 系列（饼图 1 系列）。超出范围请拆分或由 Agent重新组织，不得静默丢内容。

网页动画导出为静态终态。复杂 SmartArt、分组、视频、OLE、复杂图表等会报告限制，不用整页截图代替可编辑页面。独立图片裁切可能烘焙像素；字体不嵌入，换设备须检查替代字体。原生 Office 图表由 PowerPoint 绘制，轴线、图例等细节与网页不保证逐像素一致。

[详细导入支持](references/import-support.md) · [内容模型](references/model-contract.md) · [依赖和许可](references/dependencies.md) · [质量检查](references/quality-checks.md) · [测试记录](references/test-record.md)

## 开发者验证

普通用户不需要运行 Node.js 测试。已有 Python 即可运行必要辅助流程测试：

```bat
py -3 -m unittest discover -s tests -p "test_*.py" -v
```

已有 Node.js、Playwright 和本地测试浏览器的开发者可运行独立模型测试及完整浏览器链路，具体命令见测试记录。测试不自动安装依赖。当前 macOS + Chrome 已有完整浏览器链路实测记录；macOS Safari、PowerPoint for Mac、Windows 11 的 Edge/Chrome 与 PowerPoint 仍需目标环境实机验收。macOS 与 Windows 的 Office 结果分别记录，不能互相替代；详见 [测试记录](references/test-record.md) 和 [验收清单](references/quality-checks.md)。

Gate C 浏览器复测示例（传入已有 Playwright 模块和 Chrome 可执行文件，不安装依赖）：

```sh
CORPORATE_TEST_BROWSER='/path/to/chrome' node tests/test_gate_c_browser.mjs /absolute/path/to/playwright/index.mjs /temporary/gate-c-check
```

该验证会用中文/空格目录写出 HTML 和 PPTX；独立解包检查 OOXML 原生富文本。它不等同于 PowerPoint UI 验收。

## 重新打包

维护者完成检查后，可用现有 Python 生成独立 ZIP：

```bat
py -3 scripts/package.py --output "..\corporate-web-slides.zip"
```

ZIP 内是平铺安装目录 `corporate-web-slides/`，并带 `PACKAGE-MANIFEST.json` 的逐文件 SHA-256。脚本排除运行缓存和旧压缩包；只在本地写文件，不安装或发布。

### English interface and technology themes

Generated controls, presenter tools, help and runtime messages default to English. The Theme selector includes Tech Cyan, Digital Violet and Tech Light alongside brand-specific presets. Technology presets use `brand: "universal"`, retain the deck brand and logo, and remap theme card and border colours without moving objects. Custom colours remain explicit overrides. A white logo backing keeps an unmodified dark wordmark readable on dark slides in HTML and native PowerPoint layouts. These presets are presentation styles, not official brand approvals.
