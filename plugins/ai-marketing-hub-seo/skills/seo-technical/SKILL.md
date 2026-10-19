---
name: seo-technical
description: "Diagnose crawlability, indexing controls, canonicals, rendering, redirects and performance evidence. Use for technical SEO issues."
license: MIT
---

# Technical SEO

## Input

A site/page URL, crawl export, source snapshot, response headers, or deployment comparison.

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

- [technical and performance evidence](../../references/technical-checks.md).
- [supplied crawl inputs](../../references/dataset-contracts.md).

- [field and lab CWV report template](../../assets/cwv-report.md).

## Workflow

1. Check crawl access and index controls separately. Review robots groups, meta directives and supplied X-Robots-Tag headers without assuming the page should be public.
2. Trace canonical intent, duplicate/parameter URLs, redirects, pagination and sitemap alignment from evidence. Do not canonicalize distinct useful paginated or filtered pages indiscriminately.
3. Compare initial HTML with a rendered observation when available. Identify missing primary content, crawlable links and mobile/desktop parity risks.
4. Use actual response data for status, TLS and redirects. A generic browser error cannot establish a specific HTTP code or WAF cause.
5. Assess LCP, INP and CLS using named field or lab data and the current-search-facts reference. HTML-only performance concerns are hypotheses.
6. Give the smallest fix that addresses the observed defect and the exact post-change check. Review the impact of any robots, noindex or canonical change before applying it.

## Deliverable

A technical findings table, affected templates/URLs, a dependency-ordered patch plan, and verification commands or browser checks supported by the host.

## Boundary

Do not require headless Chromium, invent crawler fetch limits, recommend IndexNow for Google, or submit URLs without explicit authorization.

Adapted from the public [Claude SEO seo-technical workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-technical/SKILL.md).
