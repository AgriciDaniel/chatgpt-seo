---
name: seo-audit
description: "Audit a website for SEO problems and prioritize a practical fix plan. Use for whole-site audits or a broad request to improve a site."
license: MIT
---

# Website SEO audit

## Input

A site URL or a supplied crawl. Use any stated business goal, market and page inventory.

## Evidence and runtime

Read [the operating contract](../../references/operating-contract.md) when this
workflow is selected. Use [runtime and data paths](../../references/runtime-and-data.md)
when choosing a tool or handling missing data. Recheck relevant
[search facts and primary sources](../../references/current-search-facts.md)
before date-sensitive claims. For a quantitative diagnostic, read
[scoring](../../references/scoring.md); unavailable categories stay unknown.

## Supporting resources

Read only the resources needed for the selected part of this task:

- [technical coverage](../../references/technical-checks.md).
- [editorial checks](../../references/content-review.md).
- [markup decisions](../../references/schema-decisions.md).

## Workflow

1. Start with the homepage and detect the page families that support the business: products, services, locations, articles, documentation or landing pages.
2. Discover a bounded representative sample using available links, sitemap entries or a supplied crawl. Record discovery method, visited URLs and failed requests. A suggested first pass is the homepage and one or two pages from each material family; state the sampling limit.
3. Inspect technical controls, intent and content quality, metadata and internal links, structured data, performance evidence, image purpose and AI-search accessibility. Use narrow bundled skills only for the relevant depth.
4. Identify repeated template defects separately from individual-page issues. Confirm an apparent indexing blocker is unintended before escalating it.
5. Synthesize findings into a dependency sequence: verified blockers first, then important templates/pages, then measurable content and search-experience improvements.
6. Read the scoring reference if a score is useful. With unavailable field/lab performance or other category evidence, withhold the overall score and show coverage.

## Deliverable

A report using ../../assets/audit-template.md, an evidence ledger, and a fix backlog with owner role, dependency, effort assumption and success check. Produce files when the host supports them.

## Boundary

Do not claim a complete crawl, actual index status, measured CWV or traffic growth without the corresponding evidence.

Adapted from the public [Claude SEO seo-audit workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-audit/SKILL.md).
