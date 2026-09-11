# Contributing / 贡献指南

Edit the canonical skill in `skills/homebrew-cli-creator/`; do not maintain parallel copies for each host. Keep English and Chinese README instructions aligned. Keep host-specific configuration in its own manifest.

修改 `skills/homebrew-cli-creator/` 中的唯一内容源，避免为不同宿主维护重复 skill。英中 README 保持同步，宿主特有配置放在各自清单中。

Before a pull request / 提交前：

- Run `python scripts/validate.py` with `requirements-dev.txt` installed.
- For behavior changes, exercise a realistic request in an isolated project and record the host, checks run, and unresolved limitations.
- Include only guidance supported by actual requirements or observed failures. Preserve formatting; do not introduce automatic formatters.
- Keep personal paths, credentials, generated project outputs, and local caches out of the package.

Explain the user-visible outcome and validation evidence in your pull request. Contributions are provided under the repository's Apache-2.0 license.
