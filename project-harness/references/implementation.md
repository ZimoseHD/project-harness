# Implementation

Implement the task described by the Issue and the user's current instructions, then prepare a Draft Product PR.

Read the Issue, relevant code, and any existing branch or PR. Resume useful work instead of duplicating it. Choose the implementation plan, tools, and decomposition that fit the task. A repair round can use ordinary review findings without a structured failure artifact.

Keep changes focused on the requested result. Adapt the plan as facts emerge and keep the Issue accurate when the scope changes. Resolve material uncertainty with the user when necessary; do not require a separate `spec` invocation just to update wording or document an already authorized change.

Work on the task branch, preserve other changes, and implement the behavior with appropriate tests. Run the checks needed for the changed area, fix failures within scope, and explain any limitation that remains. Keep useful recovery notes in the conversation or Draft PR; no task packet is required.

Commit and push the implementation and create or update a Draft Product PR using the [Product PR template](product-pr-template.md) and [Hosting operations](hosting.md). Summarize the result, main changes, tests actually run, and relevant limitations. Mention useful memory candidates if any arose; no fixed category table is needed.

Return the PR link and test summary. A standalone invocation stops with the Draft PR. Within `delivery`, use this guidance as helpful and choose what to do next. If an external problem prevents completion, retain useful work and report what remains and where to resume.
