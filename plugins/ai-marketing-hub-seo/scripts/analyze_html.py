"""Inspect a supplied HTML snapshot. No network, rendering, or ranking score."""

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

from seo_io import read_text, run, strict_json
from url_values import absolute_url


def clean(value):
    return re.sub(r'\s+', ' ', value).strip()


def fingerprint(value):
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = set()
        self.titles = []
        self.descriptions = []
        self.canonicals = []
        self.hreflang = []
        self.robots = {}
        self.headings = []
        self.images = []
        self.links = []
        self.json_blocks = []
        self.visible = []
        self.base = None
        self.lang = None
        self.viewport = None
        self.captures = []
        self.json_parts = None
        self.suppressed = []
        self.svg_depth = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): v for k, v in attrs}
        self.tags.add(tag)
        if tag in ('script', 'style', 'template', 'noscript'):
            if not self.suppressed and tag == 'script' and (a.get('type') or '').lower().split(';')[0].strip() == 'application/ld+json':
                self.json_parts = []
            self.suppressed.append(tag)
            return
        if self.suppressed:
            return
        if tag == 'svg':
            self.svg_depth += 1
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'base' and not self.base:
            self.base = a.get('href')
        if tag == 'meta':
            name = (a.get('name') or '').lower()
            value = a.get('content') or ''
            if name == 'description':
                self.descriptions.append(clean(value))
            if name in ('robots', 'googlebot', 'bingbot'):
                self.robots.setdefault(name, []).append(clean(value))
            if name == 'viewport':
                self.viewport = value
        if tag == 'link':
            rel = (a.get('rel') or '').lower().split()
            if 'canonical' in rel:
                self.canonicals.append(a.get('href') or '')
            if 'alternate' in rel and a.get('hreflang'):
                self.hreflang.append({'language': a['hreflang'], 'url': a.get('href') or ''})
        if tag == 'img':
            alt = a.get('alt')
            lazy = 'native' if (a.get('loading') or '').lower() == 'lazy' else 'none'
            if lazy == 'none' and (a.get('data-src') or a.get('data-srcset') or
                                   'lazy' in (a.get('class') or '').lower()):
                lazy = 'javascript_hint'
            self.images.append({
                'src': a.get('data-src') or a.get('src') or '',
                'alt': alt,
                'alt_state': 'missing' if 'alt' not in a else ('present' if alt else 'empty'),
                'has_dimensions': bool(a.get('width') and a.get('height')),
                'lazy_method': lazy,
            })
        if tag == 'title' or re.fullmatch(r'h[1-6]', tag) or (tag == 'a' and 'href' in a):
            self.captures.append({'tag': tag, 'parts': [], 'attrs': a,
                                  'svg_title': tag == 'title' and self.svg_depth > 0})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'template', 'noscript'):
            if tag == 'script' and self.json_parts is not None:
                self.json_blocks.append(''.join(self.json_parts))
                self.json_parts = None
            if tag in self.suppressed:
                del self.suppressed[self.suppressed.index(tag):]
            return
        if self.suppressed:
            return
        if tag == 'svg':
            self.svg_depth = max(0, self.svg_depth - 1)
        for index in range(len(self.captures) - 1, -1, -1):
            if self.captures[index]['tag'] != tag:
                continue
            capture = self.captures.pop(index)
            value = clean(''.join(capture['parts']))
            if tag == 'title':
                if not capture['svg_title']:
                    self.titles.append(value)
            elif tag == 'a':
                self.links.append({'url': capture['attrs']['href'] or '', 'text': value})
            else:
                self.headings.append({'level': int(tag[1]), 'text': value})
            break

    def handle_data(self, data):
        if self.json_parts is not None:
            self.json_parts.append(data)
        if self.suppressed:
            return
        for capture in self.captures:
            capture['parts'].append(data)
        if not any(capture['tag'] == 'title' for capture in self.captures):
            self.visible.append(data)


def json_summary(raw):
    try:
        payload = strict_json(raw)
        if not isinstance(payload, (dict, list)):
            raise ValueError('JSON-LD root must be an object or array')
        types = set()

        def walk(value):
            if isinstance(value, dict):
                kind = value.get('@type', [])
                if isinstance(kind, str):
                    types.add(kind)
                elif isinstance(kind, list):
                    types.update(x for x in kind if isinstance(x, str))
                for nested in value.values():
                    walk(nested)
            elif isinstance(value, list):
                for nested in value:
                    walk(nested)

        walk(payload)
        return {'parse_status': 'parsed', 'types': sorted(types),
                'fingerprint': fingerprint(payload), 'eligibility_validated': False}
    except (ValueError, RecursionError) as error:
        message = 'JSON-LD exceeds supported nesting' if isinstance(error, RecursionError) else str(error)
        return {'parse_status': 'invalid', 'error': message, 'types': [],
                'fingerprint': hashlib.sha256(raw.encode()).hexdigest(), 'eligibility_validated': False}


