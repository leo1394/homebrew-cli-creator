# General implementation patterns

Choose a pattern according to CLI complexity, dependencies, and target platforms. Paths and command names below are illustrative and do not refer to existing projects.

| Pattern | Suitable when | Implementation considerations |
| --- | --- | --- |
| Single Shell script | Lightweight external-command orchestration with few dependencies | Provide help, version, completion, and manual generation in `bin/cli` so standalone distribution remains self-documenting |
| Build from source | Local platform compilation is needed or source distribution already exists | Declare build dependencies in the Formula; verify the source archive and toolchain in the installer, then check the built version |
| Prebuilt single binary | Cross-platform delivery without requiring a compiler | Publish assets per OS/architecture; embed or bundle completion and manuals so installed tools need no source directory |

## Nested commands and supporting resources

- Generate candidates according to command level and argument type. Avoid flattening every action into a single top-level list for complex CLIs.
- Prefer a shared command contract for parsing, help, manuals, and completion. When using static files, detect drift through tests.
- Internal generation interfaces should write only the requested file content to stdout, without starting application services or requiring project initialization.
- Keep static resources and binaries at the same version. Single-file distributions must not reference files in a developer's workspace.

## Documentation as a product introduction

- Explain value in one sentence, then present differentiators, installation, and the first successful result.
- Use architecture diagrams for real component relationships and flowcharts for real operation sequences. Do not impose complex diagrams on simple tools.
- Keep English `README.md` and Chinese `README-ZH.md` synchronized. Use repository-relative image paths.
- Use neutral `cli` examples, replaceable arguments, and explicit expected results rather than an author's account or private project.

## Prevent distribution drift

- Formula download URLs, checksums, tags, CLI versions, and test assertions must identify the same release.
- Completion tests must check filenames containing spaces, directories, enums, and non-path arguments rather than merely checking files exist.
- Use isolated fixtures or mocks for dynamic candidates to avoid starting real services during tests.
- Provide manuals and completion in a new project's first release. Keep compatibility branches only when historical releases are actually supported.
- Add PowerShell completion, Windows installers, and Homebrew bottles according to target-platform needs, not as mandatory dependencies for every project.
