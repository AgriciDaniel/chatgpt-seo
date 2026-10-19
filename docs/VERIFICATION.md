# Verification and release status

This repository separates package checks, installed-host behavior, and OpenAI
publication. Passing one does not establish the others.

## Reproduce the local checks

```bash
python3 tools/validate_plugin.py
python3 -m unittest discover -s tests -v
python3 tools/package_plugin.py
```

The existing suite covers HTML parsing, GSC calculations, missing evidence,
sitemap boundaries, crawl and hreflang inputs, image headers, JSON-LD fact
agreement, URL safety, resource containment, archive reproducibility, and
provenance. Additional tests cover the deferred rollout's failure boundaries.

The downloadable archive has a SHA-256 sidecar and a per-file inventory in
`downloads/`. Build it again to compare the archive hash. The validation mode
is local package validation; it does not fetch or approve listing URLs.

On 19 October 2026, the staged 0.2.13 package passed local validation and 129
tests: the existing 120 checks plus nine rollout tests using a simulated GitHub
backend and a real local Git repository. Two independent ZIP builds produced identical bytes. The nine helper
commands and two shared Python modules are byte-identical to the earlier public
candidate. The rollout tests do not perform public GitHub writes.

## Host and publication limits

Earlier private-host behavior tests and a bounded live-site audit were recorded
for previous versions. They are not fresh acceptance of 0.2.13. This preparation
changes publication metadata, publisher links, and documentation; the offline
analysis implementations are retained. It does not install an account update.

Physical mobile behavior, every host/tool combination, and OpenAI review are
not established by local tests or a mobile-sized GitHub README preview.
Image creation requires an exposed integrated image tool; an image brief alone
is not a generated image. Reports must state actual coverage and unknowns.

## Public release checks

The repository rollout completed on 19 October 2026 at commit
`52c63c96c4136727c494d104159e01914fcc03f2`, a direct descendant of the preserved
legacy source. The repository and policy URLs are public, the old repository
URL redirects here, and all seven reviewed issues and twenty PRs are closed
with one migration comment each. PRs were closed without merging. Repository
identity and public visibility were preserved.

The product remains pending public directory submission. Developer verification,
OpenAI skill scans, policy attestations, and review approval remain separate
portal requirements.

The name SEO-pro retains a generic-name review risk. A repository redesign
does not guarantee eligibility or approval. See [submission preparation](SUBMISSION.md)
for current primary sources and fields.

## README presentation

The README uses original animated pixel SVG scenes and click-to-reveal quest and
loadout panels. The game elements navigate documentation; they do not track user
progress or claim measured SEO gains. Essential prompts, capabilities, installation
steps, and policy links remain normal text. SVG motion has a reduced-motion
fallback and both light and dark artwork. No JavaScript or runtime was added.

The private GitHub preview was inspected on desktop and at a narrow mobile
viewport on 19 October 2026. Quest and inventory disclosures, FAQ expansion,
local anchors, image loading, and badge sizing were exercised. Light and dark
GitHub backgrounds were inspected. The documented `picture` markup follows
the browser color scheme in the in-app browser, which can differ from a manual
GitHub theme override. Both artwork palettes remain legible.

After rollout, an unauthenticated download of the public ZIP matched the local
archive byte for byte. Its SHA-256 is
`752e490c16442e2247fbcab9493813bdd5570ec3cd3fa232dbe0a784600bc8a8`.
The README, support and policy documents, and all README SVG assets also
matched the approved candidate. The public quest board was expanded in the
browser and its images loaded. This resolves the earlier private raw-download
access limitation; browser download completion is still a separate check.

The final artwork pass adds three independently expandable quest cards, native
code-block copy controls, an animated evidence outpost, and a dedicated mobile
hero selected at narrow widths. The knight and embedded fonts have resource
credits in NOTICE. Desktop and mobile quest reveals, the loadout reveal, normal
text navigation, and local anchors were exercised again after this pass. The
native copy control rendered, but clipboard completion could not be confirmed
through the in-app browser bridge. The task prompts also remain selectable text.

The quest-board refinement replaces its decorative progress bars with three
linked item cards. Each card names a real input and deliverable and links to
its corresponding prompt. All three links and prompt reveals were exercised
on GitHub. At a 390-pixel CSS viewport the cards stack in one column without
page overflow. Decorative lens, quill, and ledger motion does not represent
measured SEO progress. Package content is unchanged by this artwork pass.
