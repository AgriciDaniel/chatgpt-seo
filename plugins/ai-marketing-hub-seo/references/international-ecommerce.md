# International and ecommerce decisions

## International SEO

Collect the actual locale-to-URL equivalents, canonical intent, language/region
audiences and implementation method. Validate absolute targets, language tags,
self references, reciprocals and consistent equivalent clusters. Check canonical
and indexability agreement from actual crawl/response evidence. A partial
annotation sample cannot prove a reciprocal is absent from the live site.
Use [validate_hreflang.py](../scripts/validate_hreflang.py) for supplied rows and
[dataset contracts](dataset-contracts.md#hreflang-annotations) for input.

The helper checks syntax and the observed graph, not ISO registry membership,
translation quality or live target status. Verify current supported language,
script and region conventions against
[Google localized versions](https://developers.google.com/search/docs/specialty/international/localized-versions).

Review the user's locale-selection behavior, readable translations, cultural
fit, units/currency/dates, genuine offer availability and internal navigation.
Avoid forcing locale redirects that hide useful versions from users/crawlers.
Select x-default only where its actual fallback/selector role fits. Machine
translation needs editorial and factual QA proportional to the content risk.

## Ecommerce

Assess product/category intent, variant URL/canonical relationships, real
inventory, offer changes, filters/facets, pagination, out-of-stock behavior,
useful internal paths, actual images and truthful policies. Confirm indexing
intent for facet combinations before treating noindex as a defect. Preserve
important distinct variant information where the actual offer requires it.

Markup, merchant listings, feeds and product pages must agree on the genuine
facts. Inspect currency, price, stock, identifiers, reviews, shipping and returns
only when supplied or accessible. Do not fabricate missing values or assume
unsupported marketplaces/checkout integrations. Recheck current Google product
requirements with [Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product).

Agentic commerce needs a tested journey and actual declared protocol/tools.
Inspect discovery, product understanding, variant selection, cart, delivery,
price totals and confirmation flow when that scope is authorized. A protocol
file's presence does not prove transaction support. Never complete a purchase
merely to validate a page. Keep read-only checks and a reviewable implementation
proposal useful when checkout testing is unavailable.

Use [schema decisions](schema-decisions.md), [technical checks](technical-checks.md)
and [native imagery](native-images.md) for their respective parts. Page/offer
edits, feed submission and live checkout changes require explicit scope.

## Annotation methods and optional commerce profiles

Compare HTML-head, HTTP Link-header and XML-sitemap alternate sets when they
are supplied. Reconcile absolute target URLs, source membership and namespace
for sitemap annotations, return relationships across domains, and canonical,
redirect/indexability facts for the final targets. Compare actual body language,
html lang, localized metadata, schema facts, alt text, important sections and
customer tasks. Localized currency, units, dates, phone/address formats and
offer differences need actual locale facts. Do not infer translation method
or abuse from writing style alone.

If a UCP or other commerce profile is supplied, review its JSON syntax, stated
version, declared capabilities and real endpoint evidence as an optional
protocol review. Check the current protocol's official schema before claiming
conformance. Missing optional protocol files are not defects. Profile presence
does not prove that a checkout works or authorize a purchase. For generated
merchant imagery, verify current official provenance/metadata requirements
before recommending a submission workflow.
