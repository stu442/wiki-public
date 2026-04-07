#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

VAULT = Path('/Users/bagminsu/hermes-agent/Hermes')
OUTPUTS = VAULT / '30-Outputs'
DEST = Path('/Users/bagminsu/wiki-public/quartz/content/public-output')

TITLE_RE = re.compile(r'^#\s+(.+)$', re.MULTILINE)
WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]')


def has_publish_true(text: str) -> bool:
    if not text.startswith('---\n'):
        return False
    end = text.find('\n---', 4)
    if end == -1:
        return False
    frontmatter = text[4:end]
    return bool(re.search(r'(?m)^publish:\s*true\s*$', frontmatter))


def title_of(text: str, fallback: str) -> str:
    m = TITLE_RE.search(text)
    return m.group(1).strip() if m else fallback


def slugify(name: str) -> str:
    return name.replace('/', '-').replace(':', ' -').strip()


def clear_dest() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True, exist_ok=True)


def main() -> None:
    clear_dest()
    published: dict[str, Path] = {}
    raw_contents: dict[str, str] = {}

    for md in sorted(OUTPUTS.glob('*.md')):
        text = md.read_text(encoding='utf-8')
        if not has_publish_true(text):
            continue
        title = title_of(text, md.stem)
        dest_name = slugify(md.name)
        dest_path = DEST / dest_name
        dest_path.write_text(text, encoding='utf-8')
        published[title] = dest_path
        raw_contents[title] = text

    issues: list[str] = []
    for title, text in raw_contents.items():
        links = set(WIKILINK_RE.findall(text))
        for link in sorted(links):
            link_title = Path(link).name
            if link_title in published:
                continue
            issues.append(f'{title} -> {link_title}')

    report = DEST / '_publish-report.md'
    lines = ['# Publish Report', '', '## Published Notes']
    for title in sorted(published):
        lines.append(f'- {title}')
    lines += ['', '## Private Link Warnings']
    if issues:
        lines.extend(f'- {item}' for item in issues)
    else:
        lines.append('- none')
    report.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f'published={len(published)}')
    print(f'warnings={len(issues)}')
    for title, path in sorted(published.items()):
        print(f'{title} => {path}')
    if issues:
        print('private_link_warnings:')
        for item in issues:
            print(f'  - {item}')


if __name__ == '__main__':
    main()
