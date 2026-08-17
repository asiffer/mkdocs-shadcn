---
title: pymdownx.blocks.tab
summary: Tabbed content
external_links:
  Reference: https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/tab/

---



The `pymdownx.blocks.tab` extension is a Python-Markdown plugin that allows you to create interactive tabbed content in your Markdown files.

Tab blocks are aimed at replacing the `pymdownx.tabbed` extension (see [tab documentation](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/tab/#tab)).

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - pymdownx.blocks.tab
```

## Syntax

```md
/// tab | `pip`

    :::bash
    pip install mkdocs-shadcn
///

/// tab | uv

    :::bash
    uv add mkdocs-shadcn
///

/// tab | poetry

    :::bash
    poetry add mkdocs-shadcn
///
```

/// tab | `pip`
    new: true

    :::bash
    pip install mkdocs-shadcn
///

/// tab | uv

    :::bash
    uv add mkdocs-shadcn
///

/// tab | poetry

    :::bash
    poetry add mkdocs-shadcn
///
