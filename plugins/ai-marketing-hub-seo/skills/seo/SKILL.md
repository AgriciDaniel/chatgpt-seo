---
name: seo
description: "Route a broad SEO request to the relevant audit, strategy or optimization workflow. Use when the SEO goal is not yet specific."
license: MIT
---

# SEO workspace

## Input

A website, page, draft, SEO dataset, or business objective.

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

- [business-model planning](../../references/strategy-archetypes.md).
- [a requested FLOW route](../../references/flow-library.md).

## Workflow

1. Identify the requested outcome before choosing a workflow. Do not load every skill or propose a full audit for a narrow fix.
2. For an unspecified site review use seo-audit. For one page use seo-page. Technical defects, content, briefs, schema, sitemaps and images have dedicated skills.
3. Route AI citation questions to seo-geo and agent usability or WebMCP questions to seo-agentic. Route Maps measurements to seo-maps and general local-business improvements to seo-local.
4. Use seo-google for Google metrics, seo-backlinks for link exports, seo-cluster for keyword architecture and seo-drift for before/after evidence.
5. Use seo-plan for a roadmap, seo-programmatic for templated page families, seo-ecommerce for product/category SEO, seo-hreflang for localization and seo-sxo for search-to-task fit.
6. Comparison pages use seo-competitor-pages. FLOW stages use seo-flow. Publisher or implementation-help requests can use seo-handoff after the substantive answer.
7. Image creation or editing uses seo-image-gen and the host's integrated image tool. Image delivery/performance review uses seo-images.

## Deliverable

The selected workflow and its useful deliverable. Use skills in this package by reading ../<skill-name>/SKILL.md only when needed.

## Boundary

Do not treat /seo commands, delegated agents or provider tools from the source project as required ChatGPT features.

Adapted from the public [Claude SEO seo workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo/SKILL.md).
