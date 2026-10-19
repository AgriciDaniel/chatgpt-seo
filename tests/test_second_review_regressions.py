"""Concrete failures reproduced by the second independent package review."""

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
SCRIPTS = BASE / 'plugins/ai-marketing-hub-seo/scripts'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(BASE / 'tools'))

from analyze_gsc import analyze_gsc_csv
from analyze_crawl import analyze_crawl
from analyze_html import analyze_html
from compare_snapshots import FIELDS, compare_snapshots
from package_plugin import build
from url_values import absolute_url
from validate_plugin import DEFAULT_ROOT, package_content_digest, validate
from validate_sitemap import NAMESPACE, validate_sitemap
from validate_hreflang import validate_hreflang
from validate_structured_data import pointer_value, validate_structured_data
from seo_io import strict_json


class SecondEvidenceRegressions(unittest.TestCase):
    def snapshot(self):
        return analyze_html('<html><head><title>A</title></head><body><h1>A</h1></body></html>', 'https://example.test/a')

    def sitemap(self, entry):
        return validate_sitemap(('<urlset xmlns="'+NAMESPACE+'">'+entry+'</urlset>').encode())

    def test_gsc_position_cannot_underflow_or_lose_supplied_precision(self):
        for position in ['1e-999', '19.000000000000001', '1e999']:
            with self.subTest(position=position), self.assertRaises(ValueError):
                analyze_gsc_csv('page,clicks,impressions,position\na,1,10,'+position+'\n')
        result = analyze_gsc_csv('page,clicks,impressions,position\na,1,10,19.25\n')
        self.assertEqual(result['rows'][0]['position'], 19.25)
        self.assertEqual(result['totals']['impression_weighted_position'], 19.25)

    def test_url_controls_are_rejected_before_relative_resolution(self):
        for value in ['a\tb', '/a\nb', 'https://example.test/a\rb', '/a\x00b', '/a\x7fb', ' /a']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                absolute_url(value, 'https://example.test/')
        with self.assertRaises(ValueError):
            absolute_url('/a', 'https://example.test:bad/')
        self.assertEqual(absolute_url('../a', 'https://example.test/b/c'), 'https://example.test/a')

    def test_html_context_rejects_bad_ports_empty_credentials_and_whitespace(self):
        for url in ['https://example.test:bad/', 'https://example.test:65536/', 'https://@example.test/',
                    'https://example.test/A B', 'https://example.test/A\tB']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                analyze_html('<html><h1>A</h1></html>', url)

    def test_nonself_canonical_is_an_intent_gated_observation(self):
        result = analyze_html('<html><head><link rel="canonical" href="/preferred"></head><body><h1>A</h1></body></html>', 'https://example.test/a')
        finding = next(item for item in result['findings'] if item['id'] == 'CANONICAL_REVIEW')
        self.assertEqual(finding['evidence_pointer'], '/canonicals')
        self.assertTrue(finding['intent_confirmation_required'])
        self.assertEqual(finding['resolved_canonical'], 'https://example.test/preferred')
        same = analyze_html('<html><head><link rel="canonical" href="https://EXAMPLE.test:443/a"></head><body><h1>A</h1></body></html>', 'https://example.test/a')
        self.assertNotIn('CANONICAL_REVIEW', {item['id'] for item in same['findings']})

    def test_null_or_wrongly_typed_snapshots_cannot_establish_no_change(self):
        valid = self.snapshot()
        bad = {'format_version': True, 'evidence_level': 'source_html', 'url': '', **{field: None for field in FIELDS}}
        with self.assertRaises(ValueError):
            compare_snapshots(bad, bad)
        for field, replacement in [('format_version', True), ('url', ''), ('titles', None),
                                   ('noindex_observed', 0), ('headings', [{'level': True, 'text': 'A'}]),
                                   ('images', [{}]), ('json_ld', [{}]), ('visible_word_count', True),
                                   ('visible_text_sha256', 'invalid')]:
            with self.subTest(field=field):
                bad = copy.deepcopy(valid)
                bad[field] = replacement
                with self.assertRaises(ValueError):
                    compare_snapshots(valid, bad)
        self.assertEqual(compare_snapshots(valid, valid)['changes'], [])

    def test_sitemap_nested_loc_is_invalid_and_does_not_truncate_evidence(self):
        result = self.sitemap('<url><loc>https://example.test/a<b>tail</b></loc></url>')
        self.assertEqual(result['locations'], ['https://example.test/atail'])
        self.assertEqual(result['invalid_location_rows'], [1])
        self.assertEqual(result['hosts'], [])

    def test_sitemap_nested_or_duplicate_lastmod_is_invalid(self):
        for dates in ['<lastmod>2026-10-12<b/></lastmod>',
                      '<lastmod>2026-10-12</lastmod><lastmod>2026-10-12</lastmod>']:
            with self.subTest(dates=dates):
                result = self.sitemap('<url><loc>https://example.test/a</loc>'+dates+'</url>')
                self.assertEqual(result['invalid_lastmod_rows'], [1])
                self.assertIn('LASTMOD_INVALID', {finding['id'] for finding in result['findings']})

    def test_sitemap_findings_carry_observed_entry_locators(self):
        result = self.sitemap('<url><loc>https://example.test/a</loc><lastmod>2026-02-30</lastmod></url><url><loc>https://example.test/a</loc></url>')
        duplicate = next(item for item in result['findings'] if item['id'] == 'LOCATION_DUPLICATE')
        invalid = next(item for item in result['findings'] if item['id'] == 'LASTMOD_INVALID')
        self.assertEqual(duplicate['affected_entry_rows'], [1, 2])
        self.assertEqual(duplicate['evidence_pointer'], '/duplicate_locations')
        self.assertEqual(invalid['affected_entry_rows'], [1])
        self.assertEqual(invalid['evidence_pointer'], '/invalid_lastmod_rows')

    def test_equivalent_json_numbers_agree_without_equating_booleans(self):
        for observed, expected, agrees in [(19.0, 19, True), ({'price': [19.0]}, {'price': [19]}, True),
                                           ({'value': True}, {'value': 1}, False), ('19', 19, False)]:
            with self.subTest(observed=observed):
                result = validate_structured_data({'value': observed}, {'checks': [
                    {'pointer': '/value', 'expected': expected, 'evidence': 'synthetic visible fact'}]})
                self.assertEqual(result['visible_fact_checks'][0]['agrees_with_supplied_fact'], agrees)

    def test_large_equal_json_decimal_numbers_agree_despite_binary_float_rounding(self):
        data = strict_json('{"@type":"Offer","price":100000000000000000000000}')
        facts = strict_json('{"checks":[{"pointer":"/price","expected":1e23,"evidence":"synthetic numeric fact"}]}')
        result = validate_structured_data(data, facts)
        self.assertTrue(result['visible_fact_checks'][0]['agrees_with_supplied_fact'])
        self.assertEqual(result['findings'], [])
        facts['checks'][0]['expected'] = 100000000000000000000001
        self.assertFalse(validate_structured_data(data, facts)['visible_fact_checks'][0]['agrees_with_supplied_fact'])

    def test_json_pointers_reject_invalid_escapes_and_non_ascii_array_indices(self):
        for pointer in ['/a~2b', '/a~']:
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                pointer_value({'a~2b': 'A', 'a~': 'B'}, pointer)
        for pointer in ['/01', '/١', '/-']:
            with self.subTest(pointer=pointer), self.assertRaises(ValueError):
                pointer_value(['zero', 'one'], pointer)
        self.assertEqual(pointer_value({'a/b': {'~': ['value']}}, '/a~1b/~0/0'), 'value')

    def test_crawl_optional_urls_do_not_coerce_wrong_types_to_absent(self):
        for field in ['canonical', 'start_url']:
            for value in [False, 0, '', [], {}]:
                with self.subTest(field=field, value=value):
                    data = {'pages': [{'url': 'https://example.test/'}]}
                    target = data['pages'][0] if field == 'canonical' else data
                    target[field] = value
                    with self.assertRaises(ValueError):
                        analyze_crawl(data)
        result = analyze_crawl({'pages': [{'url': 'https://example.test/', 'canonical': None}], 'start_url': None})
        self.assertIsNone(result['depth_from_supplied_start'])

    def test_reciprocal_hreflang_chain_keeps_full_cluster_consistency_unknown(self):
        rows = [{'source_url': 'https://example.test/'+source, 'language': language, 'target_url': 'https://example.test/'+target}
                for source, language, target in [('en', 'en', 'en'), ('en', 'fr', 'fr'),
                    ('fr', 'en', 'en'), ('fr', 'fr', 'fr'), ('fr', 'de', 'de'), ('de', 'fr', 'fr'), ('de', 'de', 'de')]]
        result = validate_hreflang({'annotations': rows})
        self.assertEqual(result['findings'], [])
        self.assertEqual(result['cluster_consistency_scope'], 'observed_pairs_only')
        self.assertTrue(any('Complete connected-cluster' in item for item in result['limitations']))


