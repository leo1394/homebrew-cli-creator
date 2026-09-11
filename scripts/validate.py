#!/usr/bin/env python3
"""Check this repository's package invariants, not marketplace approval."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml


def validate(root):
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    manifests = [json.loads((root / folder / 'plugin.json').read_text())
                 for folder in ('.codex-plugin', '.claude-plugin')]
    for key in ('name', 'version', 'description', 'author', 'license'):
        check(manifests[0].get(key) == manifests[1].get(key), f'Manifests differ: {key}')
        check(bool(manifests[0].get(key)), f'Missing manifest value: {key}')
    name = manifests[0]['name']
    check(name == 'homebrew-cli-creator', 'Unexpected package name')
    check(bool(re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', manifests[0]['version'])), 'Invalid version')
    check(manifests[0].get('skills') == './skills/', 'Invalid Codex skills path')
    skill = root / 'skills' / name
    content = (skill / 'SKILL.md').read_text()
    frontmatter = re.match(r'\A---\n(.*?)\n---\n', content, re.S)
    check(frontmatter is not None, 'Missing skill frontmatter')
    if frontmatter:
        metadata = yaml.safe_load(frontmatter[1])
        check(isinstance(metadata, dict), 'Skill frontmatter must be a mapping')
        if isinstance(metadata, dict):
            check(metadata.get('name') == name, 'Skill name mismatch')
            check(bool(metadata.get('description')), 'Missing skill description')
    ui = yaml.safe_load((skill / 'agents/openai.yaml').read_text())
    check('$' + name in ui['interface']['default_prompt'], 'Default prompt misses skill invocation')
    for required in ('README.md', 'README-ZH.md', 'LICENSE', 'CONTRIBUTING.md', 'docs/PUBLISHING.md'):
        check((root / required).is_file(), f'Missing {required}')
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if any(part in ('.git', '.venv', '__pycache__') for part in relative.parts):
            continue
        check(not path.is_symlink(), f'Package must be self-contained: {relative}')
        if not path.is_file() or path.suffix not in ('.md', '.json', '.yaml', '.yml'):
            continue
        text = path.read_text()
        check(not re.search(r'/Users/[^/\s]+/', text), f'Personal absolute path: {relative}')
        check('[TODO:' not in text, f'Unfinished scaffold: {relative}')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                parsed = urlsplit(target)
                if parsed.scheme or not parsed.path:
                    continue
                linked = (path.parent / unquote(parsed.path)).resolve()
                check(linked.is_relative_to(root) and linked.exists(), f'Broken or external local link: {relative} -> {target}')
    return errors


if __name__ == '__main__':
    try:
        problems = validate(Path(__file__).resolve().parent.parent)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        problems = [str(error)]
    if problems:
        print('\n'.join('ERROR: ' + problem for problem in problems), file=sys.stderr)
        sys.exit(1)
    print('Package checks passed (manifests, skill metadata, references, portability).')
