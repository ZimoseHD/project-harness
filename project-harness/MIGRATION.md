# Migration to v3

v3 将 Harness 改为工作流指引，取消所有 Harness 自建 gate。两条交付路径和七个阶段入口保留，阶段如何推进由 Agent 根据任务、实际结果和已有授权判断。本次为行为与兼容性断代，不是对 v2 校验器的可选开关。保留稳定分支已有的 GitHub/GitLab 支持，PR 在 GitLab 对应 MR。

## 保留与变化

| 表面 | v3 行为 |
| --- | --- |
| 完整路径 | plan → spec → delivery；delivery 根据 Issue 自主组织工作，参考 reviewer 与 context-promotion 提醒，无固定内部流程 |
| express | 范围说明 → 实现与测试 → 轻量 PR → 合并 → 总结 |
| 阶段入口 | 保留 init、spec、implementation、review、context-promotion、delivery、express；支持自然语言和已有上下文，不要求当前消息重复结构化角色及来源 |
| 阶段停止位置 | 单独调用仍在该阶段结束；选择完整路径或调用 delivery 时连续推进 |
| 路径与计划确认 | Agent 说明路径后推进；grilling 和提问按需，不要求固定确认回合 |
| Issue 与 PR | 改为可调整的写作模板；移除唯一范围授权语法、八类受保护表面及强制升级、精确标题顺序和固定字段 |
| 测试与 review | 保留实际测试和代码审查；移除固定三项 verdict、PASS schema 和五类精确“无”判定 |
| 平台 I/O 与合并 | 使用普通工具操作；删除 L2/L3、基线/tuple/digest 比对、强制回读、required-check discovery、merge evidence key 集和结果 envelope |
| 记忆写入 | 在已有授权内由 Agent 判断并完成；移除 split-turn source-bound 确认、proposal/callback/terminal 和 active lineage 协议 |
| Issue 关闭 | 使用普通显式关闭或适合交付时机的 closing reference，无证据关闭门 |
| 项目配置 | 可选偏好，沿用 integration 字段；无严格 schema 校验、版本迁移前置或固定 develop 限制 |
| 宿主适配 | 保留 Codex 显式加载与 Claude 加载方式；不再以角色字段校验代替理解用户请求 |

用户指示、真实授权和宿主权限继续适用；GitHub/GitLab 自身的分支保护和规则不会被改写。取消 Harness gate 不表示测试失败、未完成工作或未发生的合并可以报告为成功。

## Delivery 自主执行调整

后续精简取消 delivery 的固定阶段顺序、恢复分支表和合并/关闭时序，仅保留从 Issue 获取任务信息、使用 reviewer 和 context-promotion 三项提醒。reviewer 的选择、介入时机与协作方式由 Agent 决定，不引入拓扑或证据要求；没有值得记录的知识时，context-promotion 可简短说明无需写入。单阶段入口仍可独立使用，delivery 按需参考其内容。已有任务直接按实际进度继续，无配置或持久数据迁移。

## 投入与收口提醒

入口的协作提醒适用于两条路径和单阶段：委派时缩小任务，沿用项目已有工具预算和 checkpoint；协调者整合结果并定点复核，不重复扫描已委派范围。宿主有完成自动通知时使用通知机制，不为等待代理创建 Monitor 或空转工具调用；外部进程/CI 的轮询则使用固定截止时间并区分成功、失败、取消和超时，不以安静时长判断代理失败。累计投入包含协调成本，不等同于当前上下文长度；继续探索应有新的证据目标，反复检索或循环总结时缩小工作并压缩交接。

Review 按改动和风险选择覆盖范围，必要时扩大，尊重用户明确的全面评审要求。调用其他 review skill 前核对其展开方式并传入实际 diff 范围及适用约束；不默认选择大规模嵌套评审。Spec 复用规划与调查证据，事实充分后进入用户裁决，不在 grilling 中重新发现同一组事实。必要测试、缺陷检查及单阶段停止位置保持原意。

本次是 v3 内的行为指引调整，不新增合同、预算字段、计数脚本或阶段 gate，不修改第三方 skill 或宿主。实际计数和等待能力取决于宿主；无法获取计数时如实说明，以调用数和可观察上下文增长辅助判断，不将其冒充 token 用量。已有入口、模板和配置继续使用，无需迁移数据；已加载旧指引的会话在手动更新后用新会话接续。

## 删除的资源

- `scripts/config_guard.py`、`scripts/transport_guard.py`、`scripts/markdown_digest.py` 及其专用测试；不再提供这些 Python API 或命令行入口。
- `references/evidence-contract.md` 和两个 `*-transport.md` 协议；日常操作指引位于 [Hosting operations](references/hosting.md)。
- `references/issue-contract.md`、`references/product-pr-contract.md`；替换为 [Issue template](references/issue-template.md) 与 [Product PR template](references/product-pr-template.md)。
- `${marker_namespace}:context-promotion` marker、review verdict、proposal artifact、awaiting-confirmation、confirmed、memory-pr-merged、no-promotion 等持久格式不再生产或解析为流程状态。

依赖旧脚本、路径、严格输入输出或持久 schema 的外部自动化需同步调整；v3 没有模拟成功的兼容桩，也不把旧记录重写成新格式。维护测试只检查 Skill 包资源的完整性，不参与消费项目交付。

## 在途 v1/v2 工作

保留已有 Issue、PR、评论、分支和项目记忆。读取真实 diff、测试、review 反馈及合并状态，按剩余工作继续：

- 未合并的 Product PR：继续实现或 review，随后正常合并。缺少新模板字段不要求返回 spec 或迁移 Issue。
- 产品已合并：处理仍有价值的记忆工作并关闭 Issue；不再补写 verdict 或终态记录。
- 已有 Draft/Ready Memory PR：审阅实际内容，结合用户最新指示完成或修订；已有明确暂停、拒绝或待用户决定的事项仍需遵守。旧 marker 的存在本身不要求新确认回合。
- 已合并的 Memory PR 或已完成任务：复用现有结果，不重复写入或合并。

旧评论可以提供历史线索，但不作为机器状态或用户授权。不要改写或删除它们来迁移，也不要仅因旧 schema 无法验证就阻塞。目标或用户决定确实不清楚时，提出普通澄清即可。

## 消费项目配置与更新

已有 `.project-harness/config.yaml` 可以原样保留。v3 按需读取 `integration` 偏好，忽略历史 `schema_version` 和 `marker_namespace` 的协议含义；无需批量迁移。无配置也可开始工作。新建或精简后的可选配置不保证能供旧版校验器使用；混用旧版 Agent 时保留旧配置，或分别固定 Skill 版本。

从本仓库稳定分支更新整个 `project-harness/`，确保旧脚本与协议文件随替换被移除。CC-Switch 刷新及向 Codex/Claude 同步由用户手动完成。已加载旧内容的会话应切换到新会话。双端发现与调用验收只在用户更新后明确要求时进行。

## v1 → v2 历史说明

v2 曾将 `definition` 改为 `spec`、`closeout` 改为 `review`，删除 `context-authoring`，并移除固定 subagent 拓扑、delegation envelope、stage observation、eligibility registration、validation reuse 和强制独立 Reviewer。v3 沿用这七个现有入口，不恢复 v1 编排或持久协议。
