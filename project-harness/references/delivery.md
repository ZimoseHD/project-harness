# Delivery

Deliver the task autonomously. Keep four core aspects in view:

- **Plan-mode start:** Launch delivery in Harness's plan mode before making changes. Form a delivery plan and establish a clear task state machine (milestones, execution stages, and acceptance criteria) from the Issue to anchor focus and sharpen model attention.
- **Issue:** Read the Issue to understand the task, desired outcome, and relevant context.
- **Reviewer:** Involve a reviewer to examine the work. Choose the reviewer and timing to suit the task; use [Review](review.md) to scale coverage and choose a review method, including when calling another review skill.
- **Context promotion:** Include [Context Promotion](context-promotion.md) in the work. Preserve useful knowledge for future tasks; when there is nothing worth recording, say so briefly.

## Orchestration and subagent lifecycle

The primary agent primarily acts as the maintainer of the task state machine. Keep heavy analysis, wide file reads, code modifications, and trial-and-error execution delegated to subagents rather than accumulating raw investigation and tool outputs in the primary context:

- **Isolated execution:** Subagents run in isolated child contexts or environments. Raw file dumps, verbose command outputs, and intermediate repair loops remain contained inside the subagent's scope.
- **Lifecycle reclamation:** Upon completing a delegated assignment, the subagent returns only a compact high-level summary—core conclusions, modified file paths/ranges, verification status, and remaining blockers. The subagent's child context and intermediate execution history are immediately reclaimed and discarded, preventing internal noise from leaking into the primary context.

## Active context management

To prevent context bloat and reasoning degradation across both the primary agent and long-running subagents:

- Periodically check own context length against model capabilities.
- When context becomes excessive (exceeding 500k tokens or approaching the host's safe working threshold), actively compact the context.
- Retain the core objective, current state machine position, critical decisions, affected paths, and active blockers; collapse or discard obsolete tool outputs, intermediate scratch logs, and superseded discussion into a compact checkpoint.

Decide the implementation approach, iteration depth, and completion actions using the task and the user's authorization. Other phase references are resources to draw on.
