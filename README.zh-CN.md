# Agent Project Manager

[English](README.md) · [Skill 入口](SKILL.md) · [完整示例](examples/continuing-project.md)

让 Agent 担任大型、持续型项目的项目经理，按里程碑组织团队，交付完整且可追溯的成果包。

项目经理从接到需求开始，明确目标、依赖、可用资源和决策权限，根据项目需要组建团队，查证各模型的能力并进行小规模实测，为每个角色编写项目专属 skill。随后组织执行、评审、修订、验证和定版，保留每一轮实质成果及评审记录，并支持跨会话接续。

## 运行方式

1. **立项**。把目标、使用者、范围、交付格式、验收标准、依赖、预算、时间和授权写进项目章程。已知信息直接复用，关键缺口集中向用户询问。
2. **组队与选模**。先确定职责和能力要求，再查阅当前官方模型资料、评测原文与本项目试题结果。记录具体模型、配置、可用性、选择理由和候补顺序。
3. **制定管理方案和角色规范**。项目经理也有自己的专属 skill。管理方案和 PM 规范接受独立评审，明确每类成果的负责人、评审人、验证方法与定版权限。
4. **逐个里程碑推进**。按依赖派发任务，跟踪真实执行状态，处理阻塞，保留失败和恢复记录，完成当前里程碑后推进下一项可执行工作。
5. **评审、验证和定版**。关键成果绑定版本与内容摘要，独立评审后修订，按真实用户路径或专业判据验证，再由有权限的角色接受。
6. **交付与接续**。交付索引覆盖需求、成果、评审、缺陷、验证、决策、运行说明和遗留限制。会话中断时留下可被下一位 PM 直接执行的交接记录。

团队规模和成果清单随项目调整。软件、研究、内容和其他持续项目可以采用各自的产物与专业验证方式。已有项目可以从盘点、核验和补齐证据开始接管。

## 安装

将仓库克隆到宿主支持的技能目录，目标路径应尚未存在。使用 `~/.codex/skills` 的 Codex 环境可参考

```bash
git clone https://github.com/oldjin-ai/agent-project-manager.git ~/.codex/skills/agent-project-manager
```

其他支持 Agent Skills 的宿主使用其技能发现目录。也可以把 `SKILL.md` 的路径交给 Agent，明确要求按该技能执行。项目级安装目录以宿主当前规范为准。

技能正文使用英文，项目输出采用用户要求的语言。指令层由 Markdown/YAML 组成，附带工具需要 Python 3.10+，使用标准库。模型调用、团队调度、联网和存储依赖宿主提供的能力与授权。

## 开始一个项目

```text
使用 $agent-project-manager 担任这个持续型项目的项目经理。
目标是……，最终交付包括……，验收标准是……。
可用资源有……，预算和时间约束是……，已授权的操作是……。
请先完成立项、资源与模型评估、团队组建、每个角色的专属 skill，
以及经过独立评审的项目管理方案，再按里程碑推进至完整交付。
缺少会改变项目承诺的关键输入时向我询问，其他已授权工作继续执行。
```

接管在建项目可使用

```text
使用 $agent-project-manager 接管当前项目。
先核对真实进展，盘点成果和评审证据，保留已有工作，
列出交付缺口并逐个里程碑补齐。最终给我完整的成果包和交付索引。
```

## 附带工具

用本机已核实的 Python 解释器执行。下面的 `python` 是跨平台示例。

```bash
python scripts/init_project.py /项目路径/collaboration/project-office --name "项目名称"
python scripts/artifact_control.py seal /项目路径/collaboration/project-office/artifacts/A01/v1/payload
python scripts/artifact_control.py check /项目路径/collaboration/project-office/records/artifacts.json
```

初始化会创建草稿。交付检查需要先声明该里程碑必需的成果，再核对文件摘要、评审、验证、缺陷与接受记录。工具使用方法和数据格式见 [工具说明](references/tooling.md)。

## 当前成熟度

v0.1.0 是从持续迭代的真实项目中提炼的首版，包含本地工具测试和独立前向测试，具体范围见 [验证记录](docs/validation.md)。提炼开始时，来源项目的 PM 管理方案仍在评审，产物正式定版工作尚在补齐。长期效果和不同宿主上的运行需要继续积累实证。

宿主负责实际执行、调度、持久化和权限控制。附带检查器验证记录和文件的一致性。成果质量、评审真实性和业务可用性由对应角色结合原始证据判断。

## 参考与贡献

研究参考了 BMAD Method、MetaGPT、Spec Kit、Superpowers、Deep Agents 和 Agent Skills 格式，具体借鉴点与检索日期见 [设计来源](references/design-sources.md)。仓库正文与工具为独立编写。

欢迎用脱敏后的真实案例提交 issue，包括项目背景、期望行为、实际结果和证据。修改可运行

```bash
python -m unittest discover -s tests -v
```

采用 MIT 许可证，Copyright 2026 oldjin-ai。
