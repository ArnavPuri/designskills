---
name: design-system
description: >
  Build systematic component libraries with design tokens, theming,
  and composable patterns. Trigger phrases: "design system", "design tokens",
  "component library", "theming", "css variables", "spacing scale",
  "elevation system", "component API", "token hierarchy"
license: MIT
---

# Design System

Build scalable, maintainable design systems with tokens, components, and theming architecture.

## Prerequisites

Before building a design system, check for existing design context:
- Read any design-context files for existing tokens, component conventions, or tech stack constraints.
- Identify the framework (React, Vue, Svelte, vanilla) to determine component patterns.

---

## Step 1: Design Token Hierarchy

Tokens are the atomic values of a design system. Structure them in three layers:

### Layer 1: Primitive Tokens (Raw Values)

Named by what they ARE. Never used directly in components.

Define all raw values in `:root` using oklch for colors. Include:
- **Colors**: brand scale (50-900), semantic (red, green), neutrals (gray 50-900)
- **Spacing**: 4px base unit scale (0, px, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24) in rem
- **Font sizes**: xs (0.75rem) through 4xl (2.25rem)
- **Radii**: none, sm (0.25rem), md (0.5rem), lg (0.75rem), xl (1rem), 2xl (1.5rem), full (9999px)

### Layer 2: Semantic Tokens (Purpose)

Named by what they DO. These are the primary interface for themes.

Map primitives to purpose in `:root`:
- **Backgrounds**: `--bg-primary` (gray-50), `--bg-secondary` (white), `--bg-tertiary` (gray-100), `--bg-inverse` (gray-900)
- **Text**: primary (gray-900), secondary (gray-600), tertiary (gray-400), inverse, brand
- **Borders**: default (gray-200), strong (gray-300), brand (blue-500)
- **Interactive**: primary/hover/active (blue scale), secondary/hover (gray scale)
- **Semantic**: success (green-500), error (red-500)
- **Spacing**: gap-xs through gap-section mapped to space tokens
- **Radius**: button (md), card (lg), input (md), badge (full), modal (xl)

### Layer 3: Component Tokens (Scoped)

Named by WHERE they are used. Optional but powerful for complex systems.

Scope tokens to individual components. Example for `.btn`: define `--btn-padding-x`, `--btn-padding-y`, `--btn-radius`, `--btn-font-size`, `--btn-bg`, `--btn-color`, `--btn-border` using semantic tokens, then consume them in the same rule. Variants override only the component tokens they need to change.

---

## Step 2: CSS Custom Properties Architecture

### File Organization

```
tokens/
  _primitives.css     /* Layer 1: raw values */
  _semantic.css       /* Layer 2: purpose mappings */
  _themes.css         /* Theme overrides (dark mode, etc.) */
components/
  _button.css
  _card.css
  _input.css
index.css             /* Imports all */
```

### Import Order

```css
/* index.css */
@import './tokens/_primitives.css';
@import './tokens/_semantic.css';
@import './tokens/_themes.css';
@import './components/_button.css';
@import './components/_card.css';
@import './components/_input.css';
```

### Scoping with Data Attributes

```css
/* _themes.css */
[data-theme="dark"] {
  --bg-primary: var(--gray-950);
  --bg-secondary: var(--gray-900);
  --bg-tertiary: var(--gray-800);
  --text-primary: var(--gray-50);
  --text-secondary: var(--gray-300);
  --border-default: var(--gray-700);
  --interactive-primary: var(--blue-400);
}

[data-theme="high-contrast"] {
  --text-primary: black;
  --bg-primary: white;
  --border-default: black;
}
```

---

## Step 3: Component API Design

### Variants

Use CSS classes for variants. Size variants (`--sm`, `--lg`) override padding and font-size tokens. Style variants (`--secondary`, `--ghost`, `--outline`, `--danger`) override bg, color, and border tokens only.

### States

Every interactive component needs: `:hover` (adjusted bg), `:active` (darker bg + `scale(0.98)`), `:focus-visible` (2px outline + 2px offset), `:disabled` / `[aria-disabled]` (opacity 0.5, `pointer-events: none`).

### Consistent API Pattern

| Property  | Options                              |
|-----------|--------------------------------------|
| Size      | sm, md (default), lg                 |
| Variant   | primary (default), secondary, ghost, outline, danger |
| State     | default, hover, active, focus, disabled |
| Shape     | default, pill (radius-full)          |

---

## Step 4: Composable Component Patterns

### Card (Composable)

Parts: `.card` (border, radius, overflow), `.card-header` / `.card-body` / `.card-footer` (padding with semantic tokens, header/footer have border separators). `.card-media` uses `aspect-ratio: 16/9; object-fit: cover`. Variants: `--elevated` (shadow instead of border), `--interactive` (hover shadow + translateY).

