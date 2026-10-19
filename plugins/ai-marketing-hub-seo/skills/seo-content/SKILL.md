---
name: seo-content
description: "Assess a draft or page for usefulness, search intent, factual support and experience/expertise signals. Use for SEO content audits or revisions."
license: MIT
---

# Content quality

## Input

The actual content and its audience, goal and sources when provided.

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

- [editorial and factual review](../../references/content-review.md).
- [section purpose](../../references/page-type-briefs.md).

## Workflow

1. Read the main content, distinguish it from navigation and boilerplate, and identify the task a visitor should complete.
2. Evaluate who created it, how claims can be checked, why it exists, and which original examples, methods or experiences improve the answer.
3. Find unsupported statistics, vague expertise claims, stale prices or policies, and contradictions. Verify volatile claims against primary sources or mark them unresolved.
4. Assess completeness against the task and observed search intent. Do not use a universal word-count minimum, keyword-density target or AI detector as a quality verdict.
5. Propose the smallest useful improvements: source-backed passages, a clearer structure, evidence or examples, author accountability, and natural internal links.
6. When rewriting, retain the user's product facts and voice. Flag missing facts instead of inventing testimonials, experience or credentials.

## Deliverable

A content diagnosis, a claim/evidence ledger and an edit plan. Supply the revised content only when requested, with unresolved facts clearly identified.

## Boundary

E-E-A-T is a review framework here, not a directly measured ranking score. Originality claims require comparison evidence.

Adapted from the public [Claude SEO seo-content workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-content/SKILL.md).
