"""Compare two supplied HTML inspection snapshots without claiming causation."""

import argparse
import re

from seo_io import read_json, run
from url_values import absolute_url

FIELDS = ('titles', 'descriptions', 'canonicals', 'robots', 'noindex_observed',
          'headings', 'hreflang', 'lang', 'viewport', 'images', 'links', 'json_ld',
          'visible_word_count', 'visible_text_sha256')
CONTROL_FIELDS = {'canonicals', 'robots', 'noindex_observed', 'hreflang'}


def validate_snapshot(value):
    if not isinstance(value, dict) or type(value.get('format_version')) is not int or value['format_version'] != 1 or value.get('evidence_level') != 'source_html':
        raise ValueError('Inputs must be version 1 source_html inspection snapshots')
    absolute_url(value.get('url'))
    if any(key not in value for key in FIELDS):
        raise ValueError('Snapshot is missing required comparison fields')

    def strings(items):
        return isinstance(items, list) and all(isinstance(item, str) for item in items)

    def records(items, checks):
        return isinstance(items, list) and all(isinstance(item, dict) and
                all(key in item and check(item[key]) for key, check in checks.items()) for item in items)

    nullable_text = lambda item: item is None or isinstance(item, str)
    fingerprint = lambda item: isinstance(item, str) and bool(re.fullmatch(r'[0-9a-f]{64}', item))
    valid = all(strings(value[key]) for key in ('titles', 'descriptions', 'canonicals'))
    valid = valid and isinstance(value['robots'], dict) and all(isinstance(key, str) and strings(items) for key, items in value['robots'].items())
    valid = valid and type(value['noindex_observed']) is bool
    valid = valid and records(value['headings'], {'level': lambda item: type(item) is int and 1 <= item <= 6, 'text': lambda item: isinstance(item, str)})
    valid = valid and records(value['hreflang'], {'language': lambda item: isinstance(item, str), 'url': lambda item: isinstance(item, str)})
    valid = valid and nullable_text(value['lang']) and nullable_text(value['viewport'])
    valid = valid and records(value['images'], {'src': lambda item: isinstance(item, str), 'alt': nullable_text,
                'alt_state': lambda item: item in ('missing', 'empty', 'present'), 'has_dimensions': lambda item: type(item) is bool,
                'lazy_method': lambda item: item in ('none', 'native', 'javascript_hint')})
    valid = valid and records(value['links'], {'url': lambda item: isinstance(item, str), 'text': lambda item: isinstance(item, str)})
    valid = valid and records(value['json_ld'], {'parse_status': lambda item: item in ('parsed', 'invalid'),
                'types': strings, 'fingerprint': fingerprint, 'eligibility_validated': lambda item: item is False})
    valid = valid and type(value['visible_word_count']) is int and value['visible_word_count'] >= 0 and fingerprint(value['visible_text_sha256'])
    if not valid:
        raise ValueError('Snapshot comparison fields do not match the HTML inspection output contract')


def compare_snapshots(before, after, allow_url_change=False):
    for value in (before, after):
        validate_snapshot(value)
    url_changed = before['url'] != after['url']
    if url_changed and not allow_url_change:
        raise ValueError('Snapshot URLs differ; use explicit migration mode to compare')
    changes = []
    for field in FIELDS:
        if before[field] == after[field]:
            continue
        control = field in CONTROL_FIELDS
        verification = ('Confirm intended behavior, indexing intent and applicable crawler observations' if control
                        else 'Check the source difference against the intended change and a rendered observation')
        changes.append({'field': field, 'before': before[field], 'after': after[field],
                        'priority': 'high_review' if control else 'review',
                        'verification': verification})
    return {'format_version': 1, 'baseline_url': before['url'], 'current_url': after['url'],
            'url_changed': url_changed, 'changes': changes,
            'limitations': ['Supplied snapshots only', 'Changes do not establish traffic or ranking causation',
                            'No scheduled monitoring or live requests performed']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', help='Baseline inspection JSON')
    parser.add_argument('after', help='Current inspection JSON')
    parser.add_argument('--allow-url-change', action='store_true', help='Explicit migration comparison')
    args = parser.parse_args()
    run(lambda: compare_snapshots(read_json(args.before), read_json(args.after), args.allow_url_change))


if __name__ == '__main__':
    main()
