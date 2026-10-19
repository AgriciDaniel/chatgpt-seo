# Technical audit decision checks

Load for technical audits or the technical portion of a site audit. Start from
actual inspected pages and responses. Use the source-versus-rendered distinction
and record each missing evidence class. A supplied crawl sample can be analyzed
with [analyze_crawl.py](../scripts/analyze_crawl.py); it does not fetch URLs.

| Area | Check and evidence | Fix decision and verification |
| --- | --- | --- |
| Discovery | Inspected robots declarations, sitemap documents, navigation and crawl exports | Reconcile discovery paths; validate the actual declared XML and independently inspect destinations |
| Crawl controls | User-agent rules, resources, response failures and access intent | Confirm which crawler and resource is affected; retest the response and relevant rendering |
| Index controls | Source/response noindex, canonical, redirects and intended visibility | Resolve conflicting controls; check source plus rendered state and authorized URL inspection where available |
| Canonicalization | Preferred URLs, parameters, alternate protocols/hosts, duplication and supplied canonical clusters | Choose preferred URLs based on actual purpose; retest links, redirects, canonical consistency and submitted URLs |
| Pagination | Crawlable links and distinct page content, filters, load-more behavior | Provide accessible paginated URLs and appropriate canonicals; do not automatically canonicalize every page to page one |
| Internal links | Real anchor destinations, broken links observed in a sample, important-page paths | Prioritize useful discovery and reader journeys; unknown sample destinations are not proven broken |
| HTTP behavior | Actually returned status/headers, redirects, soft-error content and retry behavior | Use intended permanence and destination; verify each response rather than inferring status from a generic tool error |
| Mobile parity | Rendered primary content, metadata, structured data, interactions and resource access | Resolve observed parity loss and unusable tasks; test representative mobile layouts |
| JavaScript | Raw versus rendered content, canonicals, robots and JSON-LD | Keep essential signals consistent; missing source text requires rendered evidence before diagnosis |
| Performance | Supplied field CWV versus a dated lab run, tested page/device, LCP element and interaction evidence | Connect bottlenecks to actual measurements; retest the same conditions and later comparable field data |
| Security | Actual HTTPS/certificate/mixed-content behavior and relevant response headers | Explain observed user/resource risk; do not equate a security-header checklist with ranking loss |
| Visual usability | Tested viewport, obstructive overlays, navigation, layout shifts and task completion | Make a concrete reproduction and retest; screenshots alone cannot establish conversion rates |
| Search submissions | Existing implementation and verified engine eligibility | Prepare reviewable instructions; an indexing submission or production change requires explicit authorization |

## Crawl and rendering

Select a representative mix of templates and important user journeys. State
sample counts, discovery method, capture time and failed pages. Inspect HTML
and rendered behavior separately. Access/authentication boundaries may make
some URLs intentionally unavailable. Do not treat a logged-in product screen
as a missing public landing page without confirming purpose.

Review duplicate titles, repeated content and crawl depth as diagnostic signals.
URL length, a three-click rule, word counts and redirect-hop preferences are
not universal ranking requirements. Sitemaps provide URL suggestions; their
contents do not prove indexing. Missing URLs need purpose and discovery context.

## CWV and retest

Record metric name, unit, sample/window, percentile if supplied, device and data
source. Distinguish field LCP/INP/CLS from lab diagnostics. Never derive CWV from
HTML, image bytes or a Lighthouse score. Use [the CWV report template](../assets/cwv-report.md).
Recheck current thresholds and method at [web.dev](https://web.dev/articles/vitals)
before assigning a performance status. Field improvements and ranking/traffic
outcomes are separate observations.

For crawler taxonomy, agents and AI surfaces, load
[search and agent readiness](search-ai-agentic.md). For annotation details load
[international/ecommerce checks](international-ecommerce.md).

Adapted from the pinned source technical, performance and visual workflows.
Current implementation guidance: [Google technical requirements](https://developers.google.com/search/docs/essentials/technical).

## Response and graph detail

Inspect robots groups/directives separately from meta robots and supplied
X-Robots-Tag headers, preserving actual response status. A missing resource,
4xx, 5xx and an explicit disallow are different observations; use the relevant
engine's current documentation before interpreting crawler behavior. Compare
raw/rendered title, links, canonical, robots and JSON-LD, and inspect primary
lazy-loaded content for required interaction. Record redirect loops, protocol/
host changes and conflicting URL forms from actual responses. Sample graph
sinks and pages with no observed inlinks need confirmation and intent.
