# Project Harness 维护指南

## 适用范围

本文件适用于仓库根目录及其全部子目录。子目录若增加更具体的 `AGENTS.md`，只能补充局部约定，不得削弱这里定义的项目边界、发布要求和兼容纪律。

## 项目定位

本仓库是跨 Agent 宿主的 `project-harness` Skill 独立规范源、实现源和版本化载体。主要交付物是 `project-harness/`；根级文件只管理仓库治理，不存放消费项目配置、真实任务状态或项目记忆。

Harness 的目标是让 Agent 稳定交付代码，而不是让审计协议成为主要工作。v2 起，Harness 只定义阶段、产物和门；是否以及如何使用 subagent 是 Agent 自己的判断，Harness 不约束、不合同化。

本仓库负责：

- 两条交付路径：路径 1（plan → spec → implementation → review → context promotion）与路径 2（express 敏捷路径）；
- GitHub Issue 与 Product PR 的交付合同；
- Issue / Pull Request 原子传输、并发保护和写后回读；
- 合并门、显式 Issue 关闭和记忆写入的 source-bound 用户确认；
- 当前格式 artifact 的确定性解析、测试；
- Codex 与 Claude 的 Skill 展示和加载适配。

本仓库不负责：

- 采用 Harness 的业务项目；
- 通用项目管理或通用 GitHub 自动化；
- 消费项目 `.project-harness/config.yaml`、Issue/PR 快照或实际项目记忆的托管；
- v1 时代持久 artifact 的读取、迁移或恢复（见 `project-harness/MIGRATION.md` 的断代说明）；
- CC-Switch 刷新以及向 Codex/Claude 同步或启用 Skill。

## 工作范式

`init` 是生命周期外的项目配置操作。任务主路径只有两条：

路径 1（完整交付）：

`plan`（宿主原生规划能力 + 强制 grilling 追问 + 用户确认）→ `spec`（写成 Issue）→ `delivery`（implementation → review → 合并 Product PR → code-only 直接关闭，或 context-promotion → 合并 Memory PR → 关闭 Issue）

- plan 不是 Harness 角色：用宿主原生能力完成，但必须经 grilling 式逐题追问并由用户明确确认后才允许进入 `spec`。
- `spec` 把确认的计划固化成 Issue：紧凑 `改动范围`（普通任务写 `受保护改动：无`）、已确认决策、验收项。只有真正阻塞合同的产品决策才补充询问。
- `implementation` 专注代码、测试和 Draft Product PR。首次编辑前及最终 diff 完成后对照 Issue 的紧凑改动范围；未明确允许的重要改动一律返回 `spec`，不得静默扩权。
- `review` 只校验三件事：完整 diff 是否符合 Issue 边界（含受保护例外）、current-head 单元测试与 required checks、五类持久记忆影响判断是否成立。PASS 后写 verdict 并标记 Ready。
- Product PR 五类持久项目记忆影响均精确为 `无` 且 review PASS 明确验证 `all-five-none` 时，delivery 在产品合并后跳过 Context Promotion，直接执行 Issue 关闭门。
- 只有存在实际持久知识候选时才进入 Context Promotion；首轮全 `no_write` 直接返回 ephemeral no-promotion；实际写入必须取得 source-bound 跨回合用户确认后才合并。

路径 2（express 敏捷）：

一句话确认范围 → 从 `develop` 切分支 → 实现 + 单元测试 → 轻量 PR → merge gate（required checks、mergeability、配置 merge method、tuple、空 evidence 集）→ 合并 → 总结（记忆候选只提示不写入）。

- express 只服务普通业务改动；任何受保护表面改动必须停止并升级路径 1。
- express 无 Issue、无独立 review 阶段、无 Context Promotion 流程。

路径选择：用户给出原始需求而无精确角色时，agent 按任务规模/风险建议路径并给出一句理由，用户确认一次；精确角色调用始终绕过选择。

`implementation`、`review` 和 `context-promotion` 保留为精确单阶段/恢复入口，并在各自阶段边界停止。

## Subagent 使用不受约束

v2 删除了 v1 的全部编排合同：固定两跳拓扑、Phase Owner/Worker/Reviewer 规则、delegation schema、逐阶段 mutation envelope、Owner 复用规则。当前约定只有三条：

