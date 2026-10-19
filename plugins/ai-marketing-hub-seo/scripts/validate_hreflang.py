"""Check syntax, self references and reciprocity in supplied hreflang rows."""

import argparse
import re
from collections import defaultdict

from seo_io import read_json, run
from url_values import absolute_url

TAG = re.compile(r'^(?:x-default|[a-z]{2}(?:-[a-z]{4})?(?:-[a-z]{2})?)$', re.I)


def validate_hreflang(data):
    rows = data.get('annotations') if isinstance(data, dict) else None
    if not isinstance(rows, list) or not rows or len(rows) > 50000:
        raise ValueError('Input requires 1 to 50000 annotations')
    clusters, findings, url_keys = defaultdict(dict), [], []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f'Annotation {index}: expected an object')
        source, target = absolute_url(row.get('source_url')), absolute_url(row.get('target_url'))
        url_keys.append({'row': index, 'supplied_source_url': row['source_url'], 'supplied_target_url': row['target_url'],
                         'comparison_source_url': source, 'comparison_target_url': target})
        tag = row.get('language')
        if not isinstance(tag, str) or not TAG.fullmatch(tag):
            findings.append({'code': 'invalid_language_tag_syntax', 'row': index, 'value': tag})
            continue
        tag = tag.lower()
        if tag in clusters[source]:
            findings.append({'code': 'duplicate_annotation' if clusters[source][tag] == target else 'conflicting_language_target',
                             'row': index, 'source_url': source, 'language': tag})
        else:
            clusters[source][tag] = target
    unknown = []
    for source, mapping in clusters.items():
        if source not in mapping.values():
            findings.append({'code': 'missing_self_reference_in_supplied_rows', 'source_url': source})
        for tag, target in mapping.items():
            if target not in clusters:
                unknown.append({'source_url': source, 'target_url': target})
            elif source not in clusters[target].values():
                findings.append({'code': 'missing_reciprocal_in_supplied_rows', 'source_url': source, 'target_url': target})
            elif clusters[target].get(tag) != target:
                findings.append({'code': 'inconsistent_cluster_mapping', 'source_url': source,
                                 'target_url': target, 'language': tag})
    return {'format_version': 1, 'evidence_level': 'supplied_annotations', 'row_count': len(rows),
            'source_count': len(clusters), 'findings': findings, 'reciprocity_unknown': unknown,
            'cluster_consistency_scope': 'observed_pairs_only',
            'url_keys': url_keys,
            'limitations': ['Comparison URLs normalize scheme and hostname case and default ports, omit fragments and preserve path/query case',
                            'Language/region syntax is checked, not ISO registry membership',
                            'Annotations missing from this sample may exist in another implementation method',
                            'Complete connected-cluster locale-set consistency is not checked; no findings does not prove a complete cluster',
                            'Targets were not fetched; HTTP status, canonical and indexability are unknown',
                            'Translation quality, locale suitability and search outcomes are not measured']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='Selected annotations JSON, up to 10 MiB')
    args = parser.parse_args()
    run(lambda: validate_hreflang(read_json(args.file)))


if __name__ == '__main__':
    main()
