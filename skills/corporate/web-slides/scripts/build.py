#!/usr/bin/env python3
"""Build a self-contained presentation with Python's standard library only."""
import argparse
import base64
import copy
import html
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contracts import config, check, hyperlink

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BRAND = {"name": "Corporate", "accent": "C8102E", "background": "FFFFFF", "foreground": "171717", "muted": "666666", "fontFace": "Microsoft YaHei", "titleFontFace": "Microsoft YaHei", "logo": None}
LEGACY_BRAND = DEFAULT_BRAND.copy()
CONFIG = config()
DEFAULT_BRAND = CONFIG['brand']

HEX = re.compile(r"^[0-9a-fA-F]{6}$")


def number(value, label, minimum=None, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise ValueError(label + " must be a finite number")
    if minimum is not None and value < minimum or maximum is not None and value > maximum:
        raise ValueError(label + " is out of range")


def color(value, label):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise ValueError(label + " must be six hexadecimal digits")


def string(value, label):
    if not isinstance(value, str):
        raise ValueError(label + " must be a string")


def image_data(value, base):
    """Resolve local PNG/JPEG only, never request URLs."""
    string(value, "image source")
    if len(value) > 40000000:
        raise ValueError("Image source exceeds the 40 MB encoded limit")
    if value.startswith("data:"):
        match = re.fullmatch(r"data:image/(png|jpeg);base64,([A-Za-z0-9+/=\r\n]+)", value)
        if not match:
            raise ValueError("Only PNG/JPEG base64 data URLs are supported")
        try:
            raw = base64.b64decode(match[2], validate=True)
        except ValueError as exc:
            raise ValueError("Invalid image base64") from exc
    else:
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value) and not re.match(r"^[a-zA-Z]:[\\/]", value):
            raise ValueError("Remote and file URLs are not supported; use a local file path")
        if value.startswith(("//", "\\\\")):
            raise ValueError("Network image paths are not supported")
        path = Path(value).expanduser()
        raw = (path if path.is_absolute() else base / path).read_bytes()
    mime = "png" if raw.startswith(b"\x89PNG\r\n\x1a\n") else "jpeg" if raw.startswith(b"\xff\xd8\xff") else None
    if mime is None:
        raise ValueError("Image is not a PNG or JPEG")
    if len(raw) > 29999950:
        raise ValueError("Image exceeds the approximately 30 MB limit")
    return "data:image/" + mime + ";base64," + base64.b64encode(raw).decode("ascii")


def normalize(deck, base):
    if not isinstance(deck, dict) or type(deck.get("version")) is not int or deck.get("version") != 1:
        raise ValueError("Expected presentation model version 1")
    result = copy.deepcopy(deck)
    brand = result.get("brand", {})
    if not isinstance(brand, dict):
        raise ValueError("brand must be an object")
    result["brand"] = {**(LEGACY_BRAND if brand and "schemaVersion" not in brand else DEFAULT_BRAND), **brand}
    if not brand or brand.get("schemaVersion") == 2:
        result.setdefault("modelVersion", "1.1")
        if result["brand"].get("id") == "hsbc": result.setdefault("theme", next(t for t in CONFIG["themes"] if t["id"] == "hsbc-light"))
    if result["brand"].get("logo"):
        result["brand"]["logo"] = image_data(result["brand"]["logo"], base)
    for slide in result.get("slides", []):
        if not isinstance(slide, dict):
            raise ValueError("slide must be an object")
        for element in slide.get("elements", []):
            if isinstance(element,dict) and "paragraphs" in element and "text" not in element:
                check(element["paragraphs"],CONFIG["contracts"]["paragraphs"],"paragraphs")
                element["text"]="\n".join("".join(run["text"] for run in p["runs"]) for p in element["paragraphs"])
            if isinstance(element, dict) and element.get("type") == "image":
                element["src"] = image_data(element.get("src"), base)
    validate(result)
    return result


