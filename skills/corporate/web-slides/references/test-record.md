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
node --test tests/test_model.mjs
CORPORATE_TEST_BROWSER='/path/to/chrome' node tests/test_export_browser.mjs /path/to/playwright/index.mjs /temporary/export-check
CORPORATE_TEST_BROWSER='/path/to/chrome' node tests/test_editor_browser.mjs /path/to/playwright/index.mjs /temporary/editor-check --deliver
```

`--deliver` 会重写 `examples/six-slides.pptx` / `.potx`；不带此参数只产生临时编辑验收文件。可通过 `CORPORATE_TEST_PYTHON` 指定现有 Python，Windows 默认测试器使用 `py -3`。本记录未测平台不能因重新运行其他平台测试自动改成“通过”。
