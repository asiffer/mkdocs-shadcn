---
title: Iconify
summary: Insert any icon in your documentation
external_links:
  Icons: https://icon-sets.iconify.design/
  "Iconify API": https://iconify.design/docs/api/svg.html#query
---

This extension uses the [Iconify API](https://iconify.design/docs/api/svg.html#query) to fetch any icon from the [Iconify collection](https://icon-sets.iconify.design/) and insert it in your documentation (rendered as **inline svg**).

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - shadcn.extensions.iconify
```


## Syntax

Basically, you must wrap the iconify key with `+` symbols. The key is composed by the provider and the icon name, separated by a colon `:`. You can look at all the available collections.

```md
+lucide:rocket+
```

+lucide:rocket+


By default, the icon height is set to `20px`, but you can override it by passing the `height` parameter (and any other valid query parameter supported by the [Iconify API](https://iconify.design/docs/api/svg.html#query)).

```md
+lucide:cassette-tape;height=3em+
```

+lucide:cassette-tape;height=3em+

Remember that icons are inlined.

```md
> Mathematics +heroicons:variable;height=1em+ consists of proving 
> the most obvious thing +heroicons:exclamation-circle;color=#ba3329;height=5%+ 
> in the least obvious way +heroicons:question-mark-circle-solid;color=#0550AE;width=3em+.
> - Pólya
``` 

> Mathematics +heroicons:variable;height=1em+ consists of proving 
> the most obvious thing +heroicons:exclamation-circle;color=#ba3329;height=5%+ 
> in the least obvious way +heroicons:question-mark-circle-solid;color=#0550AE;width=3em+.
> - Pólya

