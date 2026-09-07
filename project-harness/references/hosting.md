# Hosting Operations

Use available platform tools or an authenticated official CLI for Issues and PRs. Resolve the repository and task from the user's links, the workspace remotes, and the ongoing work. In this Skill, PR also means a GitLab merge request.

| Platform | CLI | Task objects |
| --- | --- | --- |
| GitHub | `gh` | Issues, pull requests, comments and reviews |
| GitLab, including self-hosted | `glab` | Issues, merge requests, notes and discussions |

On GitLab, keep the full project path including nested groups and use the host from the project URL. Work with native states and tool results; no common result schema is required.

Create and update normal Issues, PRs, and review comments. Preserve unrelated content and metadata. Use structured text arguments or the CLI's file-input support for multiline content (`gh --body-file`, for example), so Markdown reaches the platform intact.

Inspect the branch, diff, tests, and PR state as useful for the operation. Select a merge method using the user's preferences and project conventions. On GitLab, respect the project's merge method and per-MR squash settings; fast-forward merging does not itself rebase a branch. Submit a normal merge request; the platform enforces its own branch protections and repository rules. Do not change project settings or bypass protections to force a merge.

Harness adds no checks registry, evidence keys, tuple binding, digest utility, or mandatory pre/post-read sequence. Handle ordinary conflicts and tool errors as part of delivery. If a response leaves the result uncertain, inspect the actual Issue or PR before deciding whether another attempt is needed. Retry only when that makes sense for the observed state. Report access limitations or a pending merge honestly.

Use the tool result or a follow-up read as needed to establish what happened. Link the Issue or PR in the phase summary; do not publish transport envelopes, workflow callbacks, or synthetic status comments.
