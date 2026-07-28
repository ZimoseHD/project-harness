# Product Pull Request Evidence Contract

Load this shared artifact contract only when the selected operation row in the root Skill names the Product PR contract.

Treat this file as the sole authoritative schema for the product Pull Request Body. Keep the headings and order exact, replace every placeholder with source-bound evidence, and do not publish guidance comments or empty placeholder rows. Do not use this contract for proposed-decision or project-memory-only Pull Requests, and do not look for or create a `.github` Pull Request template.

## Field rules

- Use a plain `Refs` link to associate the source Issue. Do not use a closing keyword; Context Promotion owns the closure judgment, and only its standalone role or the authorized `delivery` coordinator performs the explicit close mutation.
- Bind the exact Issue Body digest, product head SHA, and integration base ref/SHA.
- Record observable results, actual changes, plan deviations, executable verification evidence, and known limitations without copying the Issue contract.
- Classify the actual durable-memory impact from evidence. Use `无` for a category with no impact; ordinary code-discoverable implementation details are `no_write`.
- Mark every completion item truthfully. Leave the product PR Draft when any item is false.
- Leave `Closeout` empty in the Body. The independent Closeout role writes its verdict as a top-level PR comment.

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
| `decision` | <影响或无> | <证据或不适用> |
| `stable_rule` | <影响或无> | <证据或不适用> |
| `wiki_knowledge` | <影响或无> | <证据或不适用> |
| `stable_context` | <影响或无> | <证据或不适用> |
| `milestone_evidence` | <影响或无> | <证据或不适用> |

## 完成声明

- [ ] Issue 的绑定合同已完整实现。
- [ ] 所需验证已通过。
- [ ] 没有已知未完成项。
- [ ] 持久项目记忆实际影响已逐类填写证据或明确标记为“无”。
- [ ] 临时 `.project-memory/tasks/` Execution Packet 已从最终 diff 移除，或本任务未创建。

## Closeout
~~~
