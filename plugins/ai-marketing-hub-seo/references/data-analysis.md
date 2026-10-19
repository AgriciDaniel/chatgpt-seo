# SEO data analysis

Before calculating, record the source, property, time window, timezone,
filters, report/search type, row grain, row cap, and known missingness.
Different grains are not additive by default. Keep separate exports separate
until join keys and metric definitions are clear.

## Search Console

Clicks and impressions can be summed across disjoint rows at the same grain.
Aggregate CTR is `sum(clicks) / sum(impressions)`, not an average of row CTRs.
Return unavailable when impressions are zero. For comparable aggregate rows,
use impressions to weight position: `sum(position * impressions) /
sum(impressions)`. Keep the source's meaning of position visible; it is not
an exact universal rank for every impression.

Query-level exports can omit anonymized queries and be capped. A query table
need not sum to property totals. Do not fill the difference with invented
keywords or call it a data defect without checking the source's scope.
Page-level and property-level aggregation may differ, including treatment of
multiple results from one property. Never join totals onto detail and then
sum the duplicated totals.

For changes, compare like windows and filters. Show absolute and relative
change. Relative change from a zero baseline is undefined; report the new
absolute value. Account for weekday mix, reporting lag and seasonality when
interpreting movement. Separate observations, plausible mechanisms and the
test needed to distinguish them.

Useful patterns include high-impression low-CTR pages, pages losing clicks
with stable impressions, query/page intent mismatches, device-specific losses,
and duplicate targets competing for the same task. The interpretation depends
on current source and page evidence; none is automatically an algorithm penalty.

## Analytics and conversions

GSC clicks, GA4 sessions and users are different measures. Keep their scopes,
attribution models and date definitions visible. Use the event/conversion
definitions supplied by the user or source. Do not equate all organic sessions
with nonbrand acquisition or count a duplicated conversion across sources twice.

Revenue and lead quality need actual conversion/business evidence. If only
GSC data exists, report search opportunities and propose the measurement
needed to estimate commercial value.

## Backlinks

State whether a row is a link, referring page, referring domain or provider
aggregate. Normalize URLs only in ways justified by the task; a trailing slash
or parameter may identify a distinct resource. Preserve original values for
review. Mark status verified only when an actual source-page check supports it.

Referring-domain quality, anchor distributions and topical relevance need
appropriate fields and samples. Vendor authority/spam metrics are observations
from that vendor, not Google's assessment. Missing vendor rows do not imply
that no other links exist.

## Maps grids

Require a known query, grid layout/area, collection date, observed rank cap,
and cell result state. For an unweighted top-three share, divide observed
top-three cells by all measured cells, including measured not-ranked cells.
Report the measured/scheduled-cell coverage separately. A missing cell is
unknown, not not-ranked. If weights are used, publish their basis and the
weighted denominator. Do not compare grids with different layouts silently.

## Performance

Keep field and lab data separate. Record device, page versus origin scope,
collection period and tool version. A lab run is a specific observation, not
the distribution of all real visitors. Missing field data often reflects
sample availability. It cannot become a fabricated pass/fail result.

## Current source checks

Open the relevant primary documentation for the data supplied, especially if
aggregation or feature definitions changed:

- [Search Analytics API](https://developers.google.com/webmaster-tools/v1/searchanalytics/query)
- [Search Console performance](https://support.google.com/webmasters/answer/7576553)
- [GA4 Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [PageSpeed Insights](https://developers.google.com/speed/docs/insights/v5/about)
- [Chrome UX Report](https://developer.chrome.com/docs/crux)
