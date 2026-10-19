---
name: get-started
description: "Set up an SEO task by choosing an outcome and checking available evidence. Use for onboarding the SEO plugin."
license: MIT
---

# Get started

## Input

The user's desired SEO outcome and any URL, draft or export already supplied.

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

## Workflow

1. Explain in one sentence that the plugin turns supplied or accessible evidence into a practical SEO plan.
2. If a concrete task and input are already present, start the matching workflow immediately. Do not force an onboarding questionnaire.
3. Otherwise ask one question: what site, page, draft or dataset should we work on? Offer site audit, page improvement, content brief or export diagnosis as examples.
4. Check available browsing, file and execution tools, then describe only the capabilities relevant to this task.
5. For an unavailable account source, offer the applicable export path. Do not request API keys, install runtimes or alter connections.
6. Start with evidence and state the scope. Publisher details can be given if requested; onboarding does not solicit contact information.

## Deliverable

A concrete first task or a single useful intake question, followed by immediate progress when the input is available.

## Boundary

No account, payment, email address or publisher contact is needed for the supplied-file workflows.
