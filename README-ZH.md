# Homebrew CLI Creator

**让 CLI 易安装、易发现、易上手。**

[English](README.md) | 简体中文

面向 Codex 和 Claude Code 的 agent skill 插件，同时保留标准 `skills/` 目录供技能安装器发现。提供通用、可复用的工作流程，用于创建 Homebrew CLI，或补齐现有工具的发布体验。

## 能得到什么

- Bash、Zsh、Fish 上下文补全，覆盖命令、选项和带空格路径。
- `man cli`、命令帮助、使用示例与拼写错误建议。
- 与发布元数据一致的固定两行版本输出。
- 英文和中文 README、原创 Logo/Banner，必要时加入解释性图表。
- Homebrew Formula 和独立 `install.sh`，包含校验和与失败处理。
- 按需求选择 Shell、Rust 或 Go；现有项目保留语言和格式。

这是指导 agent 工作的指令包，本身不是 CLI 二进制或 Homebrew Formula。生成项目仍需实现和测试。图像生成取决于宿主工具，也支持原创 SVG 方案。skill 指令以英文编写，可用中文或英文提出需求并生成相应内容。

## 快速使用

安装 skill 后向 agent 发送：

```text
使用 $homebrew-cli-creator 创建名为 packview 的 CLI，
用于查看压缩包内的文件列表而不解压。优先 Go，支持 macOS/Linux，
包含 Homebrew 分发与独立安装脚本。
```

也可以完善现有项目：

```text
使用 $homebrew-cli-creator 补齐当前项目的 CLI 发布体验。
先检查已有实现，保留格式，并报告实际完成了哪些安装和平台验证。
```

## 从本地仓库安装

选择一种方式，避免重复加载同名 skill。

### Codex 独立 skill

将 `skills/homebrew-cli-creator` 整个目录复制到 Codex 的 skills 目录，通常为 `~/.codex/skills/`，配置了 `CODEX_HOME` 时使用其下的 `skills/`。保留 `references/` 和 `agents/`；替换旧版本前先备份。新建任务后用 `$homebrew-cli-creator` 调用。

仓库根目录另有 `.codex-plugin/plugin.json` 供插件打包。公开市场注册属于独立发布步骤，目前不声明已上架，参见[发布说明](docs/PUBLISHING.md)。

### Claude Code 插件

在仓库根目录运行：

```bash
claude --plugin-dir .
```

随后以 `/homebrew-cli-creator:homebrew-cli-creator` 加需求调用。此本地加载方式见 [Claude Code 文档](https://code.claude.com/docs/en/plugins)。

### GitHub 发布后的 Skills CLI 安装

将 `OWNER` 换成实际发布账号；以下示例在仓库公开后才可使用：

```bash
npx skills add OWNER/homebrew-cli-creator
```

[Skills CLI](https://www.skills.sh/docs/cli) 可从仓库向支持的 agent 安装技能。安装器发现与市场审核上架是不同步骤，不假设存在通用市场清单。

## 项目结构

```text
.codex-plugin/plugin.json       Codex 插件元数据
.claude-plugin/plugin.json      Claude Code 插件元数据
skills/homebrew-cli-creator/    唯一的 skill 内容源
  SKILL.md                     工作流程与验收要求
  references/                  实现模式与分发指南
  agents/openai.yaml           Codex 技能展示信息
scripts/validate.py            可移植的包检查
```

skill 先检查项目、明确命令契约，再实现 CLI 与安装方式，最后验证安装和文档体验。不依赖任何参考仓库，不包含自动执行 hook 或 MCP 服务。

## 贡献与发布

参见[贡献指南](CONTRIBUTING.md)、[发布说明](docs/PUBLISHING.md)和[更新记录](CHANGELOG.md)。本地校验：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

采用 [Apache-2.0 许可证](LICENSE)。本社区项目与 Homebrew、OpenAI、Anthropic 无隶属关系。
