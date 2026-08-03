# Project Harness 维护指南

## 适用范围

本文件适用于仓库根目录及其全部子目录。子目录若增加更具体的 `AGENTS.md`，只能补充局部约定，不得削弱这里定义的项目边界、发布要求和兼容纪律。

## 项目定位

本仓库是跨 Agent 宿主的 `project-harness` Skill 独立规范源、实现源和版本化载体。主要交付物是 `project-harness/`；根级文件只管理仓库治理，不存放消费项目配置、真实任务状态或项目记忆。

Harness 的目标是让 Agent 稳定交付代码，而不是让审计协议成为主要工作。新任务的默认路径应保持精确授权和不可逆操作保护，同时把读取、验证、独立审查和持久评论控制在实际风险所需的最小范围。

本仓库负责：

- 精确角色调用、单阶段兼容入口和 `delivery` 编排；
- GitHub Issue 与 Product PR 的交付合同；
- Implementation、Closeout、按需 Context Promotion 和自动集成；
- Issue / Pull Request 原子传输、并发保护和写后回读；
- 兼容 artifact 的确定性解析、测试和迁移；
- Codex 与 Claude 的 Skill 展示和加载适配。

本仓库不负责：

- 采用 Harness 的业务项目；
- 通用项目管理或通用 GitHub 自动化；
- 消费项目 `.project-harness/config.yaml`、Execution Packet、Issue/PR 快照或实际项目记忆的托管；
- CC-Switch 刷新以及向 Codex/Claude 同步或启用 Skill。

## 工作范式

`init` 是生命周期外的项目配置操作。特性主路径是：

`definition` → 按需 `context-authoring` → `delivery`

新 `delivery` 默认使用 Lean 路径：

`implementation` → 精简 `closeout` → 产品 PR 合并 → `code-only` 直接关闭，或按需 `context-promotion` → 按需项目记忆 PR 合并 → Issue 关闭

- Definition 对清楚、低风险的需求只固化目标、边界和验收，不强制逐题 grilling 或独立合同 Reviewer。只有真正阻塞的产品决策才询问用户；高风险、含糊或仓库规则要求时才增加独立审查。
- Implementation 专注代码、测试和 Draft Product PR。验证应与改动和风险相称。
- Closeout 保持独立 Owner，但优先复用绑定当前 head 的 Implementation 验证和 required CI；只重跑缺失、过期、矛盾或风险要求的检查。
- Product PR 五类持久项目记忆影响均精确为 `无`，且 Closeout 持久 PASS 明确验证 `all-five-none` 时，Delivery 在产品合并后跳过 Context Promotion，直接执行 Issue 关闭门。
- 只有存在实际持久知识候选时才进入 Context Promotion。首次新 promotion 轮次若最终全为 `no_write`，直接返回 no-promotion，不创建提案、Reviewer PASS、确认回调或跨回合用户门；实际写入仍必须独立 review，并在合并前取得 source-bound 用户确认。
- 已持久化的 `awaiting-confirmation`、`confirmed`、Ready、terminal 或 legacy promotion lineage 必须继续按旧链恢复，不能用 Lean 快路径绕过。

`implementation`、`closeout` 和 `context-promotion` 保留为精确兼容/恢复入口，并在各自阶段边界停止。`external-review` 只是停止目的地，不是可执行角色。

## Agent 所有权与委派

每个阶段由一个隔离 Phase Owner 执行。`delivery` Coordinator 只做状态重建、阶段调度、原子集成、必要的用户交互和最终关闭；不得代行代码实现、验收裁决或项目记忆分类。

保持 `Coordinator → Phase Owner → 直接只读 Worker / 独立 Reviewer` 两跳拓扑：

- Phase Owner 是该语义轮次唯一写入者和 hand-off 生产者；
- Worker 与 Reviewer 不得写入、持久化 verdict 或继续委派；
- 相同角色、来源 tuple、证据 URL/digest、用户决策、mutation 集和目标持续复用同一 Owner；
- 慢读取、活跃工具、liveness 变化、Worker 失败或 Reviewer FAIL 不构成替换 Owner 的理由；
- 只有绑定语义输入/目标变化、Owner 明确终止或宿主确认上下文不可恢复时才创建新 Owner。

