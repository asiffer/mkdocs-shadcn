---
title: pymdownx.tabbed
summary: Tabbed content
external_links:
  Reference: https://facelessuser.github.io/pymdown-extensions/extensions/tabbed
---


The `pymdownx.tabbed` extension is a Python-Markdown plugin that allows you to create tabbed content in your Markdown files.

This plugin is likely to be replaced by `pymdownx.blocks.tab`, [supported by `mkdocs-shadcn`](./pymdownx_blocks_tab.md).

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - pymdownx.tabbed
```

## Syntax

~~~ md
=== "`pip`"

        :::bash
        pip install mkdocs-shadcn


=== "uv"

        :::bash
        uv add mkdocs-shadcn

=== "poetry"

        :::bash
        poetry add mkdocs-shadcn

~~~

=== "`pip`"

        :::bash
        pip install mkdocs-shadcn


=== "uv"

        :::bash
        uv add mkdocs-shadcn

=== "poetry"

        :::bash
        poetry add mkdocs-shadcn