### Input (Complete)

Use component tokens (`--input-height`, `--input-border`, `--input-radius`, `--input-bg`). Default 2.5rem height, full width. States: `:hover` (stronger border), `:focus` (brand border + 3px ring at 0.15 opacity), `--error` (error border). Sizes: `--sm` (2rem), `--lg` (3rem).

---

## Step 5: Theming Architecture

### Theme Switching

Set `data-theme` attribute on `<html>`. JS: check `localStorage` first, fall back to `prefers-color-scheme: dark` media query. Listen for OS changes and update if no saved preference.

### Multi-Brand Theming

Use `[data-brand="name"]` selectors to remap Layer 2 tokens (interactive colors, fonts). Same components render differently per brand by only changing semantic token values.

---

## Step 6: Spacing Scale

Use a 4px base unit. Every spacing value is a multiple of 4.

### The Scale

| Token | Value  | rem    | Use case                           |
|-------|--------|--------|------------------------------------|
| 0.5   | 2px    | 0.125  | Hairline gaps                      |
| 1     | 4px    | 0.25   | Tight internal padding             |
| 2     | 8px    | 0.5    | Icon gaps, compact padding         |
| 3     | 12px   | 0.75   | Button padding, input padding      |
| 4     | 16px   | 1      | Card padding, standard gap         |
| 5     | 20px   | 1.25   | Card padding (comfortable)         |
| 6     | 24px   | 1.5    | Section internal gap               |
| 8     | 32px   | 2      | Between component groups           |
| 10    | 40px   | 2.5    | Large component spacing            |
| 12    | 48px   | 3      | Section padding                    |
| 16    | 64px   | 4      | Section margins                    |
| 20    | 80px   | 5      | Hero padding                       |
| 24    | 96px   | 6      | Major section breaks               |

### When to Use Each

- **Within a component** (icon-to-text, label-to-input): space-1 to space-3.
- **Between sibling components** (card-to-card, field-to-field): space-4 to space-6.
- **Between sections**: space-12 to space-24.

---

## Step 7: Shadow / Elevation System

Shadows indicate elevation. Build a layered system.

Define 6 levels: `--shadow-xs` through `--shadow-2xl` using multi-layer `oklch(0 0 0 / opacity)` shadows with increasing blur and offset.

| Level | Shadow    | Used for                            |
|-------|-----------|-------------------------------------|
| 0     | none      | Flush with surface (default)        |
| 1     | xs/sm     | Cards, buttons                      |
| 2     | md        | Dropdowns, popovers                 |
| 3     | lg        | Modals, drawers                     |
| 4     | xl/2xl    | Toast notifications, elevated modals|

In dark mode, increase shadow opacity (0.3+) or rely on surface color differences instead.

---

## Step 8: Border Radius System

Scale: none (0), sm (4px), md (8px), lg (12px), xl (16px), 2xl (24px), full (9999px).

**Nested radius rule**: `inner-radius = outer-radius - padding`. If the result is 0 or negative, use the next size down in the scale.

---

## Step 9: Transition and Animation Tokens

Define duration tokens (fast: 100ms, normal: 200ms, slow: 300ms, slower: 500ms) and easing tokens (default, in, out, spring with overshoot). Create composite transition tokens (`--transition-colors`, `--transition-transform`, `--transition-shadow`, `--transition-opacity`) that combine duration + easing. Components compose these: e.g., buttons use `var(--transition-colors), var(--transition-transform)`.

Always include reduced motion support:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Step 10: Component Documentation Patterns

### Documenting a Component

Each component in the design system should have:

1. **Description**: What it is and when to use it.
2. **Variants**: Visual variations (primary, secondary, ghost, etc.).
3. **Sizes**: Available sizes (sm, md, lg).
4. **States**: Interactive states (hover, active, focus, disabled).
5. **Anatomy**: Parts of the component and their tokens.
6. **Do / Don't**: Usage guidelines.
7. **Code example**: Copy-paste HTML/CSS.

Use a Storybook-style HTML page: each component gets a `<section>` with description, then `.doc-row` containers (flex wrap, gap, tertiary bg) showing all variants, sizes, and states side by side.

---

## Quick Reference: Design System Checklist

1. Define primitive tokens (colors, spacing, font sizes, radii).
2. Map semantic tokens (backgrounds, text, borders, interactive).
3. Set up theming with data attributes (light/dark minimum).
4. Build component tokens scoped to each component.
5. Design component API: consistent sizes (sm/md/lg) and variants.
6. Implement all interactive states (hover, active, focus-visible, disabled).
7. Use 4px spacing base unit.
8. Build a 5-6 level shadow system.
9. Define transition tokens for consistent animation.
10. Document every component with variants, sizes, states, and examples.
