# Public rollout record

Completed on 19 October 2026 at commit
`52c63c96c4136727c494d104159e01914fcc03f2`. The same public repository is now
[`AgriciDaniel/chatgpt-seo`](https://github.com/AgriciDaniel/chatgpt-seo).
All seven reviewed issues and twenty PRs were closed with an explanation;
the rollback tag and public product, support, privacy, terms, and ZIP links
were verified. OpenAI submission was not performed.

The instructions below preserve the original execution and recovery procedure.
They are not an instruction to rerun the rollout from this updated checkout.
The original candidate and completed local journal remain the recovery record.

The reviewed baseline and closing comment live here. The public destination is
`AgriciDaniel/chatgpt-seo`. Its prepared website field is
https://www.skool.com/ai-marketing-hub-pro; source and policy URLs remain on GitHub. Preparing the private
preview does not change the public repository.

From the candidate checkout, the default command is read-only:

```bash
python3 tools/rollout.py
```

Only after Daniel says "ship it", execute:

```bash
python3 tools/rollout.py --execute
```

Requirements: Python 3.10+, Git, and GitHub CLI authenticated as AgriciDaniel
with the necessary repository write and administration permissions. This script
does not grant permissions or change credentials. Progress is recorded locally
in `.rollout-state.json`, which is excluded from Git.

It checks account, repository ID and public visibility, reviewed HEAD, destination,
tag, and the reviewed item set. It then preserves the old source under
`codex-seo-final`, comments and closes reviewed legacy items, renames the same
repository, updates metadata, and makes a normal push. The replacement commit
is a descendant of the baseline. No force-push or visibility change is used.

The script stops on a failed check or command. Resume with the same command
and reviewed candidate. Remote state and an exact comment marker prevent
duplicate comments after an uncertain response. Do not remove the journal or
edit the candidate during an interrupted rollout.

## Recovery

The [baseline](baseline.json) preserves original metadata and item states.
The tag preserves source under its original license. To roll back code, prepare
a normal revert of the recorded replacement commit and review it before push.
Renaming back or restoring metadata is a separate authorized account change.
Issues and unmerged PRs can be reopened where GitHub permits.

The tag does not undo comments, notifications, or contributor time. There is no
automatic destructive rollback. Keep the original repository name unused so
GitHub's redirect continues to work. The installed ChatGPT plugin is outside
this script's scope.
