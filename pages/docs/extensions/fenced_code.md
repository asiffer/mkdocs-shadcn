---
title: Fenced code
---

The Fenced Code Blocks extension adds a secondary way to define code blocks, which overcomes a few limitations of indented code blocks.

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - fenced_code
```

## Syntax

You can add any pygments [html formatter options](https://pygments.org/docs/formatters/#HtmlFormatter).

~~~ md
``` { .python linenos="table" hl_lines="4 5" }
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```
~~~


``` { .python linenos="table" hl_lines="4 5" }
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```

As another example, you can also add references to the lines of code (goto [line 4](#fibo-4) and [line 5](#fibo-5)).

~~~ md
``` { .python linenos="inline" hl_lines="4 5" anchorlinenos="true" lineanchors="fibo" }
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```
~~~


``` { .python linenos="inline" hl_lines="4 5" anchorlinenos="true" lineanchors="fibo" }
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```