---
name: seo-hreflang
description: "Inspect or generate hreflang and localized-page mappings. Use for international SEO, multilingual or multi-region search tasks."
license: MIT
---

# International SEO

## Input

Known equivalent URLs, source/head links, HTTP Link headers or a localized sitemap.

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

- [locale, parity and annotation decisions](../../references/international-ecommerce.md).
- [offline annotation checks](../../references/dataset-contracts.md).

## Workflow

1. Map actual equivalent content across locales. Distinguish translation, script, region/currency and materially different offers.
2. Check supported language/script/region codes using current Google documentation, full URLs, self references and reciprocal alternate links.
3. Review canonicals, redirects and index controls together with the alternate set. Do not consolidate genuine translations to the source-language canonical.
4. Use x-default when an actual selector/fallback purpose exists; absence alone is not an indexing blocker.
5. Generate consistent HTML, HTTP-header or sitemap annotations for the known set. Missing counterparts remain a coverage gap.
6. Assess translated content quality, user task, local factual differences and crawlable locale navigation. Hreflang is a hint, not a guarantee.

## Deliverable

An alternate-URL matrix, evidenced annotation errors, corrected markup and a reciprocal-validation plan.

## Boundary

Do not invent country variants, assume every page exists or recommend the removed GSC country-targeting setting.

Adapted from the public [Claude SEO seo-hreflang workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-hreflang/SKILL.md).
