# Clustering and page architecture

The unit of a cluster is a useful page target, not a group of similar strings.
Make intent and page type explicit before calculating overlap.

## With measured SERPs

For each keyword retain the query, locale/language, date, device where known,
top-N limit and the actual organic URLs. Normalize URLs conservatively and
keep original values. Ads and a video/forum-heavy result pattern can provide
intent context but should not be silently mixed into an organic-URL overlap
denominator.

For URL sets A and B, report either intersection count or Jaccard overlap:

```text
intersection_count = |A intersection B|
jaccard = |A intersection B| / |A union B|
```

A suggested starting heuristic is at least three shared URLs in comparable
top-ten samples, followed by intent review. This is an internal grouping
choice, not a Google rule. Adjust it for the sample and explain the choice.
With fewer or differently sampled results, mark the comparison limited.

Check proposed groups against a representative keyword or medoid. Pure
transitive merging can create a bridge: A overlaps B and B overlaps C while
A and C address different tasks. Split on meaningful intent or page-type
differences even if a numerical threshold passes.

## Without measured SERPs

Use semantic grouping by task, entity, audience and buying stage. Label all
groupings provisional. Do not invent an overlap matrix, live search result
sample, search volume or keyword difficulty. Offer a narrow measurement plan
for the uncertain clusters if the user wants validation.

## Map clusters to real pages

Prefer a suitable existing URL when it already covers the task. Identify:

- Primary target and supporting variants for one useful page.
- Distinct intent that deserves another page.
- Existing overlap that warrants a content review before any merger.
- Missing hub, navigation or contextual link that helps both readers and discovery.

Do not merge pages based only on keyword similarity. Assess content,
performance evidence, backlinks and redirects when recommending consolidation.

Build a table with cluster ID, intent, page type, representative keyword,
evidence mode, actual metrics, current/proposed URL, hub, internal-link targets,
confidence and next validation. An interactive map is useful when it changes
the user's understanding; a clear table is sufficient for small inventories.

Attribute the planning method to the public Claude SEO clustering workflow,
including community contributions, through the package NOTICE. Thresholds and
architecture recommendations remain review heuristics.
