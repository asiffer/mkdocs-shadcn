---
title: HTML
summary: Styled standard HTML elements
new: true
---

The theme applies consistent shadcn-inspired styles to some standard HTML elements. No extra configuration is needed — just use the elements as you normally would in Markdown, and the theme will style them automatically.

Wrapping form elements inside a `<fieldset>` unlocks a richer layout: you can add a `<label>`, a hint with `<small>`, and a live value display with `<output>`.

## Buttons

The theme styles `button`, `a.button`, and `input[type="button"]` identically, so you can use whichever element is most semantically appropriate.

```html
<button>Button</button>
<a class="button" href="#">Link</a>
<input type="button" role="submit" value="Form action" />
```
<button>Button</button>
<a class="button" href="#">Link</a>
<input type="button" role="submit" value="Form action" />


The variant is set via the `class` attribute. The default style is applied when no class is specified.

```html
<button>Default</button>
<button class="secondary">Secondary</button>
<button class="outline">Outline</button>
<button class="ghost">Ghost</button>
<button class="link">Link</button>
<button class="destructive">Destructive</button>
```
<button>Default</button>
<button class="secondary">Secondary</button>
<button class="outline">Outline</button>
<button class="ghost">Ghost</button>
<button class="link">Link</button>
<button class="destructive">Destructive</button>

Four sizes are available: `xs`, `sm`, default (no class), and `lg`. Sizes can be combined with any variant.

```html
<button class="outline xs">Extra Small</button>
<button class="outline sm">Small</button>
<button class="outline">Default</button>
<button class="outline lg">Large</button>
```
<button class="outline xs">Extra Small</button>
<button class="outline sm">Small</button>
<button class="outline">Default</button>
<button class="outline lg">Large</button>

The `icon` class forces a square aspect ratio, useful for icon-only buttons (the icon syntax `+pack:icon-name+` is provided by the [Iconify extension](20_extensions/iconify.md)).

```html
<button class="icon xs">+heroicons:bolt-solid+</button>
<button class="outline icon sm">+heroicons:bolt-solid+</button>
<button class="ghost icon">+heroicons:bolt-solid+</button>
<button class="destructive icon lg">+heroicons:bolt-solid+</button>
```
<button class="icon xs">+heroicons:bolt-solid+</button>
<button class="outline icon sm">+heroicons:bolt-solid+</button>
<button class="ghost icon">+heroicons:bolt-solid+</button>
<button class="destructive icon lg">+heroicons:bolt-solid+</button>

## Slider

A standard `<input type="range">` is rendered as a styled slider.

```html
<input type="range" min="0" max="10" step="0.1" />
```

<input type="range" min="0" max="10" step="0.1" />

Wrapping it in a `<fieldset>` adds a label, a hint text, and a live `<output>` element that displays the current value (here the `oninput` handler keeps the output in sync as the user drags the slider).

```html
<fieldset>
    <label for="slider">Slider</label>
    <output for="slider">5</output>
    <input id="slider" type="range" min="0" max="10" value="5" step="0.1" oninput="document.querySelector(`output[for='${event.target.id}']`).textContent = event.target.value;"/>
    <small>Choose it carefully</small>
</fieldset>
```

<fieldset>
    <label for="slider">Slider</label>
    <output for="slider">5</output>
    <input id="slider" type="range" min="0" max="10" value="5" step="0.1" oninput="document.querySelector(`output[for='${event.target.id}']`).textContent = event.target.value;"/>
    <small>Choose it carefully</small>
</fieldset>

## Checkbox

A plain `<input type="checkbox">` is styled automatically.

```html
<input type="checkbox" />
```

<input type="checkbox" />

Use a `<fieldset>` to pair it with a label.

```html
<fieldset>
    <input type="checkbox" />
    <label>Checkbox</label>
</fieldset>
```

<fieldset>
    <input type="checkbox" />
    <label>Checkbox</label>
</fieldset>

It can be embedded into a table for instance.

```md
| Feature  | Status                                    |
| -------- | ----------------------------------------- |
| Slider   | <input type="checkbox" checked disabled/> |
| Checkbox | <input type="checkbox" checked disabled/> |
| Radio    | <input type="checkbox" disabled/>         |
```

| Feature  | Status                                    |
| -------- | ----------------------------------------- |
| Slider   | <input type="checkbox" checked disabled/> |
| Checkbox | <input type="checkbox" checked disabled/> |
| Radio    | <input type="checkbox" disabled/>         |


## Switch

A switch is a checkbox with the `switch` class applied — it renders as a toggle instead of a box.

```html
<input type="checkbox" class="switch" />
```

<input type="checkbox" class="switch" />

Pair it with a `<label>` inside a `<fieldset>` for a labelled toggle.

```html
<fieldset>
    <input type="checkbox" class="switch" />
    <label>Switch</label>
</fieldset>
```

<fieldset>
    <input type="checkbox" class="switch" />
    <label>Switch</label>
</fieldset>




## Select

A `<select>` element is styled to match the rest of the theme.

```html
<select>
    <option>Gauss</option>
    <option>Weierstrass</option>
</select>
```

<select>
    <option>Gauss</option>
    <option>Weierstrass</option>
</select>

Wrap it in a `<fieldset>` to add a label and a hint with `<small>`.

```html
<fieldset>
    <label>Mathematicians</label>
    <select>
        <option>Gauss</option>
        <option>Weierstrass</option>
    </select>
    <small>Choose your favorite</small>
</fieldset>
```

<fieldset>
    <label>Mathematicians</label>
    <select>
        <option>Gauss</option>
        <option>Weierstrass</option>
    </select>
    <small>Choose your favorite</small>
</fieldset>