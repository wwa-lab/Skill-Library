#!/usr/bin/env python3
"""Reproduce the documented offline-only derivative of the pinned PptxGenJS bundle.
No downloads, dependencies or minifier. Exact source hash/anchors fail closed.
"""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = '4fb9eac5cfefb213e2d8743c2b7151025f31bfb3f834c73c12062916daa0f3f8'

def replace_once(source, old, new):
    if source.count(old)!=1: raise ValueError('Vendor patch anchor changed: '+old[:60])
    return source.replace(old,new)

def derive(raw):
    if hashlib.sha256(raw).hexdigest()!=UPSTREAM: raise ValueError('Upstream hash mismatch')
    s=raw.decode('utf-8')
    # Chrome/Edge support modern ES: remove the entire historical Babel polyfill IIFE.
    a=s.index(',function a(n,o,i)',s.index('54:[function'))
    b=s.index(';var PptxGenJS=',a)
    s=s[:a]+';'+s[b+1:]
    # Replace two obsolete scheduler modules; never create script elements or compile strings.
    a=s.index('36:[function');b=s.index('37:[function',a)
    s=s[:a]+'36:[function(e,l,t){l.exports=function(task){queueMicrotask(task)}},{}],'+s[b:]
    a=s.index('54:[function');b=s.index('},{},[10])(10)})',a)
    s=s[:a]+'54:[function(){if(!globalThis.setImmediate){globalThis.setImmediate=function(task,...args){if(typeof task!=="function")throw new TypeError("Callback required");return setTimeout(task,0,...args)};globalThis.clearImmediate=clearTimeout}},{}]'+s[b:]
    # Media must be embedded raster data. All path/network/SVG conversion paths fail closed.
    a=s.index('function Ce(e)');b=s.index('let Se=',a)
    s=s[:a]+'''function Ce(e){for(const m of e._relsMedia){if(m.isSvgPng||m.type==="online"||m.path&&!m.data)throw new Error("Offline exporter requires embedded raster media");}return []}'''+s[b:]
    # No Node-only dynamic imports in a browser runtime.
    s=replace_once(s,'return e?(e=(yield import("node:fs")).promises,e=e.writeFile,yield e(t,r)):yield this.writeFileToBrowser(t,r),t','if(e)throw new Error("Browser export only");return yield this.writeFileToBrowser(t,r),t')
    return ('/* Corporate offline derivative: scripts/vendor_offline.py; original licenses retained. */\n'+s).encode()

def main():
    raw=(ROOT/'references/vendor/pptxgenjs-4.0.1.upstream.txt').read_bytes()
    data=derive(raw)
    target=ROOT/'assets/vendor/pptxgenjs-4.0.1.bundle.js';target.write_bytes(data)
    p=target.parent/'manifest.json';m=json.loads(p.read_text())
    m.update({'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'derivative':{'source':'references/vendor/pptxgenjs-4.0.1.upstream.txt','upstreamSha256':UPSTREAM,'recipe':'scripts/vendor_offline.py','target':'modern Chrome/Edge browsers','changes':['remove legacy Babel polyfills','replace legacy scheduler fallbacks with native microtasks/timers','reject all path/remote/SVG media loading','disable Node file export']}})
    p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print('Offline vendor:',len(data),'bytes',m['sha256'])
if __name__=='__main__':main()
