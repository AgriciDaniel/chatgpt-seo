# Transition to the ChatGPT package

The planned public rename is from the former Codex repository to
`chatgpt-seo`. This preview contains SEO-pro, the separately built
ChatGPT skills package. The public repository has not been changed by preparing
this preview.

At rollout, the `codex-seo-final` tag will preserve commit
`9a644f68d39d242a7a41a0017f7286dd0512fc3b` and its original license. The tag
is planned, not claimed to exist already. Legacy releases and history remain.
The MIT license for this replacement does not apply retroactively to that code.

The replacement does not include the old installers, agent profiles, hooks,
Python dependencies, or provider extensions. It does not migrate or remove
existing local installations. In particular, a repository rename cannot fix
an already-installed hook or repair a user's local runtime.

Existing users should review their installed version and the legacy uninstall
instructions before removing it. Keep their local data and configuration backed
up; the ChatGPT plugin does not read or import those credentials or caches.

The prepared rollout closes legacy issues as not planned and PRs unmerged,
with an explanatory comment. This is a product transition, not a claim that
reported legacy defects were fixed.

GitHub documents repository redirects and preservation of stars and followers
in [Renaming a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).
The rollout never changes the public repository to private or recreates its name.
