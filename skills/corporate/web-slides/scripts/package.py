#!/usr/bin/env python3
"""Create an offline distributable ZIP with a per-file SHA-256 manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'__pycache__', '.git', '.DS_Store', '.pytest_cache'}


def package_skill(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if not (root / 'SKILL.md').is_file():
        raise ValueError('Skill root must contain SKILL.md')
    files = []
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if any(part in SKIP for part in relative.parts) or path.suffix in ('.pyc', '.zip', '.skill'):
            continue
        if path.is_symlink():
            raise ValueError('Do not distribute symbolic links: ' + str(relative))
        if relative.as_posix() == 'PACKAGE-MANIFEST.json':
            continue
        if path.is_file() and path.resolve() != output:
            files.append((relative.as_posix(), path.read_bytes()))
    manifest = {'format': 1, 'skill': 'corporate-web-slides', 'files': [{'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for name, data in files]}
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in [*files, ('PACKAGE-MANIFEST.json', manifest_bytes)]:
            entry = zipfile.ZipInfo('corporate-web-slides/' + name, date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    with zipfile.ZipFile(output) as archive:
        for item in manifest['files']:
            if hashlib.sha256(archive.read('corporate-web-slides/' + item['path'])).hexdigest() != item['sha256']:
                raise ValueError('Archive checksum verification failed')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = package_skill(ROOT, args.output)
        print('Packaged %d files: %s' % (len(manifest['files']), args.output.resolve()))
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print('Packaging failed: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
