"""Regressions demonstrated by the independent full-package review."""

import hashlib
import base64
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SCRIPTS = BASE / 'plugins/ai-marketing-hub-seo/scripts'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(BASE / 'tools'))

from analyze_crawl import analyze_crawl
from analyze_html import analyze_html
from package_plugin import build
from seo_io import strict_json
from url_values import absolute_url, origin
from validate_hreflang import validate_hreflang
from validate_plugin import DEFAULT_ROOT, validate
from validate_sitemap import NAMESPACE, validate_sitemap
from validate_structured_data import validate_structured_data


class EvidenceRegressions(unittest.TestCase):
    def inspect(self, fragment):
        return analyze_html('<html><body>' + fragment + '</body></html>', 'https://example.test/')

    def test_linked_heading_keeps_both_source_observations(self):
        result = self.inspect('<h1><a href="/x">Linked heading</a></h1>')
        self.assertEqual(result['headings'], [{'level': 1, 'text': 'Linked heading'}])
        self.assertEqual(result['links'], [{'url': 'https://example.test/x', 'text': 'Linked heading'}])
        self.assertNotIn('H1_REVIEW', {x['id'] for x in result['findings']})

    def test_link_wrapping_a_heading_keeps_both_observations(self):
        result = self.inspect('<a href="/x"><h2>Card title</h2></a>')
        self.assertEqual(result['headings'], [{'level': 2, 'text': 'Card title'}])
        self.assertEqual(result['links'], [{'url': 'https://example.test/x', 'text': 'Card title'}])

    def test_suppressed_text_does_not_leak_into_heading_or_anchor(self):
        result = self.inspect('<h1><a href="/x">A<script>hidden</script><style>hidden</style>'
                              '<template><img src="hidden"><span>hidden</span></template>B</a></h1>')
        self.assertEqual(result['headings'][0]['text'], 'AB')
        self.assertEqual(result['links'][0]['text'], 'AB')
        self.assertEqual(result['images'], [])

    def test_anchor_without_href_is_not_a_link_but_empty_href_is_observed(self):
        result = self.inspect('<a id="section">Section</a><a href="">Explicit self link</a>')
        self.assertEqual(result['links'], [{'url': 'https://example.test/', 'text': 'Explicit self link'}])

    def test_html_jsonld_rejects_duplicate_and_lossy_numeric_input(self):
        for raw in ['{"name":"a","name":"b"}', '{"price":1e999}', '{"price":19.000000000000001}']:
            with self.subTest(raw=raw):
                result = self.inspect('<script type="application/ld+json">' + raw + '</script>')
                self.assertEqual(result['json_ld'][0]['parse_status'], 'invalid')
                self.assertIn('JSON_LD_SYNTAX', {x['id'] for x in result['findings']})

    def test_normalized_crawl_urls_keep_original_source_values(self):
        result = analyze_crawl({'pages': [{'url': 'https://example.test/', 'links': ['https://EXAMPLE.test:443/a']},
                                          {'url': 'https://EXAMPLE.test:443/a', 'status': 404}]})
        self.assertEqual(result['unobserved_internal_link_destinations'], [])
        self.assertIn('link_to_observed_http_error', {x['code'] for x in result['findings']})
        self.assertEqual(result['url_keys'][1]['supplied_url'], 'https://EXAMPLE.test:443/a')
        self.assertEqual(result['url_keys'][1]['comparison_url'], 'https://example.test/a')

    def test_url_keys_preserve_path_query_case_nondefault_ports_and_ipv6(self):
        self.assertEqual(absolute_url('HTTPS://EXAMPLE.test:443/A?Key=Value#section'), 'https://example.test/A?Key=Value')
        self.assertEqual(absolute_url('http://[2001:DB8::1]:8080/A'), 'http://[2001:db8::1]:8080/A')
        self.assertEqual(origin('https://example.test:443/'), origin('https://example.test/'))
        self.assertNotEqual(origin('https://example.test:8443/'), origin('https://example.test/'))
        with self.assertRaises(ValueError):
            absolute_url('https://@example.test/')

    def test_equivalent_hreflang_urls_do_not_create_false_reciprocity_findings(self):
        rows = [{'source_url': source, 'language': lang, 'target_url': target}
                for source in ['https://EXAMPLE.test:443/en', 'https://example.test/fr']
                for lang, target in [('en', 'https://example.test/en'), ('fr', 'https://EXAMPLE.test:443/fr')]]
        result = validate_hreflang({'annotations': rows})
        self.assertEqual(result['findings'], [])
        self.assertEqual(result['reciprocity_unknown'], [])
        self.assertEqual(result['url_keys'][0]['supplied_source_url'], rows[0]['source_url'])

    def test_nonprotocol_required_tags_are_reported_and_extensions_are_retained(self):
        for entry in ['<url xmlns="urn:other"><loc>https://example.test/a</loc></url>',
                      '<url><loc xmlns="">https://example.test/a</loc></url>']:
            with self.subTest(entry=entry):
                result = validate_sitemap(('<urlset xmlns="'+NAMESPACE+'">'+entry+'</urlset>').encode())
                self.assertEqual(result['invalid_location_rows'], [1])
                self.assertEqual(result['invalid_namespace_rows'], [1])
        xml = '<urlset xmlns="'+NAMESPACE+'" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
        xml += '<url><loc>https://example.test/a</loc><image:image><image:loc>https://example.test/a.png</image:loc></image:image></url></urlset>'
        self.assertEqual(validate_sitemap(xml.encode())['findings'], [])

    def test_invalid_location_ports_are_not_protocol_urls(self):
        for url in ['https://example.test:bad/a', 'https://example.test:65536/a', 'https://@example.test/a']:
            with self.subTest(url=url):
                xml = '<urlset xmlns="'+NAMESPACE+'"><url><loc>'+url+'</loc></url></urlset>'
                self.assertEqual(validate_sitemap(xml.encode())['invalid_location_rows'], [1])

    def test_nested_fact_comparison_preserves_json_types(self):
        for observed, expected in [({'value': True}, {'value': 1}), ([{'value': True}], [{'value': 1}]),
                                   ({'items': [True]}, {'items': [1]})]:
            with self.subTest(observed=observed):
                data = {'@type': 'CreativeWork', 'example': observed}
                facts = {'checks': [{'pointer': '/example', 'expected': expected, 'evidence': 'selected fixture'}]}
                result = validate_structured_data(data, facts)
                self.assertFalse(result['visible_fact_checks'][0]['agrees_with_supplied_fact'])
                self.assertEqual(result['findings'][0]['code'], 'visible_fact_mismatch')

    def test_strict_json_refuses_precision_loss_and_keeps_allowed_exact_strings(self):
        for raw in ['{"price":19.000000000000001}', '{"price":1e999}', '{"price":1e-999}', '{"price":1e-999999999999999999999999}']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                strict_json(raw)
        self.assertEqual(strict_json('{"price":"19.000000000000001","count":2,"ratio":0.1}')['price'], '19.000000000000001')

    def test_malformed_bounded_cli_inputs_return_unavailable_json(self):
        cases = [('analyze_gsc.py', 'field.csv', 'query,clicks,impressions,position\n'+'x'*131073+',1,2,3\n'),
                 ('analyze_gsc.py', 'count.csv', 'query,clicks,impressions,position\nx,'+'9'*4000+',2,3\n'),
                 ('scorecard.py', 'score.json', '{"categories":{"technical":{"status":"assessed","score":'+'9'*4000+',"evidence":["fixture"],"method":"fixture"}}}')]
        with tempfile.TemporaryDirectory() as temporary:
            for script, name, content in cases:
                with self.subTest(script=script, name=name):
                    path = Path(temporary) / name
                    path.write_text(content)
                    result = subprocess.run([sys.executable, str(SCRIPTS/script), str(path)], capture_output=True, text=True,
                                            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, timeout=10)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(json.loads(result.stdout)['result_status'], 'unavailable')
                    self.assertEqual(result.stderr, '')


