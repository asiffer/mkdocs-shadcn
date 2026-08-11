---
title: Attribute Lists
summary: Customize HTML attributes
external_links:
    Reference: https://python-markdown.github.io/extensions/attr_list/
---

The `attr_list` extension is a feature of Python-Markdown that allows you to add custom attributes to HTML elements generated from Markdown. 


## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - attr_list
```

## Syntax

The theme may provide some pre-computed classes. The `attr_list` extension (with `extra`) allows to customize the attribute of the output html. Here is a example with the `reference` class.

```md
[Reference](https://python-markdown.github.io/extensions/attr_list/){: class="reference" }
```


[Reference](https://python-markdown.github.io/extensions/attr_list/){: class="reference" }