def validate(deck):
    if not isinstance(deck, dict) or type(deck.get("version")) is not int or deck.get("version") != 1:
        raise ValueError("Expected presentation model version 1")
    if "modelVersion" in deck and deck["modelVersion"] != "1.1": raise ValueError("Unsupported modelVersion")
    if "theme" in deck:
        check(deck["theme"], CONFIG["contracts"]["theme"], "theme")
        if deck.get("brand", {}).get("id") not in (None, deck["theme"]["brand"]): raise ValueError("Theme brand mismatch")
    string(deck.get("id"), "deck.id")
    string(deck.get("title"), "deck.title")
    if not deck["id"] or len(deck["title"]) > 300:
        raise ValueError("Deck ID is empty or title exceeds 300 characters")
    brand = deck.get("brand")
    if not isinstance(brand, dict):
        raise ValueError("brand must be an object")
    if "schemaVersion" in brand: check(brand, CONFIG["contracts"]["brand"], "brand")
    for key in ("accent", "background", "foreground", "muted"):
        color(brand.get(key), "brand." + key)
    for key in ("name", "fontFace", "titleFontFace"):
        string(brand.get(key), "brand." + key)
        if len(brand[key]) > 200:
            raise ValueError("Brand text exceeds 200 characters")
    if brand.get("logo") is not None:
        image_data(brand["logo"], Path.cwd())
    slides = deck.get("slides")
    if not isinstance(slides, list) or not 1 <= len(slides) <= 200:
        raise ValueError("Expected between 1 and 200 slides")
    seen = set()
    slide_ids = {s.get("id") for s in slides if isinstance(s,dict)}
    for slide in slides:
        validate_slide(slide, seen)
        if "section" in slide and (not isinstance(slide["section"],str) or len(slide["section"])>100): raise ValueError("Invalid section")
        for el in slide["elements"]:
            for p in el.get("paragraphs",[]):
                for run in p["runs"]:
                    if "hyperlink" in run: hyperlink(run["hyperlink"],slide_ids)
            if "hyperlink" in el: hyperlink(el["hyperlink"],slide_ids)
            if "altText" in el and (not isinstance(el["altText"],str) or len(el["altText"])>2000): raise ValueError("Invalid alt text")
    if not isinstance(deck.get("warnings", []), list) or any(not isinstance(w, str) for w in deck.get("warnings", [])):
        raise ValueError("warnings must be an array of strings")


def unique_id(item, seen):
    identity = item.get("id")
    if not isinstance(identity, str) or not identity or identity in seen:
        raise ValueError("IDs must be nonempty and globally unique: " + str(identity))
    seen.add(identity)


def validate_style(item):
    for key in ("color", "fill", "accent"):
        if key in item:
            color(item[key], key)
    if "fontSize" in item:
        number(item["fontSize"], "fontSize", 12, 160)
    if "align" in item and item["align"] not in ("left", "center", "right"):
        raise ValueError("Unsupported alignment")
    for k in ("role",):
        if k in item and item[k] not in CONFIG["themes"][0]["typography"]: raise ValueError("Unknown semantic role")
    if "layoutOverride" in item and not isinstance(item["layoutOverride"],bool): raise ValueError("layoutOverride must be boolean")
    if "bold" in item and not isinstance(item["bold"], bool):
        raise ValueError("bold must be boolean")


def validate_slide(slide, seen):
    if not isinstance(slide, dict):
        raise ValueError("slide must be an object")
    unique_id(slide, seen)
    string(slide.get("title"), "slide.title")
    if len(slide["title"]) > 52:
        raise ValueError("Slide title exceeds 52 characters; shorten or split it")
    string(slide.get("notes"), "slide.notes")
    if len(slide["notes"]) > 100000:
        raise ValueError("Slide notes exceed 100000 characters")
    if slide.get("layout") not in [x["id"] for x in CONFIG["layouts"]]:
        raise ValueError("Unsupported slide layout")
    if "background" in slide:
        color(slide["background"], "slide.background")
    if "titleBox" in slide:
        box=slide["titleBox"]
        check(box,CONFIG["contracts"]["layout"]["properties"]["title"],"titleBox")
        if box["x"]+box["w"]>1600.1 or box["y"]+box["h"]>900.1: raise ValueError("Title outside canvas")
    if "titleStyle" in slide:
        if not isinstance(slide["titleStyle"], dict):
            raise ValueError("titleStyle must be an object")
        validate_style(slide["titleStyle"])
    if not isinstance(slide.get("elements"), list):
        raise ValueError("slide.elements must be an array")
    if len(slide["elements"]) > 100:
        raise ValueError("At most 100 objects per slide")
    for item in slide["elements"]:
        validate_element(item, seen)


