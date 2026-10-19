---
name: seo-plan
description: "Create an SEO strategy and implementation roadmap around business goals, available evidence and resources. Use for SEO planning."
license: MIT
---

# SEO strategy

## Input

A business model, target audience/market, website if present, and known constraints.

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

- [all six business-model archetypes](../../references/strategy-archetypes.md).
- [page family decisions](../../references/page-type-briefs.md).

- [strategy worksheet](../../assets/strategy-plan.md).

## Workflow

1. Start from the desired business outcome and current evidence. Use explicit assumptions for missing baselines, staffing or budgets rather than manufacturing forecasts.
2. Choose priorities by business type: SaaS tasks and product education, local services and service areas, ecommerce catalogs, publishers' trust and coverage, or agencies' proof and lead journeys.
3. Assess demand and competitive intent from sources that are actually available. Distinguish researched opportunities from unvalidated topic candidates.
4. Design page families, internal-link architecture and content priorities that support the product's real value. Retain existing useful content and contracts.
5. Sequence technical blockers, high-value template changes, evidence-rich content and measurement. Give phased options with effort assumptions and decision-relevant tradeoffs.
6. Define baselines, leading indicators, outcomes and a review cadence. Revenue or traffic targets should be user goals or explicit scenarios, not promised results.

## Deliverable

A strategy, dependency roadmap, content/page priorities and measurement framework. Include what evidence would change the recommendation.

## Boundary

Planning does not authorize publishing, hiring, provider spending or monitoring automation.

Adapted from the public [Claude SEO seo-plan workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-plan/SKILL.md).
