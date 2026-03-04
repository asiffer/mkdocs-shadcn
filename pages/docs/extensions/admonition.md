---
title: Admonitions
summary: Notes, infos, warnings, dangers and successes
external_links:
    Reference: https://python-markdown.github.io/extensions/admonition/
---

The Admonition extension adds rST-style admonitions to Markdown documents.

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - admonition
```

## Syntax

    :::md {.light}
    !!! info "Information:"
        Something **new** is coming to `mkdocs-shadcn`

    !!! note "Note:"
        We notice that `x=2`

    !!! warning "Warning:"
        There is a *risk* doing `x/0`

    !!! danger "Danger:"
        Don't look at `node_modules` **please**! 
    
    !!! success "Success:"
        It works! Tell your friends to download `mkdocs-shacn`


!!! info "Information:"
    Something **new** is coming to `mkdocs-shadcn`

!!! note "Note:"
    We notice that `x=2`

!!! warning "Warning:"
    There is a *risk* doing `x/0`

!!! danger "Danger:"
    Don't look at `node_modules` **please**! 

!!! success "Success:"
    It works! Tell your friends to download `mkdocs-shacn`

## Code

You cannot use [`fenced_code`](./fenced_code.md) inside admonition since:
> Fenced Code Blocks are only supported at the document root level ([source](https://python-markdown.github.io/extensions/fenced_code_blocks/#syntax))

Currently, only [`codehilite`](./codehilite.md) can be nested inside admonition, like in the example below.

```md
!!! note "Admonition + Code"
    You may face the limits of `codehilite` however.

        :::python
        def fibonacci(n):
            a, b = 0, 1
            for _ in range(n):
                yield a
                a, b = b, a + b

        for num in fibonacci(10):
            print(num)
```

!!! note "Admonition + Code"
    You may face the limits of `codehilite` however.

        :::python
        def fibonacci(n):
            a, b = 0, 1
            for _ in range(n):
                yield a
                a, b = b, a + b

        for num in fibonacci(10):
            print(num)
