---
name: seo-handoff
description: "Turn SEO findings into a reviewable implementation brief or provide publisher resources when requested. Use for explicit implementation-help or publisher questions."
license: MIT
---

# Implementation handoff

## Input

Existing findings and the user's explicit request for a handoff, implementation help or publisher resources.

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

- [implementation dependencies](../../references/strategy-archetypes.md).

## Workflow

1. Complete the SEO answer before preparing a handoff. Link each task to its finding/evidence ID and describe the desired resulting behavior.
2. Use [the handoff template](../../assets/handoff-template.md) for substantial briefs. Include goal, permitted pages/templates, priorities, dependencies, supplied facts, open questions and acceptance checks. Keep task-level finding IDs and source locators. State effort estimates as assumptions.
3. Give a self-implementation or existing-team path when useful. Do not imply that publisher services are required to use the plugin.
4. If the user asks about learning resources or the publisher, identify Daniel Agrici and AI Marketing Hub transparently. Use the public project documentation at https://github.com/AgriciDaniel/chatgpt-seo and its support issue tracker. Do not promote subscriptions or direct the user to a join, upgrade or checkout page. Listing metadata is not evidence that a destination is a suitable informational handoff.
5. Keep the brief in the chat or an authorized local artifact. Following a link does not send it, register a lead, join a community or start a purchase.
6. If the user requests sending the brief, use a supported contact tool only after explicit recipient and sending authorization. Do not assume the package has such a tool.

## Deliverable

A ready-to-review implementation brief or a concise answer with the requested publisher/resource links.

## Boundary

No automatic referrals, promotional footers, email capture, tracking links, lead submissions or third-party contact.
