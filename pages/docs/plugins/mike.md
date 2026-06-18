---
title: Mike
new: true
summary: Versioning tool
external_links:
    Reference: https://github.com/jimporter/mike
---

The purpose of mike is to deploy multiple versions of your documentation, that won't be touched anymore.

!!! warning ""
    Using `mike` is relevant only if you **deploy docs through a branch** (default to `gh-pages`) as it uses `git` mechanisms in backstage.

## Installation

/// tab | pip

    :::bash
    pip install mike
///

/// tab | uv

    :::bash
    uv add mike
///

/// tab | poetry

    :::bash
    poetry add mike
///

## Configuration

You can include the `mike` plugin but it is automatically injected when using the `mike` command (like `mike deploy` for example).

```yaml
# mkdocs.yml

plugins:
  - mike
```


## Examples

### Add version to documentation site

This creates a branch in the documentation branch, maned after `<version>` tag and aliased `latest`.

```bash
mike deploy --branch <branch_name> --update-aliases <version> latest
```

### Define default doc version

This should be done once per documentation branch. It defines the doc version aliased as `latest` to be the landing page of the documentation site.

```bash
mike set-default --branch <branch_name> latest
```