def validate_element(item, seen):
    if not isinstance(item, dict):
        raise ValueError("element must be an object")
    unique_id(item, seen)
    for key, limit in (("x", 1600), ("w", 1600), ("y", 900), ("h", 900)):
        number(item.get(key), key, 0, limit)
    if item["x"] + item["w"] > 1600 or item["y"] + item["h"] > 900 or item["w"] <= 0 or item["h"] <= 0:
        raise ValueError("Element must fit within the 1600 × 900 canvas with positive size")
    validate_style(item)
    if item["id"] == "__title__":
        raise ValueError("Reserved element ID __title__")
    if "text" in item and (not isinstance(item["text"], str) or len(item["text"]) > 20000):
        raise ValueError("Element text exceeds 20000 characters or is invalid")
    kind = item.get("type")
    if "paragraphs" in item:
        if kind!="text": raise ValueError("Rich text only supported on text objects")
        check(item["paragraphs"],CONFIG["contracts"]["paragraphs"],"paragraphs")
        fallback="\n".join("".join(run["text"] for run in p["runs"]) for p in item["paragraphs"])
        if item.get("text")!=fallback: raise ValueError("Rich text fallback must match paragraphs")
    if kind == "text":
        string(item.get("text"), "text")
    elif kind == "image":
        if not isinstance(item.get("src"), str) or not item["src"].startswith("data:"):
            raise ValueError("Validated images must be embedded")
        image_data(item["src"], Path.cwd())
        string(item.get("alt", ""), "alt")
        if item.get("fit", "contain") not in ("contain", "cover"):
            raise ValueError("Unsupported image fit")
        for key in ("positionX", "positionY"):
            number(item.get(key, 0.5), key, 0, 1)
    elif kind == "shape":
        if item.get("shape") not in ("rect", "roundRect", "ellipse", "arrow", "line"):
            raise ValueError("Unsupported shape")
        string(item.get("text", ""), "shape.text")
    elif kind == "table":
        rows = item.get("rows")
        if not isinstance(rows, list) or not 1 <= len(rows) <= 12 or not isinstance(rows[0], list) or not 1 <= len(rows[0]) <= 8:
            raise ValueError("Tables support 1–12 rows and 1–8 columns")
        if any(not isinstance(row, list) or len(row) != len(rows[0]) or any(not isinstance(cell, str) or len(cell) > 2000 for cell in row) for row in rows):
            raise ValueError("Table rows must be rectangular arrays of strings")
    elif kind == "chart":
        validate_chart(item)
    else:
        raise ValueError("Unsupported element type: " + str(kind))


def validate_chart(item):
    kind, labels, series = item.get("chartType"), item.get("labels"), item.get("series")
    if kind not in ("bar", "line", "pie") or not isinstance(labels, list) or not 1 <= len(labels) <= 12 or any(not isinstance(label, str) or len(label) > 60 for label in labels):
        raise ValueError("Charts require bar/line/pie and 1–12 text labels")
    if not isinstance(series, list) or not 1 <= len(series) <= 4 or kind == "pie" and len(series) != 1:
        raise ValueError("Charts support 1–4 series; pie requires one")
    for group in series:
        if not isinstance(group, dict):
            raise ValueError("Chart series must be objects")
        string(group.get("name"), "series.name")
        values = group.get("values")
        if not isinstance(values, list) or len(values) != len(labels):
            raise ValueError("Chart values must match labels")
        for value in values:
            number(value, "chart value", None if kind == "line" else 0)
    if kind == "pie" and not any(value > 0 for value in series[0]["values"]):
        raise ValueError("Pie chart must have a positive total")
    if "colors" in item:
        if not isinstance(item["colors"], list) or not item["colors"]:
            raise ValueError("Chart colors must be a nonempty array")
        for value in item["colors"]:
            color(value, "chart color")


