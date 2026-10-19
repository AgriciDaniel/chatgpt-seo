---
name: seo-content-brief
description: "Create an SEO writing brief or outline from a topic, audience and available search evidence. Use for content briefs before writing."
license: MIT
---

# SEO content brief

## Input

A topic or query and the intended site/audience. A URL is helpful but not required for a new-site brief.

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

- [page-type outlines](../../references/page-type-briefs.md).
- [claim requirements](../../references/content-review.md).

## Workflow

1. Define the page type and primary intent before drafting the outline. State locale assumptions and whether live search was inspected.
2. Review available search results as an intent sample. Include forums, video, reference pages or marketplaces when they reveal what searchers need; do not automatically discard them as irrelevant competitors.
3. Separate measured keyword data from brainstormed candidates. Never invent search volume, difficulty or a top-ten ranking sample.
4. Design an outline around useful questions, evidence gaps and original contributions. Map each important claim to a source or a fact the writer must obtain.
5. Specify internal link opportunities from real known URLs, suitable metadata drafts, visual ideas and any relevant schema after checking eligibility.
6. Provide acceptance criteria: reader task completed, claims supported, known facts retained, useful differentiation and a clear next action.

## Deliverable

A writer-ready brief with intent, evidence scope, outline, primary/supporting topics, unique contribution, fact requirements and internal links. For outline-only requests keep it short.

## Boundary

A keyword list without SERP data is a planning hypothesis. The brief does not promise rankings or require a particular word count.

Adapted from the public [Claude SEO seo-content-brief workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-content-brief/SKILL.md).
