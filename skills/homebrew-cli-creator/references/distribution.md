# Distribution and validation

## Formula

Define the CLI in `Formula/<command>.rb` with actual desc, homepage, license, an immutable release download URL, and a real SHA256. Declare only actual dependencies. Install scripts for Shell projects; build or install Go/Rust binaries according to the distribution approach. Do not assume every project needs automated bottle publishing.

The following installs supporting resources after the executable is installed. It assumes `cli __completion <shell>` exists and is not a complete Formula:

```ruby
generate_completions_from_executable(bin/"cli", "__completion", shell_parameter_format: :arg)
man1.install "man/cli.1"
```

A single-file artifact can generate the manual through an internal interface instead of the static `man1.install` above:

```ruby
man1.mkpath
(man1/"cli.1").write Utils.safe_popen_read(bin/"cli", "__manpage")
```

Interface names may follow existing project conventions, but the Formula, CLI, and installer must agree. Generation must emit only file content and require no application services. Use Homebrew directory helpers rather than hardcoding `/opt/homebrew` or `/usr/local`.

The Formula's `test do` must verify version output, at least one meaningful command without external side effects, and the presence of manual/Bash/Zsh/Fish files. Version assertions must match the release artifact downloaded by that Formula.

Official references, checked on 2026-09-11; recheck when implementation depends on changed behavior:

- [Formula Cookbook](https://docs.brew.sh/Formula-Cookbook): installation, manual directories, and testing conventions.
- [Formula API](https://docs.brew.sh/rubydoc/Formula): completion-generation helpers and arguments.
- [Shell Completion](https://docs.brew.sh/Shell-Completion): shell activation guidance; distinguish brew's own completion from the CLI's completion.

## install.sh

- Declare the interpreter and minimum version. When supporting macOS's bundled Bash 3.2, avoid newer features such as associative arrays and mapfile. Do not mix Bash syntax into POSIX sh scripts.
- Default to user-writable locations such as `~/.local/bin` and `~/.local/share`. Allow explicit version and installation-directory overrides. Explain upgrades through repeat execution.
- Distribute verified scripts for Shell tools. Prefer matching OS/architecture release binaries for Go/Rust; state toolchain requirements when offering source fallback. Exit clearly for unsupported operating systems, architectures, or system versions.
- Resolve latest once to a concrete version, then fetch that version's artifacts, checksums, and supporting resources. Do not mix versions from moving branches.
- Use HTTPS, downloads that fail on errors, temporary directories, and trap cleanup. Confirm download success and verify the matching asset's SHA256 before executing version checks or completion generation.
- Finish downloads, integrity checks, version checks, and resource preparation before replacing the executable. Stage on the destination filesystem and replace the executable atomically. Report supporting-resource failures; do not claim the entire multi-file installation is an atomic transaction.
- Do not default to sudo or silently change shell startup files. Give clear instructions for missing dependencies; automatic system-dependency installation must stay within user authorization.
- Deploy `share/man/man1/cli.1`, Bash completion, Zsh `_cli`, and Fish `cli.fish`. Provide actual PATH, MANPATH, and shell activation instructions. Copying files does not mean the current shell has enabled them. Preserve default system manual search paths when setting MANPATH.
- Piped installation may have no script-file location. Remote installation must not assume repository sources exist beside `install.sh`. Handle local-build mode separately when needed.
- Distinguish outdated Homebrew, operating systems, and runtime libraries in documentation. List actual minimum supported platforms. Older macOS deployment targets, Linux libc, and toolchain compatibility require evidence; disclose what cannot be verified.

## Meaningful validation

Validate with an isolated temporary HOME and installation directory to avoid modifying the user's real tools or shell configuration. Run necessary checks for the language and target platforms; do not repeat unrelated tests solely to increase coverage.

| Scope | Behavior to verify |
| --- | --- |
| Version | `version` and `--version` produce exactly two lines, a valid release date, the correct URL, exit 0, and no extra ANSI sequences or logs |
| Help | Top-level, command, and nested help explain purpose, examples, and caveats without triggering application operations |
| Errors | Misspelled commands/options receive plausible suggestions; unrelated input is not guessed; stderr and exit status are correct; no automatic execution |
| Completion | Execute completion functions or shell test entry points to check subcommands, options, enums, paths with spaces, directories, `--`, and non-path values |
| Manuals | After isolated installation, `man -w cli` finds the manual; man or groff/mandoc renders it successfully and its content is checked |
| Installation | Normal installation, upgrades, explicit versions, and custom paths work; integrity failures, download failures, and version mismatches preserve the previous executable |
| Release consistency | Tags, release files, SHA256, Formula, CLI, and manuals belong to one version; unpublished resources are not reported as successfully installation-tested |
| Documentation and visuals | READMEs link to each other, commands are copyable, asset and documentation links work, and images/diagrams are actually previewed |

Use mocked downloads or local fixtures for failure paths. Run project tests and Formula `brew test <tap/formula>` where available. Use an authorized isolated environment when Formula installation would affect a real system. `ruby -c` alone does not validate Homebrew installation. Explicitly list unverified checks when Bash, Zsh, Fish, or cross-platform environments are unavailable.
