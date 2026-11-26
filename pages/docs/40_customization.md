---
title: Customization
summary: How to override the default theme
---

The main way to override the theme is to provide custom css, notably through the website or page `extra_css` key.

```yml
extra_css:
    - css/custom.css
```

This css is **not tailwind related**. It means that you do not have to know tailwind but also that any tailwind class or utility won't be understood. It is **bare css**. However you could use the variables set by either [tailwind](https://tailwindcss.com/docs/theme) of the [shadcn configuration](https://github.com/asiffer/mkdocs-shadcn/blob/master/tailwind/shadcn.css).

!!! important "Note"
    Nothing prevent you from using a css tool to generate that custom css.


## Layers

Tailwind defines [4 layers](https://tailwindcss.com/docs/preflight#disabling-preflight):

```css
@layer theme, base, components, utilities;
```

While tailwind populates some presets in some of these layers, `mkdocs-shadcn` use `base` and `theme` to define the theme.

To override the theme, you should then use upper level layers like `components`. For instance, if you want to justify text on pages, you can write it as follows:

```css
/* css/custom.css */
@layer components {
    article p {
        text-align: justify;
    }
}
```

!!! warning "Important"
    If your style does not override the theme style, it is probably due to a **selector specificity issue**, i.e. the theme selector is probably more specific than yours. You can find it in your browsr inspector or directly in the [tailwind definitions of the repo](https://github.com/asiffer/mkdocs-shadcn/tree/master/tailwind) and align your css rule to it.


## Theme configuration

Obvioulsy there are also some [theme options](./15_configuration.md) you can configure to customize the website, like defining the logo, the accent color or the pygments style.

## Templates

`mkdocs-shadcn` tries to follow the spirit of `MkDocs` that allows theme templates to be overriden by users. 

All the templates are located in [`shadcn/templates`](https://github.com/asiffer/mkdocs-shadcn/tree/master/shadcn/templates). Currently they are organized as follows:

| Location    | Description                           |
| ----------- | ------------------------------------- |
| `./`        | Main templates to define a page       |
| `partials/` | Smaller components                    |
| `icons/`    | SVG icons used in the theme           |
| `external/` | Templates specific plugins/extensions |

!!! warning "Warning"
    This structure is quite fragile and remain a work in progress. It means that some main templates are likely to be splitted into several partials.


You can override a template by declaring a custom directory in the the mkdocs configuration:

```yaml
theme:
  name: shadcn
  custom_dir: custom_theme/
```

Then you can for instance either replace a template to modify the aspect of an element (if the css is not enough),

```html
<!-- custom_theme/templates/partials/next.html -->
<a id="next-button" href="{{ page.next_page.url | url }}">Next</a>
```

or use a template hook, like `extra_head.html` to inject additional stuff in the `<head>` of the website:

```html
<!-- custom_theme/templates/extra_head.html -->
<link href="https://fonts.googleapis.com/css2?family=Geist+Pixel&display=swap" rel="stylesheet">
```

Similarly, `header_links.html` is a hook to inject content in the top bar (right side, before the search). By default, it renders the [`topbar_links`](./15_configuration.md#topbar_links-dict) theme option. The theme css classes are available in the header, so your elements stay consistent with the rest of the top bar:

```html
<!-- custom_theme/templates/header_links.html -->
<a class="button ghost" href="/fr/">Français</a>
```
