---
title: pymdownx.progressbar
summary: Visually appealing progress bars
external_links:
  Reference: https://facelessuser.github.io/pymdown-extensions/extensions/progressbar/
---



The `pymdownx.progressbar` extension is a Python-Markdown plugin that allows you to create visually appealing progress bars directly in your Markdown content.

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - pymdownx.progressbar
```

## Syntax

You can also leverage `attr_list` to colorize the progress bar.

```md
[=50% ""]
[=75% "75%"]
[=95% "Awesome"]{: .success}
[=25% "25%"]{: .warning}
[=5% "5%"]{: .danger}
```

[=50% ""]
[=75% "75%"]
[=95% "Awesome"]{: .success}
[=25% "25%"]{: .warning}
[=5% "5%"]{: .danger}
