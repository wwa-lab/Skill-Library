# 本地交付测试记录

日期：2026-09-05，Asia/Shanghai。平台：macOS；Python 3.14.3；开发测试 Node 25.9.0；本机 Chrome 152.0.7977.76（无头、全新上下文、网络禁用）。没有安装或升级依赖，没有使用 Office 自动化、在线转换或外部 CDN。

## 已通过

| 验证 | 结果与证据 |
| --- | --- |
| Python 自动测试 | 23 项：构建、Markdown/图片/讲稿、模型限制、安全 ZIP/XML、真实 PPTX 往返、POTX 品牌/布局、解释器选择、中文及空格路径、仅本机预览、分发完整性 |
| 纯内容模型测试 | 6 项：不可变历史、撤销重做、顺序、错误数据拒绝、数据约束、原样保存脚本文字 |
| 网页真实 UI 全链路 | 修改标题/正文/讲稿/字号/强调色/对齐/图片及裁切/表格/图表；拖动和按钮排序；增删复制、撤销重做；两次下载 HTML 并重开，完整模型逐项一致 |
| 导出最新内容 | 从第二次保存的 HTML 通过 UI 导出 PPTX/POTX，检查最新文字、字体大小/颜色/对齐、讲稿、图片裁切字节、页序、表格内容和图表值 |
| 原生 PPTX 结构 | 六页、六份讲稿、一张独立图片、一张原生表格、一张原生图表及内嵌工作簿；原生流程框、箭头、文字；主题和布局包含东亚字体和占位符 |
| 新增布局页模拟 | 导出组件增加 CORPORATE_CONTENT 页，检查七页/七份讲稿、布局关系和标题占位符。是 OOXML 模拟，未在 PowerPoint 中点击新建页 |
| 导出单项测试 | 离线运行；非中心裁切像素、深色表格对比度、导入页新增标题、空标题、水平线、原生形状、错误/外链拒绝、模型不变、POTX 主内容类型 |
| 实际成品重新导入 | `six-slides.pptx → ooxml.py → build.py`，六份讲稿逐字一致，标题/正文完整，图片独立，表格与图表数据一致；POTX 提取 1 个母版和 5 个布局，含归一化占位符坐标 |
| 中文画布 | 1280×720、1366×768、1920×1080、1024×768 检查所有样例对象无溢出；另查看全部六页截图、编辑模式和三组风格预览 |
| 展示交互 | 键盘翻页、首尾页、讲稿、手动减少动态、无头浏览器全屏通过；CSS 提供系统 prefers-reduced-motion |
| 独立离线文件 | 浏览器上下文断网、禁止 HTTP 请求，核心展示/编辑/保存/导出通过；`python3 -S` 禁用 site 包后仍能构建 |
| Skill 校验 | 本 Skill `quick_validate.py` 通过；仓库 `node scripts/validate-skills.mjs` 通过（42 Skills） |
| 分发包 | 标准库 ZIP、相对文件名、排除缓存、逐文件 SHA-256 验证；解包得到完整 `corporate-web-slides/` |

机器可读证据：[浏览器报告](../tests/records/browser-test-report.json)。截图：[常见桌面](../tests/records/display-1280x720.png)、[4:3 投影](../tests/records/projection-1024x768.png)、[编辑模式](../tests/records/editing.png)、[封面](../tests/records/slide-1.png)、[图片页](../tests/records/slide-3.png)、[流程页](../tests/records/slide-4.png)、[表格页](../tests/records/slide-5.png)、[图表页](../tests/records/slide-6.png)。

成品主样例保持六页。导出单项测试中的第七页只存在于测试输出，用于验证新增页布局；没有额外加到交付演示。

## 平台支持与验收矩阵

“支持”表示 Skill 的设计与运行方式覆盖该平台；“已验证”只表示下表列出的实际环境完成过对应验收。不得用其他平台或 OOXML 结构测试替代目标平台实机结论。

