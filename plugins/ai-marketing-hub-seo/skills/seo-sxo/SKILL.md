---
name: seo-sxo
description: "Assess whether a page satisfies searcher intent and supports the next useful task. Use for SXO, page-type mismatch or search journey reviews."
license: MIT
---

# Search experience

## Input

A query/audience and page, plus observed search examples or funnel evidence if available.

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

- [taxonomy, persona and task fit](../../references/sxo-method.md).
- [conversion review templates](../../references/flow-library.md).

- [search experience worksheet](../../assets/sxo-review.md).

## Workflow

1. Classify the page's actual task and observed result types. Keep search sampling, locale and date explicit.
2. Write concrete user stories from evidence: what a searcher needs to learn, compare, evaluate or do. Label inferred personas as hypotheses.
3. Assess the first-screen promise, answer finding, navigation, decision information, trust evidence and task completion path.
4. Use rendered and keyboard observations for interaction claims. A screenshot can reveal layout but not prove a form, checkout or accessibility works.
5. Connect each friction point to an observed step and give a specific copy/layout/content improvement.
6. Define a measurement or usability check with a success criterion. Keep any SXO rubric distinct from the SEO health score.

## Deliverable

A search-to-task diagnosis, observed frictions, user-story improvements and an experiment/retest plan.

## Boundary

Do not invent conversion rates, persona research, behavioral tests or a quantitative uplift.

Adapted from the public [Claude SEO seo-sxo workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-sxo/SKILL.md).
