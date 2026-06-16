---
title: Mike
alpha: true
summary: Versioning tool
external_links:
    Reference: https://github.com/jimporter/mike
---



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

```yaml
# mkdocs.yml

plugins:
  - mike
```

The purpose of mike is to deploy multiple versions of your documentation, that won't be touched anymore. The documentation is built into a site, published into a branch in your repository. The management of this branch should be done with mike.

## Examples
The commands presented in this section can be run with pip, uv or poetry.

/// tab | pip

    :::bash
    mike ...
///

/// tab | uv

    :::bash
    uv run mike ...
///

/// tab | poetry

    :::bash
    poetry run mike ...
///

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
