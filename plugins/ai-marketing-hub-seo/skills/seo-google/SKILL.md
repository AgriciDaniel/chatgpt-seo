---
name: seo-google
description: "Interpret Google Search Console, Analytics, PageSpeed or CrUX evidence from exports or authorized read tools. Use for Google SEO metrics."
license: MIT
---

# Google search data

## Input

An explicit property export/tool result, dates, filters and report type.

## Evidence and runtime

If a skill-resource reader fails to open a linked supporting file, try the
available file or execution tool using the installed plugin root returned by
the host or resolved from this skill's location. Do not hardcode a home folder,
version, or working directory. Distinguish a failed reader call from an absent
file, and files actually attempted from files not attempted. Report a resource
as unavailable only after the supported access paths have failed. If no file
or execution access is available, continue within the evidence you can read
and state that limit.

Read [the operating contract](../../references/operating-contract.md) when this
workflow is selected. Use [runtime and data paths](../../references/runtime-and-data.md)
when choosing a tool or handling missing data. Recheck relevant
[search facts and primary sources](../../references/current-search-facts.md)
before date-sensitive claims. For a quantitative diagnostic, read
[scoring](../../references/scoring.md); unavailable categories stay unknown.

## Supporting resources

Read only the resources needed for the selected part of this task:

- [supplied metric interpretation](../../references/data-analysis.md).
- [field versus lab performance evidence](../../references/technical-checks.md).
- [Google performance report template](../../assets/google-performance-report.md).
- [index and discovery report template](../../assets/indexation-report.md).

## Workflow

1. Identify the property, row grain, time window, timezone, search type, device/country filters, aggregation and any provider truncation.
2. Read [data analysis](../../references/data-analysis.md) for metric definitions and comparability checks. When a CSV and Python are available, run [the offline GSC calculator](../../scripts/analyze_gsc.py). Report clicks, impressions and CTR with their denominators; aggregate position with impression weights when that matches the export. The helper's totals cover supplied rows only. Use `--metadata` with a user-supplied property/date/filter sidecar when context is known; it remains supplied scope, not independently verified account access.
3. Compare equal-length periods and segment page/query/device patterns. Keep missing/private queries and reporting lag visible. A traffic drop's timing is not proof of an algorithm cause.
4. For performance data, separate PageSpeed lab runs from CrUX field samples and page-level from origin-level results. Record device and dates.
5. Translate supported patterns into specific page/technical hypotheses and the next check. Keep GSC clicks separate from GA4 sessions and conversions.
6. For inspection or indexing requests, use actual returned status and current API scope. Draft steps rather than running write endpoints without explicit authorization.

## Deliverable

A source-scoped metric readout, segment findings, calculation notes, priorities and a validation plan. Use the linked performance template for a substantial metric report and the index template for URL inspection or discovery evidence.

## Boundary

This package has no Google OAuth integration. Never request a key/token in chat, invent account access, or use the Indexing API for ordinary articles.

Adapted from the public [Claude SEO seo-google workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-google/SKILL.md).
