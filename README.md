# sssimp 🐍
The **S**tatic **S**ite **S**olution **I**n **M**odern **P**ython

It's simp with 3 s!

A simple tool to generate a static website while being able to use powerful HTML
templates (Jinja2), Markdown files converted to HTML, and other preprocessors.


## Why?

I wanted a simple way to generate static websites and I like Jinja2. I had
previous experiences working with Jekyll but it seemed like too much work to
setup everytime and overkill for the job as it supports many features I don't
necessarily use.

One of the main goals with sssimp is being able to generate a usable website
without any configuration file or dependency. You only install the sssimp
package and run it.

## Installing

```
pip install --user sssimp
```

## How to use

Create a folder called `input`, it will hold the data to generate the site.

Running `python -m sssimp` will generate content in the `output` folder.

Input and output destination can be changed:
```bash
python -m sssimp --input ../some-other/input-dir ~/some-other/output-dir
```

Use `python -m sssimp --help` for more details.

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


- Files placed in `input/data` will exposes their content in templates inside
  the `data` variable. They can be in either YAML or JSON. The path is part of
  their position in the data structure tree.

  Example:  
  `./input/data/categories/tech.yml`  
  With content
  ```yaml
  description: Nerdy stuff
  color: #121212
  related:
    - computers
    - dev
  ```
  Will populate the `data` variable in templates as so:
  ```json
  {
    "categories": [
      {
        "tech": {
          "description": "Nerdy stuff",
          "color": "#121212",
          "related": ["computers", "dev"]
        }
      }
    ]
  }
  ```
  
  ## Examples
  
  See [the `example` branch for an example input folder](https://github.com/Tina-otoge/sssimp/tree/example)
  or my personal website https://github.com/Tina-otoge/tina-simp for a real-world example.


## Additional Jinja2 filters

- `|a` makes any relative path point to the top of the output folder.

  Example:  
  `input/content/blog/post/tech/2021/11/some-post.html`
  -> `output/blog/post/tech/2021/11/some-post.html`  
  With content
  ```html
  <link rel="stylesheet" href="{{ "style.css"|a }}">
  ```
  Will be rendered as `"../../../../style.css"`

  See also [the `<base>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/base)

## Additional Jinja2 variables

- `page` is a `sssimp.generators.html.Page`, it contains many information about
the current document. Markdown files are an instance of
`sssimp.generators.markdown.MarkdownPage` instead, which inherits from `Page`

  This variable itself contains many useful variables:
  - `page.modified_at` and `page.created_at` (`modified_at` forcibly set to `None` if same as `created_at`)
  - `page.href`: The path to the file relative to the output folder
  - `page.src`: A `pathlib.Path` object of the source file in the input folder
  - `page.target` A `pathlib.Path` object of the target file in the output
folder
  - `page.name`: Shortcut for `page.target.name`, the filename of the outputed
    file
  - `page.parent`: Shortcut for `page.target.parent`, the name of the parent
directory in the output folder
file
  - `page.meta`: The Markdown meta variables, prefixing a var with `=` will
    interpret it as raw JSON
    Example
    ```markdown
    ---
    some_var: some value
    something_else: 42
    some_tags:= ["tag1", "tag2"]
    ---

    My cool blog post
    ...
    ```
    The meta variable will always contain a `template` which will resolve to the
    parent directory name with .html appended if none is set in the meta fields.

    The `page.meta` variable is `None` for raw HTML pages, this avoids KeyErrors
    when trying to filter pages by a specific meta variable.
- `plain_text`[^md]: A plain text representation of the Markdown file
- `markdown`[^md]: The Markdown content converted to HTML
- `meta`[^md]: A shortcut for `page.meta`
- `title`[^md]: Returns `page.meta.title` if it exists, else the filename with
  the characters `-` and `_` replaced by whitespaces, the suffix removed and the
  first letter capitalized.

  Example:  
  `input/content/some-cool-page.md`'s title is "Some cool page"
- `BUNDLE_FILE` always evaluates to `"bundle.css"` for now
- `BUNDLE_TIME` modification time of the latest updated file in `input/css`,
  very useful to make the browser refresh the file only if any of the CSS files
  changed.

  Example:
  ```html
  <link rel="stylesheet" href="{{ BUNDLE_FILE}}?{{ BUNDLE_TIME }}">
  ```
- `PAGES` a list of `sssimp.generators.html.Page` objects containing every HTML
  and Markdown files sourced by the site. You can loop over it to generate an
  index. In conjunction with looking up meta values it can be used to filter by
  content type.

  Example:
  ```html+jinja
  {% for page in PAGES if page.meta.template == 'post.html' %}
  <a href="{{ page.href }}">{{ page.title }}</a>
  <div class="tags">
    {% for tag in page.meta.tags %}
    <span class="tag">{{ tag }}</span>
    {% endfor %}
  </div>
  Posted on <time>{{ page.created_at }}</time>
  {% endfor %}
  ```

[^md]: Markdown only
