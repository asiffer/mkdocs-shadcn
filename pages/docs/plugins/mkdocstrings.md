---
title: Mkdocstrings
alpha: true
summary: Documentation from code
external_links:
    Reference: https://mkdocstrings.github.io/
---


!!! warning "Limits"
    This theme tries to support the output of the **python handler** first. We do not know how it behaves woth other languages.

## Installation

/// tab | pip

    :::bash
    pip install 'mkdocstrings[python]'
///

/// tab | uv

    :::bash
    uv add 'mkdocstrings[python]'
///

/// tab | poetry

    :::bash
    poetry add 'mkdocstrings[python]'
///

## Configuration

```yaml
# mkdocs.yml

plugins:
  - mkdocstrings
```

You can look at all the available options in the [python handler documentation](https://mkdocstrings.github.io/python/usage/).

## Syntax

~~~md
::: shadcn.plugins.excalidraw.ExcalidrawPlugin
    options:
        members: true
        heading_level: 3
        docstring_section_style: table
~~~

::: shadcn.plugins.excalidraw.ExcalidrawPlugin
    options:
        members: true
        heading_level: 3
        docstring_section_style: table

