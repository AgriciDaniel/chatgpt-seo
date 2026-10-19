"""Calculate diagnostic scores while keeping unavailable categories unknown."""

import argparse
import math

from seo_io import read_json, run

WEIGHTS = {'technical': 22, 'content': 23, 'on_page': 20, 'schema': 10,
           'performance': 10, 'ai_search': 10, 'images': 5}


def calculate_scorecard(envelope):
    if not isinstance(envelope, dict) or not isinstance(envelope.get('categories'), dict):
        raise ValueError('Input must contain a categories object')
    categories = envelope['categories']
    if set(categories) - set(WEIGHTS):
        raise ValueError('Unknown scoring category')
    coverage = 0
    earned = 0.0
    unavailable = []
    for key, weight in WEIGHTS.items():
        value = categories.get(key, {'status': 'unavailable'})
        if not isinstance(value, dict):
            raise ValueError(f'{key}: category must be an object')
        status = value.get('status')
        if status == 'unavailable':
            if value.get('score') is not None:
                raise ValueError(f'{key}: unavailable category cannot have a score')
            unavailable.append(key)
            continue
        if status != 'assessed':
            raise ValueError(f'{key}: status must be assessed or unavailable')
        score = value.get('score')
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= score <= 100 or not math.isfinite(score):
            raise ValueError(f'{key}: score must be a finite number between 0 and 100')
        evidence = value.get('evidence')
        if not isinstance(evidence, list) or not evidence or not all(isinstance(x, str) and x.strip() for x in evidence):
            raise ValueError(f'{key}: assessed score requires nonempty evidence locators')
        if not isinstance(value.get('method'), str) or not value['method'].strip():
            raise ValueError(f'{key}: assessed score requires a calculation method')
        coverage += weight
        earned += score * weight / 100
    return {'format_version': 1, 'metric': 'heuristic SEO diagnostic',
            'health_score': round(earned, 2) if coverage == 100 else None,
            'assessed_score': round(earned / coverage * 100, 2) if coverage else None,
            'coverage_percent': coverage, 'unavailable_categories': unavailable,
            'possible_score_range': [round(earned, 2), round(earned + 100 - coverage, 2)],
            'limitations': ['Evidence truth and category applicability require human review',
                            'Not a Google ranking metric or traffic forecast']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='Category evidence JSON')
    args = parser.parse_args()
    run(lambda: calculate_scorecard(read_json(args.file)))


if __name__ == '__main__':
    main()
