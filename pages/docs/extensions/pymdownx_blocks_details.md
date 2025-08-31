---
title: pymdownx.blocks.details
summary: Collapsible details
external_links:
  Reference: https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/details/
---


The `pymdownx.blocks.details` extension is a Python-Markdown plugin that provides a simple way to create collapsible "details" blocks in your Markdown content. 

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - pymdownx.blocks.details
```

## Syntax

```md
### FAQ

/// details | Is this theme an official shadcn port?
No. But you can still [star it +heroicons:star+](hhttps://github.com/asiffer/mkdocs-shadcn)
///


/// details | Why a new mkdocs theme while `material` exists?
First the [shadcn/ui](https://ui.shadcn.com/) theme is just incredible. 

Actually, nothing can compete with the [material](https://squidfunk.github.io/mkdocs-material/) theme which is very mature and feature rich. 

In addition to sticking to the shadcn theme, the idea is to remain a simple theme, providing some special built-in features that we may not find in other themes.
///


/// details | Is it open to contributions?
Yes, yes and yes! On its own, the theme tries to provide more and more relevant extensions/plugins. But anyone can define what could be relevant! 

[Open an issue](https://github.com/asiffer/mkdocs-shadcn/issues) and let us discuss about it +heroicons:face-smile+
///

/// details | Is `mkdocs-rube-goldberg-plugin-extension` supported?
In general no.
///
```


### FAQ

/// details | Is this theme an official shadcn port?
No. But you can still [star it +heroicons:star+](hhttps://github.com/asiffer/mkdocs-shadcn)
///


/// details | Why a new mkdocs theme while `material` exists?
First the [shadcn/ui](https://ui.shadcn.com/) theme is just incredible. 

Actually, nothing can compete with the [material](https://squidfunk.github.io/mkdocs-material/) theme which is very mature and feature rich. 

In addition to sticking to the shadcn theme, the idea is to remain a simple theme, providing some special built-in features that we may not find in other themes.
///


/// details | Is it open to contributions?
Yes, yes and yes! On its own, the theme tries to provide more and more relevant extensions/plugins. But anyone can define what could be relevant! 

[Open an issue](https://github.com/asiffer/mkdocs-shadcn/issues) and let us discuss about it +heroicons:face-smile+
///

/// details | Is `mkdocs-rube-goldberg-plugin-extension` supported?
In general no.
///

