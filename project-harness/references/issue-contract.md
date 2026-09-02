# Issue Delivery Contract

Load this shared artifact contract only when the selected operation row in the root Skill names the Issue contract.

Treat this file as the sole authoritative schema for the source Issue Body. Keep the headings and order exact, replace every placeholder with task-specific content, and do not publish guidance comments or empty placeholder rows. Do not look for or create a platform Issue template.

## Field rules

- `原始需求 / 问题背景` preserves the original problem, affected user or system, and desired outcome without copying the conversation or substituting an implementation.
- `目标`, `非目标与边界` (including its `改动范围`), `已确认决策`, and `验收与验证` form the binding delivery contract.
- Put one compact `### 改动范围` subsection inside `非目标与边界`. Describe the ordinary business behavior, modules, or code areas that may change, then use the exact field `受保护改动`. For an ordinary task, write exactly `受保护改动：无`; do not ask the user to approve an empty category checklist.
- Treat architecture or module boundaries, public APIs, DTOs or serialization, databases or migrations, message protocols, configuration formats, security or permissions, and core dependencies or frameworks as protected surfaces. This list is authoritative for every phase. An Issue authorizes a protected change only when `受保护改动` names the surface and states the exact allowed change plus its compatibility or migration boundary. A broad phrase such as “允许相关调整” is invalid. `受保护改动：无`, an omitted surface, or an ambiguous exception means that protected change is forbidden; the ordinary-business line, implementation plan, Product PR, or an ADR cannot expand it.
- `按需读取的项目记忆 / 代码事实` lists only sources that materially changed the contract and the conclusion obtained from each.
- `合并后 Context Promotion 候选` records non-binding leads only. It never promises a durable write.
- `confirmed` is required for decisions affecting goals, boundaries, external behavior, constraints, or acceptance. Use `assumed` only for reversible low-risk implementation details and `deferred` only for non-blocking future or externally controlled matters; record the risk and reopening trigger.
- `实施计划` is a non-binding starting prediction and never grants change authority. Return to `spec` when an implementation discovery changes the binding contract or requires a protected change not explicitly allowed by `改动范围`.

The compact `改动范围` subsection identifies the current Issue format. Publish it for every new `spec`. Before continuing an open, unmerged legacy task, return to `spec` and add the subsection to the same Issue. Do not bulk-migrate history or rewrite an old Issue solely for this format after its product Pull Request has merged; such a lineage may only complete its existing read-only recovery and closure path without new product-code mutation.

## Exact Body shape

~~~markdown
## 原始需求 / 问题背景

<最初要解决的问题、受影响对象与期望结果>

## 目标

<可验证的行为结果>

## 非目标与边界

<明确不做的内容及兼容性、安全、性能或交付限制>

### 改动范围

- 普通业务改动：<允许修改的业务行为、模块或代码区域>
- 受保护改动：<精确填写“无”，或逐条写明受保护表面、允许的具体变化及兼容/迁移边界>

## 按需读取的项目记忆 / 代码事实

| 来源 | 为什么此刻需要 | 获得的结论 |
| --- | --- | --- |
| <精确来源> | <需要原因> | <采用结论> |

## 持久项目记忆影响

### 合并后 Context Promotion 候选

- `decision`：<候选或无>
- `stable_rule`：<候选或无>
- `wiki_knowledge`：<候选或无>
- `stable_context`：<候选或无>
- `milestone_evidence`：<候选或无>

## 已确认决策

| 决策 | 选择 | 理由 | 状态 |
| --- | --- | --- | --- |
| <决策> | <选择> | <理由及风险/重开条件> | confirmed / assumed / deferred |

## 实施计划

1. <受影响区域、依赖顺序、阶段结果和所需测试>

## 验收与验证

- [ ] <可执行的验收或验证项>
~~~
