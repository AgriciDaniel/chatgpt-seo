---
name: seo-competitor-pages
description: "Research and draft fair comparison or alternatives pages with verifiable product facts. Use for competitor comparison page requests."
license: MIT
---

# Comparison pages

## Input

The products, intended audience, comparison criteria and known first-party evidence.

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

- [comparison structure](../../references/page-type-briefs.md).
- [decision criteria](../../references/sxo-method.md).
- [fact and proof requirements](../../references/content-review.md).

## Workflow

1. Choose the comparison intent: direct versus, alternatives or a category shortlist. Specify the user decision the page should support.
   If competitors are unnamed or current sources are unavailable, deliver a provisional comparison against a known category/manual alternative, with explicit missing facts and a research plan. Use the [content-brief worksheet](../../assets/content-brief.md), including its dated fact ledger. Do not invent a competitor.
2. Open current official sources for factual features, limitations and prices. Record date and scope; unknown is not the same as unsupported or absent.
3. Compare equivalent plans and actual user needs. Distinguish facts, tested observations and editorial judgments, and acknowledge competitor strengths.
4. Draft a transparent feature matrix, decision criteria, suitable use cases, limitations and a truthful next action.
5. Never invent ratings, testimonials, trials, discounts, capabilities or benchmarks. Structured data must match the visible page and current eligibility.
6. Supply metadata/internal links grounded in known site structure and a refresh list for volatile claims.

## Deliverable

A sourced comparison brief, matrix or requested draft with a fact ledger and outstanding checks.

## Boundary

Do not claim direct tests were run when only documentation was inspected. Do not misrepresent affiliation or fabricate competitor weaknesses.

Adapted from the public [Claude SEO seo-competitor-pages workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-competitor-pages/SKILL.md).
