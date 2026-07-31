# Init

Execute this setup operation only after `project-harness` dispatches `role: init` from a current user's explicit invocation.

Initialize or validate the project-owned Harness configuration without entering a feature-iteration lifecycle phase.

## Accept the public initialization input

Apply the root Skill's public-invocation adapter. For a new configuration or explicit schema-v1 migration, require an exact `role: init` and the complete schema-v2 configuration:

~~~yaml
role: init
configuration:
  schema_version: 2
  marker_namespace: project-slug
  integration:
    base_branch: develop
    product_pr:
      merge_method: merge
    memory_pr:
      merge_method: merge
~~~

For strict compatibility, also accept the historical configuration containing only `configuration.marker_namespace` when validating an existing schema-v1 file. When `.project-harness/config.yaml` already exists, all configuration fields may be omitted to request validation without migration. Validate the configuration semantics rather than a hand-off envelope: reject partial schema-v2 policy and unknown or duplicate configuration keys, while continuing to accept the root adapter's older structured public form.

## Enforce the boundary

- Resolve `.project-harness/config.yaml` relative to the current project root.
- Create, validate, or explicitly migrate only that config file and its parent directory.
- Do not load or execute a lifecycle phase, inspect task Issues or Pull Requests, create callbacks, or persist markers.
- Do not create branches, commits, pushes, Issues, Pull Requests, comments, reviews, merges, releases, or deployments.
- Stop after returning the initialization result. Never treat descriptive public metadata as authority to enter another operation.

## Write schema version 2

Use schema version 2 as the only current write form:

~~~yaml
schema_version: 2
marker_namespace: project-slug
integration:
  base_branch: develop
  product_pr:
    merge_method: merge
  memory_pr:
    merge_method: merge
~~~

Require `marker_namespace` to:

- be an explicit lowercase kebab-case ASCII slug;
- contain 1–63 characters;
- match `^[a-z0-9]+(?:-[a-z0-9]+)*$`;
- exclude `:`, whitespace, template syntax, and marker suffixes.

Require `integration.base_branch` to equal `develop`. Require each `merge_method` to equal exactly `merge`, `squash`, or `rebase`. Product and project-memory methods may differ. Do not infer or normalize any value from a directory, repository name, remote URL, Issue, enabled merge buttons, prior callback, or conversation. If the file is missing and the initialization input omits any current configuration field, return `blocked`.

Use `scripts/config_guard.py` to parse and validate the exact file. For migration, invoke its standard read-only interface with the user's exact choices:

~~~text
python3 -B scripts/config_guard.py CONFIG_PATH \
  --migrate-v1 \
  --product-method merge \
  --memory-method merge
~~~

Resolve the script from the loaded Skill root and `CONFIG_PATH` to the consumer project's exact config file. Replace the two example methods only with the explicit configuration choices and consume `rendered_config` from the `outcome: migration-rendered` JSON. The helper is read-only and deterministic; `init` retains all file-write authority and must still protect the baseline and independently read the result back.

## Dual-read schema version 1

Continue reading an existing exact legacy form:

~~~yaml
schema_version: 1
marker_namespace: project-slug
~~~

Reject extra or duplicate keys. Preserve its historical `develop` base. Validation-only `init` returns `verified-existing` without rewriting it. Lifecycle consumers may resolve a schema-v1 merge method only when the authoritative repository capability reports exactly one available method; otherwise `delivery` must stop before its first mutation and request the explicit migration below.

Never create a new schema-v1 file and never silently add integration defaults to one.

## Create or verify idempotently

1. If the config is absent, require the complete current configuration input, create the parent directory, and write canonical schema-v2 exactly once.
2. Read the file back through `scripts/config_guard.py`. Return `initialized` only when every persisted schema-v2 value exactly matches the requested namespace and integration policy.
3. If a valid schema-v2 config already exists and the supplied configuration is absent or identical, do not rewrite it; return `verified-existing`.
4. If a valid schema-v1 config already exists and the current initialization input supplies the complete schema-v2 policy with the exact same namespace, capture the complete file digest, re-read it immediately before replacement, and require the baseline to remain unchanged.
5. Render one canonical schema-v2 replacement, write only that file, independently read it back, and require exact schema, namespace, base, and both methods before returning `migrated`.
6. If an existing schema-v1 validation input omits integration policy, validate without migration and return `verified-existing`.
7. If any existing file is malformed, unsupported, concurrently changed, contains unknown or duplicate keys, differs from the supplied namespace, or conflicts with the supplied current policy, do not overwrite it; return `blocked` with the exact conflict.
8. Never rename an established namespace or migrate schema-v2 backward. Preserve every existing workflow marker through the unchanged namespace.

Do not add implicit defaults, environment overrides, compatibility aliases, a second config path, or another migration role.

## Return a closed result

~~~yaml
outcome: initialized | migrated | verified-existing | blocked
config_path: .project-harness/config.yaml
schema_version: 1 | 2
marker_namespace: null
integration:
  base_branch: null | develop
  product_pr:
    merge_method: null | merge | squash | rebase
  memory_pr:
    merge_method: null | merge | squash | rebase
reason: null
recovery_condition: null
~~~

For schema-v1 validation, return null integration values to distinguish legacy policy from configured schema-v2 policy. For `blocked`, identify the missing or conflicting field and the exact current `init` input required. Do not claim that the project is initialized or migrated.