def markdown_deck(source):
    """Deliberately small Markdown subset; reject constructs we cannot preserve."""
    slides = []
    for index, block in enumerate(re.split(r"(?m)^\s*---\s*$", source)):
        if not block.strip():
            continue
        notes = "\n".join(re.findall(r"<!--\s*notes:\s*(.*?)-->", block, re.S))
        block = re.sub(r"<!--\s*notes:\s*.*?-->", "", block, flags=re.S)
        if re.search(r"```|~~~|^\s*\||<[^>]+>|(?<!!)\[[^\]]*\]\([^)]*\)", block, re.M):
            raise ValueError("Markdown tables, code fences, HTML and links are unsupported; use the JSON model")
        lines = block.strip().splitlines()
        if not lines or not re.match(r"^#{1,2}\s+", lines[0]):
            raise ValueError("Every Markdown slide must begin with # or ## heading")
        title = re.sub(r"^#{1,2}\s+", "", lines[0]).strip()
        images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", "\n".join(lines[1:]))
        text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", "\n".join(lines[1:])).strip()
        if re.search(r"!\[|^#{1,6}\s", text, re.M):
            raise ValueError("Malformed image or additional heading; split pages with ---")
        text = re.sub(r"(?m)^\s*[-*+]\s+", "• ", text)
        if len(images) > 1:
            raise ValueError("Markdown supports one image per page; use JSON for more")
        elements = []
        prefix = "s" + str(index + 1)
        if text:
            elements.append({"id": prefix + "-text", "type": "text", "x": 100, "y": 255, "w": 670 if images else 1400, "h": 530, "fontSize": 34, "text": text})
        if images:
            alt, path = images[0]
            elements.append({"id": prefix + "-image", "type": "image", "x": 830 if text else 200, "y": 255, "w": 670 if text else 1200, "h": 530, "src": path, "alt": alt, "fit": "contain"})
        slides.append({"id": prefix, "title": title, "notes": notes, "layout": "cover" if not slides else "content", "elements": elements})
    return {"version": 1, "id": "deck-" + uuid.uuid4().hex, "title": slides[0]["title"] if slides else "", "brand": DEFAULT_BRAND.copy(), "slides": slides, "warnings": []}


def safe_script(value):
    return re.sub(r"</script", r"<\\/script", value, flags=re.I)


