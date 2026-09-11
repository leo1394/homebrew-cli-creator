---
name: homebrew-cli-creator
description: Create open-source CLI projects distributed through Homebrew, or improve an existing CLI with shell completions, man pages, helpful errors, consistent version output, bilingual READMEs, branding, and a standalone installer. Use for CLI project creation and release readiness, not routine brew installation or troubleshooting.
---

# Homebrew CLI Creator

Build open-source CLIs that are easy to install, discover, and learn. Examples use `cli`; replace it with the actual command name. Apply these requirements to new projects across domains, or address relevant gaps in existing projects.

## Before implementation

- Inspect the directory, project instructions, existing implementation, language, and release process. Preserve existing formatting; do not run formatters.
- Determine the command name, purpose, repository URL, core operations, and target platforms from context. Continue independent work when information is missing; ask about gaps that affect product behavior instead of treating example operations as requirements.
- Prefer Shell, Rust, or Go for new projects. Use Shell for simple external-command orchestration; consider Go for complex state, concurrency, and cross-platform single binaries; consider Rust when performance, memory control, or type constraints matter more. Choose according to the task; do not force an existing project to change languages.
- Define commands, subcommands, options, argument types, and side effects as a shared contract for parsing, help, completion, manuals, and tests. A small Shell project does not need a framework solely for this purpose.
- Read [Implementation patterns](references/design-patterns.md) when choosing an implementation or packaging approach. Read [Distribution and validation](references/distribution.md) when implementing installation, Formulae, or compatibility. These references require no particular repository or local environment.

## Required CLI contract

### 1. Shell completion

Provide at least Bash, Zsh, and Fish completion for commands, nested actions, short and long options, enumerated values, and path arguments. This completes the installed `cli` command, not the `brew` command itself.

- Complete according to argument semantics: files for file arguments, directories for directory arguments, and valid values for enums. Do not suggest local files for URL arguments.
- Handle filenames containing spaces, quoting, repeated options, options with values, the `--` separator, and `cli help <TAB>`.
- Dynamic candidates must use lightweight, read-only queries. Pressing Tab must not start services, write configuration, or download dependencies.
- Expose `cli completion bash|zsh|fish`, or provide an internal `cli __completion bash|zsh|fish` interface for installers. Generation output must not contaminate normal command output.
- Both the Formula and install.sh must deploy completion files. Document activation for each shell and test actual candidates, not just file existence.

### 2. Manual pages

Support `man cli` after installation. Provide a valid roff `cli.1`, either distributed with the source or emitted by an internal binary interface. A standalone single-file download must embed the manual or install a matching version alongside it.

Include NAME, SYNOPSIS, DESCRIPTION, COMMANDS/OPTIONS, EXAMPLES, and relevant caveats. Add EXIT STATUS, ENVIRONMENT, FILES, and SEE ALSO where applicable. Keep content consistent with CLI behavior and examples executable. Help, manual, and completion generation must work without an initialized application workspace.

### 3. Consistent version output

`cli version` and `cli --version` must succeed and write exactly two lines to stdout, ending with a newline, without colors, banners, or logs:

```text
cli version 0.1.0 (2026-09-11)
https://github.com/<owner>/homebrew-cli
```

The second line is a plain URL, not a Markdown link. Use shared metadata for the version, release date, and repository URL. The date is the release date, not the current runtime date. The name, date, and version above are illustrative. Clearly label development builds rather than presenting them as published releases. Keep Formula, tag, installer, binary, and manual metadata aligned.

### 4. Help commands

Support `cli help`, `cli --help`, `cli help <command>`, and `cli <command> --help`. Provide help for the corresponding path of nested commands.

Top-level help should explain the product in one sentence and list common commands and quick examples. Command help must include purpose, syntax, arguments and defaults, copyable examples, prerequisites, and caveats. Explain actual side effects such as overwriting files, deletion, or network requests. Help requests must succeed without performing application operations or requiring application dependencies to be installed.

### 5. Errors and suggestions

For unknown commands or options, show the original error, the closest plausible candidates at the current command level, and how to access help. Use edit distance or framework suggestions with a reasonable threshold. Sort tied candidates consistently; do not guess when no candidate is credible.

For example, `cli versoin` should suggest `Did you mean 'version'?`. Write errors to stderr and exit nonzero. Suggest corrections without executing them automatically. Do not classify paths, URLs, or user data as misspelled commands.

## Bilingual documentation and visual assets

Generate a default English `README.md` and Chinese `README-ZH.md`, linked to each other at the top. Keep features, examples, and installation constraints aligned. Treat READMEs as product introductions; put exhaustive option tables and lengthy design explanations in help, manuals, or docs.

Adapt this suggested content order to the product:

1. Logo/product banner, name, one-sentence value proposition, and language switch.
2. A few concrete differentiators explaining the problem solved; do not invent performance claims, user counts, or badge status.
3. Requirements, Homebrew installation, and standalone installation.
4. A short sequence from installation to the first useful result, with expected output and prerequisites.
5. Typical scenarios or a compact command table. Add a concise Mermaid architecture diagram or flowchart when it helps explain relationships or data flow.
6. Actual limitations and caveats, deeper documentation, contribution guidance, and license.

New users should quickly understand what the tool does, why to use it, how to install it, and how to achieve a first success. Avoid repetitive sections or fictional multilayer architectures for simple CLIs.

Create a separate logo and wide banner for the actual product in `assets/`. Embed them appropriately in both READMEs using relative paths and alt text. Keep a consistent visual identity and check thumbnail recognition, text readability, and appearance on light and dark backgrounds. Deliver real files for both assets, not only prompts or remote placeholders.

Use available image-generation capabilities and their applicable skill instructions for raster illustrations or AI-generated images. Simple vector marks can be authored directly as SVG. If image tools are unavailable, use suitable original vector artwork; disclose any requested visual effect that cannot be delivered. Do not reuse another project's branding. Separate bilingual banners are optional; a shared text-free banner is acceptable. Essential information must also exist outside images.

## Installation, release, and validation

Include an executable root-level `install.sh` for systems without Homebrew, with outdated Homebrew, or on explicitly supported older platforms. It must work independently of brew and install the CLI, manuals, and completion files. Older-platform support depends on Shell, system APIs, and binary compatibility; an installer alone does not establish compatibility with every old system.

Complete the Formula, installer, and necessary tests using [Distribution and validation](references/distribution.md). Clearly identify unpublished URLs or checksums. Do not claim unavailable artifacts are downloadable, or publish tags, releases, or repository changes without authorization.

Before delivery, confirm:

- Core functionality works; command, option, and path completion have behavioral checks.
- `man cli` is discoverable and renders; help includes explanations, examples, and caveats.
- Version output matches the exact two-line contract; invalid input produces reasonable suggestions and a nonzero exit status.
- Both READMEs provide clear introductions with working links and embedded, previewed logo and banner assets.
- Formula and standalone installation include the executable, completion, and manuals; installer failures preserve the existing executable.
- Tests cover real behavior. Explicitly list checks not run on target platforms as unverified.

Conclude with the output location, language choice, run/install instructions, actual validation results, and any information still needed from the user.
