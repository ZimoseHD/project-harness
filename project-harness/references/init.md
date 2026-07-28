# Init

Execute this setup operation only after `project-harness` dispatches `role: init` from a current user's explicit invocation.

Initialize or validate the project-owned Harness configuration without entering a feature-iteration lifecycle phase.

## Accept only the initialization packet

Accept:

~~~yaml
role: init
configuration:
  marker_namespace: project-slug
next_action: null
~~~

When `.project-harness/config.yaml` already exists, `configuration.marker_namespace` may be omitted to request validation only. Reject unknown configuration keys.

## Enforce the boundary

- Resolve `.project-harness/config.yaml` relative to the current project root.
- Create or validate only that config file and its parent directory.
- Do not load or execute a lifecycle phase, inspect task Issues or Pull Requests, create callbacks, or persist markers.
- Do not create branches, commits, pushes, Issues, Pull Requests, comments, reviews, merges, releases, or deployments.
- Stop after returning the initialization result. `next_action` is descriptive only and never authorizes another operation in the same invocation.

## Validate schema version 1

For schema version 1, accept exactly:

~~~yaml
schema_version: 1
marker_namespace: "project-slug"
~~~

Require `marker_namespace` to:

- be an explicit lowercase kebab-case ASCII slug;
- contain 1–63 characters;
- match `^[a-z0-9]+(?:-[a-z0-9]+)*$`;
- exclude `:`, whitespace, template syntax, and marker suffixes.

Do not infer or normalize the value from a directory, repository name, remote URL, Issue, prior callback, or conversation. If the file is missing and the packet omits the value, return `blocked`.

## Create or verify idempotently

1. If the config is absent and the packet supplies a valid namespace, create the parent directory and write the schema exactly once.
2. Read the file back and independently parse both fields. Return `initialized` only when the persisted values exactly match schema version 1 and the requested namespace.
3. If a valid config already exists and the supplied namespace is absent or identical, do not rewrite it; return `verified-existing`.
4. If the existing file is malformed, has an unsupported schema version, contains unknown or duplicate keys, or differs from the supplied namespace, do not overwrite it; return `blocked` with the exact conflict.
5. Never rename an established namespace. A requested change is outside `init` and requires a separately approved compatibility migration that preserves existing persisted markers through verified dual-read behavior.

Do not add defaults, environment overrides, compatibility aliases, or a second config path.

## Return a closed result

~~~yaml
outcome: initialized | verified-existing | blocked
config_path: .project-harness/config.yaml
schema_version: 1
marker_namespace: null
reason: null
recovery_condition: null
~~~

For `blocked`, identify the missing or conflicting field and the exact user or migration input required. Do not claim that the project is initialized.
