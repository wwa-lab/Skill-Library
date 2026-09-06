"""Standard-library regression tests: python -m unittest discover -s tests -p test_build.py."""
import base64
from contextlib import contextmanager
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


build = module("slide_build", "build.py")
runtime = module("slide_runtime", "python-runtime.py")
preview = module("slide_preview", "preview.py")
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aZ1kAAAAASUVORK5CYII=")


def deck():
    return {"version": 1, "id": "test", "title": "中文标题", "brand": build.DEFAULT_BRAND.copy(), "warnings": [], "slides": [{"id": "s1", "title": "中文标题", "notes": "讲稿\n完整保留", "layout": "content", "elements": [{"id": "t1", "type": "text", "text": "正文", "x": 100, "y": 250, "w": 1400, "h": 400}]}]}


def fixture_assets(root):
    assets = root / "assets"
    (assets / "vendor").mkdir(parents=True)
    (assets / "shell.html").write_text('<!doctype html><title>__TITLE__</title><style>__CSS__</style><script id="deck-data" type="application/json">__DECK_JSON__</script><script>__VENDOR__</script><script>__APP_JS__</script><pre>__LICENSES__</pre>', encoding="utf-8")
    (assets / "style.css").write_text("body{color:#171717}", encoding="utf-8")
    for name in ("model.js", "render.js", "export.js", "app.js"):
        (assets / name).write_text("/* " + name + " </script> */", encoding="utf-8")
    (assets / "vendor" / "pptx.js").write_text("window.PptxGenJS=function(){};", encoding="utf-8")
    (assets / "vendor" / "LICENSE.txt").write_text("MIT <copyright>", encoding="utf-8")


