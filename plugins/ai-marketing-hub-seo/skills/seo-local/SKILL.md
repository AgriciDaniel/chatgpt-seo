---
name: seo-local
description: "Review local-business visibility signals, service pages, business information and review evidence. Use for local SEO requests."
license: MIT
---

# Local business SEO

## Input

A business URL, public business profile or user-supplied profile/export, and a stated service area if known.

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

- [business-shape and profile checks](../../references/maps-checks.md).
- [local page families](../../references/strategy-archetypes.md).

## Workflow

1. Check whether the business actually serves the claimed locations. Use public business facts without inventing addresses, branches or service areas.
2. Compare name, address/contact facts, opening hours and services across inspected website/profile sources. Redact unrelated personal information.
3. Review profile category fit, completeness, relevant photos and review responses from available evidence. A website-only review cannot establish profile verification or map-pack rank.
4. Assess location/service pages for real local information, original proof and a clear customer task. Avoid doorway pages that merely swap place names.
5. Draft accurate LocalBusiness or appropriate subtype markup only from visible facts after checking current requirements.
6. Use seo-maps for measured geographic rankings. Prioritize factual corrections and useful local content, with a verification step for each.

## Deliverable

A local SEO findings report, consistency table and prioritized website/profile recommendations.

## Boundary

Do not edit a business profile, create reviews, contact directories, promise map-pack placement or apply universal review-count benchmarks.

Adapted from the public [Claude SEO seo-local workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-local/SKILL.md).
