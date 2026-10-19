"""Validate one supplied sitemap XML document without fetching destinations."""

import argparse
import re
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date, datetime
from urllib.parse import urlsplit

from seo_io import read_bytes, run

MAX_BYTES = 50 * 1024 * 1024
NAMESPACE = 'http://www.sitemaps.org/schemas/sitemap/0.9'


def name(tag):
    return tag.rsplit('}', 1)[-1]


def valid_date(value):
    try:
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            date.fromisoformat(value)
            return True
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})', value):
            datetime.fromisoformat(value.replace('Z', '+00:00'))
            return True
    except ValueError:
        pass
    return False


def absolute_web_url(value):
    try:
        p = urlsplit(value)
        p.port
        return (p.scheme in ('http', 'https') and bool(p.hostname) and
                p.username is None and p.password is None and not p.fragment and
                len(value) < 2048 and
                not re.search(r'\s', value))
    except ValueError:
        return False


def validate_sitemap(data):
    if len(data) > MAX_BYTES:
        raise ValueError('Sitemap exceeds the 50 MiB uncompressed helper limit')
    if b'\x00' in data:
        raise ValueError('Sitemap must use UTF-8 encoding')
    text = data.decode('utf-8-sig')
    if re.search(r'<!\s*(?:DOCTYPE|ENTITY)', text, re.I):
        raise ValueError('DTD and entity declarations are not supported')
    try:
        root = ET.fromstring(text)
    except ET.ParseError as error:
        raise ValueError(f'Invalid XML: {error}') from error
    kind = name(root.tag)
    if kind not in ('urlset', 'sitemapindex'):
        raise ValueError('Document root must be urlset or sitemapindex')
    findings = []

    def add(code, severity, observation, verification):
        findings.append({'id': code, 'severity': severity, 'observation': observation,
                         'verification': verification, 'evidence_level': 'supplied_xml'})

    if root.tag != '{'+NAMESPACE+'}'+kind:
        add('NAMESPACE_REVIEW', 'high', 'Standard sitemap namespace is missing or different',
            'Use the sitemap protocol namespace and revalidate the XML')
    expected = 'url' if kind == 'urlset' else 'sitemap'
    entries = [x for x in root if name(x.tag) == expected]
    if len(entries) > 50000:
        add('ENTRY_LIMIT_EXCEEDED', 'high', 'More than 50,000 entries in one document',
            'Split into bounded sitemaps and an index as appropriate')
    if not entries:
        add('NO_ENTRIES', 'medium', 'No expected sitemap entries present',
            'Confirm whether an empty sitemap is intentional')
    if any(name(x.tag) != expected for x in root):
        add('UNEXPECTED_CHILD', 'medium', 'Unexpected root-level XML element present',
            'Check protocol structure and extension namespaces')
    locations, invalid_rows, invalid_dates, namespace_rows = [], [], [], []
    ignored_tag_count = 0
    hosts = set()
    for row, entry in enumerate(entries, 1):
        loc = [x for x in entry if x.tag == '{'+NAMESPACE+'}loc']
        wrong_namespace = entry.tag != '{'+NAMESPACE+'}'+expected
        if not loc and any(name(x.tag) == 'loc' for x in entry):
            wrong_namespace = True
        if wrong_namespace:
            namespace_rows.append(row)
        value = ''.join(loc[0].itertext()).strip() if loc else ''
        locations.append(value)
        if wrong_namespace or len(loc) != 1 or len(loc[0]) or not absolute_web_url(value):
            invalid_rows.append(row)
        elif value:
            hosts.add(urlsplit(value).hostname)
        lastmod = [child for child in entry if child.tag == '{'+NAMESPACE+'}lastmod']
        if len(lastmod) > 1:
            invalid_dates.append(row)
        for child in entry:
            local = name(child.tag)
            if child.tag == '{'+NAMESPACE+'}lastmod' and (len(child) or not valid_date((child.text or '').strip())):
                invalid_dates.append(row)
            if child.tag in ('{'+NAMESPACE+'}priority', '{'+NAMESPACE+'}changefreq'):
                ignored_tag_count += 1
    if namespace_rows:
        add('NAMESPACE_REVIEW', 'high', 'Some entries or required locations use a different or missing protocol namespace',
            'Use namespace-qualified sitemap entries and locations; keep extension elements in their own namespace')
    duplicates = sorted(x for x, count in Counter(locations).items() if x and count > 1)
    if invalid_rows:
        add('LOCATION_INVALID', 'high', f'{len(invalid_rows)} entry row(s) have invalid locations',
            'Provide exactly one absolute HTTP(S) location per entry, without credentials or fragments')
    if duplicates:
        add('LOCATION_DUPLICATE', 'medium', f'{len(duplicates)} repeated location(s)',
            'Deduplicate exact locations and compare canonical equivalents separately')
    if invalid_dates:
        add('LASTMOD_INVALID', 'medium', 'Some lastmod values do not have supported W3C date syntax',
            'Use at most one plain-text accurate modification date per entry; do not use the generation date')
    if ignored_tag_count:
        add('IGNORED_HINTS', 'info', 'priority or changefreq tags are present',
            'Google ignores these hints; focus on accurate locations and lastmod')
    locators = {'LOCATION_INVALID': ('/invalid_location_rows', invalid_rows),
                'LOCATION_DUPLICATE': ('/duplicate_locations', [row for row, value in enumerate(locations, 1) if value in duplicates]),
                'LASTMOD_INVALID': ('/invalid_lastmod_rows', sorted(set(invalid_dates))),
                'NAMESPACE_REVIEW': ('/invalid_namespace_rows' if namespace_rows else '/observed_root_tag', namespace_rows)}
    for finding in findings:
        if finding['id'] in locators:
            pointer, rows = locators[finding['id']]
            finding.update({'evidence_pointer': pointer, 'affected_entry_rows': rows})
    return {'format_version': 1, 'kind': kind, 'observed_root_tag': root.tag, 'entry_count': len(entries),
            'uncompressed_bytes': len(data), 'locations': locations,
            'hosts': sorted(hosts), 'invalid_location_rows': invalid_rows,
            'invalid_namespace_rows': namespace_rows,
            'duplicate_locations': duplicates, 'invalid_lastmod_rows': sorted(set(invalid_dates)),
            'destination_status': None, 'children_fetched': False, 'findings': findings,
            'limitations': ['No destination requests', 'No canonical or indexing checks',
                            'Index children and extension-specific requirements not validated']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='Explicitly selected uncompressed sitemap XML, up to 50 MiB')
    args = parser.parse_args()
    run(lambda: validate_sitemap(read_bytes(args.file, MAX_BYTES)))


if __name__ == '__main__':
    main()
