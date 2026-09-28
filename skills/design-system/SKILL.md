---
name: design-system
description: >
  Build a coded design system: three-layer design tokens (CSS variables and W3C
  DTCG JSON), spacing/radius/shadow/motion scales, light/dark/multi-brand theming,
  and component APIs with states and docs. Use when building or extending a component
  library or token architecture. Trigger phrases: "design system", "design tokens",
  "component library", "theming", "css variables", "spacing scale", "elevation system",
  "component API", "token hierarchy", "tokens.json". Consumes color-palette (colors) and
  typography (type scale); for capturing brand basics only, use design-context.
license: MIT
---

# Design System

Build scalable, maintainable design systems with tokens, components, and theming architecture.

## Prerequisites

Before building a design system, check for existing design context:
- Read `.agents/design-context.md` (see `design-context`) for colors, fonts, Base Size, Scale Ratio, Border Radius, Shadow Style, and Spacing System. Primitive tokens must derive from it, not from invented values.
- Scan the codebase for existing tokens (CSS variables, Tailwind theme, `tokens.json`) and extend them.
- Identify the framework (React, Vue, Svelte, vanilla) to determine component patterns.
- Don't re-derive what siblings own: color scales come from `color-palette` (`--brand-*`, `--gray-*`, `--success-*`, `--warning-*`, `--error-*`, `--info-*`), the type scale from `typography` (`--text-xs` … `--text-5xl`).

---

## Step 1: Design Token Hierarchy

Tokens are the atomic values of a design system. Structure them in three layers:

### Layer 1: Primitive Tokens (Raw Values)

Named by what they ARE. Never used directly in components.

Define all raw values in `:root` using oklch for colors. Include:
- **Colors**: `--brand-50…950`, `--gray-50…950`, semantic `--success-*`, `--warning-*`, `--error-*`, `--info-*` (from color-palette)
- **Spacing**: `--space-N` = N × 4px, in rem (0, px, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24) -- see Step 6
- **Font sizes**: `--text-xs` … `--text-5xl` generated from design-context Base Size × Scale Ratio (typography skill). Don't hard-code a separate scale.
- **Radii**: none, sm (0.25rem), md (0.5rem), lg (0.75rem), xl (1rem), 2xl (1.5rem), full (9999px); set md to the design-context Border Radius

### Layer 2: Semantic Tokens (Purpose)

Named by what they DO. These are the primary interface for themes.

Map primitives to purpose in `:root`:
- **Backgrounds**: `--bg-primary` (gray-50), `--bg-secondary` (white), `--bg-tertiary` (gray-100), `--bg-inverse` (gray-900)
- **Text**: primary (gray-900), secondary (gray-600), tertiary (gray-400), inverse, brand
- **Borders**: default (gray-200), strong (gray-300), brand (brand-500)
- **Interactive**: `--interactive-primary` / `-hover` / `-active` (brand-500/600/700), secondary/hover (gray scale)
- **Brand aliases**: `--color-primary`, `--color-secondary`, `--color-accent` (names design-context auto-detects)
- **Semantic**: `--color-success` (success-500), `--color-warning` (warning-500), `--color-error` (error-500)
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
  --interactive-primary: var(--brand-400);
}

