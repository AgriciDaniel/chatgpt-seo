"""Document-title regressions reproduced during the live claude-seo.md audit."""

from pathlib import Path
import sys
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'plugins/ai-marketing-hub-seo/scripts'))
from analyze_html import analyze_html


class SvgDocumentTitleRegressions(unittest.TestCase):
    def inspect(self, head, body):
        return analyze_html('<html><head>' + head + '</head><body><h1>Case study</h1>'
                            + body + '</body></html>', 'https://example.test/case-study')

    def test_svg_accessibility_titles_do_not_duplicate_document_title(self):
        result = self.inspect('<title>Case study</title>',
                              '<svg><title>Clicks chart</title><svg><title>Nested chart</title>'
                              '</svg></svg><svg/><svg><title>Comparison chart</title></svg>')
        self.assertEqual(result['titles'], ['Case study'])
        self.assertNotIn('TITLE_REVIEW', {finding['id'] for finding in result['findings']})

    def test_svg_title_cannot_replace_a_missing_document_title(self):
        result = self.inspect('', '<svg><title>Chart accessibility name</title></svg>')
        self.assertEqual(result['titles'], [])
        self.assertIn('TITLE_REVIEW', {finding['id'] for finding in result['findings']})

    def test_real_duplicate_document_titles_remain_a_finding(self):
        result = self.inspect('<title>First</title><title>Second</title>',
                              '<svg><title>Chart accessibility name</title></svg>')
        self.assertEqual(result['titles'], ['First', 'Second'])
        self.assertIn('TITLE_REVIEW', {finding['id'] for finding in result['findings']})


if __name__ == '__main__':
    unittest.main()
