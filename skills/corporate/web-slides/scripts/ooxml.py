#!/usr/bin/env python3
"""Import .pptx content or analyze .pptx/.potx brands without external services."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile
from ooxml_package import Package, NS, find, all_nodes, tag, text_content
from ooxml_shapes import parse_element, geometry

DEFAULT_BRAND = {'name': 'Corporate', 'accent': 'C8102E', 'background': 'FFFFFF', 'foreground': '171717', 'muted': '666666', 'fontFace': 'Microsoft YaHei', 'titleFontFace': 'Microsoft YaHei', 'logo': None}

class Importer:
    def __init__(self, package, out):
        self.package = package
        self.out = out
        self.warnings = []
        self.assets = []
        self.unconverted = []
        self.brand = dict(DEFAULT_BRAND)
        self.sx = 1600 / 12192000
        self.sy = 900 / 6858000

    def warn(self, part, message):
        self.warnings.append(part + ': ' + message)

    def omit(self, part, node, message):
        self.unconverted.append({'part': part, 'objectType': tag(node), 'text': text_content(node), 'reason': message})
        self.warn(part, message + '; available text preserved in conversion-report.json unconvertedContent')

    def check_limits(self, deck):
        if len(deck['slides']) > 200: raise ValueError('Model supports at most 200 slides; split the presentation')
        if len(deck['title']) > 300 or any(len(deck['brand'][key]) > 200 for key in ('name', 'fontFace', 'titleFontFace')):
            raise ValueError('Presentation title / brand fields exceed model length limits')
        for page in deck['slides']:
            if len(page['notes']) > 100000: raise ValueError(page['id'] + ': notes exceed 100000 characters; split this page')
            if len(page['elements']) > 100: raise ValueError(page['id'] + ': more than 100 editable objects; split this page')
            for element in page['elements']:
                if len(element.get('text', '')) > 20000: raise ValueError(element['id'] + ': text exceeds 20000 characters; split this object')
                if len(element.get('src', '')) > 40000000: raise ValueError(element['id'] + ': embedded image exceeds model size limit; resize source image')
                if any(len(cell) > 2000 for row in element.get('rows', []) for cell in row): raise ValueError(element['id'] + ': table cell exceeds 2000 characters')
                if any(len(label) > 60 for label in element.get('labels', [])): raise ValueError(element['id'] + ': chart label exceeds 60 characters')
        return deck

    def image(self, part, relid):
        rel = self.package.relationships(part).get(relid)
        if not rel:
            self.warn(part, 'image relationship missing: ' + str(relid)); return None
        if rel['external']:
            self.warn(part, 'external image omitted; no network access: ' + rel['target']); return None
        image = self.package.image(rel['target'])
        if image:
            return image
        data = self.package.data(rel['target'])
        suffix = Path(rel['target']).suffix.lower()
        suffix = suffix if suffix in ('.svg', '.emf', '.wmf', '.gif', '.tif', '.tiff', '.bmp', '.webp') else '.bin'
        filename = 'source-asset-' + str(len(self.assets) + 1) + suffix
        (self.out / 'assets').mkdir(exist_ok=True)
        (self.out / 'assets' / filename).write_bytes(data)
        self.assets.append({'source': rel['target'], 'file': 'assets/' + filename})
        self.warn(part, 'unsupported image preserved as assets/' + filename + '; convert manually to PNG/JPEG')
        return None

    def inventory_object(self, part, item):
        identity = find(item, './/p:cNvPr')
        placeholder = find(item, './/p:ph')
        transform = find(item, 'p:spPr/a:xfrm')
        if transform is None: transform = find(item, 'p:xfrm')
        preset = find(item, 'p:spPr/a:prstGeom')
        descriptor = {'kind': tag(item), 'name': identity.get('name', '') if identity is not None else '',
                      'text': text_content(item), 'geometry': geometry(self, part, item) if transform is not None else None}
        if placeholder is not None: descriptor['placeholder'] = dict(placeholder.attrib)
        if preset is not None: descriptor['shape'] = preset.get('prst')
        if tag(item) == 'grpSp': descriptor['childCount'] = max(0, len(list(item)) - 2)
        return descriptor

    def analyze_brand(self, source):
        presentation = self.package.xml('ppt/presentation.xml')
        size = find(presentation, 'p:sldSz')
        if size is not None:
            width, height = int(size.get('cx', 0)), int(size.get('cy', 0))
            if width <= 0 or height <= 0: raise ValueError('Invalid presentation dimensions')
            self.sx, self.sy = 1600 / width, 900 / height
        themes = sorted(n for n in self.package.names if n.startswith('ppt/theme/') and n.endswith('.xml'))
        colors, fonts = {}, []
        if themes:
            root = self.package.xml(themes[0])
            scheme = find(root, './/a:clrScheme')
            if scheme is not None:
                for item in scheme:
                    child = next(iter(item), None)
                    value = child.get('val') if child is not None and tag(child) == 'srgbClr' else child.get('lastClr') if child is not None else None
                    if value: colors[tag(item)] = value.upper()
            for item in all_nodes(root, './/a:fontScheme//*[@typeface]'):
                face = item.get('typeface')
                if face and face not in fonts: fonts.append(face)
            for group, field in [('majorFont', 'titleFontFace'), ('minorFont', 'fontFace')]:
                node = find(root, './/a:' + group)
                ea, latin = find(node, 'a:ea'), find(node, 'a:latin')
                face = ea.get('typeface') if ea is not None else None
                face = face or (latin.get('typeface') if latin is not None else None)
                if face: self.brand[field] = face
            if len(themes) > 1: self.warn('brand', 'multiple themes found; first theme used for normalized brand: ' + themes[0])
        for key, color in [('accent', 'accent1'), ('background', 'lt1'), ('foreground', 'dk1')]:
            if color in colors: self.brand[key] = colors[color]
        inventories, logos = {}, []
        for folder, key in [('slideMasters', 'masters'), ('slideLayouts', 'layouts')]:
            inventory = []
            for part in sorted(n for n in self.package.names if n.startswith('ppt/' + folder + '/') and n.endswith('.xml') and '/_rels/' not in n):
                root = self.package.xml(part); common = find(root, 'p:cSld')
                tree = find(common, 'p:spTree')
                objects = [self.inventory_object(part, item) for item in tree if tag(item) not in ('nvGrpSpPr', 'grpSpPr')] if tree is not None else []
                placeholders = [{**item['placeholder'], 'objectName': item['name'], 'geometry': item['geometry']} for item in objects if 'placeholder' in item]
                inventory.append({'part': part, 'name': common.get('name', '') if common is not None else '', 'type': root.get('type', ''), 'placeholders': placeholders, 'objects': objects})
                for pic in all_nodes(root, './/p:pic'):
                    blip = find(pic, './/a:blip')
                    if blip is not None:
                        image = self.image(part, blip.get('{' + NS['r'] + '}embed'))
                        if image and not any(x['src'] == image for x in logos): logos.append({'source': part, 'src': image, 'reviewRequired': True})
            inventories[key] = inventory
        self.brand.update({'name': source.stem, 'source': {'file': source.name, 'themes': themes}, 'themeColors': colors, 'fonts': fonts, **inventories, 'logoCandidates': logos})
        self.warn('brand', 'masters/layouts analyzed as inventory, not cloned; logo candidates require review before selecting brand.logo')
        return self.brand

    def notes(self, part):
        rels = self.package.relationships(part)
        candidates = [r for r in rels.values() if r['type'] == 'notesSlide' and not r['external']]
        if not candidates: return ''
        root = self.package.xml(candidates[0]['target']); paragraphs = []
        for shape in all_nodes(root, './/p:sp'):
            placeholder = find(shape, './/p:ph')
            if placeholder is not None and placeholder.get('type') in ('sldNum', 'dt', 'hdr', 'ftr', 'sldImg'): continue
            value = text_content(find(shape, 'p:txBody'))
            if value: paragraphs.append(value)
        if all_nodes(root, './/p:pic') or all_nodes(root, './/p:graphicFrame'):
            self.warn(part, 'notes images/graphics omitted; notes text preserved')
        return '\n'.join(paragraphs)

    def inherited_warnings(self, part, visited=None):
        visited = set() if visited is None else visited
        if part in visited: return
        visited.add(part)
        expected = 'slideLayout' if part.startswith('ppt/slides/') else 'slideMaster' if part.startswith('ppt/slideLayouts/') else None
        for rel in self.package.relationships(part).values():
            if rel['type'] != expected or rel['external'] or rel['target'] in visited: continue
            target = rel['target']; root = self.package.xml(target)
            tree = find(root, 'p:cSld/p:spTree')
            for index, item in enumerate(tree if tree is not None else []):
                if tag(item) not in ('nvGrpSpPr', 'grpSpPr'):
                    self.omit(part, item, 'inherited ' + tag(item) + ' from ' + target + ' object ' + str(index) + ' not rendered; source layout/master requires review')
            self.inherited_warnings(target, visited)

    def deck(self, source):
        part = 'ppt/presentation.xml'; root = self.package.xml(part)
        if root.tag != '{' + NS['p'] + '}presentation':
            raise ValueError('Unsupported OOXML namespace; save as standard .pptx in PowerPoint first')
        self.warn(part, 'typography normalized to brand font; paragraph spacing, text margins, line styles and fine formatting may differ')
        size = find(root, 'p:sldSz')
        if size is not None:
            width, height = int(size.get('cx', 0)), int(size.get('cy', 0))
            if width <= 0 or height <= 0: raise ValueError('Invalid presentation dimensions')
            self.sx, self.sy = 1600 / width, 900 / height
            if abs(width / height - 16 / 9) > .001: self.warn(part, 'source aspect ratio differs from 16:9; geometry normalized independently to 1600×900')
        rels = self.package.relationships(part); slides = []
        ids = all_nodes(root, 'p:sldIdLst/p:sldId')
        if not ids: raise ValueError('No slides found; use --brand-only for an empty company template')
        if len(ids) > 200: raise ValueError('Presentation exceeds 200-slide model limit; split it before importing')
        for index, item in enumerate(ids):
            rel = rels.get(item.get('{' + NS['r'] + '}id'))
            if not rel or rel['external']: raise ValueError('Invalid slide relationship')
            slidepart = rel['target']; slide = self.package.xml(slidepart)
            if slide.get('show') in ('0', 'false'): self.warn(slidepart, 'hidden source slide imported as visible page')
            elements = []; tree = find(slide, 'p:cSld/p:spTree')
            for ordinal, shape in enumerate(tree if tree is not None else []):
                element = parse_element(self, slidepart, shape, 's%d-e%d' % (index + 1, ordinal + 1))
                if element: elements.append(element)
            self.inherited_warnings(slidepart)
            for kind in ('timing', 'transition'):
                if find(slide, 'p:' + kind) is not None: self.warn(slidepart, kind + ' converted to static final state; author explicit step slides if required')
            page = {'id': 's' + str(index + 1), 'title': '', 'notes': self.notes(slidepart), 'layout': 'imported', 'elements': elements, 'source': slidepart}
            bg = find(slide, 'p:cSld/p:bg/p:bgPr/a:solidFill/a:srgbClr')
            if bg is not None: page['background'] = bg.get('val', 'FFFFFF')
            elif find(slide, 'p:cSld/p:bg') is not None: self.warn(slidepart, 'non-RGB or inherited background replaced by brand background')
            slides.append(page)
        digest = hashlib.sha256()
        with source.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''): digest.update(chunk)
        return self.check_limits({'version': 1, 'id': 'imported-' + digest.hexdigest()[:16], 'title': source.stem, 'brand': self.brand, 'slides': slides, 'warnings': self.warnings, 'source': {'file': source.name}})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--brand-only', action='store_true')
    args = parser.parse_args(argv)
    if args.input.suffix.lower() == '.ppt': parser.error('Legacy .ppt is unsupported; save as .pptx in PowerPoint first.')
    if args.input.suffix.lower() not in ('.pptx', '.potx'): parser.error('Expected .pptx or .potx')
    try:
        args.out.mkdir(parents=True, exist_ok=True)
        with Package(args.input) as package:
            importer = Importer(package, args.out)
            brand = importer.analyze_brand(args.input)
            deck = None if args.brand_only else importer.deck(args.input)
            outputs = {'brand.json': brand, 'conversion-report.json': {'source': args.input.name, 'warnings': importer.warnings, 'preservedAssets': importer.assets, 'unconvertedContent': importer.unconverted, 'completeFidelity': False}}
            if deck is not None: outputs['deck.json'] = deck
            for name, value in outputs.items(): (args.out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
            print('Wrote ' + ', '.join(outputs) + '; warnings=' + str(len(importer.warnings)))
        return 0
    except (ValueError, OSError, zipfile.BadZipFile, KeyError, OverflowError) as exc:
        print('Import failed: ' + str(exc), file=sys.stderr)
        return 1

if __name__ == '__main__': sys.exit(main())
