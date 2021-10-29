import logging
from markdown import markdown

import sssimp
from sssimp import jinja
from sssimp.utils import mkdir, path_strip


def convert(content: str) -> str:
    return markdown(
        content,
        extensions=[
            # cf https://python-markdown.github.io/extensions/ (in order)
            'abbr', 'fenced_code', 'footnotes', 'admonition', 'codehilite',
            'meta', 'smarty', 'toc'
        ],
    )

def generate(from_file):
    out_path = (
        sssimp.OUTPUT_DIR
        / (
            path_strip(from_file, sssimp.CONTENT_DIR).removesuffix('.md')
            + '.html'
        )
    )
    relative_output = path_strip(out_path, sssimp.OUTPUT_DIR)
    relative_input = path_strip(from_file, sssimp.CONTENT_DIR)
    template_name = f'{from_file.parent.name}.html'
    with open(from_file) as f:
        html = convert(f.read())
    template = jinja.get_template(template_name)
    mkdir(out_path)
    with open(out_path, 'w') as f:
        logging.info(f'Generating {relative_output} from {relative_input}')
        f.write(template.render(markdown=html))


def main():
    for file in sssimp.CONTENT_DIR.glob('**/*.md'):
        generate(file)
        sssimp.IGNORE_ASSETS.add(str(file))
