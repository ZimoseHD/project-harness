# Migration: v1 → v2

v2 是一次刻意的**断代发布**。它删除了 v1 的 subagent 编排合同和全部 legacy 持久证据兼容层，把流程收敛为两条路径。本文件说明断代内容和在途工作的收尾方式。

## 路径变化

- 路径 1：`plan`（宿主原生 + 强制 grilling + 用户确认）→ `spec` → `implementation` → `review` → `context-promotion`，由 `delivery` 端到端协调。
- 路径 2：`express`——免 Issue 的敏捷路径，口述需求 → 代码+测试 → 轻量 PR → 合并。

## 角色改名与删除

| v1 | v2 | 说明 |
| --- | --- | --- |
| `definition` | `spec` | 改名；前置条件改为"计划已 grilling 并经用户确认"；删除独立 Reviewer 轮次 |
| `closeout` | `review` | 改名并精简为三项校验：Issue 边界、current-head 单元测试、五类记忆影响 |
| `context-authoring` | （删除） | 实现前 ADR 门取消；决策类持久知识一律走 `context-promotion` |
| `init` / `implementation` / `context-promotion` / `delivery` | 保留 | 语义精简但角色名不变 |
| — | `express`（新增） | 路径 2 |

## 删除的机制

- 固定两跳拓扑（Coordinator → Phase Owner → Worker/Reviewer）、delegation schema v1/v2/v3、逐阶段 mutation envelope、Owner 复用规则。subagent 使用改为 agent 自主判断。
- `evidence_bundle.py` 及 schema-v2 delegation dual-read。
- `delivery_log.py`、`delivery-log-contract.md` 与全部 `delivery-stage-observation` 处理。
- `validation_impact.py`（advanced-base 验证复用）：memory PR 一律要求 current-head 验证。
- `context_review_input.py` 与强制独立 Reviewer：memory 写入的唯一批准门是 source-bound 用户确认。
- Product acceptance Issue callback 与 `context-promotion-eligible` eligibility registration。
- marker 从三个收缩为一个：`${marker_namespace}:context-promotion`。

## 持久证据断代

v2 不读取、不解释、不迁移任何 v1 持久 artifact，包括：

- `closeout-pass` / Issue callback / eligibility registration 评论；
- Reviewer PASS、validation-impact artifact；
- unversioned 或 schema-v2 的 promotion callback（`awaiting-confirmation`、`confirmed`、`memory-pr-ready`、`memory-pr-merged`、`no-promotion`）；
- `delivery-stage-observation` 评论。

v2 的 merge evidence key 集已改变：product=`review-pass`，memory=`proposal`+`confirmation`，express=空集。新 artifact 格式见 `references/evidence-contract.md`（proposal artifact 升为 `artifact_schema_version: 2`，callback 不再携带 schema_version/legacy 字段）。

## 在途 v1 任务如何收尾

- **Draft/Ready 未合并的 Product PR**：用 v1 版 Skill 完成交付；或人工核对 diff 符合 Issue 后手动合并、关闭 Issue。
- **已合并但未走 promotion/关闭的 lineage**：人工确认无持久记忆候选后直接关闭 Issue；有候选时人工整理记忆并关闭。
- **等待确认的 promotion 提案（awaiting-confirmation）**：人工审阅提案，接受则手动合并 memory PR，然后关闭 Issue。
- v2 遇到任何 v1 artifact 时将其视为普通历史评论，不作为工作流状态；同一 Issue 若要以 v2 重新交付，按 `spec` 更新 Issue 后走新路径（v1 已合并的 lineage 不允许再发生产品代码 mutation 的规则不变）。

## 消费项目配置

`.project-harness/config.yaml` 的 schema v1/v2 解析不变，无需迁移。唯一变化：`marker_namespace` 的保留后缀列表收缩为 `context-promotion`；既有 namespace 不受影响。