class BuildTests(unittest.TestCase):
    def test_round_trip_unicode_spaces_embedded_image_and_injection(self):
        with tempfile.TemporaryDirectory(prefix="公司 中文 空格 ") as tmp:
            root = Path(tmp)
            fixture_assets(root)
            (root / "图片 样例.png").write_bytes(PNG)
            model = deck()
            attack = '</script><script>alert(1)</script>__TITLE__'
            model["title"] = attack
            model["slides"][0]["elements"][0]["text"] = attack
            model["slides"][0]["elements"].append({"id": "im1", "type": "image", "src": "图片 样例.png", "x": 20, "y": 20, "w": 50, "h": 50})
            source, out = root / "输入 内容.json", root / "输出 结果.html"
            source.write_text(json.dumps(model, ensure_ascii=False), encoding="utf-8")
            built = build.build(source, out, root=root)
            saved = out.read_text(encoding="utf-8")
            payload = saved.split('type="application/json">')[1].split("</script>")[0]
            reopened = json.loads(payload)
            self.assertEqual(reopened, built)
            self.assertEqual(reopened["slides"][0]["elements"][0]["text"], attack)
            self.assertEqual(reopened["slides"][0]["notes"], "讲稿\n完整保留")
            self.assertTrue(reopened["slides"][0]["elements"][1]["src"].startswith("data:image/png;base64,"))
            self.assertNotIn('<script>alert(1)', saved)
            self.assertIn("<\\/script>", saved)
            self.assertNotIn('<script src=', saved)

    def test_markdown_notes_images_and_order(self):
        model = build.markdown_deck("# 开场\n- 第一点\n<!-- notes: 讲稿第一行\n第二行 -->\n---\n## 内容页\n![图](中文 空格.png)\n结论")
        self.assertEqual([s["title"] for s in model["slides"]], ["开场", "内容页"])
        self.assertEqual(model["slides"][0]["notes"], "讲稿第一行\n第二行 ")
        self.assertEqual(model["slides"][0]["elements"][0]["text"], "• 第一点")
        self.assertEqual(model["slides"][1]["elements"][1]["src"], "中文 空格.png")

    def test_markdown_unsupported_content_fails(self):
        for content in ("| a | b |", "```python\nprint(1)\n```", "![a](a.png)\n![b](b.png)", "[链接](https://example.com)", "<iframe src=x>", "### 隐藏子标题"):
            with self.subTest(content=content), self.assertRaises(ValueError):
                build.markdown_deck("# 标题\n" + content)

    def test_remote_images_and_invalid_bytes_fail(self):
        for value in ("https://example.com/image.png", "//server/image.png", "\\\\server\\image.png", "file:///secret.png", "data:image/svg+xml;base64,PHN2Zz4=", "data:image/png;base64,YWJj"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                build.image_data(value, Path.cwd())

    def test_rejects_unknown_invalid_and_overflow_elements(self):
        mutations = ({"type": "video"}, {"x": float("nan")}, {"y": True}, {"w": 1600}, {"h": 0}, {"fontSize": 999}, {"color": "red"})
        for mutation in mutations:
            model = deck()
            model["slides"][0]["elements"][0].update(mutation)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                build.validate(model)

    def test_chart_table_constraints(self):
        for changes in ({"type": "table", "rows": [["a"], ["b", "c"]]}, {"type": "chart", "chartType": "pie", "labels": ["a"], "series": [{"name": "x", "values": [-1]}]}, {"type": "chart", "chartType": "bar", "labels": ["a"], "series": [{"name": "x", "values": [float("inf")]}]}):
            model = deck()
            model["slides"][0]["elements"][0].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                build.validate(model)

    def test_duplicate_ids_fail(self):
        model = deck()
        model["slides"].append(copy.deepcopy(model["slides"][0]))
        with self.assertRaises(ValueError):
            build.validate(model)

    def test_previews_have_cover_content_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture_assets(root)
            folder = build.previews(deck(), root / "main.html", root)
            self.assertEqual(len(list(folder.glob("*.html"))), 3)
            for path in folder.glob("*.html"):
                payload = path.read_text(encoding="utf-8").split('type="application/json">')[1].split("</script>")[0]
                model = json.loads(payload)
                self.assertEqual([s["layout"] for s in model["slides"]], ["cover", "content", "data"])
                self.assertTrue(any(e["type"] == "chart" for e in model["slides"][2]["elements"]))

    def test_brand_local_image_relative_to_brand_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture_assets(root)
            brand_dir = root / "品牌 目录"
            brand_dir.mkdir()
            (brand_dir / "logo.png").write_bytes(PNG)
            brand = brand_dir / "brand.json"
            brand.write_text(json.dumps({"logo": "logo.png", "accent": "CC0000"}), encoding="utf-8")
            source = root / "input.json"
            source.write_text(json.dumps(deck()), encoding="utf-8")
            result = build.build(source, root / "out.html", brand, root)
            self.assertEqual(result["brand"]["accent"], "CC0000")
            self.assertTrue(result["brand"]["logo"].startswith("data:image/png"))


class RuntimeTests(unittest.TestCase):
    def test_windows_prefers_py3(self):
        with patch.object(runtime, "probe", return_value="C:/中文 空格/python.exe") as probe, patch.object(runtime.shutil, "which", return_value="py.exe"):
            self.assertEqual(runtime.resolve_python(environ={}, platform="win32"), "C:/中文 空格/python.exe")
            probe.assert_called_once_with(["py", "-3"])

    def test_invalid_explicit_does_not_fallback(self):
        with patch.object(runtime, "probe", side_effect=ValueError("invalid")) as probe:
            with self.assertRaises(ValueError):
                runtime.resolve_python("C:/不存在/python.exe", environ={"CORPORATE_SLIDES_PYTHON": "other"})
            probe.assert_called_once_with(["C:/不存在/python.exe"])

    def test_environment_override_is_single_argument(self):
        with patch.object(runtime, "probe", return_value="chosen") as probe:
            self.assertEqual(runtime.resolve_python(environ={"CORPORATE_SLIDES_PYTHON": "C:/公司 Python/python.exe"}), "chosen")
            probe.assert_called_once_with(["C:/公司 Python/python.exe"])

    def test_current_interpreter_is_real_python3(self):
        self.assertTrue(Path(runtime.probe([runtime.sys.executable])).is_file())


class PreviewTests(unittest.TestCase):
    def test_loopback_content_traversal_symlink_and_listing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            public = root / "public"
            public.mkdir()
            (public / "slides.html").write_text("<!doctype html>ok", encoding="utf-8")
            (root / "secret.txt").write_text("private", encoding="utf-8")
            try:
                (public / "leak.txt").symlink_to(root / "secret.txt")
                symlink = True
            except OSError:
                symlink = False
            with preview.make_server(public, 0) as server:
                self.assertEqual(server.server_address[0], "127.0.0.1")
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    base = "http://127.0.0.1:" + str(server.server_port)
                    with urlopen(base + "/slides.html") as response:
                        self.assertEqual(response.read(), b"<!doctype html>ok")
                    paths = ("/", "/%2e%2e/secret.txt", "/..%5csecret.txt") + (("/leak.txt",) if symlink else ())
                    for path in paths:
                        with self.subTest(path=path), self.assertRaises(HTTPError) as error:
                            urlopen(base + path)
                        self.assertEqual(error.exception.code, 403)
                        error.exception.close()
                finally:
                    server.shutdown()
                    thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
