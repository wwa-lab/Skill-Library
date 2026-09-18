#!/usr/bin/env python3
"""Static release gate for maintained runtime sources and built HTML (stdlib only).
This is a bounded source audit, not a general JavaScript theorem prover.
"""
import argparse
import ast
import base64
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from vendor_offline import derive
ROOT=Path(__file__).resolve().parents[1]
RULES={
 'dynamic-code':r'\b(?:eval|Function)\s*\(|\bnew\s+Function\b',
 'network-api':r'\b(?:fetch\s*\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon\s*\()',
 'dynamic-import':r'\bimport\s*\(',
 'unsafe-dom':r'\b(?:document\.write\s*\(|innerHTML\s*=|outerHTML\s*=|insertAdjacentHTML\s*\()',
 'script-element':r'createElement\s*\(\s*[\"\'](?:script|iframe)[\"\']',
 'executable-url':r'javascript\s*:',
}
URL=re.compile(r'https?://[^\s\"\'<>`\\)]+')

def scan_code(text,label,allowed):
 issues=[]
 for rule,pattern in RULES.items():
  for m in re.finditer(pattern,text,0 if rule=="dynamic-code" else re.I):issues.append(f'{label}: {rule} at offset {m.start()}')
 for m in URL.finditer(text):
  if m[0] not in allowed:issues.append(f'{label}: unexpected URL {m[0]}')
 return issues

class HTMLAudit(HTMLParser):
 def __init__(self,allowed):
  super().__init__(convert_charrefs=False);self.allowed=allowed;self.issues=[];self.scripts=[];self.styles=[];self.current=None;self.data=[];self.csp='';self.script_id=None;self.data_blocks={}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ('iframe','object','embed','base'):self.issues.append('HTML: forbidden '+tag)
  for k,v in attrs:
   if k.lower().startswith('on') or k=='srcdoc':self.issues.append('HTML: inline handler / srcdoc')
   if k in ('src','href','action','poster') and v:
    # Only raster/blob resources or internal anchors in generated chrome; no active external links.
    if not (v.startswith(('data:image/png;base64,','data:image/jpeg;base64,','blob:','#'))):self.issues.append('HTML: external/unsafe resource '+k)
  if tag=='script':
   if 'src' in a:self.issues.append('HTML: external script')
   self.current='data' if a.get('type')=='application/json' else 'script';self.script_id=a.get('id');self.data=[]
  if tag=='style':self.current='style';self.data=[]
  if tag=='meta' and a.get('http-equiv','').lower()=='content-security-policy':self.csp=a.get('content','')
 def handle_data(self,data):
  if self.current:self.data.append(data)
 def handle_endtag(self,tag):
  if tag=='script' and self.current in ('script','data'):
   value=''.join(self.data)
   if self.current=='script':self.scripts.append((self.script_id,value))
   else:
    try:self.data_blocks[self.script_id]=json.loads(value)
    except ValueError:self.issues.append('HTML: invalid JSON data')
   self.current=None
  if tag=='style' and self.current=='style':self.styles.append(''.join(self.data));self.current=None
 def finish(self):
  directives={d.strip().split(' ',1)[0]:d.strip().split(' ',1)[1] if ' ' in d.strip() else '' for d in self.csp.split(';') if d.strip()}
  for k in ('default-src','connect-src','object-src','base-uri','frame-src','worker-src','form-action'):
   if directives.get(k)!="'none'":self.issues.append('CSP: '+k+' must be none')
  if 'unsafe-' in self.csp or 'blob:' in directives.get('script-src',''):self.issues.append('CSP: unsafe script/style allowance')
  for ident,text in self.scripts:
   self.issues+=scan_code(text,'HTML script '+str(ident),self.allowed)
   token="'sha256-"+base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()+"'"
   if token not in directives.get('script-src','').split():self.issues.append('CSP: script hash mismatch')
  for text in self.styles:
   self.issues+=scan_css(text,'HTML CSS')
   token="'sha256-"+base64.b64encode(hashlib.sha256(text.encode()).digest()).decode()+"'"
   if token not in directives.get('style-src','').split():self.issues.append('CSP: style hash mismatch')
  return self.issues

def scan_css(text,label):
 return [label+': external CSS resource'] if re.search(r'@import|url\s*\(|@font-face',text,re.I) else []

def audit_html(path,root=ROOT):
 from build import validate
 allowed={v['value'] for v in json.loads((root/'assets/security-allowlist.json').read_text())['urls']}
 p=HTMLAudit(allowed);p.feed(Path(path).read_text(encoding='utf-8'));issues=p.finish()
 try:validate(p.data_blocks.get('deck-data'))
 except (ValueError,TypeError,KeyError) as exc:issues.append('HTML model: '+str(exc))
 for ident,source in p.scripts:
  if ident=='corporate-vendor':
   expected=(root/'assets/vendor/pptxgenjs-4.0.1.bundle.js').read_text().replace('</script','<\\/script')
   if source!=expected:issues.append('HTML: vendor integrity mismatch')
 if not any(i=='corporate-vendor' for i,_ in p.scripts):issues.append('HTML: missing bundled vendor')
 return issues

def audit_source(root=ROOT):
 root=Path(root);issues=[]
 manifest=json.loads((root/'assets/vendor/manifest.json').read_text())
 vendor=root/'assets/vendor'/manifest['file'];raw=vendor.read_bytes()
 if len(raw)!=manifest['bytes'] or hashlib.sha256(raw).hexdigest()!=manifest['sha256']:issues.append('Vendor manifest/hash mismatch')
 if raw!=derive((root/'references/vendor/pptxgenjs-4.0.1.upstream.txt').read_bytes()):issues.append('Vendor does not reproduce from locked upstream recipe')
 if {p.name for p in (root/'assets/vendor').glob('*.js')}!={manifest['file']}:issues.append('Unapproved runtime dependency')
 allowlist=json.loads((root/'assets/security-allowlist.json').read_text())
 allowed={v['value'] for v in allowlist['urls'] if v.get('reason')}
 for p in [*root.glob('assets/*.js'),*root.glob('assets/vendor/*.js')]:issues+=scan_code(p.read_text(),str(p.relative_to(root)),allowed)
 for p in root.glob('assets/*.css'):issues+=scan_css(p.read_text(),str(p.relative_to(root)))
 for p in root.glob('scripts/*.py'):
  tree=ast.parse(p.read_text())
  for n in ast.walk(tree):
   if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('eval','exec','compile','__import__'):issues.append(str(p)+': dynamic Python execution')
   if isinstance(n,ast.Import):
    for alias in n.names:
     if alias.name.split('.')[0] not in sys.stdlib_module_names and alias.name not in ('contracts','vendor_offline','build','ooxml_package','ooxml_shapes'):issues.append(str(p)+': unapproved Python dependency '+alias.name)
 package=root/'PACKAGE-MANIFEST.json'
 if package.exists():
  m=json.loads(package.read_text())
  for f in m['files']:
   path=root/f['path']
   if not path.resolve().is_relative_to(root.resolve()) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=f['sha256']:issues.append('Package manifest mismatch: '+f['path'])
 return issues

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--html',type=Path,action='append',default=[]);p.add_argument('--root',type=Path,default=ROOT);a=p.parse_args()
 try:
  issues=audit_source(a.root)
  for path in a.html:issues+=audit_html(path,a.root)
 except (OSError,ValueError,KeyError,TypeError) as exc:issues=['Audit failed: '+str(exc)]
 print('\n'.join(issues) if issues else 'PASS: source, locked vendor and requested HTML security checks')
 return 1 if issues else 0
if __name__=='__main__':sys.exit(main())
