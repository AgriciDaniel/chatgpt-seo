import copy
import json
import struct
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'plugins/ai-marketing-hub-seo/scripts'
sys.path.insert(0, str(SCRIPTS))

from analyze_crawl import analyze_crawl
from inspect_image import inspect_image
from validate_hreflang import validate_hreflang
from validate_structured_data import pointer_value, strict_json, validate_structured_data


class CrawlTests(unittest.TestCase):
    def fixture(self):
        return {'start_url': 'https://example.test/', 'scope': 'synthetic sample',
                'pages': [{'url': 'https://example.test/', 'status': 200, 'title': 'Title',
                           'links': ['/a', '/unobserved', 'https://other.test/']},
                          {'url': 'https://example.test/a', 'status': 404, 'title': 'Title',
                           'indexable': False, 'canonical': '/canonical'}],
                'sitemap_urls': ['https://example.test/a', 'https://example.test/unknown']}

    def test_sample_graph_retains_unknown_destinations(self):
        result = analyze_crawl(self.fixture())
        self.assertEqual(result['depth_from_supplied_start']['https://example.test/a'], 1)
        self.assertEqual(result['unobserved_internal_link_destinations'], ['https://example.test/unobserved'])
        self.assertEqual(result['sample_pages_without_observed_inlinks'], ['https://example.test/'])
        self.assertEqual(len(result['duplicate_title_groups']), 1)

    def test_supplied_controls_and_sitemap_keep_intent_and_unknowns(self):
        result = analyze_crawl(self.fixture())
        codes = {x['code'] for x in result['findings']}
        self.assertTrue({'observed_http_error', 'link_to_observed_http_error',
                         'index_intent_review', 'nonself_canonical_review'} <= codes)
        self.assertIsNone(result['sitemap_observations'][1]['observed_status'])
        self.assertFalse(result['sitemap_observations'][1]['in_supplied_sample'])
        self.assertTrue(all(x['evidence_pointer'].startswith('/pages/') for x in result['findings']))

    def test_duplicate_pages_and_invalid_observations_are_refused(self):
        for mutation in ('duplicate', 'status', 'indexable', 'start'):
            data = self.fixture()
            if mutation == 'duplicate':
                data['pages'].append(copy.deepcopy(data['pages'][0]))
            elif mutation == 'status':
                data['pages'][0]['status'] = True
            elif mutation == 'indexable':
                data['pages'][0]['indexable'] = 'false'
            else:
                data['start_url'] = 'https://example.test/unobserved'
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                analyze_crawl(data)

    def test_fragments_do_not_invent_distinct_pages(self):
        data = self.fixture()
        data['pages'][0]['links'] = ['/a#details']
        self.assertEqual(analyze_crawl(data)['unobserved_internal_link_destinations'], [])

    def test_url_credentials_and_unsupported_schemes_are_refused(self):
        for url in ['https://user:password@example.test/', 'file:///secret', 'https://example.test:bad/']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                analyze_crawl({'pages': [{'url': url}]})


class HreflangTests(unittest.TestCase):
    def fixture(self):
        return {'annotations': [{'source_url': source, 'language': language, 'target_url': target}
                                for source in ['https://example.test/en', 'https://example.test/fr']
                                for language, target in [('en', 'https://example.test/en'), ('fr', 'https://example.test/fr')]]}

    def test_complete_reciprocal_sample(self):
        result = validate_hreflang(self.fixture())
        self.assertEqual(result['findings'], [])
        self.assertEqual(result['reciprocity_unknown'], [])

    def test_unobserved_target_is_unknown(self):
        data = self.fixture()
        data['annotations'] = data['annotations'][:2]
        result = validate_hreflang(data)
        self.assertEqual(len(result['reciprocity_unknown']), 1)
        self.assertNotIn('missing_reciprocal_in_supplied_rows', {x['code'] for x in result['findings']})

    def test_conflicts_and_invalid_syntax_are_reported(self):
        data = self.fixture()
        data['annotations'].extend([
            {'source_url': 'https://example.test/en', 'language': 'en', 'target_url': 'https://example.test/other'},
            {'source_url': 'https://example.test/en', 'language': 'english', 'target_url': 'https://example.test/en'}])
        codes = {x['code'] for x in validate_hreflang(data)['findings']}
        self.assertTrue({'conflicting_language_target', 'invalid_language_tag_syntax'} <= codes)

    def test_missing_reciprocity_in_observed_target(self):
        data = self.fixture()
        data['annotations'] = [row for row in data['annotations'] if not (row['source_url'].endswith('/fr') and row['language'] == 'en')]
        codes = {x['code'] for x in validate_hreflang(data)['findings']}
        self.assertIn('missing_reciprocal_in_supplied_rows', codes)

    def test_registry_membership_is_not_claimed_from_syntax(self):
        result = validate_hreflang({'annotations': [{'source_url': 'https://example.test/',
                                                    'language': 'zz-ZZ', 'target_url': 'https://example.test/'}]})
        self.assertEqual(result['findings'], [])
        self.assertIn('not ISO registry membership', ' '.join(result['limitations']))