def render_html(deck, root=ROOT):
    validate(deck)
    assets = root / "assets"
    shell = (assets / "shell.html").read_text(encoding="utf-8")
    vendor_files = sorted((assets / "vendor").glob("*.js"))
    if not vendor_files:
        raise ValueError("Bundled PPTX vendor library missing")
    manifest_path = assets / "vendor" / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected = manifest.get("sha256")
        bundle = assets / "vendor" / manifest.get("file", "")
        if bundle not in vendor_files or hashlib.sha256(bundle.read_bytes()).hexdigest() != expected:
            raise ValueError("Bundled PPTX library does not match its locked manifest")
    vendor = "\n;\n".join(path.read_text(encoding="utf-8") for path in vendor_files)
    app = "\n;\n".join((assets / name).read_text(encoding="utf-8") for name in ("theme.js", "model.js", "qa.js", "editor.js", "render.js", "export.js", "app.js") if (assets / name).exists())
    license_files = sorted(path for path in (assets / "vendor").iterdir() if path.is_file() and ("license" in path.name.lower() or "notice" in path.name.lower()))
    upstream = root / "references" / "upstream-LICENSE.txt"
    if upstream.exists():
        license_files = [*license_files, upstream]
    licenses = "\n\n".join(path.name + "\n" + path.read_text(encoding="utf-8") for path in license_files)
    tokens = {"__DECK_JSON__": json.dumps(deck, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"), "__CSS__": (assets / "style.css").read_text(encoding="utf-8"), "__VENDOR__": safe_script(vendor), "__APP_JS__": safe_script(app), "__TITLE__": html.escape(deck["title"]), "__LICENSES__": html.escape(licenses)}
    if "__CONFIG__" in shell: tokens["__CONFIG__"] = json.dumps(CONFIG, ensure_ascii=False).replace("<", "\\u003c")
    if "__CSP__" in shell:
        hashes = ["\'sha256-" + base64.b64encode(hashlib.sha256(tokens[k].encode()).digest()).decode() + "\'" for k in ("__VENDOR__", "__APP_JS__")]
        css_hash = "\'sha256-" + base64.b64encode(hashlib.sha256(tokens["__CSS__"].encode()).digest()).decode() + "\'"
        tokens["__CSP__"] = "default-src 'none'; script-src " + " ".join(hashes) + "; style-src " + css_hash + "; img-src data: blob:; font-src 'none'; connect-src 'none'; media-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-src 'none'; worker-src 'none'"
    # Replace in one pass so content containing a placeholder is never interpreted.
    for token in tokens:
        if token not in shell:
            raise ValueError("HTML shell is missing placeholder " + token)
    return re.sub("|".join(map(re.escape, tokens)), lambda m: tokens[m[0]], shell)


def build(input_path, output_path, brand_path=None, root=ROOT):
    input_path, output_path = Path(input_path), Path(output_path)
    source = input_path.read_text(encoding="utf-8-sig")
    if input_path.suffix.lower() == ".json":
        deck = json.loads(source)
    elif input_path.suffix.lower() in (".md", ".markdown"):
        deck = markdown_deck(source)
    else:
        raise ValueError("Input must be .json or .md; extract PPTX with the import helper first")
    if brand_path:
        brand_path = Path(brand_path)
        brand = json.loads(brand_path.read_text(encoding="utf-8-sig"))
        if not isinstance(brand, dict):
            raise ValueError("Brand file must be a JSON object")
        if brand.get("logo"):
            brand = {**brand, "logo": image_data(brand["logo"], brand_path.parent)}
        deck = {**deck, "brand": {**deck.get("brand", {}), **brand}}
    deck = normalize(deck, input_path.parent)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(deck, root), encoding="utf-8")
    return deck


def previews(deck, output_path, root=ROOT):
    """Three conservative directions, each with cover/content/data preview pages."""
    selected = []
    for layout in ("cover", "content", "data"):
        match = next((s for s in deck["slides"] if s["layout"] == layout), None)
        if match is None:
            match = {"id": "preview-" + layout, "title": {"cover": "公司分享 · 标准封面", "content": "核心观点与行动", "data": "用数据说明结果"}[layout], "layout": layout, "notes": "风格预览示例。", "elements": [{"id": "preview-element-" + layout, "type": "text", "x": 100, "y": 300, "w": 1400, "h": 400, "text": "简洁表达核心观点\n让证据与行动清晰可见", "fontSize": 44}]}
            if layout == "data":
                match["elements"] = [{"id": "preview-chart", "type": "chart", "chartType": "bar", "x": 150, "y": 260, "w": 1300, "h": 500, "labels": ["第一阶段", "第二阶段", "第三阶段"], "series": [{"name": "达成率", "values": [45, 68, 92]}]}]
        selected.append(copy.deepcopy(match))
    folder = Path(output_path).parent / "previews"
    folder.mkdir(parents=True, exist_ok=True)
    for name, overrides in (("default", {}), ("black", {"background": "171717", "foreground": "FFFFFF", "muted": "BBBBBB"}), ("red-cover", {})):
        result = {**copy.deepcopy(deck), "id": deck["id"] + "-preview-" + name, "slides": copy.deepcopy(selected), "brand": {**deck["brand"], **overrides}}
        for slide in result["slides"]:
            if name == "black":
                for element in slide["elements"]:
                    for key in ("color",):
                        if element.get(key, "").upper() == deck["brand"]["foreground"].upper():
                            element[key] = result["brand"]["foreground"]
                        elif element.get(key, "").upper() == deck["brand"]["muted"].upper():
                            element[key] = result["brand"]["muted"]
                if slide.get("titleStyle", {}).get("color", "").upper() == deck["brand"]["foreground"].upper():
                    slide["titleStyle"] = {**slide["titleStyle"], "color": result["brand"]["foreground"]}
        if name == "red-cover":
            result["slides"][0] = {**result["slides"][0], "background": result["brand"]["accent"], "titleStyle": {"color": "FFFFFF"}, "elements": [{**element, "color": "FFFFFF"} if element["type"] == "text" else element for element in result["slides"][0]["elements"]]}
        (folder / (name + ".html")).write_text(render_html(result, root), encoding="utf-8")
    return folder


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--brand", type=Path)
    parser.add_argument("--preview-styles", action="store_true")
    args = parser.parse_args(argv)
    try:
        deck = build(args.input, args.output, args.brand)
        if args.preview_styles:
            print("Style previews:", previews(deck, args.output))
        print("Saved:", args.output.resolve())
        for warning in deck.get("warnings", []):
            print("Warning:", warning)
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print("Build failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
