---
name: seo-images
description: "Review image discoverability, accessibility, page performance risks and SEO asset briefs. Use for image SEO or image optimization requests."
license: MIT
---

# Image SEO

## Input

A page/source snapshot, image files, or a clearly described asset purpose.

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

- [requested asset creation](../../references/native-images.md).
- [actual file metadata](../../references/dataset-contracts.md).
- [image recipes](../../assets/image-recipes.md) for brief-only composition and placement choices.

## Workflow

1. Inventory meaningful, decorative and functional images. Distinguish a missing alt attribute from intentionally empty decorative alt.
2. Assess descriptive text, surrounding content, discoverable source URLs and relevant image markup. Draft alt text that conveys purpose without keyword stuffing.
3. Check actual file dimensions, bytes and formats only when files or reliable responses are available. Treat universal file-size limits as suggestions, not ranking requirements.
4. Inspect explicit dimensions or aspect ratio and likely LCP candidates. Native lazy loading and JavaScript lazy-loader hints require different checks; do not recommend lazy loading the likely hero by default.
5. For requested creation or edits, use [the native generation workflow](../seo-image-gen/SKILL.md). Generate through the integrated tool when available, then provide the actual artifact, context, filename and purpose-based alt text.
6. Validate rendered appearance and mobile delivery when tools permit. Flag untested output instead of claiming compression, visual fidelity or accessibility compliance.

## Deliverable

An image inventory and fix list, or an asset brief and requested generated files with accurate alt text.

## Boundary

The host's integrated image tool creates requested assets. The package has no external image provider or binary optimizer. Source HTML cannot measure image bytes, actual LCP or visual quality.

Adapted from the public [Claude SEO seo-images workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-images/SKILL.md).
