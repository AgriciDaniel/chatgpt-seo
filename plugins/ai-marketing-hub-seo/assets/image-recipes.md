# SEO image recipes

These are composition defaults, not promised output dimensions. User-supplied
brand and placement requirements override them. Generate through the native
image tool, then inspect the actual file before specifying implementation sizes.

| Use | Starting composition | Prompt focus | Delivery check |
| --- | --- | --- | --- |
| Social / Open Graph preview | Wide; 1200 x 630 is an implementation target | Clear subject, short exact title when requested, generous crop margins | Legibility at thumbnail scale, platform crop, actual output size |
| Blog hero | Wide, usually 16:9 | One topic-relevant visual, editorial style, copy space only when needed | Relevance, mobile crop, likely LCP treatment |
| Product concept | Square or 4:3 | Supplied product details, honest materials and scale, simple background | Preserve features; identify conceptual imagery |
| Product cutout | Match supplied product framing | Edit only the background; genuine transparency | Product edges, labels, alpha, no altered features |
| Social square | 1:1 | One message, supplied brand palette, strong focal point | Exact text, small-screen legibility, safe margins |
| Explainer infographic | Portrait or modular landscape | Verified labels and facts, clear hierarchy, short text blocks | Every label/data value, reading order and text equivalent |
| Local service illustration | Wide or 4:3 | Truthful service scenario; no invented real staff/premises | Concept labelling and suitability for the business |
| Favicon / mark exploration | 1:1 | Simple silhouette, supplied brand cues, monochrome legibility | Small-scale recognition; vector/ICO conversion is separate |

## Prompt examples

Blog hero: "Create an editorial illustration for a guide to [verified topic].
Show [relevant subject] in [scene], with [supplied brand colors]. Use a wide
composition and a clear focal point. [Exact requested text or text-free]."

Product edit: "Use image 1 as the edit target. Replace only its background with
[requested background or transparency]. Preserve the product shape, material,
color, label text and perspective. Image 2 supplies [specific reference role]."

Infographic: "Illustrate this supplied, verified process: [steps]. Use the exact
labels [labels], in this reading order [order]. Do not add numbers, claims or
steps. Keep a clear hierarchy and an accessible contrast palette."

Social preview: "Create a wide preview for [topic]. The exact title is
\"[requested title]\". Use [brand cues], one relevant subject and generous safe
margins. Preserve the supplied spelling and avoid adding extra text."

Adapted from the public image-use cases and presets in Claude SEO at the pinned
commit recorded in provenance. External model presets and post-processing
commands were replaced with native tool instructions and verified delivery.
