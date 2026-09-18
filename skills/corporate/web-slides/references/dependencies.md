# 离线依赖与原生 PowerPoint 导出

## 随包运行时

| 组件 | 锁定版本/来源 | 用途 | 许可 |
| --- | --- | --- | --- |
| PptxGenJS 浏览器运行时 | 4.0.1；按仓库脚本从 npm 官方发布包派生 | 原生文本、图片、形状、表格、图表及工作簿、讲稿、布局 | MIT |
| JSZip（已包含在完整包内） | 3.10.1 | PPTX 打包、主题规范化、POTX 内容类型转换 | 选择 MIT 许可 |
| Pako、Lie、Immediate、setImmediate | 完整包内嵌代码，由整体 SHA-256 锁定 | ZIP 压缩及异步兼容 | MIT；Pako 内 zlib 派生代码另含 Zlib 许可 |
| Babel polyfill、core-js、regenerator runtime | 上游源包内嵌；core-js 标识为 2.6.11 | 上游旧版兼容代码；派生的运行时移除它们，许可证/来源记录保留 | MIT |

上游原始 bundle 以未修改字节保存在 `references/vendor/pptxgenjs-4.0.1.upstream.txt`：460,889 字节，SHA-256 `4fb9eac5cfefb213e2d8743c2b7151025f31bfb3f834c73c12062916daa0f3f8`。可离线分发的运行时 `assets/vendor/pptxgenjs-4.0.1.bundle.js` 由 `scripts/vendor_offline.py` 可复现派生，361,796 字节，SHA-256：

```text
4fb9eac5cfefb213e2d8743c2b7151025f31bfb3f834c73c12062916daa0f3f8
```

