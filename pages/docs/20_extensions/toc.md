---
title: Table of Contents
summary: Known as TOC to its friends 
new: true
external_links:
    Reference: https://python-markdown.github.io/extensions/toc/
---

The `toc` extension is not fully supported since the theme already provides 
at table of contents in the right sidebar.


## Configuration

You can notably activate permalinks.

```yaml
# mkdocs.yml

markdown_extensions:
  toc:
    permalink: true
```

When you click on such a link, the browser copies it in the clipboard.

For **leading marker**, you must set the permalink class as follows:

```yaml
# mkdocs.yml

markdown_extensions:
  toc:
    permalink: true
    permalink_leading: true
    permalink_class: "headerlink leading"
```