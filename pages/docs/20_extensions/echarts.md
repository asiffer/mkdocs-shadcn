---
title: Apache ECharts
summary: An Open Source JavaScript Visualization Library
alpha: true
external_links:
    Reference: https://echarts.apache.org/en/index.html
---


The theme provides an alpha version of an `echarts` extensions, allowing to render 
charts based on the provided options. 

## Configuration

```yaml
# mkdocs.yml

markdown_extensions:
  - shadcn.extensions.echarts.alpha
```

## Syntax

From a `js` config it basically plots charts through the Apache ECharts library. 
The extension uses the [PyMdown Blocks Extension API](https://facelessuser.github.io/pymdown-extensions/extensions/blocks/) so its syntax (similar to [tab](pymdownx_blocks_tab.md) or [details](pymdownx_blocks_details.md)).

```md
/// echarts
{ 
  /* echarts js config */
}
///
```

Currently, the extension does not support dark mode.


!!! warning "Important"
    The `js` config is passed to the `.setOption` method. The extension crops the input so that it keeps the outtermost curly braces (`{` and `}`) and removes what is outside. You can look at the library [API](https://echarts.apache.org/en/option.html). In a nutshell, it removes code outside of the config object. 

!!! info "Tip"
    You can either inline all the config within the block or insert snippets from file thanks to the [`pymdownx.snippets` extension](https://facelessuser.github.io/pymdown-extensions/extensions/snippets/).


    <div class="codehilite"><pre><span></span><code>/// echarts
      &ndash;&ndash;8<-- "example.js"
    ///
    </code></pre></div>


## Options

You can pass attributes to the chart container through the builtin `attrs` key. The attributes are passed to the `div` element that contains the chart. In addition e expose a `renderer` key that defines the output format of the chart (`svg` or `canvas`). The default values are given below.

~~~md
/// echarts
    renderer: "svg"
    attrs:
        class: "echarts"
        style: "width:100%;height:500px;"

/* config here */
///
~~~

In the following example we use the `canvas` renderer and re-define `style` to `width:100%;height:60vh;` (note also that it resizes with the window).

/// tab | Output

/// echarts
    renderer: "canvas"
    attrs:
        style: "width:100%;height:60vh;"

--8<-- "docs/assets/echarts/line.js"
///

///


/// tab | Code

~~~md
/// echarts
    renderer: "canvas"
    attrs:
        style: "width:100%;height:60vh;"

--8<-- "docs/assets/echarts/line.js"

///
~~~

///


## Examples

### Line


/// tab | Output

/// echarts

--8<-- "docs/assets/echarts/line.js"
///

///


/// tab | Code

~~~md
/// echarts

--8<-- "docs/assets/echarts/line.js"

///
~~~

///


### Bars

/// tab | Output

/// echarts
--8<-- "docs/assets/echarts/bars.js"
///

///


/// tab | Code

~~~md
/// echarts
--8<-- "docs/assets/echarts/bars.js"
///
~~~

///


### Pie

/// tab | Output

/// echarts
--8<-- "docs/assets/echarts/pie.js"
///

///


/// tab | Code

~~~md
/// echarts
--8<-- "docs/assets/echarts/pie.js"
///
~~~

///


### Scatter

/// tab | Output

/// echarts
--8<-- "docs/assets/echarts/scatter.js"
///

///


/// tab | Code

~~~md
/// echarts
--8<-- "docs/assets/echarts/scatter.js"
///
~~~

///

### Radar

/// tab | Output

/// echarts
--8<-- "docs/assets/echarts/radar.js"
///

///


/// tab | Code

~~~md
/// echarts
--8<-- "docs/assets/echarts/radar.js"
///
~~~

///



