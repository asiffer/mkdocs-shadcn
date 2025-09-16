---
title: pymdownx.blocks.caption
summary: Enter into legend
external_links:
  Reference: https://facelessuser.github.io/pymdown-extensions/extensions/blocks/plugins/caption/
---


The `pymdownx.blocks.caption` extension is a Python-Markdown plugin that wraps blocks (table or figure) in `<figure>` tags and inserting a `<figcaption>` tag with specified content.

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - pymdownx.blocks.caption
```

## Syntax



```md
Here is a table:

| Invoice    | Status  | Method        |        Amount |
| :--------- | :------ | :------------ | ------------: |
| **INV001** | Paid    | Credit Card   |       $250.00 |
| **INV002** | Pending | PayPal        |       $150.00 |
| **INV003** | Unpaid  | Bank Transfer |       $350.00 |
| **INV004** | Paid    | Credit Card   |       $450.00 |
| **INV005** | Paid    | PayPal        |       $550.00 |
| **INV006** | Pending | Bank Transfer |       $200.00 |
| **INV007** | Unpaid  | Credit Card   |       $300.00 |
| **Total**  |         |               | **$2,500.00** |

/// caption 
A list of your recent invoices.
///

```

Here is a table:

| Invoice    | Status  | Method        |        Amount |
| :--------- | :------ | :------------ | ------------: |
| **INV001** | Paid    | Credit Card   |       $250.00 |
| **INV002** | Pending | PayPal        |       $150.00 |
| **INV003** | Unpaid  | Bank Transfer |       $350.00 |
| **INV004** | Paid    | Credit Card   |       $450.00 |
| **INV005** | Paid    | PayPal        |       $550.00 |
| **INV006** | Pending | Bank Transfer |       $200.00 |
| **INV007** | Unpaid  | Credit Card   |       $300.00 |
| **Total**  |         |               | **$2,500.00** |

/// caption 
A list of your recent invoices.
///

For table or figure numbering, you can use `table-caption` or `figure-caption` instead of `caption`.

/// tab | `table-caption` 

```md
| Task      | Title                                                                                           | Status      | Priority |
| --------- | ----------------------------------------------------------------------------------------------- | ----------- | -------- |
| TASK-8782 | **Documentation** You can't compress the program without quantifying the open-source SSD pixel! | In Progress | Medium   |
| TASK-7878 | **Documentation** Try to calculate the EXE feed, maybe it will index the multi-byte pixel!      | Backlog     | Medium   |
| TASK-7839 | **Bug** We need to bypass the neural TCP card!                                                  | TODO        | High     |

/// table-caption
A list of your current tasks.
///
```

| Task      | Title                                                                                           | Status      | Priority |
| --------- | ----------------------------------------------------------------------------------------------- | ----------- | -------- |
| TASK-8782 | **Documentation** You can't compress the program without quantifying the open-source SSD pixel! | In Progress | Medium   |
| TASK-7878 | **Documentation** Try to calculate the EXE feed, maybe it will index the multi-byte pixel!      | Backlog     | Medium   |
| TASK-7839 | **Bug** We need to bypass the neural TCP card!                                                  | TODO        | High     |

/// table-caption
A list of your current tasks.
///

///

/// tab | `figure-caption` 

```md
![Mountain](https://images.unsplash.com/photo-1554629947-334ff61d85dc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&h=666&q=80)

/// figure-caption
Aoraki / Mount Cook, New Zealand
///
```

![Mountain](https://images.unsplash.com/photo-1554629947-334ff61d85dc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&h=666&q=80)

/// figure-caption
Aoraki / Mount Cook, New Zealand
///

///


