---
title: Codexec
summary: Execute code(hilite) snippets
new: true
---

The Codexec extensions extends a [codehilite](codehilite.md) code block to execute the code and display the output.

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - codehilite
  - shadcn.extensions.codexec
```

## Syntax

It supports the following languages: `r`, `c`, `cpp`, `csharp`, `java`, `python`, `javascript`, `typescript`, `scala`, `dart`, `ruby`, `golang`, `php`, `swift` and `rust`.

!!! warning "Warning"
    The extension parses the language set in the codehilite block


~~~md
/// codexec

    :::python
    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    for num in fibonacci(10):
        print(num)

///
~~~

/// codexec

    :::python
    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    for num in fibonacci(10):
        print(num)

///

## Errors

Syntax or compiling errors are highlighted in the output,

=== "Python"

    /// codexec

        :::python
        print("hello world!"

    ///

=== "C"

    /// codexec

        :::c
        #include <stdio.h>

        int main(void) {
            const int a = 42;
            a = -1;
            printf("a = %d\n", a);
        }

    ///



while exceptions are printed normally.



=== "Python"

    /// codexec

        :::python
        def raise_exception():
            raise Exception("This is an error")
        
        raise_exception()

    ///

=== "C++"

    /// codexec

        :::cpp
        void raise_exception() {
            throw "This is an error";
        }

        int main(void) {
            raise_exception();
            return 0;
        }

    ///

