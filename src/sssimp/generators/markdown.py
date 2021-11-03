from collections import namedtuple
import functools
from io import StringIO
import json
from markdown import Markdown, Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor

import sssimp
from sssimp.generators.html import Page, PAGES
from sssimp import jinja
from sssimp.utils import path_strip


class MarkdownPage(Page):
    def __init__(self, src, target):
        super().__init__(src, target)
        with open(self.src) as f:
            self.content = f.read()
        self.plain_text = markdown_to_text(self.content)

    @functools.cache
    def render(self):
        result = markdown_to_html(self.content)
        meta = {
            key: json.loads(value[-1][1:])
            if value[-1].startswith('=')
            else value[-1]
            for key, value in result.meta.items()
        }
        meta.setdefault('template', f'{self.src.parent.name}.html')
        template = jinja.get_template(meta['template'])
        return template.render(
            **self.vars,
            meta=meta,
            markdown=result.html,
            plain_text=self.plain_text,
        )


class StrikeSubExtension(Extension):
    @staticmethod
    def _add_pattern(md, char, tag):
        proc = SimpleTagInlineProcessor(r'(\{0}\{0})(.+?)(\{0}\{0})'.format(char), tag)
        md.inlinePatterns.register(proc, tag, 200)

    def extendMarkdown(self, md):
        self._add_pattern(md, '~', 'del')
        self._add_pattern(md, '_', 'ins')


def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()
Markdown.output_formats['plain'] = unmark_element


def markdown_to_html(text):
    HtmlWithMeta = namedtuple('HtmlWithMeta', ('html', 'meta'))
    markdown = Markdown(
        extensions=[
            # Builtin extensions
            # cf https://python-markdown.github.io/extensions/ (in order)
            'abbr', 'fenced_code', 'footnotes', 'admonition', 'codehilite', 'meta',
            'smarty', 'toc',
            # Custom extensions
            StrikeSubExtension(),
        ],
        extension_configs={'smarty': {'smart_angled_quotes': True}},
        output_format='html',
    )
    return HtmlWithMeta(markdown.convert(text), markdown.Meta)

def markdown_to_text(text):
    markdown = Markdown(
        extensions=[
            'abbr', 'meta', 'admonition',
            StrikeSubExtension()
        ],
        output_format='plain',
    )
    markdown.stripTopLevelTags = False
    result = markdown.convert(text)
    result = result.replace('[TOC]', '')
    return result


def prepare():
    for file in sssimp.CONTENT_DIR.glob('**/*.md'):
        stripped = path_strip(file, sssimp.CONTENT_DIR)
        target = sssimp.OUTPUT_DIR / (stripped.removesuffix('.md') + '.html')
        PAGES.add(MarkdownPage(src=file, target=target))
        sssimp.IGNORE_ASSETS.add(str(file))
