"""Check supplied JSON-LD syntax and agreement with explicit visible-fact checks."""

import argparse
import re
from decimal import Decimal, InvalidOperation

from seo_io import read_text, run, strict_json


def same_json_value(observed, expected):
    if type(observed) in (int, float) and type(expected) in (int, float):
        return Decimal(str(observed)) == Decimal(str(expected))
    if type(observed) is not type(expected):
        return False
    if isinstance(observed, dict):
        return observed.keys() == expected.keys() and all(same_json_value(value, expected[key]) for key, value in observed.items())
    if isinstance(observed, list):
        return len(observed) == len(expected) and all(same_json_value(a, b) for a, b in zip(observed, expected))
    return observed == expected


def pointer_value(value, pointer):
    if pointer == '':
        return value
    if not isinstance(pointer, str) or not pointer.startswith('/'):
        raise ValueError('A fact check needs a JSON pointer')
    for raw in pointer[1:].split('/'):
        if re.search(r'~(?![01])', raw):
            raise ValueError('A fact check contains an invalid JSON pointer escape')
        part = raw.replace('~1', '/').replace('~0', '~')
        try:
            if isinstance(value, list):
                if not re.fullmatch(r'0|[1-9][0-9]*', part):
                    raise KeyError(part)
                value = value[int(part)]
            elif isinstance(value, dict):
                value = value[part]
            else:
                raise KeyError(part)
        except (KeyError, IndexError):
            raise ValueError(f'Fact pointer is missing: {pointer}') from None
    return value


def validate_structured_data(data, facts=None):
    if not isinstance(data, (dict, list)) or not data:
        raise ValueError('JSON-LD must be a nonempty object or array')
    findings, types = [], set()
    pending = [(data, '')]
    while pending:
        value, pointer = pending.pop()
        if isinstance(value, list):
            pending.extend((item, f'{pointer}/{i}') for i, item in enumerate(value))
        elif isinstance(value, dict):
            kind = value.get('@type', [])
            kind = [kind] if isinstance(kind, str) else kind
            if not isinstance(kind, list) or any(not isinstance(x, str) for x in kind):
                raise ValueError(f'Invalid @type at {pointer}')
            types.update(kind)
            for field in ('ratingValue', 'bestRating', 'worstRating', 'price', 'reviewCount', 'ratingCount'):
                if field not in value:
                    continue
                try:
                    number = Decimal(str(value[field]))
                    if not number.is_finite() or number < 0 or isinstance(value[field], bool):
                        raise ValueError
                    if field.endswith('Count') and number != number.to_integral_value():
                        raise ValueError
                except (InvalidOperation, ValueError):
                    findings.append({'code': 'invalid_numeric_value', 'pointer': pointer+'/'+field})
            if all(field in value for field in ('ratingValue', 'bestRating', 'worstRating')):
                try:
                    rating, best, worst = (Decimal(str(value[field])) for field in ('ratingValue', 'bestRating', 'worstRating'))
                    if all(x.is_finite() for x in (rating, best, worst)) and not worst <= rating <= best:
                        findings.append({'code': 'rating_outside_declared_scale', 'pointer': pointer})
                except InvalidOperation:
                    pass
            pending.extend((item, pointer+'/'+key.replace('~', '~0').replace('/', '~1')) for key, item in value.items())
    agreement = []
    if facts is not None:
        checks = facts.get('checks') if isinstance(facts, dict) else None
        if not isinstance(checks, list) or not checks:
            raise ValueError('Visible facts require a nonempty checks array')
        for check in checks:
            if not isinstance(check, dict) or not isinstance(check.get('evidence'), str) or not check['evidence'].strip() or 'expected' not in check:
                raise ValueError('Each visible-fact check needs expected value and a nonempty evidence locator')
            observed = pointer_value(data, check.get('pointer'))
            agrees = same_json_value(observed, check['expected'])
            agreement.append({'pointer': check['pointer'], 'evidence': check['evidence'],
                              'agrees_with_supplied_fact': agrees, 'markup_value': observed, 'supplied_fact': check['expected']})
            if not agrees:
                findings.append({'code': 'visible_fact_mismatch', 'pointer': check['pointer']})
    return {'format_version': 1, 'evidence_level': 'supplied_jsonld_and_optional_fact_ledger',
            'json_syntax': 'passed', 'observed_types': sorted(types), 'findings': findings,
            'visible_fact_checks': agreement, 'content_agreement': 'checked_fields_only' if agreement else 'unverified',
            'limitations': ['No schema.org vocabulary or current Google eligibility validation is performed',
                            'Supplied fact locators are not independently fetched or authenticated',
                            'Unchecked fields and genuine review provenance remain unverified',
                            'Passing syntax or checked facts does not guarantee a rich result']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='Selected JSON-LD document, up to 10 MiB')
    parser.add_argument('--facts', help='Optional selected visible-fact checks JSON')
    args = parser.parse_args()
    run(lambda: validate_structured_data(strict_json(read_text(args.file)),
                                        strict_json(read_text(args.facts)) if args.facts else None))


if __name__ == '__main__':
    main()
