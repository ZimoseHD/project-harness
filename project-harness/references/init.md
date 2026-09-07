# Init

Set up optional project preferences. This operation is outside the delivery paths and stops after setup.

Read existing project instructions and `.project-harness/config.yaml`, if present. Explain the branch and merge conventions already in use. When the user wants them recorded, create or update this project-owned file with only useful preferences. For example:

```yaml
integration:
  base_branch: develop
  product_pr:
    merge_method: squash
  memory_pr:
    merge_method: squash
```

The example is a starting point, not a required schema. Omit unused fields and use the project's actual target branch and preferred merge method. Preserve unrelated existing settings. No namespace or version field is needed for new files.

Read the same `integration` preferences from older configuration when useful. Leave historical namespace and version fields alone; they have no workflow role in v3. Missing configuration, extra keys, or a partial legacy file do not require migration before delivery. If a setting cannot be interpreted, explain the uncertainty and use established project conventions where the choice is clear; ask when the choice materially matters. Do not silently replace an explicit project preference with an incompatible one.

If the project already documents these conventions elsewhere, report them without creating another file. Do not start a feature task, create an Issue, commit, or publish as part of standalone setup.

Return the settings used and any file changed. Lifecycle operations read these preferences directly and run without a configuration validator.
