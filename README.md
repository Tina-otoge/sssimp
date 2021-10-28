# sssimp :snake:
Simple Static Site Inductor Made in Python

## How to use

Create a folder called `input`, inside create a folder called `content` and an
empty file called `__init__.py`

Running `python -m sssimp` will generate `output` using it

## Generators
- HTML files from the content folder will be parsed as Jinja2 templates, they
  can use templates defined in the `input/templates` folder
- CSS files in `input/content/css` will be merged together in a single file `output/bundle.css`
