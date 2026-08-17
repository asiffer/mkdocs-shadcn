---
title: Hover Card
summary: A rich tooltip
new: true
---

This extension tries to mimick the [shadcn hover card component](https://ui.shadcn.com/docs/components/radix/hover-card) (just html and css).

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - shadcn.extensions.hover_card
```

## Syntax

You can either put the content inline or in a saparate block.

```md
If you want to [put it inline]^[something to `display` right *now* but in **hover card**, like $f(x) = x^2$].
Or choose the [block syntax]^[#hc0].

/// hover-card | hc0

Like a Fibonacci function.

    :::python
    def fib(n):
        a, b = 0, 1
        while a < n:
            print(a, end=' ')
            a, b = b, a+b
            print()
    fib(1000)

///

```

Which gives:

If you want to [put it inline]^[something to `display` right *now* but in **hover card**, like $f(x) = x^2$].
Or choose the [block syntax]^[#hc0].

/// hover-card | hc0

Like a Fibonacci function.

    :::python
    def fib(n):
        a, b = 0, 1
        while a < n:
            print(a, end=' ')
            a, b = b, a+b
            print()
    fib(1000)

///


## Position

By default the card is positioned at the bottom of the trigger.
In the **block syntax** you can pass the `position` option.

```md
You can [hover it at the bottom]^[#test] (default),
or [at the top]^[#test-top],
or [at the right]^[#test-right],
or [at the left]^[#test-left].

/// hover-card | test

I am at the bottom.

///

/// hover-card | test-top
    position: top

I am the top.

///

/// hover-card | test-right
    position: right

I am at the right.

///

/// hover-card | test-left
    position: left

I am at the left.

///
```

It outputs:

You can [hover it at the bottom]^[#test] (default),
or [at the top]^[#test-top],
or [at the left]^[#test-left],
or [at the right]^[#test-right].

/// hover-card | test

I am at the bottom.

///

/// hover-card | test-top
    position: top

I am the top.

///

/// hover-card | test-right
    position: right

I am at the right.

///

/// hover-card | test-left
    position: left

I am at the left.

///

## Customization

Currently, you can pass a `class` option to the card if you want to modify its style.

```md
You can [customize]^[#test-class] a block.

/// hover-card | test-class
    class: "font-bold font-mono"

Yeah! Just look at the result.

///
```

You can [customize]^[#test-class] a block.

/// hover-card | test-class
    class: "font-bold font-mono"

Yeah! Just look at the result.

///