class ImageMetadataTests(unittest.TestCase):
    def test_png_header_dimensions_and_alpha_are_limited(self):
        data = b'\x89PNG\r\n\x1a\n' + struct.pack('>I', 13) + b'IHDR' + struct.pack('>II', 1200, 630) + bytes([8, 6, 0, 0, 0]) + b'\x00'*4
        result = inspect_image(data)
        self.assertEqual((result['width'], result['height']), (1200, 630))
        self.assertTrue(result['alpha_channel_in_header'])
        self.assertIn('does not prove pixels are transparent', ' '.join(result['limitations']))

    def test_gif_header_and_unknown_transparency(self):
        result = inspect_image(b'GIF89a' + struct.pack('<HH', 80, 60) + b'\x00'*3)
        self.assertEqual(result['format'], 'GIF')
        self.assertIsNone(result['alpha_channel_in_header'])

    def test_jpeg_frame_dimensions(self):
        data = b'\xff\xd8\xff\xc0' + struct.pack('>H', 11) + bytes([8]) + struct.pack('>HH', 600, 800) + bytes([1, 1, 0x11, 0])
        self.assertEqual(inspect_image(data)['width'], 800)

    def test_truncated_unknown_and_zero_headers_are_refused(self):
        for data in [b'', b'\x89PNG\r\n\x1a\n', b'GIF89a', b'\xff\xd8\xff\xc0\x00\x40', b'GIF89a'+b'\x00'*7]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                inspect_image(data)


class StructuredDataTests(unittest.TestCase):
    def test_nonstandard_numbers_and_duplicate_properties_are_refused(self):
        for text in ['{"price":NaN}', '{"price":Infinity}', '{"name":"a","name":"b"}']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                strict_json(text)

    def test_syntax_does_not_claim_eligibility_or_content_agreement(self):
        result = validate_structured_data({'@context': 'https://schema.org', '@type': 'Product', 'name': 'Example'})
        self.assertEqual(result['content_agreement'], 'unverified')
        self.assertIn('No schema.org vocabulary or current Google eligibility', ' '.join(result['limitations']))

    def test_visible_fact_mismatch_has_a_locator(self):
        facts = {'checks': [{'pointer': '/offers/price', 'expected': '19.00', 'evidence': 'page.html visible price'}]}
        result = validate_structured_data({'@type': 'Product', 'offers': {'@type': 'Offer', 'price': '29.00'}}, facts)
        self.assertEqual(result['findings'][0]['code'], 'visible_fact_mismatch')
        self.assertFalse(result['visible_fact_checks'][0]['agrees_with_supplied_fact'])

    def test_fact_check_requires_evidence_and_existing_pointer(self):
        for check in [{'pointer': '/name', 'expected': 'A'}, {'pointer': '/missing', 'expected': 'A', 'evidence': 'page'}]:
            with self.subTest(check=check), self.assertRaises(ValueError):
                validate_structured_data({'name': 'A'}, {'checks': [check]})

    def test_declared_rating_scale_and_numeric_counts(self):
        result = validate_structured_data({'@type': 'AggregateRating', 'ratingValue': 6,
                                          'worstRating': 1, 'bestRating': 5, 'ratingCount': 1.5})
        codes = {x['code'] for x in result['findings']}
        self.assertTrue({'invalid_numeric_value', 'rating_outside_declared_scale'} <= codes)

    def test_pointer_escaping_and_type_validation(self):
        self.assertEqual(pointer_value({'a/b': {'~key': 7}}, '/a~1b/~0key'), 7)
        with self.assertRaises(ValueError):
            pointer_value([1], '/00')
        with self.assertRaises(ValueError):
            validate_structured_data({'@type': None})


if __name__ == '__main__':
    unittest.main()
