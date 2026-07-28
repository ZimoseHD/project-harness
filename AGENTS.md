# Project Harness 维护指南

## 适用范围

本文件适用于仓库根目录及其全部子目录。若未来某个子目录增加更具体的 `AGENTS.md`，则该文件只补充局部约定，不得削弱这里定义的项目边界和兼容性要求。

## 项目定位

本仓库是跨 Agent 宿主的 `project-harness` Skill 工作范式独立规范源、实现源和版本化载体。它负责迭代并交付一套兼容 Agent Skills 目录格式、可由 CC-Switch 分发到 Codex 与 Claude 的 Skill，用明确的角色、权威输入、持久产物、验证证据和隔离 Agent 交接来约束一次特性从定义到实现、验收、知识沉淀及 Issue 关闭的全过程。

本仓库管理的是工作范式本身，包括：

- Skill 的显式调用契约、单阶段调度和多 Agent 交付编排；
- `init` 初始化操作、五个特性迭代阶段以及 `delivery` 多 Agent 编排入口；
- GitHub Issue 与 Product PR 的文档契约；
- GitHub Issue / Pull Request 的内部原子传输协议；
- `delivery` 各环节耗时、修改项和证据摘要的持久审计观察；
- Markdown 摘要、并发基线保护、幂等判断和回读验证等确定性工具；
- Skill 的展示元数据、自动化测试和兼容性约束。

本仓库不是：

- 采用 Harness 的具体业务项目；
- 通用项目管理框架或通用 GitHub 自动化工具；
- 某次需求、Issue、PR、执行状态或项目记忆的存储位置；
- 消费项目 `.project-harness/config.yaml` 的托管位置。

仓库的主要交付物是 `project-harness/` 目录。维护该目录是在演进 Skill；除非用户通过宿主对应语法显式调用该 Skill（Codex 为 `$project-harness`，Claude Code 为 `/project-harness`）并提供规定输入，否则不得把普通的仓库维护任务误判为某个 Harness 运行阶段。

## 工作范式

`init` 是生命周期外的项目配置操作。特性迭代的主路径是：

`definition` → 按需 `context-authoring` → `delivery`

`delivery` 在一次显式调用中由协调 Agent 自动编排：

`implementation` → `closeout` → 产品 PR 合并 → `context-promotion` → 按需项目记忆 PR 合并 → Issue 关闭

`implementation`、`closeout` 和 `context-promotion` 仍是精确的兼容/恢复入口。它们保留各自阶段边界，不自动获得 `delivery` 的合并权限。`external-review` 仍是 `context-authoring` 及兼容阶段入口的停止和交接目的地，不是可执行角色。

Skill 运行时的每个阶段 Agent 必须一次只执行一个精确角色并在角色边界停止。`delivery` 协调 Agent 不得代行阶段语义，而应自动创建隔离的阶段 Agent、消费经持久证据绑定的最小 hand-off，并在相同顶层调用中推进后续阶段；不得要求用户为正常阶段迁移手工创建新会话。独立 Reviewer 和每轮重新审查同样使用新的隔离 Agent 上下文。聊天摘要、普通 hand-off 或隐式记忆不能补全权威事实和写权限。

`delivery` 协调 Agent 在每个有持久证据的受界定尝试或成功边界后，把耗时质量、分域修改项预览和证据绑定为 Source Issue 上的版本化阶段观察。观察仅用于审计和统计，不是第四个 workflow marker，不能充当状态恢复、授权、PASS、合并或语义关闭证据；完整观察覆盖只是 Delivery 自身的合规完成门禁。实时运行可记录单调时钟实测耗时，恢复与补录不得伪造历史时长。Issue 关闭后还要追加 `issue-closed` 观察并确认 Issue 仍保持关闭；若评论被锁定，只能保留关闭状态并恢复日志，禁止重开。

维护 Skill 源码时则应读取所有受影响的生产者、消费者和共享契约，以保证跨文件一致性。不要把“运行时只加载一个操作”的限制错误套用为“维护时只检查一个文件”。

## 目录职责

