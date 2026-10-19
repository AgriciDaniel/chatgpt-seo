---
name: seo-image-gen
description: "Create or edit SEO images with ChatGPT's integrated image generation. Use for requested blog heroes, social previews, product illustrations, local-service visuals and infographics."
license: MIT
---

# SEO image generation

## Input

The requested image, its placement and known brand/product facts. Existing
images can be edit targets or visual references; identify their role.

## Evidence and runtime

If a skill-resource reader fails to open a linked supporting file, try the
available file or execution tool using the installed plugin root returned by
the host or resolved from this skill's location. Do not hardcode a home folder,
version, or working directory. Distinguish a failed reader call from an absent
file, and files actually attempted from files not attempted. Report a resource
as unavailable only after the supported access paths have failed. If no file
or execution access is available, continue within the evidence you can read
and state that limit.

Read [the operating contract](../../references/operating-contract.md) and
[native image workflow](../../references/native-images.md). Choose a relevant
[asset recipe](../../assets/image-recipes.md) when the brief needs one.

## Workflow

1. Preserve the user's concept, exact requested text, brand cues and supplied
   product details. Ask one question only if an essential input is missing.
2. Decide whether this is creation, a variant or an edit. For an edit, inspect
   the actual target first and state which elements must be preserved.
3. Build a concise prompt: purpose, subject, composition, style, exact text,
   reference roles and constraints. Use known facts for diagrams, labels and
   infographics. Generated visuals cannot establish real product appearance,
   business premises, staff identities, testimonials or statistical evidence.
4. Call the host's integrated image-generation/editing tool directly when it
   is available. Follow that tool's current instructions for reference-image
   selection, transparency and returning the result. A normal creation request
   does not require an API key, provider installation or another confirmation.
5. Use genuine transparency for a requested cutout and preserve existing
   alpha on edits. Include the actual edit target/reference using the tool's
   supported mechanism. If a required reference is missing, request that image.
6. Inspect the returned image for subject fidelity, text accuracy, composition,
   cropping and preserved edit constraints. Make a targeted correction when
   the result materially misses the brief. Do not manufacture a success claim
   after a failed generation or use unrelated output as the requested asset.
7. Deliver the generated image inline and any actual file the host returned.
   Include a useful filename, context-sensitive alt text and intended placement.
   State actual dimensions/format only from the returned file or metadata.
   Provide responsive/lazy-loading guidance through seo-images when relevant.

## Deliverable

The requested visual, a concise prompt/recipe record, filename and alt text.
Use [the image delivery template](../../assets/image-delivery.md) for multiple
assets or implementation handoff. Preserve existing files; a generated draft
does not authorize replacing or publishing a live asset.

## Boundary

If integrated image generation is unavailable in this chat, state that limit
and deliver a ready-to-run visual brief. Do not switch to an external provider,
paid API, CLI or dependency installation. Existing editable SVG/icon assets
can be edited as vectors when that better fits the user request.

Adapted from the public [SEO image workflow](https://github.com/AgriciDaniel/claude-seo/blob/4b99de2f7de7e7d5247042e5fb5b4ea9368ef734/skills/seo-image-gen/SKILL.md).