def analyze_html(html, url):
    absolute_url(url)
    parsed = urlsplit(url)
    if not html.strip():
        raise ValueError('Empty input does not establish a page inspection')
    inspector = Inspector()
    inspector.feed(html)
    inspector.close()
    if not inspector.tags.intersection({'html', 'head', 'body', 'main', 'article', 'title', 'h1'}):
        raise ValueError('Input has no supported HTML document or content structure')
    base = urljoin(url, inspector.base or '')
    links = [{**x, 'url': urljoin(base, x['url'])} for x in inspector.links]
    counts = {'internal': 0, 'external': 0, 'other': 0}
    for link in links:
        target = urlsplit(link['url'])
        kind = ('other' if target.scheme not in ('http', 'https') else
                'internal' if target.hostname == parsed.hostname else 'external')
        counts[kind] += 1
    robot_tokens = {token.lower() for values in inspector.robots.values() for value in values
                    for token in re.split(r'[\s,;]+', value)}
    noindex = bool(robot_tokens.intersection({'noindex', 'none'}))
    text = clean(' '.join(inspector.visible))
    findings = []
    evidence_pointers = {
        'TITLE_REVIEW': '/titles', 'DESCRIPTION_REVIEW': '/descriptions',
        'CANONICAL_REVIEW': '/canonicals', 'NOINDEX_REVIEW': '/robots',
        'H1_REVIEW': '/headings', 'SOURCE_CONTENT_UNAVAILABLE': '/visible_word_count',
        'IMAGE_ALT_REVIEW': '/images', 'JSON_LD_SYNTAX': '/json_ld',
    }

    def add(code, severity, observation, verification, **extra):
        findings.append({'id': code, 'severity': severity, 'observation': observation,
                         'verification': verification, 'evidence_level': 'source_html',
                         'affected_url': url, 'evidence_pointer': evidence_pointers[code], **extra})

    if len(inspector.titles) != 1 or not inspector.titles[0]:
        add('TITLE_REVIEW', 'medium', 'A single nonempty title was not observed',
            'Inspect source and rendered document title; create a descriptive title if needed')
    if not inspector.descriptions or not any(inspector.descriptions):
        add('DESCRIPTION_REVIEW', 'medium', 'No nonempty meta description observed',
            'Decide whether an editorial search preview would help this page')
    if len(inspector.canonicals) != 1 or not inspector.canonicals[0]:
        add('CANONICAL_REVIEW', 'medium', 'A single nonempty canonical was not observed',
            'Check header canonicals, duplicate URLs and intended preferred URL before changing tags')
    else:
        try:
            canonical = absolute_url(inspector.canonicals[0], base)
        except ValueError:
            add('CANONICAL_REVIEW', 'medium', 'The supplied canonical is not a supported HTTP(S) URL',
                'Confirm the intended preferred URL and inspect header and rendered canonicals before changing tags',
                intent_confirmation_required=True, supplied_canonical=inspector.canonicals[0])
        else:
            if canonical != absolute_url(url):
                add('CANONICAL_REVIEW', 'medium', 'The source canonical resolves to a different URL',
                    'Confirm canonical intent and equivalent content before changing tags; a non-self canonical may be intentional',
                    intent_confirmation_required=True, supplied_canonical=inspector.canonicals[0], resolved_canonical=canonical)
    if noindex:
        add('NOINDEX_REVIEW', 'high', 'A noindex or none meta directive is present',
            'Confirm indexing intent and inspect response headers and crawler-specific controls',
            intent_confirmation_required=True)
    if len([h for h in inspector.headings if h['level'] == 1]) != 1:
        add('H1_REVIEW', 'info', 'The source does not contain exactly one H1',
            'Review the heading structure for clarity; this is not evidence of a ranking penalty')
    if not text:
        add('SOURCE_CONTENT_UNAVAILABLE', 'high', 'No visible-text heuristic content found in source',
            'Inspect a rendered snapshot before diagnosing an empty page or indexing defect')
    missing_indices = [i for i, image in enumerate(inspector.images) if image['alt_state'] == 'missing']
    if missing_indices:
        pointers = [f'/images/{i}' for i in missing_indices]
        add('IMAGE_ALT_REVIEW', 'medium', f'{len(missing_indices)} image(s) lack an alt attribute',
            'Determine image purpose; describe meaningful images and give decorative images empty alt',
            evidence_pointer=pointers[0], evidence_pointers=pointers)
    blocks = [json_summary(raw) for raw in inspector.json_blocks]
    if any(x['parse_status'] == 'invalid' for x in blocks):
        add('JSON_LD_SYNTAX', 'high', 'At least one JSON-LD block could not be parsed',
            'Repair the JSON and check applicable structured-data requirements and visible facts')
    return {
        'format_version': 1, 'url': url, 'evidence_level': 'source_html',
        'source_sha256': hashlib.sha256(html.encode()).hexdigest(),
        'titles': inspector.titles, 'descriptions': inspector.descriptions,
        'canonicals': [urljoin(base, x) if x else '' for x in inspector.canonicals],
        'robots': inspector.robots, 'noindex_observed': noindex,
        'headings': inspector.headings, 'hreflang': [
            {**x, 'url': urljoin(base, x['url']) if x['url'] else ''} for x in inspector.hreflang],
        'lang': inspector.lang, 'viewport': inspector.viewport,
        'images': [{**x, 'src': urljoin(base, x['src']) if x['src'] else ''} for x in inspector.images],
        'links': links, 'link_counts': counts, 'json_ld': blocks,
        'visible_word_count': len(text.split()),
        'word_count_scope': 'All unsuppressed source text, including incidental or adversarial text; not main-content quality',
        'visible_text_sha256': hashlib.sha256(text.encode()).hexdigest(),
        'findings': findings,
        'measurements': {'http_status': None, 'indexing': None, 'core_web_vitals': None,
                         'rankings': None, 'backlinks': None, 'ai_citations': None},
        'manual_review_required': ['Metadata usefulness', 'Main-content relevance and factual support',
                                   'Image purpose', 'Structured-data eligibility'],
        'limitations': ['Static snapshot only', 'CSS visibility and JavaScript not evaluated',
                        'Links and response headers not checked', 'No overall SEO score'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='Explicitly selected UTF-8 HTML snapshot, up to 10 MiB')
    parser.add_argument('--url', required=True, help='Page URL used only to resolve relative references')
    args = parser.parse_args()
    run(lambda: analyze_html(read_text(args.file), args.url))


if __name__ == '__main__':
    main()
