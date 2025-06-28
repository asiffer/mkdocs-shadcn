---
title: Install
---

Add the package to your project.

=== "pip"

        :::bash
        pip install mkdocs-shadcn


=== "uv"

        :::bash
        uv add mkdocs-shadcn

=== "poetry"

        :::bash
        poetry add mkdocs-shadcn


Configure MkDocs:

```yaml
# mkdocs.yml
site_name: "awesome-project"
theme:
  name: shadcn
  show_title: true # show the title in the top bar
  show_stargazers: true # show the stargazers in the top bar
  pygments_style: # default styles 
        light: shadcn-light
        dark: github-dark
  icon: heroicons:rocket-launch # use the shadcn svg if not defined
```

Currently there are not many options and they are likely to change. You can define an `icon` (image url or [iconify class](https://icon-sets.iconify.design/)) for the top bar.