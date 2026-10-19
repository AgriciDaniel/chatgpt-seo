"""Analyze a supplied crawl sample, link graph and optional sitemap URL list."""

import argparse
from collections import defaultdict, deque

from seo_io import read_json, run
from url_values import absolute_url, origin


def analyze_crawl(data):
    if not isinstance(data, dict) or not isinstance(data.get('pages'), list) or not data['pages']:
        raise ValueError('Input requires a nonempty pages array')
    if len(data['pages']) > 50000:
        raise ValueError('At most 50000 supplied pages are supported')
    pages, inlinks, adjacency, titles = {}, defaultdict(set), {}, defaultdict(list)
    for index, raw in enumerate(data['pages']):
        if not isinstance(raw, dict):
            raise ValueError(f'Page {index}: expected an object')
        url = absolute_url(raw.get('url'))
        if url in pages:
            raise ValueError(f'Duplicate supplied page URL: {url}')
        status = raw.get('status')
        if status is not None and (type(status) is not int or not 100 <= status <= 599):
            raise ValueError(f'Page {index}: status must be an HTTP integer or null')
        if raw.get('indexable') is not None and type(raw['indexable']) is not bool:
            raise ValueError(f'Page {index}: indexable must be boolean or null')
        links = raw.get('links', [])
        if not isinstance(links, list) or len(links) > 10000:
            raise ValueError(f'Page {index}: links must be a bounded URL array')
        canonical = absolute_url(raw['canonical'], url) if raw.get('canonical') is not None else None
        pages[url] = {**raw, 'url': url, 'supplied_url': raw['url'], 'canonical': canonical, 'source_index': index}
        adjacency[url] = sorted(set(absolute_url(link, url) for link in links))
        title = raw.get('title')
        if title is not None and not isinstance(title, str):
            raise ValueError(f'Page {index}: title must be text or null')
        if title and title.strip():
            titles[title.strip()].append(url)
    findings, unobserved = [], set()

    def finding(code, url, field, observation):
        findings.append({'id': f'C{len(findings)+1:03d}', 'code': code,
                         'affected_url': url, 'supplied_url': pages[url]['supplied_url'], 'evidence_level': 'supplied_crawl_sample',
                         'evidence_pointer': f"/pages/{pages[url]['source_index']}/{field}",
                         'observation': observation})

    for url, page in pages.items():
        if page.get('status') is not None and page['status'] >= 400:
            finding('observed_http_error', url, 'status', page['status'])
        if page.get('indexable') is False:
            finding('index_intent_review', url, 'indexable', 'Supplied indexability is false; confirm intended visibility')
        if page['canonical'] and page['canonical'] != url:
            finding('nonself_canonical_review', url, 'canonical', page['canonical'])
        for target in adjacency[url]:
            if origin(target) != origin(url):
                continue
            inlinks[target].add(url)
            if target not in pages:
                unobserved.add(target)
            elif pages[target].get('status') is not None and pages[target]['status'] >= 400:
                finding('link_to_observed_http_error', url, 'links', target)
    sitemap = data.get('sitemap_urls', [])
    if not isinstance(sitemap, list):
        raise ValueError('sitemap_urls must be a URL array')
    sitemap_observations = []
    for raw in sitemap:
        url = absolute_url(raw)
        page = pages.get(url)
        sitemap_observations.append({'url': url, 'in_supplied_sample': page is not None,
                                     'observed_status': page.get('status') if page else None,
                                     'supplied_indexable': page.get('indexable') if page else None,
                                     'observed_canonical': page.get('canonical') if page else None})
    start = absolute_url(data['start_url']) if data.get('start_url') is not None else None
    depth = {}
    if start:
        if start not in pages:
            raise ValueError('start_url is not in the supplied sample')
        depth[start], queue = 0, deque([start])
        while queue:
            current = queue.popleft()
            for target in adjacency[current]:
                if target in pages and origin(target) == origin(start) and target not in depth:
                    depth[target] = depth[current] + 1
                    queue.append(target)
    return {'format_version': 1, 'evidence_level': 'supplied_crawl_sample',
            'page_count': len(pages), 'scope': data.get('scope'), 'findings': findings,
            'url_keys': [{'source_index': page['source_index'], 'supplied_url': page['supplied_url'], 'comparison_url': url}
                         for url, page in pages.items()],
            'duplicate_title_groups': [{'title': title, 'urls': urls} for title, urls in titles.items() if len(urls) > 1],
            'sample_pages_without_observed_inlinks': sorted(url for url in pages if not inlinks[url]),
            'unobserved_internal_link_destinations': sorted(unobserved),
            'depth_from_supplied_start': depth if start else None,
            'sitemap_observations': sitemap_observations,
            'limitations': ['Comparison URLs normalize scheme and hostname case and default ports, omit fragments and preserve path/query case',
                            'No URLs were fetched; status and indexability are supplied observations',
                            'A page without an observed sample inlink is not proven orphaned',
                            'Unobserved destinations are unknown, not broken',
                            'Duplicate titles, depth and canonicals require intent review',
                            'Supplied indexability does not prove search-engine indexing']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='Selected JSON crawl evidence, up to 10 MiB')
    args = parser.parse_args()
    run(lambda: analyze_crawl(read_json(args.file)))


if __name__ == '__main__':
    main()
