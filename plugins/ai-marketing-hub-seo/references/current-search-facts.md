# Search facts and refresh points

Checked on 2026-10-13. Reopen the relevant primary source before making a
date-sensitive eligibility, policy, API, or vendor claim. These notes are a
baseline for the workflows, not a guarantee that documentation stays fixed.

## Google AI search

Google's guidance keeps ordinary SEO fundamentals relevant to AI Overviews and
AI Mode. A supporting page must be indexed and eligible for a Search snippet.
No special AI markup is required, and eligibility does not guarantee inclusion.
Search Console includes these features in overall Web search reporting. Do not
claim to isolate AI Overview traffic from an ordinary GSC export.

Source: [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features).

Google's June 15, 2026 changelog says llms.txt files do not positively or
negatively affect Google visibility or rankings. Their presence can be
reported for systems that use them, without awarding ranking or citation
points. The same changelog records retirement of FAQ rich results beginning
May 7, 2026. Existing FAQPage markup is not itself a critical error. Do not
recommend new FAQPage for a Google rich-result benefit or promise AI citations.

Source: [Google Search documentation updates](https://developers.google.com/search/updates).

## Core Web Vitals

The good thresholds are LCP at or below 2.5 seconds, INP at or below 200 ms,
and CLS at or below 0.1, assessed at the 75th percentile with mobile and
desktop segmented. Missing CrUX samples are unknown, not failed or passed.
Lab measurements help diagnosis; static HTML cannot measure real-user CWV.

Source: [Web Vitals](https://web.dev/articles/vitals).

## Indexing API

Google's Indexing API is limited to pages with JobPosting or BroadcastEvent
inside VideoObject. It is not a general fast-indexing endpoint for articles,
products, or service pages. A successful notification does not prove indexing.
Draft appropriate sitemap and inspection guidance for other page types.

Source: [Using the Indexing API](https://developers.google.com/search/apis/indexing-api/v3/using-api).

## Workflow source points

For current requirements, open the page that matches the task:

- [Search Essentials](https://developers.google.com/search/docs/essentials)
- [Helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies)
- [Structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Structured data gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery)
- [Sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Localized page versions](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product)
- [OpenAI crawler roles](https://platform.openai.com/docs/bots)

Title and description lengths are editorial previews, not hard ranking limits.
Word counts, keyword density, and uniqueness percentages are diagnostics only.
Training-crawler policy, search discovery, and user-triggered browsing have
different purposes. Verify the vendor's current crawler documentation before
recommending access-policy changes. Agent usability and AI-search citation
visibility require different evidence.
