# sssimp :snake:
Simple Static Site Inductor Made in Python

## Why?

I wanted a simple way to generate static websites and I like Jinja2. I had
previous experiences working with Jekyll but it seemed like too much work to
setup everytime and overkill for the job as it supports many features I don't
necessarily use.

## Installing

```
pip install sssimp
```

## How to use

Create a folder called `input`, it will hold the data to generate the site.

Running `python -m sssimp` will generate content in the `output` folder.

## Generators

- Files placed in `input/content` will be directly copied to the `output` folder

  Example:  
  `input/content/favicon.png` -> `output/favicon.png`

- HTML files with the suffix .html placed in `input/content` will be parsed as
  Jinja2 templates, they can use templates defined in `input/templates`.  
  See the [Jinja2 documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/)

  Example:  
  `input/content/index.html` -> `output/index.html`  
  Starting with content  
  ```jinja2
  {% extends "base.html" %}

  ...
  ```
  Will use the template `input/templates/base.html`

- CSS files in `input/css` will be merged together in a single file
  `output/bundle.css`

- Markdown files with the suffix .md placed in `input/content` will be parsed to
  HTML and passed to a template with the same name as their parent folder as the
  parameter `markdown`

  Example:  
  `./input/content/post/hello-world.md` -> `./output/post/hello-world.html`  
  Using the template `./input/templates/post.html`  
  Generated with context `{'markdown': 'the markdown file converted to HTML'}`

  The template name can be overriden using the markdown meta argument "template"

  Example:  
  `./input/content/post/special.md` -> `./output/post/special.html`  
  Starting with content  
  ```md
  ---
  template: special.html
  ---

  ...
  ```
  Will use the template `./input/templates/special.html` instead of `post.html`
  
  ## Examples
  
  See [the `example` branch for an example input folder](https://github.com/Tina-otoge/sssimp/tree/example)
