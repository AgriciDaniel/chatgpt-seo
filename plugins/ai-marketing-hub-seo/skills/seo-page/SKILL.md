---
name: seo-page
description: "Inspect and improve one page for search intent, metadata, content, links and markup. Use for page-level SEO reviews."
license: MIT
---

# Single-page SEO review

## Input

A page URL, supplied HTML or a draft, plus a target query if known.

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

- [page usefulness](../../references/content-review.md).
- [reader decision fit](../../references/sxo-method.md).
- [page controls](../../references/technical-checks.md).
- [schema decisions](../../references/schema-decisions.md) and [the fact-agreement helper](../../scripts/validate_structured_data.py) when JSON-LD is present.

## Workflow

1. Classify the page purpose and the user task. Open the page when possible; distinguish source, rendered view and a supplied draft.
2. Check title/description usefulness, heading hierarchy, canonical and robots observations, internal link destinations, and the page's ability to satisfy its intended task.
3. Review first-hand detail, factual support, author or organization accountability, content freshness and missing decision information. Treat length and density as editorial diagnostics.
4. Inspect image purpose and JSON-LD agreement with visible facts. If Python is available, use ../../scripts/analyze_html.py on a supplied snapshot for repeatable tag evidence.
5. Separate confirmed defects from rendering or performance hypotheses. Give rewritten title/description options only from known page facts.
6. Where edits are requested, provide a scoped draft or patch, then a validation checklist tailored to the affected page.

## Deliverable

A page diagnosis with evidence, ordered changes, suitable metadata drafts and any requested code. Include limitations and avoid an unsupported overall score.

## Boundary

Exactly one H1 and character-count previews are clarity conventions, not evidence of penalties. Missing source content needs rendered evidence.

Adapted from the public [Claude SEO seo-page workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-page/SKILL.md).
