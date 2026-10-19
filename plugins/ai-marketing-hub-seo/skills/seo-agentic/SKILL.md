---
name: seo-agentic
description: "Inspect how a website can be read and used by browsing agents. Use for agent readiness, accessibility trees, discovery files or WebMCP."
license: MIT
---

# Agent readiness

## Input

A URL, rendered observation, agent-run evidence, tool definitions or discovery files.

## Evidence and runtime

Read [the operating contract](../../references/operating-contract.md) when this
workflow is selected. Use [runtime and data paths](../../references/runtime-and-data.md)
when choosing a tool or handling missing data. Recheck relevant
[search facts and primary sources](../../references/current-search-facts.md)
before date-sensitive claims. For a quantitative diagnostic, read
[scoring](../../references/scoring.md); unavailable categories stay unknown.

## Supporting resources

Read only the resources needed for the selected part of this task:

- [tested agent tasks and access](../../references/search-ai-agentic.md).
- [source versus rendered controls](../../references/technical-checks.md).

## Workflow

1. Define the task an agent should complete and the tested agent/browser. Agent readability, ability to act and decision reliability are separate checks.
2. Inspect semantic landmarks, headings, link/button names, labels, stable navigation, visible states and keyboard interactions when rendered tools are available.
3. Test relevant crawl/access policy and discoverability using actual responses. Markdown or llms.txt can help specific consumers; their existence does not prove ranking or citation value.
4. Review WebMCP/MCP operations only when their definitions are observable. Check clear inputs, scoped authorization, tool annotations and confirmation around consequential actions.
5. If Lighthouse agentic data is supplied, record its version and interpret its fraction as a browsing-readiness signal for the tested page. Reverify current vendor documentation rather than assuming an audit exists.
6. Give an evidence-based fix plan and repeat the concrete task when possible. Do not perform checkout, messages or other irreversible actions as an unapproved test.

## Deliverable

A task-based readiness report with observed failures, source locators and a retest plan. Draft markup/tool improvements only within the requested scope.

## Boundary

A static HTML check cannot validate an accessibility tree, WAF behavior, real agent completion or WebMCP support.

Adapted from the public [Claude SEO seo-agentic workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-agentic/SKILL.md).
