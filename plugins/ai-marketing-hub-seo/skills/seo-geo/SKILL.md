---
name: seo-geo
description: "Review a site for useful, attributable and accessible answers in AI-search surfaces. Use for GEO, AI Overviews or citation-readiness questions."
license: MIT
---

# AI search visibility

## Input

A site/page and the named AI-search surface or supplied citation observations.

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

- [AI-search evidence and crawler purposes](../../references/search-ai-agentic.md).
- [original contribution and claim support](../../references/content-review.md).

## Workflow

1. Identify the exact surface: Google AI features, ChatGPT Search or another system. Recheck the relevant vendor source before making access or eligibility claims.
2. Audit normal SEO prerequisites, snippet eligibility, crawl access, clear entity attribution, useful answer structure, factual evidence and content that contributes original detail.
3. Separate crawler training policy from search discovery and user-triggered browsing. Inspect robots/WAF evidence before recommending access changes.
4. Use observed citation data only within its recorded prompts, locales and dates. Readiness improvements are hypotheses about usefulness, not measured share of voice.
5. Report llms.txt as optional infrastructure where applicable. Do not assign it Google ranking or citation weight, and do not invent a required AI schema.
6. Propose testable content/access improvements and a repeatable observation plan with specified prompts and source capture.

## Deliverable

An AI-search readiness assessment, evidenced blockers, content improvements and a scoped measurement plan.

## Boundary

Do not promise citations, infer AI traffic from ordinary GSC Web totals, or use a generic GEO score as measured platform visibility.

Adapted from the public [Claude SEO seo-geo workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-geo/SKILL.md).
