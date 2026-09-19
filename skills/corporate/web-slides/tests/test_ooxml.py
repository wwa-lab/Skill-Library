"""Portable synthetic OOXML checks; run with Python's unittest discovery."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'ooxml.py'
sys.path.insert(0, str(SCRIPT.parent))
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
PNG = __import__('base64').b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jX1sAAAAASUVORK5CYII=')

def rels(items):
    return '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join('<Relationship Id="%s" Type="%s/%s" Target="%s"/>' % (i, R, t, p) for i, t, p in items) + '</Relationships>'

def slide(text, extra=''):
    return f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:sp><p:nvSpPr><p:cNvPr id="2" name="标题"/></p:nvSpPr><p:spPr><a:xfrm><a:off x="100" y="100"/><a:ext cx="6000000" cy="800000"/></a:xfrm><a:prstGeom prst="rect"/></p:spPr><p:txBody><a:p><a:r><a:rPr sz="2400"/><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>{extra}</p:spTree></p:cSld></p:sld>'

def fixture(path):
    picture = '<p:pic><p:nvPicPr><p:cNvPr id="3" name="图"/></p:nvPicPr><p:blipFill><a:blip r:embed="img"/></p:blipFill><p:spPr><a:xfrm><a:off x="100" y="900000"/><a:ext cx="900000" cy="900000"/></a:xfrm></p:spPr></p:pic><p:grpSp><p:nvGrpSpPr/><p:grpSpPr/><p:sp><p:txBody><a:p><a:r><a:t>分组内保留文字</a:t></a:r></a:p></p:txBody></p:sp></p:grpSp>'
    files = {
        'ppt/presentation.xml': f'<p:presentation xmlns:p="{P}" xmlns:r="{R}"><p:sldIdLst><p:sldId id="257" r:id="second"/><p:sldId id="256" r:id="first"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/></p:presentation>',
        'ppt/_rels/presentation.xml.rels': rels([('first','slide','slides/slide1.xml'),('second','slide','slides/slide2.xml')]),
        'ppt/slides/slide1.xml': slide('第一页'),
        'ppt/slides/slide2.xml': slide('第二页', picture),
        'ppt/slides/_rels/slide2.xml.rels': rels([('img','image','../media/image1.png'), ('notes','notesSlide','../notesSlides/notesSlide1.xml')]),
        'ppt/notesSlides/notesSlide1.xml': f'<p:notes xmlns:p="{P}" xmlns:a="{A}"><p:cSld><p:spTree><p:sp><p:nvSpPr><p:nvPr><p:ph type="body"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>完整中文讲稿</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:notes>',
        'ppt/theme/theme1.xml': f'<a:theme xmlns:a="{A}"><a:themeElements><a:clrScheme name="Company"><a:accent1><a:srgbClr val="C8102E"/></a:accent1><a:dk1><a:srgbClr val="171717"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1></a:clrScheme><a:fontScheme name="公司"><a:majorFont><a:latin typeface="Arial"/><a:ea typeface="Microsoft YaHei"/></a:majorFont><a:minorFont><a:latin typeface="Arial"/><a:ea typeface="Microsoft YaHei"/></a:minorFont></a:fontScheme></a:themeElements></a:theme>',
        'ppt/slideMasters/slideMaster1.xml': f'<p:sldMaster xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld name="公司母版"><p:spTree>{picture}</p:spTree></p:cSld></p:sldMaster>',
        'ppt/slideMasters/_rels/slideMaster1.xml.rels': rels([('img','image','../media/image1.png')]),
        'ppt/slideLayouts/slideLayout1.xml': f'<p:sldLayout xmlns:p="{P}" type="title"><p:cSld name="封面"/></p:sldLayout>',
        'ppt/media/image1.png': PNG,
    }
    with zipfile.ZipFile(path, 'w') as archive:
        for name, data in files.items(): archive.writestr(name, data)

class OOXMLTests(unittest.TestCase):
    def test_order_notes_images_brand_and_warnings(self):
        with tempfile.TemporaryDirectory(prefix='中文 空格 ') as tmp:
            path = Path(tmp) / '公司 模板.pptx'; fixture(path)
            out = Path(tmp) / '输出 文件'
            subprocess.run([sys.executable, str(SCRIPT), str(path), '--out', str(out)], check=True, capture_output=True)
            deck = json.loads((out / 'deck.json').read_text(encoding='utf-8'))
            self.assertEqual(deck['slides'][0]['elements'][0]['text'], '第二页')
            self.assertEqual(deck['slides'][1]['elements'][0]['text'], '第一页')
            self.assertEqual(deck['slides'][0]['notes'], '完整中文讲稿')
            self.assertTrue(deck['slides'][0]['elements'][1]['src'].startswith('data:image/png;base64,'))
            self.assertTrue(any('group' in warning for warning in deck['warnings']))
            brand = json.loads((out / 'brand.json').read_text(encoding='utf-8'))
            self.assertEqual(brand['accent'], 'C8102E')
            self.assertEqual(brand['fontFace'], 'Arial')
            self.assertEqual(len(brand['masters']), 1)
            self.assertEqual(brand['masters'][0]['objects'][0]['kind'], 'pic')
            self.assertIsNotNone(brand['masters'][0]['objects'][0]['geometry'])
            self.assertEqual(len(brand['layouts']), 1)
            self.assertEqual(len(brand['logoCandidates']), 1)
            report = json.loads((out / 'conversion-report.json').read_text(encoding='utf-8'))
            self.assertEqual(report['unconvertedContent'][0]['text'], '分组内保留文字')

    def test_potx_brand_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / '公司.potx'; fixture(path)
            out = Path(tmp) / 'brand'
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), '--out', str(out), '--brand-only'], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((out / 'brand.json').is_file())
            self.assertFalse((out / 'deck.json').exists())

    def test_rejects_unsafe_archive_and_dtd(self):
        from ooxml_package import Package
        for name, content in [('../escape.xml', '<x/>'), ('ppt/presentation.xml', '<!DOCTYPE x [<!ENTITY y "boom">]><x>&y;</x>')]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / 'bad.pptx'
                with zipfile.ZipFile(path, 'w') as archive: archive.writestr(name, content)
                with self.assertRaises(ValueError):
                    with Package(path) as package: package.xml('ppt/presentation.xml')

    def test_native_tables_charts_and_unsupported_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'native.pptx'; fixture(source)
            with zipfile.ZipFile(source) as archive:
                files = {name: archive.read(name) for name in archive.namelist()}
            cell = '<a:tc><a:txBody><a:p><a:r><a:t>单元格</a:t></a:r></a:p></a:txBody></a:tc>'
            table = '<p:graphicFrame><a:graphic><a:graphicData><a:tbl><a:tr>' + cell + cell + '</a:tr></a:tbl></a:graphicData></a:graphic></p:graphicFrame>'
            chart = '<p:graphicFrame><a:graphic><a:graphicData><c:chart xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart" r:id="chart"/></a:graphicData></a:graphic></p:graphicFrame>'
            files['ppt/slides/slide1.xml'] = slide('数据', table + chart)
            files['ppt/slides/_rels/slide1.xml.rels'] = rels([('chart', 'chart', '../charts/chart1.xml')])
            files['ppt/charts/chart1.xml'] = '<c:chartSpace xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:chart><c:plotArea><c:barChart><c:ser><c:tx><c:v>销量</c:v></c:tx><c:cat><c:multiLvlStrRef><c:multiLvlStrCache><c:lvl><c:pt idx="0"><c:v>中文</c:v></c:pt></c:lvl></c:multiLvlStrCache></c:multiLvlStrRef></c:cat><c:val><c:numLit><c:pt idx="0"><c:v>42</c:v></c:pt></c:numLit></c:val></c:ser></c:barChart></c:plotArea></c:chart></c:chartSpace>'
            files['ppt/media/image1.png'] = b'<svg xmlns="http://www.w3.org/2000/svg"/>'
            with zipfile.ZipFile(source, 'w') as archive:
                for name, data in files.items(): archive.writestr(name, data)
            out = Path(tmp) / 'output'
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--out', str(out)], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            deck = json.loads((out / 'deck.json').read_text(encoding='utf-8'))
            elements = deck['slides'][1]['elements']
            self.assertEqual(elements[1]['rows'], [['单元格', '单元格']])
            self.assertEqual(elements[2]['series'][0]['values'], [42.0])
            report = json.loads((out / 'conversion-report.json').read_text(encoding='utf-8'))
            self.assertTrue(report['preservedAssets'])
            self.assertTrue(any('unsupported image' in value for value in report['warnings']))

    def test_external_and_escaping_relationships(self):
        from ooxml_package import Package
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'external.pptx'
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('ppt/_rels/presentation.xml.rels', rels([('r1', 'image', 'https://example.invalid/test.png')]))
            with Package(path) as package:
                self.assertTrue(package.relationships('ppt/presentation.xml')['r1']['external'])
            with zipfile.ZipFile(path, 'w') as archive:
                archive.writestr('ppt/_rels/presentation.xml.rels', rels([('r1', 'image', '../../escape.png')]))
            with Package(path) as package:
                with self.assertRaises(ValueError): package.relationships('ppt/presentation.xml')

    def test_importer_respects_browser_model_limits(self):
        from ooxml import Importer, DEFAULT_BRAND
        importer = Importer(None, Path('.'))
        deck = {'title': '测试', 'brand': DEFAULT_BRAND, 'slides': [{'id': 's1', 'notes': '完整讲稿', 'elements': []}]}
        self.assertIs(importer.check_limits(deck), deck)
        oversized = {**deck, 'slides': [{**deck['slides'][0], 'notes': '长' * 100001}]}
        with self.assertRaisesRegex(ValueError, 'notes'): importer.check_limits(oversized)
        oversized = {**deck, 'slides': deck['slides'] * 201}
        with self.assertRaisesRegex(ValueError, '200'): importer.check_limits(oversized)

    def test_bundled_six_slide_round_trip(self):
        from ooxml import Importer
        from ooxml_package import Package
        from build import build
        examples = SCRIPT.parents[1] / 'examples'
        source = json.loads((examples / 'six-slides.json').read_text(encoding='utf-8'))
        with tempfile.TemporaryDirectory(prefix='成品 中文 ') as tmp:
            out = Path(tmp)
            with Package(examples / 'six-slides.pptx') as package:
                importer = Importer(package, out)
                importer.analyze_brand(examples / 'six-slides.pptx')
                deck = importer.deck(examples / 'six-slides.pptx')
            self.assertEqual(len(deck['slides']), 6)
            self.assertEqual(deck['id'], 'imported-' + hashlib.sha256((examples / 'six-slides.pptx').read_bytes()).hexdigest()[:16])
            for original, imported in zip(source['slides'], deck['slides']):
                self.assertEqual(original['notes'], imported['notes'])
                texts = '\n'.join(item.get('text', '') for item in imported['elements'])
                self.assertIn(original['title'], texts)
                for element in original['elements']:
                    if element.get('text'): self.assertIn(element['text'], texts)
                    if element['type'] == 'table': self.assertTrue(any(item.get('rows') == element['rows'] for item in imported['elements']))
                    if element['type'] == 'chart': self.assertTrue(any(item.get('labels') == element['labels'] and item.get('series') == element['series'] for item in imported['elements']))
                    if element['type'] == 'image': self.assertTrue(any(item['type'] == 'image' for item in imported['elements']))
            self.assertFalse(any(w.startswith('ppt/slideMasters/') and 'inherited' in w for w in deck['warnings']))
            path = out / '导入.json'; path.write_text(json.dumps(deck, ensure_ascii=False), encoding='utf-8')
            self.assertEqual(build(path, out / '演示.html'), deck)
            with Package(examples / 'six-slides.potx') as package:
                brand = Importer(package, out).analyze_brand(examples / 'six-slides.potx')
            self.assertEqual(brand['accent'], 'C8102E')
            cover = next(item for item in brand['layouts'] if item['name'] == 'CORPORATE_COVER')
            title = next(item for item in cover['placeholders'] if item.get('type') == 'title')
            self.assertAlmostEqual(title['geometry']['x'], 100, delta=.01)
            self.assertAlmostEqual(title['geometry']['y'], 92, delta=.01)
            self.assertEqual(title['geometry']['w'], 1400)

    def test_old_ppt_clear_message(self):
        result = subprocess.run([sys.executable, str(SCRIPT), 'old.ppt', '--out', 'unused'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('.pptx', result.stderr)

if __name__ == '__main__': unittest.main()
