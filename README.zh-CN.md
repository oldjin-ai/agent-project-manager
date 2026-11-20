# Agent Project Manager

![Agent project manager](assets/illustrations/hero.png)

[English](README.md) · [Skill 入口](SKILL.md) · [完整示例](examples/continuing-project.md)

让 Agent 担任大型、持续型项目的纯粹总控项目经理（`v0.2.1`），通过职责隔离、两平面零重封控制、风险分级治理与独立评审，组织多角色团队跨会话稳定交付完整成果。

项目经理在立项时明确目标、风险分级与权限边界，于运行时实查可调用模型并将易变绑定写入 `PROJECT-PROFILE.md`，为每个角色生成项目专属 skill，遵循“0 亲跑命令、0 亲改代码、0 自审代签”的纯调度铁律组织推进，并产出可审计的交接索引。

## v0.2.x 核心升级

- **非阻塞派单即止与极简打断白名单（`v0.2.1`）**：派完后台子智能体立即回报并结束回合，严禁调用 `wait_agent` 等阻塞等待工具卡住交互；常规推进与非 A 级技术裁定全自动流转，仅在 4 类明确边界时停下请示用户。
- **两平面封签（`seal-scope` + 外置治理平面）**：内容清单仅封存交付物本体（自动排除 `.git`、缓存与治理目录），评审文件、历史归档、测试日志与签署件全部外置并向下绑定 `manifest_sha256`——新增评审或签认**零重封**。
- **纯总控调度铁律**：多 Agent 模式下总控主会话严禁直接跑 Shell、直接改源码/契约/产物、或代跑自验；单轮轻读受控，优先使用可回调子智能体。
- **风险分级治理（`Light` / `Standard` / `Strict`）**：按项目风险匹配治理重量；方案与 PM 规范限 1–2 轮建制复核；稳定方法与易变绑定分层，单一只追加 `RULEBOOK.md` 统一口径。
- **送审一次封签与同批原子定版**：草稿期零封签，先过机械前置门再在送审时一次封签；耦合产物停留在 `review_passed` 集中一次签认并整批原子定版，杜绝“草稿已签又重签”的循环。
- **精简复审与额度韧性**：第 2 轮起基于 diff 增量复审；稀缺强评审聚焦终验，常规卡走机械门禁+非作者复核；遇 429 原地冻结或启用合格备选，严禁换弱模型冒充席位；同一缺陷最多 2 轮即升级。
- **真实用户完整性底线与跨宿主适配**：内置 8 类真实用户可感知缺口判据、诚实空态规范、固定三行汇报口径与多宿主工具适配指南。

## 安装

将仓库克隆或真实复制到宿主支持的技能目录（勿使用符号链接或目录联接），目标路径应尚未存在。Codex（`~/.codex/skills`）示例：

```bash
git clone https://github.com/oldjin-ai/agent-project-manager.git ~/.codex/skills/agent-project-manager
```

其他支持 Agent Skills 的宿主（如 DeepSeek Harness 的 `~/.dsh/skills`）可复制到对应技能目录，或将 `SKILL.md` 路径显式交给 Agent 执行。

技能正文为英文，项目输出使用用户指定语言。工具脚本仅依赖 Python 3.10+ 标准库，无第三方依赖。

## 开始一个项目

```text
使用 $agent-project-manager 担任这个持续型项目的项目经理。
目标是……，最终交付包括……，验收标准是……。
可用资源有……，预算和时间约束是……，已授权的操作是……。
请先完成立项、PROJECT-PROFILE.md、运行时模型核验、各角色专属 skill，
以及按风险分级的项目管理方案，再按里程碑推进至完整交付。
缺少会改变项目承诺的关键输入时向我询问，其他已授权工作继续执行。
```

接管在建项目可使用：

```text
使用 $agent-project-manager 接管当前项目。
先依据原始凭证核对真实进展，保留已有成果与兼容旧门禁，
切换至两平面零重封并消除提前草稿签认，逐个里程碑补齐交付缺口。
```

![Purpose-built agent team](assets/illustrations/team.png)

## 附带工具

使用本机已核实的 Python 解释器执行（下文 `python` 为跨平台示例）：

```bash
python scripts/init_project.py /项目路径/collaboration/project-office --name "项目名称"
python scripts/artifact_control.py seal-scope /项目路径/collaboration/project-office/artifacts/A09/v1/manifest.json --root /项目路径 --scope apps/backend/src apps/backend/tests --exclude-prefix collaboration/project-office
python scripts/artifact_control.py seal /项目路径/collaboration/project-office/artifacts/A01/v1/payload
python scripts/artifact_control.py check /项目路径/collaboration/project-office/records/artifacts.json --project-root /项目路径
```

初始化会自动生成包含 `PROJECT-PROFILE.md` 与 `RULEBOOK.md` 的草稿办公室；交付检查同时校验双平面漂移、总控回避（`coordinator_actor`）、只追加 `review_history`、原子 `batches` 与独立缺陷闭环。详见 [工具说明](references/tooling.md)。

![Reviewed milestone delivery](assets/illustrations/delivery.png)

## 当前成熟度

v0.2.1 在 v0.2.0 吸收多模型一线跑批教训的基础上，进一步根除了阻塞等待卡死界面与过度频繁打断用户的问题，并与两平面零重封、同批原子定版与纯调度铁律形成闭环。验证范围与实测结果见 [验证记录](docs/validation.md)。

## 参考与贡献

设计参考了 BMAD Method、MetaGPT、Spec Kit、Superpowers、Deep Agents 与 Agent Skills 规范，演进依据见 [设计来源](references/design-sources.md)。提交改进前请运行：

```bash
python -m unittest discover -s tests -v
```

采用 MIT 许可证，Copyright 2026 oldjin-ai。
