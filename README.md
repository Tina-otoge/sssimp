# sssimp :snake:
Simple Static Site Inductor Made in Python

## How to use

Create a folder called `input`, inside create a folder called `content` and an
empty file called `__init__.py`

Running `python -m sssimp` will generate `output` using the `content` folder

## Generators
- HTML files from the content folder will be parsed as Jinja2 templates, they
  can use templates defined in the `input/templates` folder
- CSS files in `input/content/css` will be merged together in a single file `output/bundle.css`
- Markdown files with the suffix .md from the content folder will be parsed to
  HTML and passed to a template with the same name as their parent folder as the parameter `markdown`  
  Example:
  `./input/content/post/hello-world.md` -> `./output/post/hello-world.html`  
  Using the template `./input/templates/post.html`  
  Generated with context `{'markdown': 'the markdown file converted to HTML'}`
