---
name: seo-cluster
description: "Group keywords into useful page targets and an internal-link architecture using intent and available SERP overlap. Use for topic clusters."
license: MIT
---

# Topic clustering

## Input

A seed/topic or keyword inventory, with optional measured SERP results and locale.

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

- [intent, page differentiation and overlap sensitivity](../../references/backlinks-clusters.md).

## Workflow

1. Normalize exact duplicates without erasing distinct intent. Keep measured volume/difficulty separate from generated keyword candidates.
2. Read [clustering](../../references/clustering.md). With measured SERP URLs, compute or explain overlap for a stated locale, date and top-N sample. Without SERPs label the grouping semantic and provisional.
3. Split mismatched intents/page types even when keywords share words. Avoid one page per minor variant and avoid merging distinct customer tasks.
4. Check transitive bridge clusters against a representative page/medoid so an A-B and B-C overlap does not automatically justify A-C consolidation.
5. Map clusters to existing suitable URLs, new page candidates and hub/spoke links. Preserve useful pages; a merge proposal needs content and redirect evidence.
6. Prioritize from business relevance and measured data, or clearly stated assumptions. Produce a map/table when it helps review the architecture.

## Deliverable

A cluster-to-URL table with intent, evidence type, representative keyword, known metrics, link plan and review flags.

## Boundary

Do not claim live SERP overlap or search demand when using semantic grouping alone. Clustering does not authorize content publication or redirects.

Adapted from the public [Claude SEO seo-cluster workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-cluster/SKILL.md).
