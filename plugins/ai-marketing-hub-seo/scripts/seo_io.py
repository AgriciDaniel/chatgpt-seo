"""Bounded offline input and JSON output for the packaged SEO helpers."""

import csv
import json
import math
import sys
from decimal import Decimal
from pathlib import Path


def read_bytes(path, limit=10 * 1024 * 1024):
    with Path(path).open('rb') as handle:
        value = handle.read(limit + 1)
    if len(value) > limit:
        raise ValueError('Input exceeds the helper size limit')
    return value


def read_text(path):
    return read_bytes(path).decode('utf-8-sig')


def read_json(path):
    return strict_json(read_text(path))


def strict_json(text):
    def invalid(value):
        raise ValueError(f'Nonstandard JSON constant: {value}')

    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f'Duplicate JSON property: {key}')
            value[key] = item
        return value

    def exact_float(raw):
        try:
            value = float(raw)
            exact = math.isfinite(value) and Decimal(raw) == Decimal(str(value))
        except (ArithmeticError, ValueError):
            exact = False
        if not exact:
            raise ValueError('JSON number exceeds supported finite decimal precision; supply an exact string where the schema permits')
        return value

    return json.loads(text, parse_constant=invalid, parse_float=exact_float, object_pairs_hook=unique)


def emit(value):
    print(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False))


def run(action):
    try:
        emit(action())
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, csv.Error, ArithmeticError, RecursionError) as error:
        emit({'error': str(error), 'result_status': 'unavailable'})
        sys.exit(2)
