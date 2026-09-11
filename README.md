# Homebrew CLI Creator

**Make your CLI easy to install, discover, and learn.**

English | [简体中文](README-ZH.md)

An agent skill packaged for Codex and Claude Code, with a portable `skills/` directory for skill installers. It provides a reusable workflow for new Homebrew CLI projects and existing tools that need a complete release experience.

## What it delivers

- Context-aware Bash, Zsh, and Fish completion, including paths with spaces.
- `man cli`, useful command help, examples, and typo suggestions.
- Consistent two-line version output, backed by release metadata.
- English and Chinese READMEs, original Logo/Banner assets, and diagrams where useful.
- A Homebrew Formula and independent `install.sh`, with checksums and failure handling.
- Shell, Rust, or Go selected for the actual problem; existing projects keep their language and formatting.

This is an instruction package, not a CLI binary or a Homebrew formula itself. Generated projects still require implementation and testing. Image generation depends on the host's available tools; original SVG artwork is a supported alternative. The skill instructions are written in English; prompts and project output may be in English or Chinese.

## Try it

After installing the skill, ask your agent:

```text
Use $homebrew-cli-creator to create a CLI named packview that lists files in
an archive without extracting them. Prefer Go, target macOS and Linux,
and include Homebrew packaging and a standalone installer.
```

For an existing project:

```text
Use $homebrew-cli-creator to complete this project's CLI release experience.
Inspect the implementation first, preserve formatting, and report which
installation and platform checks you actually ran.
```

## Install from a checkout

Choose one route to avoid loading duplicate copies of the skill.

### Codex standalone skill

From the repository root, copy `skills/homebrew-cli-creator` into your Codex skills directory (typically `~/.codex/skills/`, or `$CODEX_HOME/skills` when configured). Preserve the nested `references/` and `agents/` directories. Back up an existing copy before replacing it, then start a new task and invoke `$homebrew-cli-creator`.

The root `.codex-plugin/plugin.json` is also provided for plugin packaging. Public marketplace registration is a separate publishing step; this repository does not claim an existing marketplace listing. See [distribution notes](docs/PUBLISHING.md).

### Claude Code plugin

From the repository root:

```bash
claude --plugin-dir .
```

Then invoke `/homebrew-cli-creator:homebrew-cli-creator` with your request. This is the local plugin workflow documented by [Claude Code](https://code.claude.com/docs/en/plugins).

### Skills CLI after GitHub publication

Replace `OWNER` with the actual publishing account. This example becomes usable after that repository exists:

```bash
npx skills add OWNER/homebrew-cli-creator
```

The [Skills CLI](https://www.skills.sh/docs/cli) installs skills from a repository for supported agents. Installer discovery and public marketplace acceptance are separate; no universal marketplace manifest is assumed.

## Repository layout

```text
.codex-plugin/plugin.json       Codex plugin metadata
.claude-plugin/plugin.json      Claude Code plugin metadata
skills/homebrew-cli-creator/    Single source of skill instructions
  SKILL.md                     Workflow and acceptance criteria
  references/                  Implementation patterns and distribution guidance
  agents/openai.yaml           Codex skill presentation
scripts/validate.py            Portable package checks
```

The skill reads the project, defines the command contract, implements CLI and packaging behavior, then validates the install and documentation experience. It does not require any reference repository, run hooks, or start an MCP service.

## Contribute and release

See [contribution guidance](CONTRIBUTING.md), [publishing notes](docs/PUBLISHING.md), and the [changelog](CHANGELOG.md). Local validation:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

[Apache-2.0 License](LICENSE). This community project is not affiliated with Homebrew, OpenAI, or Anthropic.
