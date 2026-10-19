# Offline helper input contracts

Use explicitly selected files. If converting a supplied CSV/export to these
JSON structures, preserve source rows and record the field mapping. Do not
invent missing status, canonical, indexability, target or visible facts.
Helpers read bounded inputs and emit JSON; none fetches URLs or sends data.
JSON inputs reject duplicate properties, nonfinite numbers and decimal values
that would lose supplied digits when converted to a supported JSON float.
Use exact strings only where the relevant schema allows them. Visible-fact
comparisons preserve JSON categories recursively, including boolean versus
number. Numerically equal integer and decimal representations agree, while
numeric strings remain distinct from numbers. Fact pointers use standard
`~0` and `~1` escapes and ASCII, non-padded array indices.

## Crawl sample

[Example input](../assets/crawl-evidence.json) is for
[analyze_crawl.py](../scripts/analyze_crawl.py). `pages` is a nonempty array
with absolute `url`. Optional `status` is an observed HTTP integer or null;
`indexable` is a supplied boolean or null; `canonical` and `links` are supplied
URLs; `title` is supplied text. `scope`, `start_url` and `sitemap_urls` describe
only the selected evidence. A computed sample depth is not full-site depth.
URL comparison keys normalize scheme and hostname case and default ports,
omit fragments, and preserve path and query case. Outputs retain supplied URL
values with their source indices.
Optional `canonical` and `start_url` accept a supported URL or null, not
boolean values, empty strings or other absence coercions.

## Hreflang annotations

[Example input](../assets/hreflang-evidence.json) is for
[validate_hreflang.py](../scripts/validate_hreflang.py). Each annotation has
absolute `source_url`, `language` and absolute `target_url`. Preserve the
implementation method and source locator in the handoff. The helper checks
observed reciprocity and syntax; complete locale validation still needs the
registry, target responses and intended equivalent-page facts.
Its `cluster_consistency_scope` is `observed_pairs_only`. An empty finding
list does not validate a complete connected cluster or identical locale sets.

## Structured data facts

[Example facts](../assets/schema-facts.json) are for
[validate_structured_data.py](../scripts/validate_structured_data.py) with
`--facts`. Supply a separate JSON-LD file. Each fact check has a JSON `pointer`,
an `expected` value with the same intended type, and an `evidence` locator for
the visible/source fact. The helper compares selected fields only and cannot
authenticate review evidence or establish rich-result eligibility.

## Image metadata

[inspect_image.py](../scripts/inspect_image.py) reads selected PNG/JPEG/GIF
headers and actual file bytes. Unsupported formats need a suitable host tool.
It does not decode pixels, optimize files or establish transparency of actual
pixels. Use native generation/editing for requested raster creation.

## Search Console scope sidecar

The GSC helper accepts `--metadata <selected-scope.json>` with optional property,
start_date, end_date, timezone, search_type, country, device, filters, completeness
and source. Values are nonempty strings; filters map supported dimension names
to strings. Dates must be valid and ordered; dated CSV rows outside the supplied
range are rejected. This metadata remains supplied context, not verified live
account access or proof that the export is complete. Without dates in the CSV,
a supplied date range cannot independently establish a daily observation.
CSV fields are limited to 128 KiB of characters. Each click or impression count
must be no greater than `2**53-1`. Out-of-range, malformed or oversized input
returns an unavailable result rather than a partial report.
Position values must retain their supplied decimal digits in the supported
finite float representation; overflow, underflow and precision loss are
rejected before metrics are calculated.

## Before/after inspections

[compare_snapshots.py](../scripts/compare_snapshots.py) accepts version 1
`source_html` outputs from [analyze_html.py](../scripts/analyze_html.py).
It validates the page URL, comparison-field types and content fingerprints.
Null arrays, boolean versions, missing text hashes and malformed source
records cannot establish an unchanged page. Valid identical snapshots mean
only that the compared supplied fields agree, not that the live site is stable.