新委派只发送根 Skill 定义的紧凑 `delegation.schema_version: 3`：精确来源、Issue/PR tuple、必要持久证据 URL/digest、用户决策、允许的 mutation 和单一 `next_action`。不得传递完整评论清单、Evidence Bundle、component identity map、原始工具输出或聊天摘要。

仅为旧运行中仍存活的委派 dual-read schema-v2 Evidence Bundle；schema-v1 走历史 complete-fresh-read fallback。新调度不得生成 v1/v2。

## 目录职责

| 路径 | 唯一职责 |
| --- | --- |
| `project-harness/SKILL.md` | Skill 入口、角色调度、紧凑委派、共享授权和跨阶段不变量 |
| `project-harness/references/delivery.md` | Lean `delivery` 编排、恢复、自动合并、按需确认和最终关闭 |
| `project-harness/references/delivery-evidence-contract.md` | Closeout 与 Promotion 持久 artifact schema、Lean code-only 判定和 legacy dual-read |
| `project-harness/references/delivery-log-contract.md` | 冻结的历史 Delivery observation schema-v1，只读诊断，不是新路径门禁 |
| `project-harness/references/init.md` | 消费项目 Harness 配置创建与校验 |
| `project-harness/references/{definition,context-authoring,implementation,closeout,context-promotion}.md` | 各角色专属输入、行为、验证、输出和停止位置 |
| `project-harness/references/{issue,product-pr}-contract.md` | Issue / Product PR Body 的唯一结构契约 |
| `project-harness/references/*-transport.md` | GitHub 原子 I/O、并发保护、merge guard 和回读结果 |
| `project-harness/scripts/` | 无业务授权判断和网络副作用的确定性辅助机制及测试 |
| `project-harness/agents/openai.yaml` | Codex 展示信息与禁止隐式调用的宿主适配元数据 |
| `CLAUDE.md` | 将根级治理规则桥接给 Claude Code |

共享规则只在 `SKILL.md` 或对应共享契约中定义一次；阶段文件引用并落实，不复制平行 schema。传输协议只处理 I/O 一致性，不替角色做产品判断。

## 必须保持的设计不变量

1. 只接受当前用户消息明确提供的 `init`、`definition`、`context-authoring`、`delivery`、`implementation`、`closeout`、`context-promotion`；不推断、不设别名。Codex 需要 `$project-harness`，Claude 加载本身不补全角色、来源或 mutation authority。
2. Issue 是交付合同，Product PR 是实现与验证载体；持久知识只进入规定的单一权威层。
3. 权威 URL、仓库事实和显式授权不能由目录名、历史聊天、普通 hand-off 或模型记忆补全。内部委派只能从当前显式 `delivery` 缩小权限。
4. GitHub 写入必须保留高价值安全门：基线读取、更新前复查、一次 mutation、写后独立回读、受保护字段和规范化 digest。
5. 只有 `verified` 或 `no-op` 表示成功；部分、歧义、缺失和字段漂移均 fail closed。
6. 只有当前显式 `delivery` Coordinator 可按配置自动合并产品/项目记忆 PR。配置 schema-v2、schema-v1 唯一方法兼容、`develop` 集成基线和 `main` release/hotfix 边界保持不变。
7. 新 code-only 路径必须同时满足 Product PR 五类精确 `无`、Closeout PASS 的 `durable-memory-impact` / `all-five-none` 证据、无 promotion state、无相关 memory PR 和未漂移 tuple；任一缺失或含糊均不得跳过。
8. 新项目记忆写入必须保留独立 Reviewer、source-bound 用户确认、current-head required checks、mergeability、配置化 merge method、合并回读和 terminal reconciliation。
9. 三个 marker 名称保持不变；现有持久 schema 不覆盖、不重写，legacy lineage 只按已验证 dual-read 迁移。
10. `delivery-stage-observation` 是冻结的历史审计数据。新运行不得写、补录、修复、要求 coverage 或用其授权 phase、merge、closure、completion；Issue 关闭后不写 post-close observation。
11. 确定性脚本保持纯粹、标准库优先、可测试，不能隐藏产品或授权判断，也不能产生网络副作用。

