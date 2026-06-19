---
title: Autonumber
summary: Cross-reference anything
new: true
---

The `autonumber` plugin automatically numbers labeled elements (figures, tables, equations...) across your documentation and replaces references to them with clickable links. It supports cross-page references.

!!! info "Info"
    While it may be similar to [`pymdownx.blocks.caption`](../extensions/pymdownx_blocks_caption.md), it goes further by enabling referencing.

## Configuration

```yaml
# mkdocs.yml

plugins:
  - search
  - autonumber
```

### Options

| Option      | Type   | Default   | Description                                                                            |
| :---------- | :----- | :-------- | :------------------------------------------------------------------------------------- |
| `numbering` | `flat` | `flat`    | Numbering strategy. Currently only `flat` (per-page sequential counters) is supported. |
| `prefixes`  | `dict` | see below | Mapping of short prefix keys to their display names.                                   |

The default `prefixes` value is:

```yaml
plugins:
  autonumber:
    prefixes:
      fig: Figure
      tbl: Table
      eq: Equation
```

You can override it or extend it with your own prefixes:

```yaml
plugins:
  autonumber:
    prefixes:
      fig: Figure
      tbl: Table
      eq: Equation
      thm: Theorem
      lem: Lemma
      prop: Proposition
```

## Syntax

The plugin works in two steps: **labeling** and **referencing**.

Place a label inline, where you want to number.

```md
{#prefix:unique-id}
```

The label is replaced by a `<span>` tag as follows:
```html
<span id="prefix:unique-id" class="autonumber prefix">{mapped_prefix} {number}</span>
```

Then you can reference it anywhere in your doc through the following syntax.
```md
@prefix:unique-id
```

This will be replaced by an `<a>` tag as follows:
```html
<a href="{page_canonical_url}#prefix:unique-id" class="autonumber prefix">{mapped_prefix} {number}</a>
```

!!! info "Tip"
    You can reference with `@Prefix:unique-id` (capitalized) if you want the mapped name to be capitalized too.



## Examples

### Figures

For tables and figures, you can pair with [`pymdownx.blocks.caption`](../extensions/pymdownx_blocks_caption.md) extension.

```md
![Mountain](https://images.unsplash.com/photo-1554629947-334ff61d85dc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&h=666&q=80)

/// caption 
{#fig﹕mountain} - Aoraki / Mount Cook, New Zealand
///

@Fig﹕mountain is awesome!
```

![Mountain](https://images.unsplash.com/photo-1554629947-334ff61d85dc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&h=666&q=80)

/// caption
{#fig:mountain} - Aoraki / Mount Cook, New Zealand
///

@Fig:mountain is awesome!

### Tables

```md
| Name  | Score |
| :---- | ----: |
| Alice |    95 |
| Bob   |    87 |


/// caption | <
{#tbl﹕scores} - List of scores
/// 

@Tbl﹕scores lists the final scores.
```

| Name  | Score |
| :---- | ----: |
| Alice |    95 |
| Bob   |    87 |


/// caption | <
{#tbl:scores} - List of scores
/// 

@Tbl:scores lists the final scores.

### Math

It can be paired with [admonitions](../extensions/admonition.md) to get a latex-like experience.

```md
!!! note "{#th﹕dominated_convergence} (Lebesgue's dominated convergence theorem)"
    Let $(f_n)_{n\in\NN}$ be a sequence of complex-valued measurable functions on a measure space $(S,\Sigma,\mu)$. Suppose that the sequence converges pointwise to a function $f$ i.e.

    $$
    \lim _{n\to \infty }f_{n}(x)=f(x)
    $$

    exists for every $x\in S$. Assume moreover that the sequence $f_{n}$ is dominated by some integrable function $g$ in the sense that

    $$
    |f_{n}(x)|\leq g(x)
    $$

    for all points $x\in S$ and all $n\in\NN$. Then $f_n$, $f$ are integrable and

    $$
    \lim _{n\to \infty}\int_{S}f_{n}\,d\mu =\int _{S}\lim _{n\to \infty }f_{n}d\mu =\int _{S}f\,d\mu 
    $$
```

!!! note "{#th:dominated_convergence} (Lebesgue's dominated convergence theorem)"
    Let $(f_n)_{n\in\NN}$ be a sequence of complex-valued measurable functions on a measure space $(S,\Sigma,\mu)$. Suppose that the sequence converges pointwise to a function $f$ i.e.

    $$
    \lim _{n\to \infty }f_{n}(x)=f(x)
    $$

    exists for every $x\in S$. Assume moreover that the sequence $f_{n}$ is dominated by some integrable function $g$ in the sense that

    $$
    |f_{n}(x)|\leq g(x)
    $$

    for all points $x\in S$ and all $n\in\NN$. Then $f_n$, $f$ are integrable and

    $$
    \lim _{n\to \infty}\int_{S}f_{n}\,d\mu =\int _{S}\lim _{n\to \infty }f_{n}d\mu =\int _{S}f\,d\mu 
    $$

The @th:dominated_convergence gives a mild sufficient condition under which limits and integrals of a sequence of functions can be interchanged.