| 平台/组件 | 目标支持 | 当前验证状态 | 备注 |
| --- | --- | --- | --- |
| macOS + `python3` | 是 | ✅ 已验证 | 本记录环境为 macOS + Python 3.14.3；构建及自动测试通过 |
| macOS + Chrome | 是 | ✅ 已验证 | Chrome 152，无头全新上下文、网络禁用；完整 UI 编辑/保存/导出链路通过 |
| macOS + Safari | 可兼容目标，不作为当前默认浏览器 | ⚠️ 未验证 | 需在公司实际 Safari 版本人工确认 file://、下载、全屏、编辑与导出 |
| PowerPoint for Mac | 是 | ⚠️ 未验证 | 需确认无修复提示、逐对象编辑、图表数据、讲稿、新增页布局及 POTX 复用 |
| Windows 11 + `py -3` / run.cmd | 是 | ⚠️ 未验证 | 已测解释器选择逻辑及中文/空格路径，不等同于 Windows 实机通过 |
| Windows 11 + Edge/Chrome | 是 | ⚠️ 未验证 | 需覆盖公司受管策略、file:// 与必要时 127.0.0.1 预览 |
| PowerPoint for Windows | 是 | ⚠️ 未验证 | 与 Mac 版相同，需真实 Office 交互验收 |
| Linux + Python | 开发/构建兼容 | 附件记录：2026-09-18 Linux 会话复测（本机未复核） | 来自 source ZIP 的历史声明；Python 3.13.5；23/23 Python 自动测试、6/6 JS 模型测试通过；不代表浏览器 UI 已验证 |

Mac 与 Windows 的 PowerPoint 验收要分别记录，不能因为其中一个平台通过就把另一个平台标记为通过。公司正式发布时，建议至少保留 Chrome(macOS)、Edge/Chrome(Windows)、PowerPoint for Mac、PowerPoint for Windows 四条主链路；Safari 是否纳入正式支持范围由公司实际使用情况决定。

## 未验证及明确限制

- **Windows 11 实机、`py -3` / run.cmd 真正启动、受管 Edge/Chrome 策略：未验证。** 已测解释器选择逻辑及中文/空格路径，不等同于这些目标环境通过。
- **实际 PowerPoint 打开、无修复提示、逐对象继续编辑、新增页/模板继承：未验证。** 已确认 OOXML 对象及布局结构；需要目标机器按 [人工清单](quality-checks.md) 验收。
- 开发机器装有 Node，浏览器产物没有调用 Node，网络隔离测试已通过；未在完全未安装 Node 的 Windows 机器上实测。Node 仅运行开发者自动测试，不是产物依赖。
- 系统字体未嵌入；Windows YaHei 与当前 macOS 中文回退字体不同，PowerPoint 字距、换行和原生图表留白须目标端复核。
- 导入始终报告 `completeFidelity: false`。富文本、图片原始裁切、源母版继承、复杂对象等规范化限制见 [导入范围](import-support.md)；本测试的通过不表示任意公司 PPTX 都能无损转换。
- 未测超大演示的性能、数小时持续播放或所有公司浏览器版本；200 页为输入上限，不是性能保证。浏览器缓存容量不足时仍依靠 HTML 下载保存。

## 可重复运行

从 Skill 根目录，标准库测试：

```bat
py -3 -m unittest discover -s tests -p "test_*.py" -v
```

已有开发测试工具时（不自动安装）：

```sh
node --test tests/test_model.mjs tests/test_theme.mjs tests/test_qa.mjs tests/test_editor.mjs
CORPORATE_TEST_BROWSER='/path/to/chrome' node tests/test_export_browser.mjs /path/to/playwright/index.mjs /temporary/export-check
CORPORATE_TEST_BROWSER='/path/to/chrome' node tests/test_editor_browser.mjs /path/to/playwright/index.mjs /temporary/editor-check --deliver
CORPORATE_TEST_BROWSER='/path/to/chrome' node tests/test_presentation_browser.mjs /path/to/playwright/index.mjs /temporary/presentation-check
CORPORATE_TEST_BROWSER='/path/to/chrome' node tests/test_gate_c_browser.mjs /path/to/playwright/index.mjs /temporary/gate-c-check
```

