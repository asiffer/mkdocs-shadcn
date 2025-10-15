---
title: Pages
summary: Metadata configuration
show_datetime: true
---

Like this page, you can define its title (and subtitle) through front-matter configuration.

```yaml
title: Pages # title
summary: Metadata configuration # subtitle
```

You can also define your page title directly with `# Page title` in the markdown content.

## Navigation

The navigation follows bare mkdocs. You should just notice that folders will create categories in the sidebar (or in the top bar when `topbar_sections: true`).
To sort the sections, you can use the common `00_section_title/` hack. The first numbers sort the folders in the filesystem (so the sections). They are removed by the theme at compile time. 

!!! warning "Important"
    `mkdocs-shadcn` has not been extensively tested with highly nested documentation (`d>2`, i.e. `root / folder / folder`). When subfolders are used, we may recommend to activate the [`topbar_sections`](./get_started.md#topbar_sections-bool) option in the theme configuration. This will display the top level sections in the top bar.

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

!!! danger "Caveat"
    The sidebar order does not change the internal navigation order. It implies that `previous` and `next` pages are unlikely to match a custom order. To prevent that, either use the classical `00_page.md`, `01_page.md`, `02_page.md` ... file pattern in your folder or set the navigation in `mkdocs.yml`.

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

The [`show_datetime` theme option](./get_started.md#show_datetime-bool) can be overriden per page 
if you want to show/hide the last update date for a specific page.

```yaml
show_datetime: true
```


Finally you an also load per-page CSS and JS files. This is done through the `extra_css` and `extra_javascript` attributes.

```yaml
extra_css:
  - css/custom.css
extra_javascript:
  - js/custom.js
```

## Example

```yaml
title: Demo page
summary: Example page for mkdocs-shadcn users
new: true
description: Example page for mkdocs-shadcn users
keywords: mkdocs,shadcn,demo
author: asiffer
image: https://raw.githubusercontent.com/asiffer/mkdocs-shadcn/refs/heads/master/.github/assets/logo.svg
order: 5
sidebar_title: Demo
show_datetime: false
external_links:
  "API Reference": https://ui.shadcn.com/docs/components
  GitHub: "https://github.com/asiffer/mkdocs-shadcn"
extra_css:
  - css/custom-style.css
extra_javascript:
  - js/custom-script.js
```