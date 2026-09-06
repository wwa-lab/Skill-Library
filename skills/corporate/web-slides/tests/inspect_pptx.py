#!/usr/bin/env python3
"""Inspect native PPTX objects against an authoritative model; no Office dependency.
This verifies the package, not PowerPoint rendering or interactive editing.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import posixpath
import re
import sys
from xml.etree import ElementTree as ET
from zipfile import ZipFile

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main", "a": "http://schemas.openxmlformats.org/drawingml/2006/main", "c": "http://schemas.openxmlformats.org/drawingml/2006/chart", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def texts(element):
    return "\n".join(node.text or "" for node in element.findall(".//a:t", NS))


def relationships(archive, part):
    directory, filename = posixpath.split(part)
    relpath = directory + "/_rels/" + filename + ".rels"
    if relpath not in archive.namelist():
        return {}
    result = {}
    for rel in ET.fromstring(archive.read(relpath)).findall(REL):
        if rel.get("TargetMode") == "External":
            continue
        result[rel.get("Id")] = posixpath.normpath(posixpath.join(directory, rel.get("Target", ""))).lstrip("/")
    return result


def inspect(path, model=None, crops=None):
    with ZipFile(path) as archive:
        names = archive.namelist()
        presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
        rels = relationships(archive, "ppt/presentation.xml")
        slide_paths = [rels[node.get("{" + NS["r"] + "}id")] for node in presentation.findall("p:sldIdLst/p:sldId", NS)]
        require(slide_paths, "Presentation has no slides")
        if model:
            require(len(slide_paths) == len(model["slides"]), "Slide count differs from latest model")
        summary = {"file": str(path), "slides": len(slide_paths), "notes": 0, "textShapes": 0, "pictures": 0, "shapes": 0, "tables": 0, "charts": 0, "chartWorkbooks": len([n for n in names if n.startswith("ppt/embeddings/") and n.endswith(".xlsx")]), "layouts": 0, "powerPointUI": "not verified"}
        for index, part in enumerate(slide_paths):
            slide = ET.fromstring(archive.read(part))
            slide_rels = relationships(archive, part)
            all_text = texts(slide)
            picture_parts = [slide_rels[n.get("{" + NS["r"] + "}embed")] for n in slide.findall(".//p:pic/p:blipFill/a:blip", NS)]
            notes = [target for target in slide_rels.values() if target.startswith("ppt/notesSlides/")]
            require(len(notes) == 1, "Every slide must have one notes part")
            notes_text = texts(ET.fromstring(archive.read(notes[0])))
            summary["notes"] += 1
            summary["textShapes"] += len(slide.findall(".//p:sp/p:txBody", NS))
            summary["pictures"] += len(picture_parts)
            summary["shapes"] += len(slide.findall(".//p:sp/p:spPr/a:prstGeom", NS))
            summary["tables"] += len(slide.findall(".//a:tbl", NS))
            summary["charts"] += len(slide.findall(".//c:chart", NS))
            require(any(target.startswith("ppt/slideLayouts/") for target in slide_rels.values()), "Slide has no reusable layout")
            if not model:
                continue
            expected = model["slides"][index]
            require(expected["title"] in all_text, "Slide order/title mismatch at " + str(index + 1))
            for line in expected.get("notes", "").splitlines():
                require(line in notes_text, "Notes missing at slide " + str(index + 1))
            for obj in expected["elements"]:
                kind = obj["type"]
                if kind in ("text", "shape"):
                    for line in obj.get("text", "").splitlines():
                        require(line in all_text, "Missing native text: " + line)
                if kind == "text" and obj.get("text"):
                    native = next((node for node in slide.findall(".//p:sp", NS) if node.find("p:nvSpPr/p:cNvPr", NS) is not None and node.find("p:nvSpPr/p:cNvPr", NS).get("name") == obj["id"]), None)
                    require(native is not None, "Named native text object missing")
                    props = native.findall(".//a:rPr", NS)
                    if "fontSize" in obj:
                        require(any(abs(float(p.get("sz", "0")) - obj["fontSize"] * 60) < 1 for p in props), "Native text font size differs")
                    if "color" in obj:
                        require(any(n.get("val", "").upper() == obj["color"].upper() for n in native.findall(".//a:rPr/a:solidFill/a:srgbClr", NS)), "Native text color differs")
                    if "align" in obj:
                        require(any(n.get("algn") == {"left": "l", "center": "ctr", "right": "r"}[obj["align"]] for n in native.findall(".//a:pPr", NS)), "Native text alignment differs")
                if kind == "shape":
                    shape = "rightArrow" if obj["shape"] == "arrow" else obj["shape"]
                    require(any(n.get("prst") == shape for n in slide.findall(".//a:prstGeom", NS)), "Native shape missing: " + shape)
                if kind == "table":
                    tables = slide.findall(".//a:tbl", NS)
                    require(tables, "Native table missing")
                    table_text = "\n".join(texts(table) for table in tables)
                    require(all(cell in table_text for row in obj["rows"] for cell in row), "Native table content missing")
                if kind == "chart":
                    chart_nodes = slide.findall(".//c:chart", NS)
                    require(chart_nodes, "Native chart missing")
                    chart_part = slide_rels[chart_nodes[0].get("{" + NS["r"] + "}id")]
                    chart = ET.fromstring(archive.read(chart_part))
                    values = [node.text or "" for node in chart.findall(".//c:v", NS)]
                    require(all(label in values for label in obj["labels"]), "Chart labels differ")
                    actual_series = chart.findall(".//c:ser", NS)
                    require(len(actual_series) == len(obj["series"]), "Chart series count differs")
                    for actual, expected_series in zip(actual_series, obj["series"]):
                        actual_numbers = [float(node.text) for node in actual.findall("c:val/c:numRef/c:numCache/c:pt/c:v", NS)]
                        require(actual_numbers == expected_series["values"], "Chart values differ from latest model")
                    require(any(target.endswith(".xlsx") for target in relationships(archive, chart_part).values()), "Chart workbook missing")
                if kind == "image":
                    require(picture_parts, "Image is not an independent picture")
                    expected_src = (crops or {}).get(expected["id"] + "/" + obj["id"], obj["src"] if obj.get("fit", "contain") == "contain" else None)
                    if expected_src:
                        raw = base64.b64decode(expected_src.split(",", 1)[1])
                        require(any(hashlib.sha256(archive.read(pic)).digest() == hashlib.sha256(raw).digest() for pic in picture_parts), "Picture pixels are stale or crop differs")
        layouts = [n for n in names if re.fullmatch(r"ppt/slideLayouts/slideLayout\d+\.xml", n)]
        summary["layouts"] = len(layouts)
        require(len(layouts) >= 5, "Four reusable layouts and base layout expected")
        require(any('type="title"' in archive.read(n).decode() and 'type="body"' in archive.read(n).decode() for n in layouts), "Native title/body placeholders missing")
        masters = [n for n in names if re.fullmatch(r"ppt/slideMasters/slideMaster\d+\.xml", n)]
        require(masters, "Native master missing")
        if model:
            theme = archive.read("ppt/theme/theme1.xml").decode()
            require('<a:accent1><a:srgbClr val="' + model["brand"]["accent"].upper() + '"' in theme, "Brand accent missing from theme")
            require(model["brand"]["fontFace"] in theme, "Theme font missing")
            require(any(model["brand"]["background"].upper() in archive.read(n).decode() for n in masters), "Master background missing")
        if Path(path).suffix.lower() == ".potx":
            require(b"presentationml.template.main+xml" in archive.read("[Content_Types].xml"), "POTX content type missing")
        return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("presentation", type=Path)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--crops", type=Path)
    args = parser.parse_args()
    try:
        model = json.loads(args.model.read_text(encoding="utf-8")) if args.model else None
        crops = json.loads(args.crops.read_text(encoding="utf-8")) if args.crops else None
        print(json.dumps(inspect(args.presentation, model, crops), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print("PPTX inspection failed: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
