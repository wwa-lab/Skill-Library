"""Small closed schema validator; schemas are maintained JSON, never user code."""
import json
import math
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def config(root=ROOT):
    assets = root / 'assets'
    load = lambda p: json.loads(p.read_text(encoding='utf-8'))
    result = {'contracts': load(assets / 'contracts.json'), 'brand': load(assets / 'brands/hsbc/brand.json'), 'themes': [load(p) for p in sorted((assets / 'themes').glob('*.json'))], 'layouts': load(assets / 'layouts.json')}
    check(result['brand'], result['contracts']['brand'], 'brand')
    for item in result['themes']: check(item, result['contracts']['theme'], 'theme')
    for item in result['layouts']: check(item, result['contracts']['layout'], 'layout')
    return result

def check(value, schema, path='config'):
    if 'enum' in schema:
        if not any(type(value) is type(v) and value == v for v in schema['enum']): raise ValueError(path + ': invalid enum')
        return
    kind = 'null' if value is None else 'boolean' if isinstance(value,bool) else 'object' if isinstance(value,dict) else 'array' if isinstance(value,list) else 'string' if isinstance(value,str) else 'number' if isinstance(value,(int,float)) else 'unknown'
    if kind not in ([schema['type']] if isinstance(schema['type'],str) else schema['type']): raise ValueError(path + ': invalid type')
    if kind == 'object':
        if set(value) - set(schema['properties']): raise ValueError(path + ': unknown field')
        if set(schema['required']) - set(value): raise ValueError(path + ': missing field')
        for k,v in value.items(): check(v,schema['properties'][k],path+'.'+k)
    elif kind == 'array':
        if not schema['minItems'] <= len(value) <= schema['maxItems']: raise ValueError(path + ': array length')
        for v in value: check(v,schema['items'],path+'[]')
    elif kind == 'number':
        if not math.isfinite(value) or not schema['minimum'] <= value <= schema['maximum']: raise ValueError(path + ': number range')
    elif kind == 'string':
        if len(value) > schema['maxLength'] or 'pattern' in schema and re.fullmatch(schema['pattern'],value) is None: raise ValueError(path + ': invalid text')

def hyperlink(value, slide_ids):
    if not isinstance(value,str) or len(value)>2048 or re.search(r'[\x00-\x20<>"\\]',value): raise ValueError('Invalid hyperlink')
    if value.startswith('#'):
        if value[1:] not in slide_ids: raise ValueError('Missing hyperlink slide')
    elif not re.fullmatch(r'https://[^/\s?#]+(?:[/?#][^\s]*)?|mailto:[^\s@]+@[^\s@]+',value,re.I):
        raise ValueError('Only https, mailto or #slide-id hyperlinks are allowed')
