"""Portable distribution must be self-contained and exclude local caches."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('corporate_package', Path(__file__).resolve().parents[1] / 'scripts/package.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def test_archive_paths_hashes_and_cache_exclusion(self):
        with tempfile.TemporaryDirectory(prefix='公司 分发 ') as directory:
            root = Path(directory) / '源 目录'
            root.mkdir()
            (root / 'SKILL.md').write_text('中文 Skill', encoding='utf-8')
            (root / 'assets').mkdir()
            (root / 'assets/离线 内容.txt').write_text('完整内容', encoding='utf-8')
            # Repackaging an unpacked distribution must replace, not duplicate, the generated manifest.
            (root / 'PACKAGE-MANIFEST.json').write_text('{\"stale\": true}\n', encoding='utf-8')
            (root / '__pycache__').mkdir()
            (root / '__pycache__/local.pyc').write_bytes(b'cache')
            out = Path(directory) / '可分发 Skill.zip'
            manifest = package.package_skill(root, out)
            self.assertEqual(len(manifest['files']), 2)
            with zipfile.ZipFile(out) as archive:
                self.assertTrue(all(name.startswith('corporate-web-slides/') for name in archive.namelist()))
                self.assertFalse(any('__pycache__' in name for name in archive.namelist()))
                self.assertEqual(archive.namelist().count('corporate-web-slides/PACKAGE-MANIFEST.json'), 1)
                embedded = json.loads(archive.read('corporate-web-slides/PACKAGE-MANIFEST.json'))
                self.assertEqual(embedded, manifest)
                for item in embedded['files']:
                    self.assertEqual(hashlib.sha256(archive.read('corporate-web-slides/' + item['path'])).hexdigest(), item['sha256'])
            first = out.read_bytes()
            package.package_skill(root, out)
            self.assertEqual(out.read_bytes(), first)
