# Windows 11 安装、Python 与离线预览

将整个 Skill 目录复制到用户可写目录；不需要管理员权限，不修改 PATH，不自动安装任何依赖。生成 JSON/Markdown 的阶段需要已批准的 Agent 与模型；生成后的 HTML 自带样式、脚本、图片和 PPTX 库，展示、编辑、保存及导出不需要模型、Python 或 Node.js。

已有 Python 时，优先在终端使用 `py -3`。路径中有中文或空格时始终加引号：

```bat
py -3 "C:\公司资料\web slides\scripts\build.py" "C:\公司资料\分享 内容.md" --output "C:\公司资料\分享.html"
py -3 "C:\公司资料\web slides\scripts\build.py" "C:\公司资料\分享.json" --brand "C:\公司资料\品牌.json" --output "C:\公司资料\分享.html" --preview-styles
```

也可使用随包启动器，它优先查找 `py -3`，然后检查当前 Python、`python3` 和 `python`；通过探测得到实际 `sys.executable`，用参数数组执行辅助程序。

```bat
"C:\公司资料\web slides\scripts\run.cmd" build.py "C:\公司资料\分享 内容.md" --output "C:\公司资料\分享.html"
"C:\公司资料\web slides\scripts\run.cmd" --python "C:\用户工具\Python\python.exe" build.py "C:\公司资料\分享.json" --output "C:\公司资料\分享.html"
```

解释器也可通过当前终端的 `CORPORATE_SLIDES_PYTHON` 环境变量配置。指定的解释器无效时明确失败，不擅自改用另一解释器。该变量仅指定一个可执行文件路径，不允许附加命令参数。可用 `py -3 scripts/python-runtime.py --print` 查看解析结果。启动器不下载、安装或升级软件。

双击生成 HTML 即可使用。公司策略若限制 `file://`，在包含输出文件的最小目录启动预览：

```bat
py -3 "C:\公司资料\web slides\scripts\preview.py" "C:\公司资料\演示输出" --port 8765
```

打开 `http://127.0.0.1:8765/分享.html`。服务只监听 `127.0.0.1`，拒绝目录列表、路径穿越和符号链接；按 Ctrl+C 停止。不要把不相关的私人文件放进预览目录。公司浏览器策略若同时禁用下载或本机服务，需要联系公司 IT；工具不会绕过策略。

在编辑模式点“保存 HTML”下载完整副本；关闭浏览器之前保存。缓存仅辅助恢复。重新打开保存的 HTML 后，可继续编辑并导出最新 PPTX。PowerPoint 的后续改动不反向同步。

## 平台验证边界

单元测试覆盖中文与空格路径、Python 解释器选择逻辑、非法解释器失败、静态 HTML 构建及本机预览访问限制。它们不等同于 Windows 11 实机验证。`run.cmd`、受管 Edge/Chrome 策略、PowerPoint 对象编辑及“新增幻灯片继承主题”必须另行在目标设备人工验收；未完成前不得标记通过。