上游文件来自 [PptxGenJS 4.0.1 发布归档](https://registry.npmjs.org/pptxgenjs/-/pptxgenjs-4.0.1.tgz) 的 `package/dist/pptxgen.bundle.js`。派生过程删除旧 Babel polyfill 和非浏览器代码路径，保持 PptxGenJS/JSZip 浏览器 API；变更由 `scripts/vendor_offline.py` 和 `tests/test_security.py` 固定检查。上游包由 [固定版本构建脚本](https://github.com/gitbrent/PptxGenJS/blob/v4.0.1/gulpfile.js) 将 [libs](https://github.com/gitbrent/PptxGenJS/tree/v4.0.1/libs) 与导出器组合。用户运行时不访问这些网址。

`assets/vendor/manifest.json` 记录派生文件校验和、上游归档来源及许可证参考包。上游内嵌的 Babel/regenerator 等代码未逐项提供版本标识，因此参考包版本用于取得对应版权许可文本，不冒充完整、可重建的 npm 锁文件；实际运行代码以派生配方和 SHA-256 锁定。所有对应许可证随包保留。分发完整 Skill 时保留 `assets/vendor/` 与此说明；单文件 HTML 的构建流程包含许可证文本/来源说明。

2026-09-05 对浏览器实际代码完成额外许可审计：PptxGenJS v4.0.1 的 `libs/jszip.min.js` 与 npm JSZip 3.10.1 的浏览器压缩分发文件字节完全一致。官方 JSZip 浏览器包共 54 个模块：JSZip 自身（1–35）、Immediate（36）、Lie（37）、Pako（38–53）、setImmediate（54）。虽然 JSZip 的 Node 包依赖 `readable-stream`，浏览器映射将其替换为自带的 `lib/readable-stream-browser.js`（模块 16），其 `stream` 映射为 `undefined`；分发文件没有包含 Node 的 readable-stream 实现及 buffer、safe-buffer、string_decoder、inherits、core-util-is、util-deprecate、process、isarray 等传递包。不能从 npm Node 依赖清单推断这些包已被嵌入；因此不添加虚构版本/许可记录。此证据与文件哈希记录在 manifest 的 `dependencyAudit` 中。

审计发现 Pako 的 `lib/zlib/` 代码另含 Jean-loup Gailly、Mark Adler、Vitaly Puzrin、Andrey Tupitsin 的 Zlib 许可声明，已补充为 `assets/vendor/pako-zlib-LICENSE.txt`，来源、参考归档哈希与受影响文件列表均保留。分发时需要同时保留 Pako MIT 与该 Zlib 声明；重新构建 HTML 会将新声明一起嵌入。

无 CDN、在线字体或转换 API。浏览器具备全部展示、编辑、HTML 保存与 PPTX/POTX 导出能力。生成内容需要用户已批准的 Agent/模型；这些离线操作不调用模型。Windows 安装及使用无需 Node.js/npm；Python 辅助流程仅使用标准库。不得因启动失败自动安装、升级依赖或修改系统 PATH。

## 导出 API

在 HTML 内先载入 vendor，再载入 `assets/export.js`。公共对象为 `CorporateExport`：

```javascript
const pptx = await CorporateExport.build(latestDeckModel);
const blob = await CorporateExport.toBlob(latestDeckModel);
await CorporateExport.download(latestDeckModel);
await CorporateExport.download(latestDeckModel, { template: true });
```

`build` 返回 PptxGenJS 实例，可以继续增加原生对象；其 `write({outputType:'blob'|'uint8array'|'base64'|...})` 会应用公司主题。应用应使用 `toBlob`/`download`；不要直接调用实例的 `writeFile`，以免绕过主题规范化。每次导出重新复制并验证传入模型，不读取缓存或静态初始内容，不修改原模型。

母版布局名为 `CORPORATE_COVER`、`CORPORATE_CONTENT`、`CORPORATE_DATA`、`CORPORATE_IMPORTED`。前三者含原生标题和正文占位符、品牌规则线、页码及可选 Logo。导入页布局保持空白，以便定位导入对象。所有布局使用同一主题颜色、标题/正文字体和东亚字体。PptxGenJS 另生成一个基础空白布局。公司源模板的任意原始母版不逐字节复制；分析结果归一化为这四种布局。

原生新增页示例：

```javascript
const slide = pptx.addSlide({masterName: 'CORPORATE_CONTENT'});
slide.addText('新增页标题', {placeholder: 'title'});
slide.addText('正文', {placeholder: 'body'});
```

这是对布局结构的程序模拟，不等价于已经在 PowerPoint 用户界面中验证“新建幻灯片”。实际 Windows/PowerPoint 验收须另行执行。

## 转换规则和边界

- 16:9 固定画布为 13.333333 × 7.5 英寸，对应网页 1600 × 900；坐标除以 120，CSS 字号乘以 0.6 转为 pt。
- 文本为原生文本框；流程节点与箭头为原生形状，节点标签为独立原生文本框；图片为独立图片对象。`cover` 按网页相同位置裁切单张图片后嵌入，裁掉的像素不包含在导出图片内；需要重新裁切原图时回 HTML 使用保留的原图。`contain` 保留原图。
- 结构化段落/文本片段分别导出为可编辑的 PowerPoint 段落和 runs，包括加粗、斜体、局部字号、颜色、项目符号、编号/缩进及 HTTPS、mailto、内部幻灯片链接。网页动画仍导出为静态终态；不会截图整页。
- 表格为最多 12 × 8 的原生矩形等列宽表格，不支持合并单元格。长文字可能被 Office 的字体度量自动撑高，导出前必须消除网页溢出并在目标 PowerPoint 复核。
- 柱形、折线、饼图生成原生图表及内嵌 XLSX 数据。最多 12 个类别、4 个系列；饼图一个系列；柱形/饼图不接受负值。原生 Office 图表的图例、刻度、留白与网页 SVG 会有差异，保留数据与可编辑性，不承诺像素级一致。
- 网页逐项动画导出为全部内容可见的静态终态。分步叙述需要在模型中建立独立页面。
- PowerPoint 页码使用原生动态页码，网页显示补零的“当前页 / 总页数”；两者格式不同，重新排列/新增 PPT 页面后原生页码可继续更新。
- POTX 通过标准 OOXML 主文档内容类型转换，保留全部页面、布局和讲稿。仍需目标 PowerPoint 打开验证。
- 不支持对象、外链图片、无效数据或坐标将报错，不通过整页截图规避。没有隐式整页栅格化或上传转换服务。

## 可选开发验证

生产使用无需 Node。已有 Node、Playwright 与本地 Chrome 的开发环境可运行：

```sh
CORPORATE_TEST_BROWSER='/path/to/chrome' node tests/test_export_browser.mjs /absolute/path/to/playwright/index.mjs /temporary/output
```

不自动安装测试依赖。测试会阻断所有网络请求，并验证原生对象 XML、图表工作簿、讲稿、主题/占位符、新增布局页、裁切像素、POTX、模型不可变性以及拒绝非法对象。输出属于开发证据，不代表 Windows 11、受管 Edge/Chrome 或 PowerPoint UI 验收通过。
