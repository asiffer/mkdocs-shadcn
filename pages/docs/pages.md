---
title: Pages
summary: Metadata configuration
---

Like this page, you can define its title (and subtitle) through front-matter configuration.

```yaml
title: Pages # title
summary: Metadata configuration # subtitle
```

You can also define your page title directly with `# Page title` in the markdown content.

## Navigation

The navigation follows bare mkdocs. You should just notice that folders will create categories in the sidebar.
To sort the sections, you can use the common `00_section_title/` hack. The first numbers sort the folders in the filesystem (so the sections). They are removed by the theme at compile time. 

!!! warning "Important"
    `mkdocs-shadcn` has not been tested with highly nested documentation (`d>2`, i.e. `root / folder / folder`)

In addition, two other attributes may help to configure pages within the sidebar.

```yaml
order: 2 
sidebar_title: Navigation title
```

The `order` attribute may help to change the rank of the page in the sidebar (without setting the `nav` setting in `mkdocs.yml`). By default, mkdocs ranks pages through alphabetical order. We keep this behavior if `order` is not set. Let us take this example:

```ini
| a.md ; order not set
| b.md ; order: 42
| c.md ; order: 0
| d.md ; order not set
```

After a first pass we will have

```ini
| a.md ; order: 0
| b.md ; order: 42
| c.md ; order: 0
| d.md ; order: 1
```

So in the sidebar we will get `a.md`, `c.md`, `d.md` and `b.md`.

## External links

You can add external links (like "API Reference") in the page header. This is done through the `external_links` attribute in the front-matter.

```yaml
external_links:
  "API Reference": https://ui.shadcn.com/docs/components
  GitHub: https://github.com/asiffer/mkdocs-shadcn
```

## SEO

The following attributes are supported for SEO (`<meta>` attributes in the `<head>`).

```yaml
description: Extra page description
keywords: mkdocs,shadcn
author: asiffer
image: https://raw.githubusercontent.com/asiffer/mkdocs-shadcn/refs/heads/master/.github/assets/logo.svg
```

## Extra

As we may find in [shadcn/ui](https://ui.shadcn.com/docs), we can add a `NEW` tag in the sidebar 
(`Alpha` and `Beta` are also available).

```yaml
new: true
# beta: true
# alpha: true
```
