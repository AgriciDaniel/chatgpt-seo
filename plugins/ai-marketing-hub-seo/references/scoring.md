# Diagnostic scoring

Preserve the public Claude SEO category weights:

| Category key | Weight | Evidence needed |
| --- | ---: | --- |
| technical | 22 | Crawl/index controls, canonical and URL behavior, rendering observations |
| content | 23 | Main-content review against intent, usefulness and documented claims |
| on_page | 20 | Metadata, headings, links and visible page purpose |
| schema | 10 | Detected markup, applicable requirements and visible factual agreement |
| performance | 10 | Named field or lab measurements with source, date and device |
| ai_search | 10 | Accessibility, clear attribution and source-supported content observations |
| images | 5 | Relevant image markup and tested image observations |

For each category use documented checks with `pass`, `partial`, `fail`, or
`unavailable` states. Derive the category score from declared applicable checks:
pass = 1, partial = 0.5, fail = 0. Divide earned points by possible points.
An unavailable material check makes that category unavailable. Explain any
weighting or applicability choice. Absence of applicable schema or images may
be a pass after inspecting the page's purpose; mark that reasoning as evidence.
This rubric is a review convention, not a validated model of ranking changes.

Do not score schema opportunities by the number of types added. Do not score
AI visibility from llms.txt presence. Do not turn a missing alt attribute,
a short title, or a lab performance concern into a claimed ranking penalty.

`scripts/scorecard.py` checks a category envelope and calculates:

- `health_score`: weighted aggregate only when all seven categories are assessed.
- `assessed_score`: a normalized score for the assessed categories, explicitly
  not an overall SEO Health Score.
- `coverage_percent`: the weight covered by assessed categories.
- `possible_score_range`: a bound that leaves unassessed categories unknown.

Example input:

```json
{
  "categories": {
    "on_page": {
      "status": "assessed",
      "score": 75,
      "evidence": ["page-inspection.json: title, headings, links"],
      "method": "Four equally weighted applicable checks, three passed"
    }
  }
}
```

The remaining categories are unavailable. Show coverage and limitations beside
any partial score. The script validates structure and arithmetic, not whether
the evidence is true or whether the reviewer chose reasonable checks.

Priorities depend on observed consequences:

- Critical: evidenced unintended indexing blockage or a serious business blocker.
- High: an evidenced defect on an important page or a dependency blocking other work.
- Medium: a supported improvement with a testable benefit.
- Low or informational: context, maintenance, or a minor concern.

Confirm intended controls before recommending removal of noindex, robots
restrictions, canonicals, or private-content protection. Numeric business
impact and fixed delivery times require their own evidence or an explicit
planning assumption.