| 路径 | 唯一职责 |
| --- | --- |
| `project-harness/SKILL.md` | Skill 入口、精确角色调度、共享规则和跨阶段不变量 |
| `project-harness/references/delivery.md` | `delivery` 顶层协调器、阶段恢复、受限委派、自动合并、结构化用户确认和最终关闭协议 |
| `project-harness/references/delivery-evidence-contract.md` | Closeout 与 Context Promotion 跨阶段持久证据的唯一 schema、tuple/digest 绑定、前驱链、active-tip 与 legacy dual-read 契约；不拥有阶段行为或写权限 |
| `project-harness/references/delivery-log-contract.md` | `delivery` 阶段观察的唯一 schema、计时质量、修改项、幂等身份、隐私与覆盖规则 |
| `project-harness/references/init.md` | 消费项目 Harness 配置的创建与校验协议 |
| `project-harness/references/{definition,context-authoring,implementation,closeout,context-promotion}.md` | 各角色独有的输入、边界、动作、验证、输出和交接协议 |
| `project-harness/references/issue-contract.md` | GitHub Issue Body 的唯一结构契约 |
| `project-harness/references/product-pr-contract.md` | Product PR Body 的唯一结构契约 |
| `project-harness/references/*-transport.md` | GitHub Issue / PR 原子操作、并发保护和回读结果协议 |
| `project-harness/scripts/` | 无业务语义决策的确定性辅助机制及其测试 |
| `project-harness/agents/openai.yaml` | Codex 展示信息和禁止隐式调用的宿主适配元数据，不得成为核心语义的唯一来源 |
| `CLAUDE.md` | 将根级 `AGENTS.md` 桥接给 Claude Code，避免维护两份仓库规则 |

共享规则只在 `SKILL.md` 或对应共享契约中定义一次；阶段文件引用并落实共享规则，不复制出容易漂移的平行版本。阶段专属行为只放在对应角色文件。传输协议只处理 I/O 一致性，不替角色做产品判断。

## 必须保持的设计不变量

1. 只接受 `init`、`definition`、`context-authoring`、`delivery`、`implementation`、`closeout`、`context-promotion` 这些精确角色，不推断、不设别名、不隐式调用。
2. Issue 是交付合同，Product PR 是实现结果和证据载体；持久知识只进入规定的单一权威层。
3. 每个阶段 Agent 只执行一个操作。`delivery` 协调 Agent 只做编排、原子集成和用户交互；阶段迁移、独立 Reviewer 和重新审查使用新的隔离 Agent。
4. 权威 URL、当前仓库事实和显式授权不可由目录名、仓库状态、历史会话或普通 hand-off 猜测。内部委派只能从当前显式 `delivery` 调用逐层缩小，并绑定精确来源、快照、持久证据和允许的 mutation。
5. GitHub 写入遵循内部 transport：规范化内容、绑定摘要、保护基线、写前复查、原子变更和独立回读。
6. 只有 `verified` 或 `no-op` 表示成功；部分成功、歧义、证据缺失和字段不匹配都必须 fail closed。
7. 阶段 Agent 都在合并前停止，不得推断 merge authority。只有当前显式 `delivery` 调用的协调 Agent 可按内部 transport 合并已绑定且通过全部门禁的产品 PR 和项目记忆 PR；合并方法必须来自权威仓库策略。产品与项目记忆的集成基线是 `develop`，`main` 保留给 release/hotfix 流程。
8. 确定性脚本保持纯粹、可测试，不能隐藏授权判断、产品判断或网络副作用。
9. Delivery 阶段观察只能由当前协调 Agent 在 Source Issue 上追加并独立回读；它们不带 `${marker_namespace}` marker、不得成为流程权威或被写入项目记忆，也不得持久化原始用户输入、聊天推理、工具日志、secret 或绝对本地路径。

以下内容属于跨版本兼容性表面：

- 精确角色名、调用包字段、内部 delegation 字段和 hand-off 字段；
- `.project-harness/config.yaml` 路径、`schema_version` 和 `marker_namespace` 规则；
- 三个持久 marker 的名称、生产者和消费者；
- Issue / Product PR Body 的标题、顺序和必填语义；
- transport 结果 envelope、成功状态、merge 操作和受保护字段；
- Markdown 规范化及 SHA-256 摘要算法；
- 各阶段及 `delivery` 的权威输入、持久输出、权限边界、自动恢复和停止位置；
- Closeout verdict/Issue callback/eligibility registration 与 Context Promotion 提案、Reviewer PASS、schema-v2 confirmation/Ready/terminal 回调的字段、marker、tuple/digest 绑定、前驱关系、active-tip 和 legacy dual-read 行为；
- Context Promotion 结构化用户确认和 Issue 关闭顺序；
- Delivery log 的 schema 版本、阶段/边界枚举、`attempt_id`、`transition_key` 算法、计时与分域修改质量、修改项上限、隐私边界、三层覆盖和关闭后观察规则。

