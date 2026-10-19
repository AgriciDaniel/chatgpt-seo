"""Calculate scoped metrics from one supplied Google Search Console CSV."""

import argparse
import csv
import io
import math
import re
from datetime import date
from decimal import Decimal, InvalidOperation

from seo_io import read_json, read_text, run

ALIASES = {'top pages': 'page', 'pages': 'page', 'url': 'page', 'top queries': 'query',
           'queries': 'query', 'dates': 'date', 'average position': 'position',
           'search appearance': 'search_appearance'}
DIMENSIONS = ('page', 'query', 'date', 'device', 'country', 'search_appearance')
MAX_COUNT = 2**53 - 1
MAX_FIELD_CHARACTERS = 128 * 1024


def integer(value, field, row):
    value = (value or '').strip()
    if not re.fullmatch(r'(?:\d+|\d{1,3}(?:,\d{3})+)', value):
        raise ValueError(f'Row {row}: {field} must be a nonnegative integer count')
    digits = value.replace(',', '').lstrip('0') or '0'
    if len(digits) > 16 or int(digits) > MAX_COUNT:
        raise ValueError(f'Row {row}: {field} exceeds the helper exact-count limit of {MAX_COUNT}')
    return int(digits)


def position_value(value, row):
    try:
        number = Decimal((value or '').strip())
        converted = float(number)
        if not number.is_finite() or number < 0 or not math.isfinite(converted) or Decimal(str(converted)) != number:
            raise ValueError
        return number
    except (InvalidOperation, ValueError):
        raise ValueError(f'Row {row}: position must be a finite nonnegative number within supported decimal precision') from None


def validate_metadata(metadata):
    if metadata is None:
        return None
    allowed = {'property', 'start_date', 'end_date', 'timezone', 'search_type',
               'country', 'device', 'filters', 'completeness', 'source'}
    if not isinstance(metadata, dict) or set(metadata) - allowed:
        raise ValueError('Scope metadata contains unsupported fields')
    for field, value in metadata.items():
        if field == 'filters':
            if not isinstance(value, dict) or set(value) - set(DIMENSIONS) or any(not isinstance(v, str) for v in value.values()):
                raise ValueError('Scope filters must be a string-to-string object')
        elif not isinstance(value, str) or not value.strip():
            raise ValueError(f'Scope {field} must be nonempty text')
    for field in ('start_date', 'end_date'):
        if field in metadata:
            try:
                date.fromisoformat(metadata[field])
            except ValueError:
                raise ValueError(f'Scope {field} must be a valid ISO date') from None
    if 'start_date' in metadata and 'end_date' in metadata and date.fromisoformat(metadata['start_date']) > date.fromisoformat(metadata['end_date']):
        raise ValueError('Scope date range is reversed')
    return metadata.copy()


def analyze_gsc_csv(text, metadata=None):
    metadata = validate_metadata(metadata)
    csv.field_size_limit(MAX_FIELD_CHARACTERS)
    reader = csv.DictReader(io.StringIO(text.lstrip('\ufeff'), newline=''))
    if not reader.fieldnames:
        raise ValueError('CSV has no header')
    headers = [ALIASES.get(x.strip().lower(), x.strip().lower()) for x in reader.fieldnames]
    if len(headers) != len(set(headers)):
        raise ValueError('CSV has duplicate or conflicting column names')
    if not {'clicks', 'impressions', 'position'} <= set(headers):
        raise ValueError('CSV requires clicks, impressions and position columns')
    dimensions = [key for key in DIMENSIONS if key in headers]
    if not dimensions:
        raise ValueError('CSV requires at least one supported dimension column')
    rows, seen = [], set()
    total_clicks = total_impressions = 0
    position_numerator = Decimal(0)
    dates = []
    for row_number, raw in enumerate(reader, 2):
        if None in raw or any(value is None for value in raw.values()):
            raise ValueError(f'Row {row_number}: CSV column count does not match the header')
        values = {headers[i]: raw[original].strip() for i, original in enumerate(reader.fieldnames)}
        if any(not values[key] for key in dimensions):
            raise ValueError(f'Row {row_number}: a dimension value is missing')
        key = tuple(values[field] for field in dimensions)
        if key in seen:
            raise ValueError(f'Row {row_number}: duplicate dimension key; aggregation needs clarification')
        seen.add(key)
        clicks = integer(values['clicks'], 'clicks', row_number)
        impressions = integer(values['impressions'], 'impressions', row_number)
        position = position_value(values['position'], row_number)
        if clicks and not impressions:
            raise ValueError(f'Row {row_number}: clicks with zero impressions need source clarification')
        if impressions and not position:
            raise ValueError(f'Row {row_number}: positive impressions require an observed positive position')
        if 'date' in dimensions:
            try:
                dates.append(date.fromisoformat(values['date']))
            except ValueError:
                raise ValueError(f'Row {row_number}: date must be a valid ISO calendar date') from None
        total_clicks += clicks
        total_impressions += impressions
        position_numerator += position * impressions
        rows.append({**{field: values[field] for field in dimensions}, 'source_csv_row': row_number,
                     'clicks': clicks, 'impressions': impressions, 'position': float(position),
                     'ctr_percent': round(clicks / impressions * 100, 4) if impressions else None})
    if not rows:
        raise ValueError('CSV contains no data rows')
    if metadata and dates:
        if metadata.get('start_date') and min(dates) < date.fromisoformat(metadata['start_date']):
            raise ValueError('CSV dates precede the supplied scope range')
        if metadata.get('end_date') and max(dates) > date.fromisoformat(metadata['end_date']):
            raise ValueError('CSV dates exceed the supplied scope range')
    totals = {'clicks': total_clicks, 'impressions': total_impressions,
              'ctr_percent': round(total_clicks / total_impressions * 100, 4) if total_impressions else None,
              'impression_weighted_position': round(float(position_numerator / total_impressions), 4) if total_impressions else None}
    return {'format_version': 1, 'evidence_level': 'supplied_gsc_csv', 'row_count': len(rows),
            'dimensions': dimensions, 'totals': totals, 'rows': rows,
            'observed_date_range': [min(dates).isoformat(), max(dates).isoformat()] if dates else None,
            'supplied_scope': metadata, 'scope_verification': 'supplied_not_independently_checked' if metadata else 'unknown',
            'review_candidates_by_impressions': sorted((row for row in rows if row['impressions'] > 0), key=lambda x: x['impressions'], reverse=True)[:10],
            'limitations': ['Totals describe supplied rows, not guaranteed property totals',
                            'Property, filters, report completeness and timezone require source context',
                            'CTR is computed from counts, not averaged from row percentages',
                            'Each CSV field is limited to 128 KiB of characters; each count is at most 2**53-1',
                            'No causal, ranking, lead or revenue conclusion is calculated']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='Explicitly selected UTF-8 comma-delimited GSC export, up to 10 MiB')
    parser.add_argument('--metadata', help='Optional selected property/date/filter metadata JSON')
    args = parser.parse_args()
    run(lambda: analyze_gsc_csv(read_text(args.file), read_json(args.metadata) if args.metadata else None))


if __name__ == '__main__':
    main()