class SecondPackageRegressions(unittest.TestCase):
    def copy_package(self, temporary):
        root = Path(temporary)/'plugin'
        shutil.copytree(DEFAULT_ROOT, root, ignore=shutil.ignore_patterns('__pycache__'))
        manifest_path = root/'plugin.json'
        manifest = json.loads(manifest_path.read_text())
        for field in ('logo', 'logoDark', 'composerIcon', 'composerIconDark'):
            manifest['extensions']['com.openai']['interface'][field] = './assets/logo.svg'
        manifest_path.write_text(json.dumps(manifest))
        return root

    def test_declared_icon_must_be_shipped_even_if_excluded_path_exists(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            (root/'node_modules').mkdir()
            shutil.copy(root/'assets/logo.svg', root/'node_modules/logo.svg')
            path = root/'plugin.json'
            manifest = json.loads(path.read_text())
            manifest['extensions']['com.openai']['interface']['logo'] = './node_modules/logo.svg'
            path.write_text(json.dumps(manifest))
            self.assertFalse(validate(root)['valid'])

    def test_markdown_resource_must_be_shipped_even_if_excluded_file_exists(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            (root/'node_modules').mkdir()
            (root/'node_modules/missing-in-zip.md').write_text('Resource\n')
            path = root/'skills/seo/SKILL.md'
            path.write_text(path.read_text()+'\n[Resource](../../node_modules/missing-in-zip.md)\n')
            self.assertFalse(validate(root)['valid'])

    def test_nested_package_output_is_rejected_before_source_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            digest = package_content_digest(root)
            with self.assertRaises(ValueError):
                build(root, root/'out')
            self.assertFalse((root/'out').exists())
            self.assertEqual(package_content_digest(root), digest)
            self.assertTrue(validate(root)['valid'])

    def test_svg_requires_real_root_and_finite_supported_dimensions(self):
        fixtures = ['<html viewBox="0 0 1024 1024"/>',
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 inf inf"/>',
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="nan 0 1024 1024"/>',
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4097 4097"/>']
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            for svg in fixtures:
                with self.subTest(svg=svg):
                    (root/'assets/logo.svg').write_text(svg)
                    self.assertFalse(validate(root)['valid'])

    def test_svg_external_and_active_resources_are_rejected(self):
        fragments = ['<image href="https://example.test/logo.png"/>', '<script/>',
                     '<rect onclick="doSomething()"/>', '<foreignObject/>',
                     '<style>@import "https://example.test/style.css"</style>',
                     '<rect fill="url(https://example.test/fill.svg)"/>']
        with tempfile.TemporaryDirectory() as temporary:
            root = self.copy_package(temporary)
            for fragment in fragments:
                with self.subTest(fragment=fragment):
                    (root/'assets/logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">'+fragment+'</svg>')
                    self.assertFalse(validate(root)['valid'])
            (root/'assets/logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024"><defs><linearGradient id="g"/></defs><rect fill="url(\'\x23g\')"/></svg>')
            self.assertTrue(validate(root)['valid'])


if __name__ == '__main__':
    unittest.main()
