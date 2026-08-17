---
title: Mkdocstrings
alpha: true
summary: Documentation from code
external_links:
    Reference: https://mkdocstrings.github.io/
---


!!! warning "Limits"
    This theme tries to support the output of the **python handler** first. We do not know how it behaves with other languages.

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
  - search
  - mkdocstrings
```

You can look at all the available options in the [python handler documentation](https://mkdocstrings.github.io/python/usage/).

!!! warning "Important"
    If you do not define `show_root_heading`, the theme sets it to `true` by default.

## Examples

~~~md
::: shadcn.plugins.excalidraw.ExcalidrawPlugin
    options:
        heading_level: 3
        docstring_section_style: table
        members: true
        inherited_members: true
        merge_init_into_class: true
~~~



::: shadcn.plugins.excalidraw.ExcalidrawPlugin
    options:
        heading_level: 3
        docstring_section_style: table
        members: true
        inherited_members: true
        merge_init_into_class: true

~~~md
::: shadcn.plugins._router.RouterMixin
    options:
        heading_level: 3
        show_symbol_type_heading: true
~~~


::: shadcn.plugins._router.RouterMixin
    options:
        heading_level: 3
        

~~~md
::: shadcn.utils
    options:
        heading_level: 3
        members: true
        show_symbol_type_heading: true
~~~


::: shadcn.utils
    options:
        heading_level: 3
        show_symbol_type_heading: true


