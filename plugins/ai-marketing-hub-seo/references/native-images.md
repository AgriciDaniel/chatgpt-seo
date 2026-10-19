# Native image creation and editing

Use the integrated host image tool for a user-requested raster image. Skill
instructions guide the brief; the tool creates the pixels. Do not substitute
a prompt-only answer when that tool is available and creation was requested.
No external image provider is required by this package.

## Brief and references

Identify the asset's job: explain a concept, show a supplied product, illustrate
an article, carry a social preview, or support a local-service page. Keep the
user's concept and brand context. Separate an edit target from style/identity
references and supporting inserts. Referencing a brand does not verify its
product facts or grant permission to invent a testimonial or a real premises.

For edits, inspect the image first and specify the change and preserved parts.
Use local paths only through a supported tool mechanism. Otherwise include the
smallest supported set of conversation images containing all required targets.
Do not provide competing target-selection mechanisms in the same call. If a
reference cannot be included, request it instead of editing a different image.

## Prompt structure

```text
Purpose and placement: [asset use and relevant page context]
Primary request: [the user's concept]
Subject and scene: [known details]
Composition: [framing, focal point and any needed copy space]
Style and brand: [supplied palette, mood, medium]
Exact text: "[only the requested, verified wording]"
References: [role of each supplied image]
Edit invariants: [parts that must stay unchanged]
Transparency: [opaque, genuinely transparent, or preserve existing alpha]
```

Use only fields that help this request. The host's tool schema controls actual
parameters, supported sizes and formats. Prompt wording does not guarantee an
exact pixel size, vector output, compression level or a perfect logo replica.

## SEO and truthfulness

- Generate diagrams from supplied or verified facts. For exact scientific or
  quantitative plots, use deterministic plotting; generation can provide an
  illustrative wrapper, not new measurements.
- Mark conceptual product, premises and team illustrations as concepts when
  they could be mistaken for real evidence. Preserve a supplied product's
  visible details in edits and check the output for invented labels/features.
- Request actual transparency for cutouts. Do not describe a white background
  as transparent. Inspect alpha when returned metadata or a file permits it.
- Draft alt text after seeing the output. Describe its purpose and information;
  decorative images can use empty alt. Avoid keyword stuffing.
- Keep the likely LCP hero eager; later/offscreen assets may be lazy-loaded.
  Intrinsic dimensions or aspect-ratio reserve space. Confirm with rendered
  and field evidence before claiming a CWV improvement.
- Format conversion, resizing and compression require an available supported
  tool and verification of the resulting file. Never claim these from a prompt.

## Delivery and failure

Show the native generated result inline. Use the actual artifact returned by
the host for download/handoff. For a project asset, keep a selected copy in the
authorized workspace if supported. Preserve prior versions unless replacement
was requested. Generation does not publish the asset or modify a live page.

For a missing tool or generation error, state the actual limitation and supply
the visual brief. Do not request credentials, quote unsupported prices, install
software or silently switch to a provider. Follow the native tool's handling
of blocked requests instead of rewriting a disallowed request to evade it.

## Page implementation notes

When requested, draft img/picture markup from actual returned assets and known
width/height, descriptive alt and intended loading behavior. A local/chat file
is not yet a public URL: do not invent a hosted path for Open Graph or an
ImageObject. Use a genuine accessible asset URL only after it exists. Requested
ImageObject metadata must agree with the real image and visible page purpose.
Output format conversion and responsive derivatives remain separate verified
operations, not something a generation prompt can prove.