以下仍是兼容性表面：精确角色名与公共输入、schema-v3 delegation 字段及 v1/v2 dual-read、配置 schema、marker、Issue/PR 标题顺序、transport envelope、Markdown digest、Closeout/Promotion 已持久 schema、阶段所有权和停止位置。历史 Delivery-log schema/算法保持可读但不再是新 producer 或完成门。

不得静默改变兼容性表面。确需变更时必须先说明影响和迁移策略，同步生产者、消费者、示例及测试；持久 marker/schema 变化还必须单独批准并验证 dual-read。

## Skill 更新工作流

**长任务执行前确认。** 在形成计划所需的最小只读勘察后，若任务较长，先向用户说明阶段、影响范围、验证方式和所有提交/发布写入，并等待明确确认。确认前不得修改文件、GitHub、提交或发布。

1. 将需求归类为文案澄清、兼容行为或兼容性变更，并明确迁移。
2. 完整阅读 `SKILL.md`、受影响阶段、共享契约及所有生产者/消费者。
3. 在唯一职责层做最小而完整的修改；行为变化同步测试。
4. 搜索受影响角色、字段、marker、标题、状态、成功门和 legacy 分支，确保无第二权威源。
5. 运行全部测试、Skill 结构检查、`git diff --check` 和人工协议核对。
6. 将通过验证的 `project-harness/` 发布到 CC-Switch 跟踪的稳定分支；兼容性变更记录迁移说明。
7. 报告来源、分支、commit、验证和兼容影响后停止。CC-Switch 刷新及两端同步由用户手动完成。
8. 仅当用户确认手动更新完成并明确要求时，才在新的 Codex/Claude 会话进行双端发现与调用验收。

修改 Markdown 时精确保留机器可识别的角色、字段、状态、marker、标题和代码块。修改 Python 时优先标准库、清晰纯函数和成对成功/失败测试。

不得生成或提交消费项目配置、Execution Packet、真实 GitHub 回调、任务临时文件或实际项目记忆。不得把 `__pycache__`、`.pyc`、`.DS_Store`、`*:Zone.Identifier`、编辑器或构建产物放入 Skill。

## 验证

从仓库根目录运行：

```bash
python3 -B -m unittest discover -s project-harness/scripts -p 'test_*.py' -v
git diff --check
```

文档或协议变更还要人工确认：

- 调度表、角色输入/输出和恢复路径与阶段文件一致；
- schema-v3 委派不扩权，v1/v2 只作 legacy；
- Lean code-only 所有正向条件同时满足，缺失/非 `无`/漂移/冲突路径全部保守升级或阻塞；
- 新 no-write classification 不创建 proposal、Reviewer、确认、terminal 或 Delivery log；实际 memory write 仍保留完整确认和 merge gate；
- 已有 promotion lineage 不会被快路径绕过；
- 新运行不写 Delivery observation、不要求 coverage、不因旧日志缺失阻止关闭；
- product/memory merge 都使用当前配置方法、当前 head checks、mergeability 和回读；
- Issue 仅在 code-only 或 promotion 终态的最终回读后关闭；
- 示例和 `agents/openai.yaml` 不承诺不存在的隐式行为；
- 没有平台元数据、临时文件或绝对本地路径进入 Skill。

即使只改文档，也必须运行现有测试。

## 完成标准

一次迭代只有在以下条件全部满足时完成：

- 变更位于正确职责层且没有重复权威；
- 新 Lean 路径和旧恢复路径生产者/消费者一致；
- 自动化与人工验证通过；
- 源版本已发布到稳定分支；
- 已向用户提供精确 CC-Switch 手动更新交接、兼容影响和遗留风险。
