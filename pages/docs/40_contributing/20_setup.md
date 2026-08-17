---
title: Setup
summary: Be ready to contribute
---

First clone the repo:
```shell
git clone https://github.com/asiffer/mkdocs-shadcn
cd mkdocs-shadcn
```

Then you can install python dependencies ([`uv`](https://docs.astral.sh/uv/) required),
```shell
uv sync --all-extras
```

and pre-commits:

```shell
uv run pre-commit install
```

Finally, you can install tailwind with your favourite package manager (npm, yarn, bun, etc.):

```shell
bun install
```

### Dev mode

We use the project pages to as a test project for this theme. You can run the local server in the `pages/` subdirectory.

```shell
cd pages/
uv run mkdocs serve --watch-theme -w ..
```

In parallel, you are likely to run the tailwind watcher to compile the css sources. In the root folder:

```shell
bun dev
```

### Tests

Tests are managed by [`pytest`](https://docs.pytest.org/en/stable/) and are located in the [tests/](https://github.com/asiffer/mkdocs-shadcn/tree/master/tests) folder.

Currently we test:
- browser issue through [playwright](https://playwright.dev/)
- [mike](https://github.com/jimporter/mike) integration


You can run them as follows.
```shell
uv run pytest -xvs .
```