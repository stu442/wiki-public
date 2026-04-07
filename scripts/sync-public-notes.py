#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from pathlib import Path

VAULT = Path('/Users/bagminsu/hermes-agent/Hermes')
OUTPUTS = VAULT / '30-Outputs'
DEST = Path('/Users/bagminsu/wiki-public/quartz/content/public-output')

TITLE_RE = re.compile(r'^#\s+(.+)$', re.MULTILINE)
WIKILINK_FULL_RE = re.compile(r'\[\[([^\]]+)\]\]')


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


def parse_wikilink(inner: str) -> tuple[str, str]:
    target, alias = inner, None
    if '|' in inner:
        target, alias = inner.split('|', 1)
    display = alias if alias else target
    target = target.split('#', 1)[0]
    display = display.split('#', 1)[0]
    target_title = Path(target).name.strip()
    display_text = display.strip() if display.strip() else target_title
    return target_title, display_text


def replace_private_links(text: str, published_titles: set[str], replaced: set[str], source_title: str) -> str:
    def repl(match: re.Match[str]) -> str:
        inner = match.group(1)
        target_title, display_text = parse_wikilink(inner)
        if target_title in published_titles:
            return match.group(0)
        replaced.add(f'{source_title} -> {target_title}')
        return display_text

    return WIKILINK_FULL_RE.sub(repl, text)


def main() -> None:
    clear_dest()
    published: dict[str, Path] = {}
    source_texts: dict[str, str] = {}

    for md in sorted(OUTPUTS.glob('*.md')):
        text = md.read_text(encoding='utf-8')
        if not has_publish_true(text):
            continue
        title = title_of(text, md.stem)
        published[title] = DEST / slugify(md.name)
        source_texts[title] = text

    replaced: set[str] = set()
    published_titles = set(published.keys())

    for title, text in source_texts.items():
        cleaned = replace_private_links(text, published_titles, replaced, title)
        published[title].write_text(cleaned, encoding='utf-8')

    replaced_list = sorted(replaced)
    print(f'published={len(published)}')
    print(f'replaced_private_links={len(replaced_list)}')
    for title, path in sorted(published.items()):
        print(f'{title} => {path}')
    if replaced_list:
        print('replaced_private_links:')
        for item in replaced_list:
            print(f'  - {item}')


if __name__ == '__main__':
    main()
