---
title: Get started
extra_css:
  - "css/pygments/all.css" # add scoped styles

---

## Install

Add the package to your project.

=== "pip"

        :::bash
        pip install mkdocs-shadcn


=== "uv"

        :::bash
        uv add mkdocs-shadcn

=== "poetry"

        :::bash
        poetry add mkdocs-shadcn

If you want to use `pymdown` extensions, you can also install the `pymdown-extensions` package:

=== "pip"

        :::bash
        pip install pymdown-extensions


=== "uv"

        :::bash
        uv add pymdown-extensions

=== "poetry"

        :::bash
        poetry add pymdown-extensions


## Configure

The theme configuration is roughly the contract with the users. When it changes, we increment the major version of the package (or minor in the `0.X.Y` case). Currently the theme does not provide so many options.

```yaml
# mkdocs.yml
site_name: "awesome-project"
theme:
  name: shadcn
  show_title: true # show the title in the top bar
  show_stargazers: true # show the stargazers in the top bar
  pygments_style: # default styles 
        light: shadcn-light
        dark: github-dark
  icon: heroicons:rocket-launch # use the shadcn svg if not defined
  topbar_sections: false # NEW!
```

### `show_title: bool` 

If `false`, only the icon will be visible in the top bar (left-side). Default to `true`.


### `show_stargazers: bool`

If `false`, hides the GitHub stargazers besides the repo icon in the top bar (right side). Default to `true`.

### `pygments_style: str | dict`

Define the pygments style for the code blocks. Supported styles are given below. 
If a single theme is provided, it is applies for both light and dark themes. If a dictionary is provided, it should contain `light` and `dark` keys with the respective styles.

<script>
function updatePygmentsStyle(event) {
    const style = event.target.value;
    for (const el of document.querySelectorAll(".pygments-demo")) {
        el.classList.remove(prevValue);
        el.classList.add(style);
    }
    prevValue = style;
}
</script>
<select id="pygments-select" onchange="updatePygmentsStyle(event)">
<option value="a11y-dark">a11y-dark</option>
<option value="a11y-high-contrast-dark">a11y-high-contrast-dark</option>
<option value="a11y-high-contrast-light">a11y-high-contrast-light</option>
<option value="a11y-light">a11y-light</option>
<option value="abap">abap</option>
<option value="algol">algol</option>
<option value="algol_nu">algol_nu</option>
<option value="arduino">arduino</option>
<option value="autumn">autumn</option>
<option value="blinds-dark">blinds-dark</option>
<option value="blinds-light">blinds-light</option>
<option value="borland">borland</option>
<option value="bw">bw</option>
<option value="coffee">coffee</option>
<option value="colorful">colorful</option>
<option value="default">default</option>
<option value="dracula">dracula</option>
<option value="emacs">emacs</option>
<option value="friendly">friendly</option>
<option value="friendly_grayscale">friendly_grayscale</option>
<option value="fruity">fruity</option>
<option value="github-dark-colorblind">github-dark-colorblind</option>
<option value="github-dark">github-dark</option>
<option value="github-dark-high-contrast">github-dark-high-contrast</option>
<option value="github-light-colorblind">github-light-colorblind</option>
<option value="github-light">github-light</option>
<option value="github-light-high-contrast">github-light-high-contrast</option>
<option value="gotthard-dark">gotthard-dark</option>
<option value="gotthard-light">gotthard-light</option>
<option value="greative">greative</option>
<option value="gruvbox-dark">gruvbox-dark</option>
<option value="gruvbox-light">gruvbox-light</option>
<option value="igor">igor</option>
<option value="inkpot">inkpot</option>
<option value="lightbulb">lightbulb</option>
<option value="lilypond">lilypond</option>
<option value="lovelace">lovelace</option>
<option value="manni">manni</option>
<option value="material">material</option>
<option value="monokai">monokai</option>
<option value="murphy">murphy</option>
<option value="native">native</option>
<option value="nord">nord</option>
<option value="nord-darker">nord-darker</option>
<option value="one-dark">one-dark</option>
<option value="paraiso-dark">paraiso-dark</option>
<option value="paraiso-light">paraiso-light</option>
<option value="pastie">pastie</option>
<option value="perldoc">perldoc</option>
<option value="pitaya-smoothie">pitaya-smoothie</option>
<option value="rainbow_dash">rainbow_dash</option>
<option value="rrt">rrt</option>
<option value="sas">sas</option>
<option value="shadcn-light" selected>shadcn-light</option>
<option value="solarized-dark">solarized-dark</option>
<option value="solarized-light">solarized-light</option>
<option value="staroffice">staroffice</option>
<option value="stata-dark">stata-dark</option>
<option value="stata-light">stata-light</option>
<option value="tango">tango</option>
<option value="trac">trac</option>
<option value="vim">vim</option>
<option value="vs">vs</option>
<option value="xcode">xcode</option>
<option value="zenburn">zenburn</option>
</select>
<script>
let prevValue = document.getElementById("pygments-select").value;
</script>


``` { .python .pygments-demo .shadcn-light  }

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```

### `icon: str`

Sets the top-left icon. If not defined, the default shadcn icon is used. You can either pass an image URL or an [iconify class](https://icon-sets.iconify.design/).


### `topbar_sections: bool`

If `true`, the top level sections (i.e. top level directories of the docs) will be displayed in the top bar (and not in the sidebar). It allows to have a deeper navigation tree within the website (basically 2 levels of nesting), but it can be used in any cases. Default to `false`.