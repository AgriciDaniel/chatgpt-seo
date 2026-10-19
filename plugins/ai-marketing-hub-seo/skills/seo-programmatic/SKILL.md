---
name: seo-programmatic
description: "Evaluate or design data-driven page families for useful differentiation, index management and scalable quality. Use for programmatic SEO."
license: MIT
---

# Programmatic SEO

## Input

A dataset, template, representative pages or proposed URL family.

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

- [scaled-content pilot and utility](../../references/content-review.md).
- [architecture choices](../../references/strategy-archetypes.md).
- [template controls](../../references/technical-checks.md).

## Workflow

1. Inspect the dataset's grain, keys, duplicates, missingness, freshness and licensing. Match each proposed page to a distinct useful task.
2. Evaluate actual differentiating content, evidence and functionality beyond swapping a city, product or keyword. Sample both rich and sparse rows.
3. Design stable unique URLs, useful hubs, related links, breadcrumbs and explicit handling of empty or low-value records.
4. Review canonical/noindex decisions for true duplicates and faceted or paginated cases. Do not automatically noindex or canonicalize distinct useful pages.
5. Define row-level content acceptance and a representative human review sample. For a small pilot, measure rendering, crawl behavior and indexing evidence before scaling.
6. Check current scaled-content and site-reputation policies. Treat uniqueness percentages, batch sizes and word counts as internal review choices, not Google rules.

## Deliverable

A data/template diagnosis, pilot architecture, row-level acceptance criteria, index-management plan and measurable expansion decision.

## Boundary

Do not generate fake location presence, product facts or mass pages with no standalone value. A quality plan does not authorize publication.

Adapted from the public [Claude SEO seo-programmatic workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-programmatic/SKILL.md).