class PackageRegressions(unittest.TestCase):
    def copy_package(self, temporary):
        target = Path(temporary) / 'plugin'
        shutil.copytree(DEFAULT_ROOT, target, ignore=shutil.ignore_patterns('__pycache__'))
        return target

    def use_png_icons(self, root):
        path = root/'plugin.json'
        manifest = json.loads(path.read_text())
        interface = manifest['extensions']['com.openai']['interface']
        for field in ('logo', 'logoDark', 'composerIcon', 'composerIconDark'):
            interface[field] = './assets/logo.png'
        path.write_text(json.dumps(manifest))

    def test_svg_presentation_preserves_exact_supplied_logo_bytes(self):
        manifest = json.loads((DEFAULT_ROOT/'plugin.json').read_text())
        interface = manifest['extensions']['com.openai']['interface']
        self.assertTrue(all(interface[field] == './assets/logo.png' for field in ('logo','logoDark','composerIcon','composerIconDark')))
        svg = ET.fromstring((DEFAULT_ROOT/'assets/logo.svg').read_text())
        images = list(svg.iter('{http://www.w3.org/2000/svg}image'))
        self.assertEqual(len(images), 1)
        data = images[0].get('href')
        self.assertTrue(data.startswith('data:image/png;base64,'))
        decoded = base64.b64decode(data.split(',', 1)[1], validate=True)
        self.assertEqual(decoded, (DEFAULT_ROOT/'assets/logo.png').read_bytes())
        self.assertEqual(hashlib.sha256(decoded).hexdigest(), '205b9b5738d7d95940df911191e09d50799d8edaa5953fb4205305fcfa887e28')
        self.assertEqual(svg.get('viewBox'), '0 0 1024 1024')

    def test_provider_exclusion_covers_unknown_types_binary_names_and_binary_content(self):
        provider = 'Data' + 'ForSEO'
        for relative, content in [('references/provider.txt', provider.encode()),
                                   ('assets/'+provider.lower()+'.png', b'fixture'),
                                   ('assets/hidden.png', provider.encode())]:
            with tempfile.TemporaryDirectory() as temporary, self.subTest(relative=relative):
                root = self.copy_package(temporary)
                (root/relative).write_bytes(content)
                result = validate(root)
                self.assertFalse(result['valid'])
                self.assertTrue(any('Excluded provider' in x for x in result['errors']))
                with self.assertRaises(ValueError):
                    build(root, Path(temporary)/'out')

    def test_unsupported_file_types_do_not_silently_enter_the_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            (root/'references/unreviewed.txt').write_text('Synthetic unreviewed text')
            self.assertTrue(any('Unsupported package file type' in x for x in validate(root)['errors']))

    def test_archive_paths_are_portable_across_extractors(self):
        for name in ['assets\\..\\..\\escape.py', 'C:escape.md']:
            with tempfile.TemporaryDirectory() as temporary, self.subTest(name=name):
                root = self.copy_package(temporary)
                (root/name).write_text('Synthetic path fixture')
                self.assertTrue(any('Nonportable archive path' in x for x in validate(root)['errors']))
                with self.assertRaises(ValueError):
                    build(root, Path(temporary)/'out')

    def test_unreviewed_and_dynamic_import_forms_are_rejected(self):
        for source in ['from urllib import request\n', 'import os\nos.system("synthetic")\n',
                       '__import__("socket")\n', 'eval("synthetic")\n']:
            with tempfile.TemporaryDirectory() as temporary, self.subTest(source=source):
                root = self.copy_package(temporary)
                (root/'scripts/unsafe.py').write_text(source)
                self.assertFalse(validate(root)['valid'])

    def test_acceptance_is_bound_to_all_package_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            manifest_path = root/'plugin.json'
            manifest = json.loads(manifest_path.read_text())
            manifest['extensions']['com.openai']['interface']['privacyPolicyURL'] = 'https://example.test/synthetic-privacy'
            manifest_path.write_text(json.dumps(manifest))
            local = validate(root)
            receipt = Path(temporary)/'synthetic-acceptance.json'
            receipt.write_text(json.dumps({'plugin_name': manifest['name'], 'version': manifest['version'],
                                          'manifest_sha256': local['manifest_sha256'], 'package_content_sha256': local['package_content_sha256'],
                                          'chatgpt_installed_acceptance': {'status': 'passed'}, 'publisher_verification': {'status': 'passed'},
                                          'openai_approval': {'status': 'passed'}}))
            self.assertTrue(validate(root, public=True, acceptance_path=receipt)['valid'])
            helper = root/'scripts/analyze_html.py'
            helper.write_text(helper.read_text()+'\n# Same-version changed content fixture\n')
            errors = validate(root, public=True, acceptance_path=receipt)['errors']
            self.assertTrue(any('does not match package content' in x for x in errors))
            self.assertEqual(local['manifest_sha256'], hashlib.sha256(manifest_path.read_bytes()).hexdigest())

    def test_malformed_manifest_containers_return_validation_errors(self):
        for mutation in ('root', 'extensions', 'interface', 'name', 'version'):
            with tempfile.TemporaryDirectory() as temporary, self.subTest(mutation=mutation):
                root = self.copy_package(temporary)
                path = root/'plugin.json'
                manifest = json.loads(path.read_text())
                if mutation == 'root':
                    manifest = []
                elif mutation == 'extensions':
                    manifest['extensions'] = []
                elif mutation == 'interface':
                    manifest['extensions']['com.openai']['interface'] = []
                else:
                    manifest[mutation] = []
                path.write_text(json.dumps(manifest))
                self.assertFalse(validate(root)['valid'])

    def test_png_limits_and_integrity_reject_header_only_or_corrupt_icons(self):
        source = (DEFAULT_ROOT/'assets/logo.png').read_bytes()
        cases = [b'\x89PNG\r\n\x1a\n', source[:-1], source[:-1]+bytes([source[-1]^1])]
        for size in (47, 4097):
            raw = bytearray(source)
            raw[16:24] = struct.pack('>II', size, size)
            raw[29:33] = struct.pack('>I', zlib.crc32(raw[12:29]))
            cases.append(bytes(raw))
        for index, content in enumerate(cases):
            with tempfile.TemporaryDirectory() as temporary, self.subTest(index=index):
                root = self.copy_package(temporary)
                self.use_png_icons(root)
                (root/'assets/logo.png').write_bytes(content)
                self.assertFalse(validate(root)['valid'])

    def test_indexed_png_palette_must_precede_pixel_data(self):
        def chunk(kind, data):
            return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
        header = chunk(b'IHDR', struct.pack('>IIBBBBB', 48, 48, 8, 3, 0, 0, 0))
        palette = chunk(b'PLTE', bytes([255, 0, 0]))
        pixels = chunk(b'IDAT', zlib.compress((b'\x00' * 49) * 48))
        end = chunk(b'IEND', b'')
        for valid, data in [(True, header + palette + pixels + end), (False, header + pixels + palette + end)]:
            with tempfile.TemporaryDirectory() as temporary, self.subTest(valid=valid):
                root = self.copy_package(temporary)
                self.use_png_icons(root)
                (root/'assets/logo.png').write_bytes(b'\x89PNG\r\n\x1a\n' + data)
                self.assertEqual(validate(root)['valid'], valid)


if __name__ == '__main__':
    unittest.main()
