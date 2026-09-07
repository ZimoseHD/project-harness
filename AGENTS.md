# Project Harness 维护指南

本文件适用于仓库根目录及全部子目录；`CLAUDE.md` 将其桥接给 Claude Code。

## 项目定位

本仓库是跨 Agent 宿主的 `project-harness` Skill 独立规范源和发布载体。交付物为 `project-harness/`；根级文件负责仓库治理，不存放消费项目配置、真实任务状态或项目记忆。

v3 只提供工作流路径和实用写作指引。Agent 自主选择实现方式、测试深度、review 判断、恢复方式和分工。不要增加阶段 gate、证据状态机、固定确认回合或强制 subagent 编排。用户请求、已有授权、宿主权限和远端仓库规则照常适用。继续支持 GitHub 和 GitLab，文中 PR 包含 GitLab MR。

## 工作范式

- 完整路径：plan → spec → delivery。delivery 自主完成 Issue 任务，具体提醒集中在 `project-harness/references/delivery.md`，不规定内部步骤或顺序。
- express：说明范围 → 实现与测试 → 轻量 PR → 合并 → 总结。无独立 Issue、review 阶段或记忆写入。
- init：生命周期外的可选项目偏好设置。

保留 `init`、`spec`、`implementation`、`review`、`context-promotion`、`delivery`、`express` 入口。支持自然语言和已有任务上下文；无指定路径时说明选择并继续。单阶段请求在该阶段结束，完整交付持续推进。grilling 与澄清按需使用，不设强制确认轮次。

Issue 是共享任务说明，PR 是改动和验证记录。按用户需求及修正保持其准确；不以固定字段、受保护表面例外、PASS、摘要、marker 或评论链判断是否允许继续。实际测试、代码审查及事实准确性仍是工作的一部分。

记忆更新根据长期价值和已有授权决定，无候选直接略过。用户明确要求暂停、审阅或限制写入时照做，不把加载 Skill 本身当成任务授权。

## 目录职责

| 路径 | 职责 |
| --- | --- |
| `project-harness/SKILL.md` | 入口、路径、共享工作原则与阶段导航 |
| `project-harness/references/{init,spec,implementation,review,context-promotion,delivery,express}.md` | 阶段工作、输出和单阶段停止位置 |
| `project-harness/references/{issue,product-pr}-template.md` | 可调整的写作模板 |
| `project-harness/references/hosting.md` | 普通托管平台操作指引（GitHub/GitLab） |
| `project-harness/scripts/` | Skill 包维护测试；不用于消费项目阶段校验 |
| `project-harness/agents/openai.yaml` | Codex 展示信息与显式加载偏好 |
| `project-harness/MIGRATION.md` | 版本断代、旧资源退役和在途任务说明 |
| `CLAUDE.md` | 根级治理桥接 |

共享原则集中在入口，阶段文档只补充该阶段的信息。保留实用内容，避免重复 schema、通用工程常识和为推进流程而制造的产物。

## Skill 更新工作流

1. 说明需求属于文案、行为或兼容性变化；兼容变化说明影响和迁移方式。按已有授权推进，只有实质缺失的决定或权限才询问。
2. 阅读受影响入口、阶段和引用资源，在对应职责层完成修改并同步调用方与示例。
3. 搜索旧引用和冲突规则，运行维护测试、Skill 结构检查、`git diff --check`，人工核对两条路径与停止位置。
4. 将完成的源版本提交并发布到 CC-Switch 跟踪的稳定分支，按仓库事实确定目标。报告来源、分支、commit、验证和兼容影响。
5. 交接 CC-Switch 手动刷新与两端同步；用户更新后明确要求时，再在新会话验收发现与调用。

维护验证用于检查发布内容，不得加入 Skill 的消费项目工作流作为阶段 gate。不要用匹配固定措辞的测试冻结文档；只有仍有实际用途的脚本才保留行为测试。

不得生成或提交消费项目配置、真实平台回调、任务临时文件或实际项目记忆。不得将 `__pycache__`、`.pyc`、`.DS_Store`、`*:Zone.Identifier`、编辑器或构建产物放入 Skill。维护脚本优先标准库，不引入隐蔽网络副作用。提交说明采用中文，不加 `Co-Authored-By`。

## 验证与交付

从仓库根目录运行：

```bash
python3 -B -m unittest discover -s project-harness/scripts -p 'test_*.py' -v
git diff --check
```

人工确认入口、阶段、模板、宿主提示及迁移说明相互一致；完整交付与单阶段停止位置清晰；原有 gate 未以新的强制检查清单形式回归；真实失败和未完成工作仍如实报告。即使只改文档，也运行现有维护测试。

交付包括稳定分支上的源版本，以及精确的 CC-Switch 更新交接、兼容影响和遗留问题。本仓库不刷新 CC-Switch，不自行同步或启用消费端 Skill。
