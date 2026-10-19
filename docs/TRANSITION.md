# Transition to the ChatGPT package

On 19 October 2026, the former Codex repository was renamed to
`chatgpt-seo` and updated with SEO-pro, the separately built ChatGPT skills
package. The same public repository retains its history, stars, and watchers.
The old repository URL redirects here.

The [`codex-seo-final` tag](https://github.com/AgriciDaniel/chatgpt-seo/tree/codex-seo-final)
preserves commit `9a644f68d39d242a7a41a0017f7286dd0512fc3b` and its original
license. Legacy releases and history remain.
The MIT license for this replacement does not apply retroactively to that code.

The replacement does not include the old installers, agent profiles, hooks,
Python dependencies, or provider extensions. It does not migrate or remove
existing local installations. In particular, a repository rename cannot fix
an already-installed hook or repair a user's local runtime.

Existing users should review their installed version and the legacy uninstall
instructions before removing it. Keep their local data and configuration backed
up; the ChatGPT plugin does not read or import those credentials or caches.

The rollout closed seven legacy issues as not planned and twenty PRs unmerged,
each with an explanatory comment. This is a product transition, not a claim
that reported legacy defects were fixed.

GitHub documents repository redirects and preservation of stars and followers
in [Renaming a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).
The rollout never changes the public repository to private or recreates its name.
