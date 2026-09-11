# Publishing / 发布说明

This repository is prepared for publication; it has no configured public origin or confirmed marketplace listing yet.
本仓库已准备发布结构，尚未配置公开远程仓库或确认市场上架。

## GitHub

1. Choose the GitHub owner and verify the Apache-2.0 license and contributor attribution. Create a repository named `homebrew-cli-creator`.
2. Set real `repository` and `homepage` URLs in both plugin manifests; replace `OWNER` in both README installation examples.
3. Run the package validator and host-specific smoke tests. Commit the reviewed files and push them after local validation passes.
4. Keep versions in both manifests identical, move the relevant changelog notes into a dated release section, and publish an immutable matching tag such as `v0.1.0`.

先确认 GitHub 账号、许可证和署名，再填写真实地址、验证、提交并发布版本。发布前不要把示例地址写成已可用入口。

## Distribution routes / 分发方式

- **Codex:** submit the root plugin package, including `.codex-plugin/plugin.json` and `skills/`, to the selected marketplace under its current submission rules. If a marketplace requires its own catalog, add this plugin to that catalog with its schema and relative layout. This repository is a plugin, not a preconfigured marketplace. See [official plugin documentation](https://learn.chatgpt.com/docs/plugins).
- **Claude Code:** test with `claude --plugin-dir .`, then ask the selected marketplace maintainer to register this repository. The `.claude-plugin/plugin.json` is already included. Follow [marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).
- **Skills CLI / skills.sh:** after publication, verify `npx skills add OWNER/homebrew-cli-creator` in an isolated environment and check that it discovers `skills/homebrew-cli-creator/SKILL.md`. Installation support is not a promise of listing, ranking, or approval. Follow [Skills CLI documentation](https://www.skills.sh/docs/cli).
- **Other skill directories:** submit the GitHub URL and the skill subdirectory as requested. Do not claim every market understands either plugin manifest.

各平台的市场登记、审核和排名独立于仓库结构。当前提供兼容的内容布局和插件清单，不表示已经被任何市场接受。

## Release checks / 发布验证

Run `python scripts/validate.py`; test fresh installation and a real CLI-generation request with each host you claim to support. Confirm there are no links outside the package and no private paths. State which tests were not run. The local validator checks package consistency, not agent behavior or marketplace acceptance.

The installed personal skill and this Git repository are independent copies. Make future edits here, validate them, and explicitly update your installed copy or plugin through its chosen installation method; no background synchronization is configured.

个人已安装 skill 与此 Git 仓库是独立副本。后续在仓库维护内容并验证，再按选定方式更新安装；没有隐式同步。
