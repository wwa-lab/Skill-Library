"""Bounded, read-only OOXML package access; Python 3.9+, standard library."""
import base64
from pathlib import PurePosixPath
import posixpath
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart'}
MAX_MEMBER = 32 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024

def tag(node):
    return node.tag.rsplit('}', 1)[-1]

def find(node, path):
    return node.find(path, NS) if node is not None else None

def all_nodes(node, path):
    return node.findall(path, NS) if node is not None else []

def text_content(node):
    return '\n'.join(''.join(n.text or '' if tag(n) != 'br' else '\n' for n in p.iter() if tag(n) in ('t', 'br')) for p in all_nodes(node, './/a:p'))

class Package:
    def __init__(self, path):
        self.archive = zipfile.ZipFile(path)
        self.names = set()
        try:
            items = self.archive.infolist()
            if len(items) > 4096 or sum(i.file_size for i in items) > MAX_TOTAL:
                raise ValueError('OOXML archive exceeds 4096 files / 128 MiB limit')
            for item in items:
                parts = PurePosixPath(item.filename).parts
                if (item.filename.startswith('/') or '\\' in item.filename or '..' in parts
                        or ':' in item.filename or item.filename in self.names):
                    raise ValueError('Unsafe or duplicate OOXML package path')
                if item.file_size > MAX_MEMBER or item.flag_bits & 1:
                    raise ValueError('Encrypted or oversized OOXML member')
                self.names.add(item.filename)
        except Exception:
            self.archive.close()
            raise

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.archive.close()

    def data(self, name):
        if name not in self.names:
            raise ValueError('Missing OOXML part: ' + name)
        return self.archive.read(name)

    def xml(self, name):
        data = self.data(name)
        # Reject XML DTD/entity declarations in UTF-8 and UTF-16 encodings.
        if re.search(br'<!\s*(DOCTYPE|ENTITY)', data.replace(b'\0', b''), re.I):
            raise ValueError('DTD / entity declarations are not allowed')
        try:
            return ET.fromstring(data)
        except ET.ParseError as exc:
            raise ValueError('Invalid XML in ' + name) from exc

    def relationships(self, name):
        relpath = posixpath.join(posixpath.dirname(name), '_rels', posixpath.basename(name) + '.rels')
        if relpath not in self.names:
            return {}
        result = {}
        for rel in self.xml(relpath):
            target = unquote(rel.get('Target', ''))
            external = rel.get('TargetMode') == 'External' or bool(urlsplit(target).scheme)
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target.lstrip('/'))) if not target.startswith('/') else posixpath.normpath(target.lstrip('/'))
            if not external and (resolved.startswith('../') or '\\' in target or ':' in target):
                raise ValueError('Unsafe relationship target in ' + name)
            result[rel.get('Id')] = {'type': rel.get('Type', '').rsplit('/', 1)[-1], 'target': target if external else resolved, 'external': external}
        return result

    def image(self, name):
        data = self.data(name)
        mime = 'image/png' if data.startswith(b'\x89PNG\r\n\x1a\n') else 'image/jpeg' if data.startswith(b'\xff\xd8\xff') else None
        return 'data:' + mime + ';base64,' + base64.b64encode(data).decode('ascii') if mime else None
