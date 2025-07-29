---
title: pymdownx.arithmatex
summary: For maths lovers
external_links:
    Reference: https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/
---

The `pymdownx.arithmatex` extension is a Python-Markdown plugin that enables rendering of mathematical expressions written in LaTeX syntax. 

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - pymdownx.arithmatex:
      generic: true # required to work
```

!!! note "Note:"
    When `pymdownx.arithmatex` is enabled, the theme automatically 
    loads [KateX](https://katex.org/) material to render math (css, js and fonts). 
    Currently we ship the version `v0.16.21`.

!!! info "NEW!"
    Now you can pass options to Katex (like macros). See the dedicated [theme option](../get_started.md#katex_options-dict) for more details.

## Syntax

Just like latex.

```tex
Let $F$ be a primitive of $f$,
$$
\int_{a}^b f(x) ~\dx = F(b) - F(a).
$$
```

Let $F$ be a primitive of $f$,

$$
\int_{a}^b f(x) ~ \dx = F(b) - F(a).
$$

You can combine with [admonition](admonition.md) for instance.

```md
!!! note "Theorem"

    Let $X_1, X_2, \dots, X_n$ be a sequence of independent and 
    identically distributed random variables with mean $\mu$ and 
    finite variance $\sigma^2$. Define the sample mean:

    $$
    \overline{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i
    $$

    Then, as  $n \to \infty$:

    $$
    \frac{\sqrt{n}(\overline{X}_n - \mu)}{\sigma} \xrightarrow{d} \mathcal{N}(0,1)
    $$

    In other words, the distribution of the standardized 
    sample mean approaches the standard normal distribution:

    $$
    \frac{\overline{X}_n - \mu}{\sigma/\sqrt{n}} \xrightarrow{d} \mathcal{N}(0,1), \quad \text{as } n \to \infty
    $$
```

!!! note "Theorem"

    Let $X_1, X_2, \dots, X_n$ be a sequence of independent and 
    identically distributed random variables with mean $\mu$ and 
    finite variance $\sigma^2$. Define the sample mean:

    $$
    \overline{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i
    $$

    Then, as  $n \to \infty$:

    $$
    \frac{\sqrt{n}(\overline{X}_n - \mu)}{\sigma} \xrightarrow{d} \mathcal{N}(0,1)
    $$

    In other words, the distribution of the standardized 
    sample mean approaches the standard normal distribution:

    $$
    \frac{\overline{X}_n - \mu}{\sigma/\sqrt{n}} \xrightarrow{d} \mathcal{N}(0,1), \quad \text{as } n \to \infty
    $$