---
title: Fenced code
summary: Another way to define code blocks
external_links:
    Reference: https://python-markdown.github.io/extensions/fenced_code_blocks/
---

The Fenced Code Blocks extension adds a secondary way to define code blocks, which overcomes a few limitations of indented code blocks.

!!! warning "Warning"
    Fenced Code Blocks are only supported at the **document root** level.

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - fenced_code
```

To enable syntax highlighting, the [`codehilite`](./codehilite.md) extension must be enabled.

## Syntax

~~~ md
```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```
~~~

produces the raw code:

``` { .python use_pygments="false" }
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```

if [`attr_list`](./attribute_lists.md) is enabled, you can add attributes to the code block by adding them after the language name:

~~~ md
``` { .python #code-id .custom-class  }
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```
~~~

If produces the same code block as above, but with the `id` and `class` attributes added.

``` { .python #code-id .custom-class use_pygments="false" }
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```


If [`codehilite`](./codehilite.md) is enabled. You can add any pygments [html formatter options](https://pygments.org/docs/formatters/#HtmlFormatter).

!!! warning 
    With [`codehilite`](./codehilite.md) enabled, [`attr_list`](./attribute_lists.md) key/value attributes are not supported.

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