from markdown import Markdown, Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor

import sssimp
from sssimp.generators.html import write_template
from sssimp import jinja
from sssimp.utils import path_strip


class StrikeSubExtension(Extension):
    @staticmethod
    def _add_pattern(md, char, tag):
        proc = SimpleTagInlineProcessor(r'(\{0}\{0})(.+?)(\{0}\{0})'.format(char), tag)
        md.inlinePatterns.register(proc, tag, 200)

    def extendMarkdown(self, md):
        self._add_pattern(md, '~', 'del')
        self._add_pattern(md, '_', 'ins')

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
)


def generate(from_file):
    out_path = (
        sssimp.OUTPUT_DIR
        / (
            path_strip(from_file, sssimp.CONTENT_DIR).removesuffix('.md')
            + '.html'
        )
    )
    with open(from_file) as f:
        html = markdown.convert(f.read())
    args = {key: value[0] for key, value in markdown.Meta.items()}
    args.setdefault('template', f'{from_file.parent.name}.html')
    template = jinja.get_template(args.pop('template'))
    write_template(out_path, template, src=from_file, markdown=html, **args)


def main():
    for file in sssimp.CONTENT_DIR.glob('**/*.md'):
        generate(file)
        sssimp.IGNORE_ASSETS.add(str(file))