- 每个阶段由当前调用（delivery 或精确单阶段角色）负责到底，阶段产物与门不因内部如何分工而改变；
- agent 自行决定何时启动 subagent、给什么上下文；委派结果必须自己整合验证；
- merge 与 Issue 关闭的权限边界按角色调用界定（见不变量 6），与是否使用 subagent 无关。

不得在新文本中恢复任何隐式编排要求。

## 目录职责

| 路径 | 唯一职责 |
| --- | --- |
| `project-harness/SKILL.md` | Skill 入口、角色调度、路径选择、共享授权和跨阶段不变量 |
| `project-harness/references/delivery.md` | 路径 1 端到端编排、状态重建、自动合并、按需确认和最终关闭 |
| `project-harness/references/evidence-contract.md` | review verdict 与 promotion 持久 artifact schema、code-only 判定、active lineage 规则 |
| `project-harness/references/init.md` | 消费项目 Harness 配置创建与校验 |
| `project-harness/references/{spec,implementation,review,context-promotion,express}.md` | 各角色专属输入、行为、验证、输出和停止位置 |
| `project-harness/references/{issue,product-pr}-contract.md` | Issue / Product PR Body 的唯一结构契约 |
| `project-harness/references/*-transport.md` | GitHub 原子 I/O、并发保护、merge guard 和回读结果 |
| `project-harness/scripts/` | 无业务授权判断和网络副作用的确定性辅助机制及测试 |
| `project-harness/agents/openai.yaml` | Codex 展示信息与禁止隐式调用的宿主适配元数据 |
| `project-harness/MIGRATION.md` | v1 → v2 断代说明 |
| `CLAUDE.md` | 将根级治理规则桥接给 Claude Code |

共享规则只在 `SKILL.md` 或对应共享契约中定义一次；阶段文件引用并落实，不复制平行 schema。传输协议只处理 I/O 一致性，不替角色做产品判断。

## 必须保持的设计不变量

1. 只接受当前用户消息明确提供的 `init`、`spec`、`implementation`、`review`、`context-promotion`、`delivery`、`express`；不设别名。无精确角色的原始需求走"agent 建议 + 用户确认"的路径选择，不静默推断。Codex 需要 `$project-harness`，Claude 加载本身不补全角色、来源或 mutation authority。
2. Issue 是交付合同，Product PR 是实现与验证载体；Issue 的紧凑 `改动范围` 是产品改动的唯一授权源；8 类受保护表面只在 `issue-contract.md` 集中定义并默认禁止；express 绝对禁止受保护表面，违者升级路径 1。
3. 权威 URL、仓库事实和显式授权不能由目录名、历史聊天、普通 hand-off 或模型记忆补全。
4. GitHub 写入必须保留 L2 安全门：基线读取、更新前复查、一次 mutation、写后独立回读、受保护字段和规范化 digest。
5. 只有 `verified` 或 `no-op` 表示成功；部分、歧义、缺失和字段漂移均 fail closed。
6. merge gate 保留 L3：exact tuple、`required_checks_known: true` 且 required checks 全绿、affirmative mergeability、配置化 merge method、base `develop`、协议拥有的固定 evidence key 集（product=`review-pass`；memory=`proposal`+`confirmation`；express=空集）。只有当前显式 `delivery` 可合并 product/memory PR 并关闭 Issue；只有当前显式 `express` 可合并自己的轻量 PR。禁止 closing keywords，Issue 以显式 `change-metadata` 关闭并回读 `closed/completed`。
7. 项目记忆实际写入必须保留 split-turn source-bound 用户确认（proposal URL + whole-comment digest，approved/revise/pause）；不强制独立 Reviewer；首轮全 `no_write` 不创建任何 artifact。
8. code-only 快路径必须同时满足：五类精确 `无`、review PASS 的 `durable-memory-impact`/`all-five-none` 证据、无任何当前格式 promotion state、无 source-linked memory PR；任一缺失或含糊均进入 promotion 分类。
9. 唯一 marker 为 `${marker_namespace}:context-promotion`；当前格式持久 schema（review verdict、proposal artifact、awaiting-confirmation、confirmed、memory-pr-merged、no-promotion）不覆盖、不重写、不静默扩字段。
10. v2 与 v1 断代：不读取、不解释、不迁移 v1 持久 artifact（eligibility registration、Reviewer PASS、validation-impact、delivery-stage-observation、unversioned/schema-v2 legacy callback 等）；在途 v1 任务按 `MIGRATION.md` 收尾。
11. 确定性脚本保持纯粹、标准库优先、可测试，不能隐藏产品或授权判断，也不能产生网络副作用。

