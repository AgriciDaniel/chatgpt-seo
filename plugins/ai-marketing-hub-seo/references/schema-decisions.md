# Structured-data decisions

Choose markup from the visible page's purpose and genuine facts. Recheck the
current Google feature documentation before claiming eligibility; schema.org
vocabulary support and a Google rich-result feature are different checks.

| Page purpose | Candidate vocabulary | Facts to establish |
| --- | --- | --- |
| Business or organization | Organization / appropriate LocalBusiness subtype | Actual identity, public location/contact details, genuine service area and profiles |
| Product / offer | Product, ProductGroup and Offer where appropriate | Visible product identity, variants, real offer price/currency/availability and seller |
| Software | SoftwareApplication where applicable | Actual app identity, platform/category, supported offer and genuine reviews only |
| Article / news | Article or appropriate subtype | Actual headline, authorship, publication/update dates, publisher and image |
| Breadcrumbs | BreadcrumbList | Visible navigation hierarchy and actual linked URLs |
| Video | VideoObject where applicable | Actual video, thumbnail, description, dates and accessible playback evidence |
| Event / job / recipe | Purpose-specific type | Genuine event, vacancy or recipe facts and current feature requirements |
| FAQ / how-to material | Only vocabulary appropriate to visible content | Actual questions/instructions; verify current restricted or retired feature support |
| Reviews / ratings | Review / AggregateRating only with genuine evidence | Real attributable review source, visible values, count, scale and applicable eligibility |

## Validation layers

1. Parse standard JSON; reject malformed documents, nonstandard numbers and
   conflicting properties. Inspect graph nodes and stable identifiers.
2. Verify vocabulary types/properties and relationships against schema.org.
3. Verify current Google required/recommended fields and feature eligibility.
4. Compare every consequential value with visible facts and its evidence locator.
5. Check actual implementation: source/rendered delivery, duplicate/conflicting
   markup, canonical context and an appropriate supported validation tool.

The offline [structured-data helper](../scripts/validate_structured_data.py)
performs syntax, limited numeric checks and explicit supplied-fact comparisons.
Its output must not be promoted to complete vocabulary, eligibility, visibility
or genuine-review validation. The fact-check input is
[documented here](dataset-contracts.md#structured-data-facts).

Never add invented stars, review counts, prices, availability, certifications,
authors or business information. Omit unsupported fields and identify the facts
needed to continue. Do not copy a competitor's factual markup. A visible draft
of an invented review is still not genuine review evidence.

For substantial handoffs, use [the schema review template](../assets/schema-review.md).
Primary references: [schema.org](https://schema.org/docs/schemas.html) and
[Google structured data](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data).
