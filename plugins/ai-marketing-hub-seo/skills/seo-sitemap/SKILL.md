---
name: seo-sitemap
description: "Validate, analyze or generate XML sitemaps from a supplied document or verified URL inventory. Use for sitemap tasks."
license: MIT
---

# Sitemap review

## Input

A sitemap URL/XML document or an explicit inventory of intended canonical URLs.

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

- [discovery and coverage reconciliation](../../references/technical-checks.md).
- [sitemap versus supplied crawl evidence](../../references/dataset-contracts.md).

## Workflow

1. Discover sitemap candidates from observed robots Sitemap declarations, linked indexes and common paths when browsing can inspect them. A declaration alone is not proof of a working sitemap.
2. Use ../../scripts/validate_sitemap.py when a supplied XML file and Python are available. Record index children that were not fetched.
3. Check protocol namespace, absolute locations, exact duplicates, date syntax, the 50,000-entry and 50 MiB uncompressed limits. Treat priority/changefreq as ignored hints for Google.
4. Join entries with separately measured status, canonical and index-control data. XML by itself cannot establish that entries return 200 or are indexable.
5. Use lastmod only for real significant content changes. Do not refresh every URL date to the current day without evidence.
6. Generate XML from known intended URLs, escaping values and splitting at protocol limits. Keep coverage gaps explicit rather than inventing site URLs.

## Deliverable

A sitemap findings report or generated sitemap/index files with URL count, validation scope and a list of untested destinations.

## Boundary

Cross-host sitemap arrangements can be valid when authorized; investigate their setup. Extension-specific image/video/news requirements need their own current checks.

Adapted from the public [Claude SEO seo-sitemap workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-sitemap/SKILL.md).
