import hashlib
import json
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'tools'))

from package_plugin import build, check_downloads
from validate_plugin import DEFAULT_ROOT, validate


class PackageTests(unittest.TestCase):
    def test_download_check_accepts_matching_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = build(destination=Path(temporary) / 'build')
            downloads = Path(temporary) / 'downloads'
            shutil.copytree(Path(result['archive']).parent, downloads)
            check_downloads(result, downloads)

    def test_download_check_rejects_stale_or_altered_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = build(destination=Path(temporary) / 'build')
            archive = Path(result['archive'])
            for suffix in ('.zip', '.sha256', '.inventory.json'):
                with self.subTest(suffix=suffix):
                    downloads = Path(temporary) / suffix[1:]
                    shutil.copytree(archive.parent, downloads)
                    (downloads / (archive.stem + suffix)).write_bytes(b'stale artifact\n')
                    with self.assertRaisesRegex(ValueError, 'differs from source build'):
                        check_downloads(result, downloads)

    def test_download_check_rejects_missing_artifact(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = build(destination=Path(temporary) / 'build')
            with self.assertRaisesRegex(ValueError, 'Missing versioned download'):
                check_downloads(result, Path(temporary) / 'absent')

    def test_download_check_cannot_compare_a_build_with_itself(self):
        with tempfile.TemporaryDirectory() as temporary:
            result = build(destination=Path(temporary))
            with self.assertRaisesRegex(ValueError, 'separate build directory'):
                check_downloads(result, temporary)

    def copy_package(self, temporary):
        target = Path(temporary) / 'plugin'
        shutil.copytree(DEFAULT_ROOT, target, ignore=shutil.ignore_patterns('__pycache__'))
        return target

    def test_real_package_resources_resolve(self):
        result = validate()
        self.assertTrue(result['valid'], result['errors'])

    def test_archive_is_reproducible_and_has_root_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = build(destination=Path(temporary) / 'one')
            second = build(destination=Path(temporary) / 'two')
            self.assertEqual(first['sha256'], second['sha256'])
            with zipfile.ZipFile(first['archive']) as archive:
                names = archive.namelist()
                self.assertIn('plugin.json', names)
                self.assertFalse(any('__pycache__' in n or n.startswith(('.sources/', 'tests/')) for n in names))
                for name in names:
                    self.assertFalse(name.startswith('/') or '..' in Path(name).parts)
            self.assertEqual(first['sha256'], hashlib.sha256(Path(first['archive']).read_bytes()).hexdigest())

    def test_escaping_asset_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            manifest = json.loads((root / 'plugin.json').read_text())
            manifest['extensions']['com.openai']['interface']['logo'] = './../outside.svg'
            (root / 'plugin.json').write_text(json.dumps(manifest))
            self.assertFalse(validate(root)['valid'])

    def test_broken_skill_resource_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            path = root / 'skills/seo/SKILL.md'
            path.write_text(path.read_text() + '\n[Missing](../../references/absent.md)\n')
            self.assertFalse(validate(root)['valid'])

    def test_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            (root / 'leak.md').symlink_to(root / 'NOTICE.md')
            self.assertFalse(validate(root)['valid'])

    def test_secrets_and_network_helpers_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            (root / 'scripts/unsafe.py').write_text('import socket\nTOKEN = "' + 'sk-' + 'a'*32 + '"\n')
            result = validate(root)
            self.assertFalse(result['valid'])
            self.assertTrue(any('Network/process' in x for x in result['errors']))
            self.assertTrue(any('Possible secret' in x for x in result['errors']))

    def test_public_release_is_not_inferred_from_local_checks(self):
        result = validate(public=True)
        self.assertFalse(result['valid'])
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            path = root / 'plugin.json'
            manifest = json.loads(path.read_text())
            manifest['extensions']['com.openai']['interface'].pop('privacyPolicyURL', None)
            path.write_text(json.dumps(manifest))
            self.assertTrue(any('privacy' in x for x in validate(root, public=True)['errors']))
        self.assertTrue(any('chatgpt_installed_acceptance' in x for x in result['errors']))

    def test_overlong_listing_cannot_be_packaged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            manifest = json.loads((root / 'plugin.json').read_text())
            manifest['extensions']['com.openai']['interface']['shortDescription'] = 'x' * 31
            (root / 'plugin.json').write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                build(root, Path(temporary) / 'out')


    def test_excluded_provider_cannot_return_in_resources(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            (root / 'references/provider-regression.md').write_text('Use ' + 'Data' + 'ForSEO' + ' for this job.\n')
            result = validate(root)
            self.assertFalse(result['valid'])
            self.assertTrue(any('Excluded provider' in x for x in result['errors']))

    def test_source_exclusion_count_must_reconcile(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            path = root / 'provenance.json'
            data = json.loads(path.read_text())
            data['excluded_source_workflow_count'] = 2
            path.write_text(json.dumps(data))
            self.assertTrue(any('inclusion and exclusion counts' in x for x in validate(root)['errors']))

    def test_flow_routes_are_unique_and_dispatch_to_real_resources(self):
        routes = json.loads((DEFAULT_ROOT / 'assets/flow-routes.json').read_text())['routes']
        self.assertEqual(len(routes), 41)
        self.assertEqual(len({(x['stage'], x['route']) for x in routes}), 41)
        for route in routes:
            self.assertTrue((DEFAULT_ROOT / 'skills' / route['skill'] / 'SKILL.md').is_file())
            self.assertTrue((DEFAULT_ROOT / route['template']).is_file())

    def test_old_acceptance_cannot_approve_a_new_version(self):
        with tempfile.TemporaryDirectory() as temporary:
            receipt = Path(temporary) / 'acceptance.json'
            receipt.write_text(json.dumps({'plugin_name': 'ai-marketing-hub-seo', 'version': '0.1.0',
                                            'chatgpt_installed_acceptance': {'status': 'passed'},
                                            'publisher_verification': {'status': 'passed'},
                                            'openai_approval': {'status': 'passed'}}))
            errors = validate(public=True, acceptance_path=receipt)['errors']
            self.assertTrue(any('another plugin or version' in x for x in errors))
            self.assertTrue(any('does not match this manifest' in x for x in errors))


if __name__ == '__main__':
    unittest.main()
