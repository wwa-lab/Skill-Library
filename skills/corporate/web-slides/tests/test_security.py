"""Gate A malicious data, bounded OOXML and reproducible offline source checks."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import build
import contracts
import ooxml_package as op
import security_audit as audit
import vendor_offline

class SecurityTests(unittest.TestCase):
 def test_theme_closed_schema_parity(self):
  c=contracts.config();good=c['themes'][0]
  for t in c['themes']:contracts.check(t,c['contracts']['theme'])
  for field,value in [('onclick','alert(1)'),('css','body{}'),('url','https://example.com'),('script','alert(1)')]:
   t={**good,field:value}
   with self.assertRaises(ValueError):contracts.check(t,c['contracts']['theme'])
  for action in [lambda t:t['colors'].update(text='url(x)'),lambda t:t['typography']['body'].update(size=float('inf')),lambda t:t['fonts'].update(body='x; @import'),lambda t:t.update(chartPalette=[]),lambda t:t.update(schemaVersion=True)]:
   t=copy.deepcopy(good);action(t)
   with self.assertRaises(ValueError):contracts.check(t,c['contracts']['theme'])
 def test_hyperlink_validation(self):
  for link in ['javascript:alert(1)','data:text/html,x','file:///x','http://a.test','#missing','https://a.test\n']:
   with self.assertRaises(ValueError):contracts.hyperlink(link,{'s1'})
  for link in ['https://example.com/a?q=1','mailto:u@example.com','#s1']:contracts.hyperlink(link,{'s1'})
 def test_v1_unchanged_and_default_hsbc(self):
  source=json.loads((ROOT/'examples/six-slides.json').read_text());d=build.normalize(source,ROOT/'examples')
  self.assertEqual(d['brand'],source['brand']);self.assertEqual(d['slides'][0]['id'],source['slides'][0]['id'])
  del source['brand'];d=build.normalize(source,ROOT/'examples');self.assertEqual(d['theme']['id'],'hsbc-light');self.assertIsNone(d['brand']['logo']);self.assertEqual(d['brand']['fontFace'],'Arial')
 def test_html_hashes_literal_malicious_title_and_vendor(self):
  d=build.normalize(json.loads((ROOT/'examples/six-slides.json').read_text()),ROOT/'examples')
  d['slides'][0]['title']='<img src=x onerror=alert(1)>';d['slides'][0]['notes']='</script><script>alert(1)</script>'
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'安全 中文.html';p.write_text(build.render_html(d));self.assertEqual(audit.audit_html(p),[])
   p.write_text(p.read_text().replace('/* Corporate Web Slides — authoritative','/* tampered Corporate Web Slides — authoritative'))
   self.assertTrue(any('hash mismatch' in x for x in audit.audit_html(p)))
 def test_audit_rejects_unsafe_runtime(self):
  for text in ['eval("x")','new Function("x")','Function("x")','fetch("x")','new XMLHttpRequest()','new WebSocket("x")','new EventSource("x")','navigator.sendBeacon("x")','import("x")','document.write("x")','x.innerHTML = value','document.createElement("script")','javascript:alert(1)','https://unexpected.invalid']:
   self.assertTrue(audit.scan_code(text,'fixture',set()),text)
  for attr in ['onclick="x()"','srcdoc="x"']:
   p=audit.HTMLAudit(set());p.feed('<div '+attr+'>');self.assertTrue(p.issues)
 def test_vendor_reproduces_and_source_audit(self):
  raw=(ROOT/'references/vendor/pptxgenjs-4.0.1.upstream.txt').read_bytes()
  self.assertEqual(vendor_offline.derive(raw),(ROOT/'assets/vendor/pptxgenjs-4.0.1.bundle.js').read_bytes());self.assertEqual(audit.audit_source(),[])
 def test_zip_limits_traversal_ratio_xml_and_source(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'模板.pptx'
   def make(items):
    with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED) as z:
     for n,data in items:z.writestr(n,data)
   for name in ['../x','/x','C:/x','a\\x']:
    make([(name,b'x')])
    with self.assertRaises(ValueError):op.Package(p)
   make([('large.xml',b'x'*100000)])
   with self.assertRaises(ValueError):op.Package(p)
   for limit,value,items in [('MAX_ENTRIES',1,[('a',b'x'),('b',b'y')]),('MAX_TOTAL',1,[('a',b'xy')]),('MAX_SOURCE',1,[('a',b'x')]),('MAX_XML',1,[('a.xml',b'<a/>')])]:
    make(items)
    with patch.object(op,limit,value),self.assertRaises(ValueError):op.Package(p)
   p.write_bytes(b'not a zip')
   with self.assertRaises(zipfile.BadZipFile):op.Package(p)
 def test_external_relationship_never_read(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'x.pptx'
   with zipfile.ZipFile(p,'w') as z:
    z.writestr('ppt/_rels/presentation.xml.rels','<Relationships><Relationship Id="r1" TargetMode="External" Target="file:///private/x" Type="x"/><Relationship Id="r2" Target="//host/share" Type="x"/></Relationships>')
   with op.Package(p) as z:
    rel=z.relationships('ppt/presentation.xml');self.assertTrue(all(r['external'] for r in rel.values()))
if __name__=='__main__':unittest.main()
