---
name: seo-backlinks
description: "Analyze a supplied backlink profile or verified link sample for coverage, quality, anchors and opportunities. Use for backlink audits."
license: MIT
---

# Backlink analysis

## Input

A link export or explicitly inspected links with provider, dates and fields.

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

- [link context and compatible comparisons](../../references/backlinks-clusters.md).

## Workflow

1. Identify the dataset scope and provider completeness. Normalize source/target URLs, domain grain, link status, rel attributes and dates without mixing unlike metrics.
2. Separate links, referring pages and referring domains. Keep new/lost link labels within the provider's measured observation dates.
3. Assess relevance, real editorial context, anchor distribution and destination fit from available evidence. Domain authority and spam scores are vendor metrics, not Google values.
4. Verify a link remains present only when its source page was actually inspected. A provider export by itself does not prove current status.
5. Treat suspicious patterns as review signals. Do not declare a link toxic or propose disavow solely because of low authority, a TLD or one anomaly.
6. Give evidence-backed opportunities, repair candidates and validation priorities. Before any disavow proposal, obtain relevant manual-action or manipulative-link evidence and explain the risk.

## Deliverable

A profile/scope summary, anchor and domain breakdown, a cited issue list and a concrete verification/opportunity backlog.

## Boundary

Do not invent profile completeness, backlink scores or competitor gaps from a handful of search results. No outreach or disavow upload is authorized by analysis.

Adapted from the public [Claude SEO seo-backlinks workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-backlinks/SKILL.md).
