import json
import logging
from collections import namedtuple
from datetime import datetime
from io import StringIO

import pymdownx.emoji
from jinja2 import TemplateNotFound
from markdown import Extension, Markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor

import sssimp
from sssimp import jinja
from sssimp.generators.html import PAGES, Page
from sssimp.utils import path_strip

# Set this if we want to have a fixed version for twemoji
# I'm considering this to have reproducible tests, but I'm not sure if it's a
# desirable implementation, since it might cause broken images in the future.
# pymdownx.emoji.TWEMOJI_PNG_CDN = (
#     "https://cdn.jsdelivr.net/gh/jdecked/twemoji@latest/assets/72x72/"
# )


class MarkdownPage(Page):
    def __init__(self, src, target):
        super().__init__(src, target)
        with open(self.src) as f:
            self.content = f.read()
        self.vars["plain_text"] = markdown_to_text(self.content)
        result = markdown_to_html(self.content)
        self.meta = {
            key: (
                json.loads(value[-1][1:])
                if value[-1].startswith("=")
                else value[-1]
            )
            for key, value in result.meta.items()
        }
        self.meta.setdefault("template", f"{self.src.parent.name}.html")
        self.vars["meta"] = self.meta
        self.vars["markdown"] = result.html

    def get_template(self):
        return jinja.get_template(self.meta["template"])

    @property
    def created_at(self):
        if "date" in self.meta:
            return datetime.fromisoformat(self.meta["date"])
        return super().created_at

    @property
    def title(self):
        if "title" in self.meta:
            return self.meta["title"]
        result = self.target.stem
        for char in "-_":
            result = result.replace(char, " ")
        return result.capitalize()


class StrikeSubExtension(Extension):
    """
    Strike text with `~` and underline text with `_`.
    """

    @staticmethod
    def _add_pattern(md, char, tag):
        proc = SimpleTagInlineProcessor(
            r"(\{0}\{0})(.+?)(\{0}\{0})".format(char), tag
        )
        md.inlinePatterns.register(proc, tag, 200)

    def extendMarkdown(self, md):
        self._add_pattern(md, "~", "del")
        self._add_pattern(md, "_", "ins")


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


Markdown.output_formats["plain"] = unmark_element


def markdown_to_html(text):
    HtmlWithMeta = namedtuple("HtmlWithMeta", ("html", "meta"))
    markdown = Markdown(
        extensions=[
            # Builtin extensions
            # cf https://python-markdown.github.io/extensions/ (in order)
            "abbr",
            "fenced_code",
            "footnotes",
            "admonition",
            "codehilite",
            "meta",
            "smarty",
            "toc",
            # Custom extensions
            StrikeSubExtension(),
            # Third-party extensions
            "pymdownx.emoji",
            "pymdownx.magiclink",
        ],
        extension_configs={
            "smarty": {"smart_angled_quotes": True},
            "pymdownx.emoji": {
                "alt": "html_entity",
                "emoji_index": pymdownx.emoji.twemoji,
                "options": {"classes": "emoji"},
            },
        },
        output_format="html",
        tab_length=2,
    )
    return HtmlWithMeta(markdown.convert(text), markdown.Meta)


def markdown_to_text(text):
    markdown = Markdown(
        extensions=["abbr", "meta", "admonition", StrikeSubExtension()],
        output_format="plain",
    )
    markdown.stripTopLevelTags = False
    result = markdown.convert(text)
    result = result.replace("[TOC]", "")
    return result


def prepare():
    for file in sssimp.CONTENT_DIR.glob("**/*.md"):
        as_html = path_strip(file.with_suffix(".html"), sssimp.CONTENT_DIR)
        target = sssimp.OUTPUT_DIR / as_html
        page = MarkdownPage(src=file, target=target)
        sssimp.IGNORE_ASSETS.add(str(file))
        try:
            page.get_template()
        except TemplateNotFound:
            logging.info(f"No matching template for {page}, ignoring file")
            continue
        PAGES.add(page)
