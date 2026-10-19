# Install and start a task

The installable file is linked in the [README](../README.md). It is a portable
plugin ZIP with `plugin.json` at the archive root. GitHub's source-code ZIP
contains the whole repository and is not the installable file.

In an eligible ChatGPT account, open Plugins, choose Add, then Upload plugin
archive. Select the plugin ZIP, add it, open its settings, install it, and use
Try in chat. Start with a public URL or a supplied draft/export and a concrete
question. New conversations avoid relying on an older conversation's selection.

This private-upload flow was exercised with the earlier private 0.2.11 package
on 13 October 2026. The 0.2.15 candidate has not been installed into the owner's
account as part of this repository preparation. Interface labels and availability
can vary by account, workspace, and client.

If the upload option is absent, do not paste the ZIP into an ordinary message
and assume it installs. Check workspace restrictions or use OpenAI support.
This project cannot enable missing account features. Public directory submission
and installation from an approved directory listing are separate milestones.

No local runtime is required for normal ChatGPT use. The nine optional helper
commands need Python 3.10 or newer in an execution-capable host. See the
[runtime contract](../plugins/ai-marketing-hub-seo/references/runtime-and-data.md).

Official reference: [Package your plugin](https://developers.openai.com/plugins/build/plugins).
