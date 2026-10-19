---
name: seo-maps
description: "Analyze supplied geographic rank grids, business profiles, reviews and local competitor observations. Use for Maps intelligence."
license: MIT
---

# Maps analysis

## Input

A geo-grid export or sourced profile/review observations, including query, center/area, spacing, dates and rank cap where available.

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

- [profile evidence and grid denominators](../../references/maps-checks.md).

- [local-grid worksheet](../../assets/local-grid-review.md).

## Workflow

1. Read the data scope before interpreting rank. Keep keyword, place, grid, device and collection date together; do not equate a single search with regional coverage.
2. For a supplied grid, identify valid cells, unobserved cells and explicit not-ranked observations. Keep missing cells out of fabricated ranks and make the denominator visible.
3. Use a declared visibility definition such as the share of measured cells ranked in the top three. Report missing scheduled-cell coverage alongside it and specify any weighting.
4. Compare business/profile facts and actual nearby competitors within the observed sample. Do not infer reviews are fake from a simple anomaly.
5. Summarize review themes with citations or row references, distinguishing counts, representative examples and interpretation.
6. Create a map/table when tools support it, then give a locally grounded action plan. A new paid grid requires explicitly approved query scope and budget.

## Deliverable

A measured coverage summary, geographic visibility table/map, review themes and local actions with the collection limits stated.

## Boundary

No live geo-grid provider is bundled. Web search cannot supply a fabricated grid or claim Google Maps API authorization.

Adapted from the public [Claude SEO seo-maps workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-maps/SKILL.md).