`--deliver` 会重写 `examples/six-slides.pptx` / `.potx`；不带此参数只产生临时编辑验收文件。可通过 `CORPORATE_TEST_PYTHON` 指定现有 Python，Windows 默认测试器使用 `py -3`。本记录未测平台不能因重新运行其他平台测试自动改成“通过”。

## v1.1 本地开发基线与 Gate A（2026-09-18）

仓库基线 main `00b9b9264a3bc011fa087f4337b2a7c52cf8e919`，开始时工作树干净。原有 Python 23/23、JS 6/6、仓库 42 Skills 校验通过。source ZIP 仅合入打包修复及文档增量；附件 Linux 结果为历史声明。

本轮环境：macOS-27.0-arm64-arm-64bit-Mach-O；Python 3.14.3；已安装 Chrome 153.0.8010.50，无头隔离离线上下文。Gate A 原有 exporter/editor 浏览器回归及新主题/CSP/恶意标题/保存重开验证通过，见 `tests/records/v1.1/gate-a-*.json`。这是自动化浏览器验收，不是人工 Office 实机验收。Windows/受管 Edge、Safari、PowerPoint Windows/macOS 均 NOT VERIFIED。

## v1.1 Gate B/C 与回归复核（2026-09-18）

当前源代码候选在 macOS-27.0-arm64；Python 3.14.3；开发测试 Node 25.9.0；本机 Chrome 153.0.8010.50；浏览器上下文断网。仓库 `node scripts/validate-skills.mjs` 通过（42 Skills），Python 套件 31/31，Node 纯模型/主题/QA/画布/富文本测试 21/21。

| 当前候选验证 | 结果与证据 |
| --- | --- |
| Gate A 主题、CSP 与离线保存回归 | 通过：三种主题、母版布局占位符、恶意标题纯文本、哈希 CSP、全新上下文保存 HTML 并精确重开；`tests/test_v11_browser.mjs` |
| Gate B 演示交互回归 | 通过：主题选择、章节目录、演讲者视图/计时/黑屏、内部/外部链接及 QA；[`gate-b-report.json`](../tests/records/v1.1/gate-b-retest/gate-b-report.json) |
| 全量编辑器回归 | 通过：四种画布尺寸、中文溢出、文字/图片/表格/图表编辑、页序、撤销重做、两次保存重开、PPTX/POTX 最新模型；输出 `/tmp/cws-v11-editor-regression`，只在当前机器保留 |
| Gate C 画布与富文本 | 通过：拖动、缩放、键盘微调、Shift 多选、对齐、单次撤销/重做、段落/项目符号/编号/缩进/字符样式和链接；离线下载 HTML 并在新上下文精确重开；[`gate-c-browser.json`](../tests/records/v1.1/gate-c/gate-c-browser.json) |
| Gate C 最新内容 PPTX | 通过 OOXML 内容检查：六页六份讲稿，检查原生文本运行、列表段落、加粗/字号/颜色、HTTPS 关系、图片、流程形状、表格、图表/工作簿及布局；成品 [`富文本与画布编辑后.pptx`](../tests/records/v1.1/gate-c/富文本与画布编辑后.pptx)，保存后 HTML [`完整 保存 中文 演示.html`](../tests/records/v1.1/gate-c/完整%20保存%20中文%20演示.html) |
| 离线供应链/源审计 | 通过：派生 vendor 可重复、源代码审计、六页及三组预览 HTML 的 CSP/资源/模型检查通过；前端无 HTTP 请求 |

Gate C 的 PPTX 检查确认 XML 对象与关系可编辑，不代表在 PowerPoint UI 中打开无修复提示或操作通过。PowerPoint for Mac/Windows、Windows 11 与公司受管 Edge/Chrome、Safari 均仍为 **NOT VERIFIED**。当前浏览器自动化在 macOS Chrome 运行，4 种视口的中文溢出检查已通过；Windows 字体度量仍需实机验收。
