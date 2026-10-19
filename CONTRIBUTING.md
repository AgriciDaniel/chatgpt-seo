# Contributing

Keep changes focused on the skills-only ChatGPT package. Preserve its identity,
source attribution, and the existing evidence and authorization boundaries.
Do not add hooks, provider dependencies, telemetry, or hosted integrations as
part of a documentation change.

Python 3.10 or newer is sufficient for validation. From the repository root:

```bash
python3 tools/validate_plugin.py
python3 -m unittest discover -s tests -v
python3 tools/package_plugin.py
```

The ZIP has `plugin.json` at its root. Development tools and repository files
remain outside it. Keep secrets and private data out of code, test fixtures,
issues, and generated archives. Use synthetic examples for regression tests.

Describe the user-visible change and the checks you ran. For privacy and
security concerns, follow [Support](SUPPORT.md).
