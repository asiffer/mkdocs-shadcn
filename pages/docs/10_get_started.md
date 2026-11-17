---
title: Get started
show_datetime: true
extra_css:
  - "css/pygments/all.css" # add scoped styles
new: true
summary: Setup an mkdocs project with shadcn theme
---

## Install

Add the package to your project.

=== "pip"

        :::bash
        pip install mkdocs-shadcn


=== "uv"

        :::bash
        uv add mkdocs-shadcn

=== "poetry"

        :::bash
        poetry add mkdocs-shadcn

If you want to use [`pymdown` extensions](https://facelessuser.github.io/pymdown-extensions/), you can also install the `pymdown-extensions` package:

=== "pip"

        :::bash
        pip install pymdown-extensions


=== "uv"

        :::bash
        uv add pymdown-extensions

=== "poetry"

        :::bash
        poetry add pymdown-extensions


!!! warning "Tip"
    Don't forget to install `Pygments` to activate syntax highlighting.


## No-brainer

You can init your new python project using `uv` and embed `mkdocs` documentation as follows.

```shell
uv init myproject 
cd myproject
uv add --dev mkdocs mkdocs-shadcn pymdown-extensions Pygments
uv run mkdocs new .
echo -e "theme:\n  name: shadcn" >> mkdocs.yml
uv run mkdocs serve --livereload
```

