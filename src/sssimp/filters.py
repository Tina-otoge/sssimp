import jinja2

import sssimp


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