以下是兼容性表面：精确角色名与公共输入、路径选择协议、配置 schema、单一 marker、Issue/PR 标题顺序与 Issue 改动范围语义、transport envelope、Markdown digest、evidence-contract 当前格式 schema、merge evidence key 集、阶段停止位置。v1 持久格式与编排合同不再是兼容表面。

不得静默改变兼容性表面。确需变更时必须先说明影响和迁移策略，同步生产者、消费者、示例及测试；持久 marker/schema 变化还必须单独批准。

## Skill 更新工作流

**长任务执行前确认。** 在形成计划所需的最小只读勘察后，若任务较长，先向用户说明阶段、影响范围、验证方式和所有提交/发布写入，并等待明确确认。确认前不得修改文件、GitHub、提交或发布。

1. 将需求归类为文案澄清、行为调整或兼容性变更，并明确迁移。
2. 完整阅读 `SKILL.md`、受影响阶段、共享契约及所有生产者/消费者。
3. 在唯一职责层做最小而完整的修改；行为变化同步测试。
4. 搜索受影响角色、字段、marker、标题、状态、成功门，确保无第二权威源。
5. 运行全部测试、Skill 结构检查、`git diff --check` 和人工协议核对。
6. 将通过验证的 `project-harness/` 发布到 CC-Switch 跟踪的稳定分支；兼容性变更记录迁移说明。
7. 报告来源、分支、commit、验证和兼容影响后停止。CC-Switch 刷新及两端同步由用户手动完成。
8. 仅当用户确认手动更新完成并明确要求时，才在新的 Codex/Claude 会话进行双端发现与调用验收。

修改 Markdown 时精确保留机器可识别的角色、字段、状态、marker、标题和代码块。修改 Python 时优先标准库、清晰纯函数和成对成功/失败测试。

不得生成或提交消费项目配置、真实 GitHub 回调、任务临时文件或实际项目记忆。不得把 `__pycache__`、`.pyc`、`.DS_Store`、`*:Zone.Identifier`、编辑器或构建产物放入 Skill。

## 验证

从仓库根目录运行：

```bash
python3 -B -m unittest discover -s project-harness/scripts -p 'test_*.py' -v
git diff --check
```

文档或协议变更还要人工确认：

- 调度表、角色输入/输出和恢复路径与阶段文件一致；
- 两条路径文本与路径选择协议一致，express 的受保护表面升级规则明确；
- spec 的 grilling 前置明确；普通任务 Issue 只需紧凑改动范围和 `受保护改动：无`；
- review 三项校验（issue-scope、unit-tests、durable-memory-impact）与 evidence-contract 的 verdict schema 一致；
- code-only 所有正向条件同时满足，缺失/非 `无`/漂移/冲突路径全部保守升级或阻塞；
- 首轮 no-write classification 不创建 proposal、确认、terminal；实际 memory write 保留 source-bound 确认和 merge gate；
- 已有当前格式 promotion lineage 不会被快路径绕过；
- product/memory/express merge 都使用当前配置方法、当前 head checks、mergeability、固定 evidence key 集和回读；
- Issue 仅在 code-only 或 promotion 终态的最终回读后关闭；
- 示例和 `agents/openai.yaml` 不承诺不存在的隐式行为；
- 没有平台元数据、临时文件或绝对本地路径进入 Skill。

即使只改文档，也必须运行现有测试。

## 完成标准

一次迭代只有在以下条件全部满足时完成：

- 变更位于正确职责层且没有重复权威；
- 新路径的生产者/消费者一致；
- 自动化与人工验证通过；
- 源版本已发布到稳定分支；
- 已向用户提供精确 CC-Switch 手动更新交接、兼容影响和遗留风险。
