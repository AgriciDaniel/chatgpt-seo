---
name: seo-ecommerce
description: "Audit product and category pages for discoverability, buyer information, variants and truthful structured data. Use for ecommerce SEO."
license: MIT
---

# Ecommerce SEO

## Input

Product/category pages, catalog data or a crawl and verified product facts.

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

- [product, category, facets and commerce evidence](../../references/international-ecommerce.md).
- [offer/variant facts](../../references/schema-decisions.md).

## Workflow

1. Distinguish product, variant, category and filtered/paginated page families. Review how buyers and crawlers reach meaningful products.
2. Check unique decision information, availability and prices, currency, shipping/return facts and image context from actual visible or supplied data.
3. Inspect variant canonical decisions and Product/ProductGroup/Offer relationships using current Google feature documentation. Do not invent identifiers, offers or review ratings.
4. Review faceted navigation and pagination by the value of each state. Avoid a blanket canonical-to-category policy for distinct useful pages.
5. Separate website findings from Merchant Center, shopping/marketplace intelligence or commerce-protocol evidence. Those need their own authorized source.
6. Prioritize a representative product/category template fix, inventory consistency checks and a measurable search-to-purchase journey improvement.

## Deliverable

A template/page findings report, variant/index decisions, product-fact gaps and any requested truthful JSON-LD draft.

## Boundary

Do not claim feed eligibility, marketplace rank, UCP support or working checkout from page HTML. No commerce/provider integration is bundled.

Adapted from the public [Claude SEO seo-ecommerce workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-ecommerce/SKILL.md).