不得静默改变兼容性表面。确需变更时，应先说明影响范围和迁移策略，同步所有生产者、消费者、示例及测试；marker 或已持久化 schema 的变更还必须具备单独批准的兼容迁移和验证过的 dual-read 行为。

## Skill 更新工作流

1. **确定变更类型。** 将需求归类为文案澄清、兼容行为变更或兼容性变更。兼容性变更必须先明确影响范围和迁移方案。
2. **修改唯一源。** 只在 `project-harness/` 中维护可分发 Skill；根级文件只负责仓库治理。先完整阅读 `SKILL.md`、直接受影响的角色文件及其共享契约，再在唯一职责层做最小且完整的修改。
3. **联动检查。** 搜索受影响的角色、字段、marker、Body 标题、状态及其生产者和消费者。行为变化必须同步更新相应测试。
4. **本地验证。** 运行现有测试和 Skill 结构校验，确认引用完整、失败路径保持 fail closed，且没有临时文件或平台元数据进入 Skill。
5. **发布源版本。** 将通过验证的 `project-harness/` 发布到 CC-Switch 当前跟踪的稳定分支。兼容性变更同时记录迁移说明；若项目采用 Git tag 或 Release，则仅把它们作为审计记录，不在多个文件中维护平行版本号。
6. **执行更新。** 在 CC-Switch 中刷新来源，确认 `project-harness` 出现更新，执行更新，并同步或启用到 Codex 与 Claude。
7. **双端验收。** 分别在新的 Codex 和 Claude 会话中确认 Skill 可发现、只能显式调用、精确角色输入能进入对应操作，缺失或错误角色会保守拒绝。任一端失败都不算发布完成；修复后从第 2 步重新执行。
8. **记录结果。** 记录发布来源、验证结果、兼容性影响和遗留风险。

修改 Markdown 协议时，精确保留机器可识别的角色名、字段名、状态值、marker、模板标题和代码块结构。修改 Python 时优先使用标准库、类型清晰的纯函数和正常路径/失败路径成对测试，除非任务明确批准新的依赖或副作用。

不要在本仓库中生成或提交消费项目的 `.project-harness/config.yaml`、Execution Packet、真实 GitHub 回调快照、任务级临时文件或实际项目记忆。不得把 `__pycache__`、`.pyc`、`.DS_Store`、`*:Zone.Identifier`、编辑器文件或构建产物放入 Skill 目录。

## 验证

从仓库根目录运行：

```bash
python3 -B -m unittest discover -s project-harness/scripts -p 'test_*.py' -v
```

文档或协议变更还必须人工确认：

- `SKILL.md` 调度表中的角色、引用、权威输入、输出和恢复路径仍与角色文件一致；
- 共享契约只有一个权威定义，引用方没有形成第二份 schema；
- marker、配置 schema、digest 和 transport 状态的生产者与消费者一致；
- `delivery` 可从每个已持久状态幂等恢复，内部 delegation 不会扩权，且阶段 Agent / sub-subagent 仍保持职责隔离；
- 产品 PR 与项目记忆 PR 只在精确门禁后合并，Context Promotion 的变更明细只在结构化用户确认后进入集成基线，Issue 只在终态回读后关闭；
- Delivery 阶段观察只由协调 Agent 追加，实时耗时与恢复补录可区分，修改项有界且不泄露原始用户输入；覆盖检查读取完整分页评论并保持观察与流程权威分离，Issue 关闭后记录精确关闭耗时/变更且绝不为补日志重开；
- 新增或修改的失败路径仍然保守关闭；
- 示例输入、输出和 `agents/openai.yaml` 没有承诺不存在的隐式行为；
- CC-Switch 更新后，Codex 与 Claude 均能发现并显式调用同一个 `project-harness` Skill；
- 未把编辑器元数据、下载元数据或临时产物当作 Skill 内容。

若任务只修改文档，也要运行现有测试，以发现协议修改对确定性工具约定造成的意外偏差。

## 完成标准

一次迭代只有在以下条件全部满足时才算完成：

- 变更落在正确的职责层，且没有引入重复权威来源；
- 所有受影响的角色、契约、传输协议、工具和元数据保持一致；
- 兼容性影响与迁移要求已明确处理；
- 自动化测试通过，人工协议核对完成，CC-Switch 更新完成，并通过 Codex 与 Claude 双端验收；
- 交付说明清楚指出行为变化、验证结果和仍存在的风险。
