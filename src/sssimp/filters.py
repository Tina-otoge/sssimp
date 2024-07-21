import json as _json

import jinja2

import sssimp
import sssimp.generators.markdown


@sssimp.filter
@jinja2.pass_context
def a(context, value: str):
    """Makes a path absolute no matter where the file is"""
    value = value.removeprefix("/")
    l1 = set(context["page"].target.parents)
    l2 = set(sssimp.OUTPUT_DIR.parents)
    l2.add(sssimp.OUTPUT_DIR)
    diff = l1.difference(l2)
    for _ in diff:
        value = "../" + value
    return value


@sssimp.filter
def markdown(value: str):
    return sssimp.generators.markdown.markdown_to_html(value).html


@sssimp.filter
def json(value: object):
    return _json.dumps(value, indent=2, default=str, sort_keys=True)