/* Follow the OS setting instead of (or as well as) a manual theme */
@media (prefers-contrast: more) {
  :root { --text-secondary: var(--text-primary); --border-default: var(--gray-900); }
}
```

In Windows High Contrast / `forced-colors: active`, custom colors are replaced by system colors: never convey state with background color alone, and keep a transparent `outline` or `border` on buttons so they stay visible.

### Exporting Tokens (W3C DTCG format)

For tools (Style Dictionary, Tokens Studio, Figma variables) also emit `tokens.json` in the Design Tokens Community Group format: every token is an object with `$value` and `$type` (`$type` can be set once on a group), aliases use `{group.token}`, and metadata goes in `$description`. The stable spec (2025.10) uses structured color and dimension values; older tools may expect `"#0F74C5"` / `"16px"` strings -- check what the consuming tool supports.

```json
{
  "color": {
    "$type": "color",
    "brand": {
      "500": { "$value": { "colorSpace": "oklch", "components": [0.55, 0.15, 250], "hex": "#0F74C5" } }
    },
    "interactive": {
      "primary": { "$value": "{color.brand.500}", "$description": "Primary buttons, links" }
    }
  },
  "space": {
    "$type": "dimension",
    "4": { "$value": { "value": 1, "unit": "rem" } }
  },
  "duration": {
    "$type": "duration",
    "normal": { "$value": { "value": 200, "unit": "ms" } }
  },
  "easing": {
    "$type": "cubicBezier",
    "out": { "$value": [0, 0, 0.2, 1] }
  }
}
```

---

## Step 3: Component API Design

### Variants

Use CSS classes for variants. Size variants (`--sm`, `--lg`) override padding and font-size tokens. Style variants (`--secondary`, `--ghost`, `--outline`, `--danger`) override bg, color, and border tokens only.

### States

Every interactive component needs: `:hover` (adjusted bg), `:active` (darker bg + `scale(0.98)`), `:focus-visible` (2px outline + 2px offset, 3:1 contrast against the background), `:disabled` / `[aria-disabled="true"]` (reduced opacity, `cursor: not-allowed`; for `aria-disabled` also block the click in JS -- it stays focusable, which is the point).

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

Set `data-theme` attribute on `<html>`. JS: check `localStorage` first, fall back to `prefers-color-scheme: dark` media query. Listen for OS changes and update if no saved preference. Run this as a tiny inline `<script>` in `<head>` (before CSS paints) to avoid a flash of the wrong theme, and set `color-scheme: light dark` so form controls and scrollbars match.

### Multi-Brand Theming

Use `[data-brand="name"]` selectors to remap Layer 2 tokens (interactive colors, fonts). Same components render differently per brand by only changing semantic token values.

---

## Step 6: Spacing Scale

Use a 4px base unit: `--space-N` = N × 4px. Every value is a multiple of 4 except the 2px hairline. If design-context says "8px base grid", keep this scale but restrict layout spacing to even steps (2, 4, 6, 8…). layout-composition uses this same scale.

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

```css
:root {
  --shadow-sm: 0 1px 2px oklch(0 0 0 / 0.06), 0 1px 3px oklch(0 0 0 / 0.08);
  --shadow-md: 0 2px 4px oklch(0 0 0 / 0.06), 0 4px 12px oklch(0 0 0 / 0.10);
  --shadow-lg: 0 4px 8px oklch(0 0 0 / 0.06), 0 12px 32px oklch(0 0 0 / 0.14);
}
```

Scale opacities to the design-context **Shadow Style**: none = borders/surface color only, subtle ≈ the values above, medium ≈ 1.5×, dramatic ≈ 2× with larger offsets.

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

Define duration tokens (`--duration-fast`: 100ms, `--duration-normal`: 200ms, `--duration-slow`: 300ms, `--duration-slower`: 500ms) and easing tokens (`--ease-out`, `--ease-in`, `--ease-in-out`, `--ease-spring`) -- the same names and values as the motion-design skill. Create composite transition tokens (`--transition-colors`, `--transition-transform`, `--transition-shadow`, `--transition-opacity`) that combine duration + easing. Components compose these: e.g., buttons use `var(--transition-colors), var(--transition-transform)`.

Always include reduced motion support:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
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

## Step 11: Verify and Save

1. **Render the docs page** (Step 10) and screenshot it in both themes: `npx playwright screenshot --full-page "file://$PWD/docs.html" light.png` and again with `--color-scheme=dark` (or toggle `data-theme`). View both with Read. Check every variant/size/state renders, focus rings are visible, disabled looks disabled, and no component uses a raw hex instead of a token (`grep -nE '#[0-9a-fA-F]{3,8}\b' components/`).
2. **Check contrast** of each text/background and button pair in both themes (use the script in the color-palette skill).
3. **Offer to write back** to `.agents/design-context.md` any primitives that changed (Color System hex, fonts, Base Size, Scale Ratio, Border Radius, Shadow Style, Spacing System), updating only those fields. Show the diff and ask before saving.

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
