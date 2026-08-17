---
title: Excalidraw
summary: The famous hand-drawn style whiteboard
alpha: true
---

The excalidraw plugin provides a true editor, integrated in the mkdocs dev server. So you can edit the drawing at dev time and display the output svg at build time.

![demo](../assets/img/excalidraw.gif)

## Configuration

```yaml
# mkdocs.yml

plugins:
  - search
  - excalidraw
```

!!! note
    The `excalidraw` injects a markdown extension  (`shadcn.extensions.excalidraw`) at runtime. You don't have to worry about it. 

The plugin need to store you excalidraw drawings (`json` and `svg` files). By default it stores these files under `excalidraw/`. So you are likely to have this layout:

```plaintext
my-project/
├── ...
├── mkdocs.yml
├── docs/
│   ├── index.md
│   └── utils.md
├── excalidraw/
│   ├── drawing0.json
│   └── drawing0.svg
```

You can change this folder with the `directory` option (the path is relative to the root directory, i.e. the directory where `mkdocs.yml` lives).

```yaml
# mkdocs.yml

plugins:
  search:
  excalidraw:
    directory: assets/excalidraw
```

!!! warning "Warning"
    Currently, you should avoid putting excalidraw files within your `docs/` folder. 
    A server hot reload triggers everytime the 
    content is edited.

## Syntax

The path to the json file is relative to the directory provided to the plugin. The title is injected as build time through a `<title></title>` tag inside the output svg file.

    :::md
    ~{title}(path/to/file.json)


~{test}(drawing0.json)


