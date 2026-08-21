# Product Pull Request Evidence Contract

Load this shared artifact contract only when the selected operation row in the root Skill names the Product PR contract.

Treat this file as the sole authoritative schema for the product Pull Request Body. Keep the headings and order exact, replace every placeholder with source-bound evidence, and do not publish guidance comments or empty placeholder rows. Do not use this contract for project-memory-only Pull Requests, and do not look for or create a `.github` Pull Request template.

## Field rules

- Use a plain `Refs` link to associate the source Issue. Do not use a closing keyword; the authorized `delivery` owns explicit closure after the selected code-only or promotion path.
- Bind the exact Issue Body digest, product head SHA, and integration base ref/SHA.
- Record observable results, actual changes, plan deviations, executable verification evidence, and known limitations without copying the Issue contract.
- Treat the Issue `改动范围` as the only task-level change authority. The Product PR records what happened and cannot grant, broaden, or repair permission through `主要改动`, a plan deviation, review text, or later evidence.
- When the final diff contains an explicitly authorized protected change, add one concise bullet under `主要改动` that names the actual change and points to the exact Issue `受保护改动` exception that authorizes it. When no protected change occurred, add no mapping table, empty field, or extra ceremony.
- Bind every reported validation result to the final product head SHA. Identify an immutable CI run when applicable; do not present a command run against an earlier code snapshot as current-head evidence.
- Classify the actual durable-memory impact from evidence. Use the exact literal `无` in the **实际影响** cell for a category with no impact; ordinary code-discoverable implementation details do not require a durable write and therefore use `无` here.
- Treat the five-row table as a candidate for the code-only fast path, not as self-approval. The `review` role must independently compare it with the exact diff and authoritative sources.
- Recognize `all-five-none` only when all five required categories are present exactly once, every **实际影响** value is exactly `无`, and every evidence cell contains a factual non-placeholder reason or source. Do not treat `none`, `no_write`, `N/A`, a blank, a missing row, or vague wording as equivalent to `无`.
- When any category has an actual durable effect, describe that concrete effect and its evidence instead of forcing `无`. Any non-`无`, missing, or ambiguous category makes Context Promotion conservatively required until `review` resolves or rejects the evidence.
- Mark every completion item truthfully. Leave the product PR Draft when any item is false.
- Leave `Review` empty in the Body. The `review` role writes its verdict as a top-level PR comment.

## Exact Body shape

~~~markdown
## 关联任务

Refs <source Issue URL>

## 实施基线

- Issue Body SHA-256：<SHA256>
- Head SHA：<COMMIT>
- Base branch / SHA：<REF> / <COMMIT>

## 结果

<实现后调用方可观察到的行为>

## 主要改动

- <实际改动>

## 计划偏差与原因

<偏差与原因，或无>

## 验证证据

| 命令 / 检查 | 结果 |
| --- | --- |
| <可复现命令或检查> | <结果及关键证据> |

## 已知限制与风险

- <限制或风险，或无>

## 持久项目记忆实际影响

| 类别 | 实际影响 | 证据 |
| --- | --- | --- |
| `decision` | <具体影响或精确填写“无”> | <证据；无影响时填写事实理由> |
| `stable_rule` | <具体影响或精确填写“无”> | <证据；无影响时填写事实理由> |
| `wiki_knowledge` | <具体影响或精确填写“无”> | <证据；无影响时填写事实理由> |
| `stable_context` | <具体影响或精确填写“无”> | <证据；无影响时填写事实理由> |
| `milestone_evidence` | <具体影响或精确填写“无”> | <证据；无影响时填写事实理由> |

## 完成声明

- [ ] Issue 的绑定合同已完整实现。
- [ ] 所需验证已通过。
- [ ] 没有已知未完成项。
- [ ] 持久项目记忆实际影响已逐类填写证据或明确标记为“无”。
- [ ] 临时 `.project-memory/tasks/` Execution Packet 已从最终 diff 移除，或本任务未创建。

## Review
~~~
