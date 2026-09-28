---
name: icon-design
description: >
  Design and implement consistent SVG icon systems for UI: keyline grids, stroke
  rules, optical corrections, outline/filled/duotone styles, icon+text alignment,
  animation, and accessible markup. Use for UI icons in code; for a logo mark use
  brand-identity, for illustrations use image-generation. Trigger phrases: "icon design", "svg icon", "icon system",
  "custom icons", "icon animation", "icon grid", "icon accessibility",
  "duotone icon", "icon set", "animated icon"
license: MIT
---

# Icon Design

Create consistent, accessible, and beautiful icon systems using SVG and CSS.

## Prerequisites

- Read `.agents/design-context.md` (see `design-context`): the Brand Marks "Icon Style" field (e.g. "Outlined, 2px stroke, rounded caps") sets fill, stroke width, and cap/join style for every icon you draw. Use the semantic colors (`--success-*`, `--error-*`, etc.) from the shared color tokens.
- If the project already uses an icon library (Lucide, Heroicons, Phosphor, Material Symbols), match its grid and stroke instead of mixing in a different style; prefer using the library icon over drawing a new one.

---

## Step 1: SVG Icon Fundamentals

### Base Template

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
  width="24" height="24" fill="none" stroke="currentColor"
  stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- icon paths here -->
</svg>
```

### Key Attributes

| Attribute        | Value         | Why                                     |
|------------------|---------------|-----------------------------------------|
| fill             | none          | Outline icons by default                |
| stroke           | currentColor  | Inherits text color from CSS            |
| stroke-width     | 2             | Consistent across all icons             |
| stroke-linecap   | round         | Friendly, modern feel                   |
| stroke-linejoin  | round         | Matches linecap for consistency         |
| viewBox          | 0 0 24 24     | Standard 24px grid                      |

---

## Step 2: Icon Grid System

### Grid Sizes

| Grid  | Usage                     | Stroke width |
|-------|---------------------------|-------------|
| 24x24 | Default UI icons          | 2px (1.5px for a lighter set) |
| 20x20 | Compact UI, form fields   | 1.5px        |
| 16x16 | Inline text, badges       | 1.5px (or filled) |
| 32x32 | Feature icons, navigation | 2-2.5px      |
| 48x48 | Illustration icons, hero  | 3px          |

Draw each size on its own grid with whole-pixel coordinates when possible. Scaling a 24px icon down to 16px via CSS also scales the stroke (2px becomes 1.33px, blurry); either draw a 16px variant or use `vector-effect="non-scaling-stroke"` on the paths.

### Keyline Shapes (24x24, Material-style)

- **Live area**: 20x20 (2px padding on each side); the padding is for optical overshoot only
- **Circle**: 20x20 diameter
- **Square**: 18x18 (circles look smaller than squares of equal size, so squares are drawn smaller)
- **Portrait rectangle**: 16w x 20h; **Landscape rectangle**: 20w x 16h

### CSS Sizing

```css
.icon { width: 1.5rem; height: 1.5rem; flex-shrink: 0; display: inline-block; vertical-align: middle; }
.icon-sm { width: 1rem; height: 1rem; }
.icon-md { width: 1.25rem; height: 1.25rem; }
.icon-lg { width: 2rem; height: 2rem; }
.icon-xl { width: 3rem; height: 3rem; }
```

---

## Step 3: Optical Alignment Corrections

| Shape       | Correction                                    |
|-------------|-----------------------------------------------|
| Triangle/Play| Shift right ~1px (optical center of mass)    |
| Circle      | Draw ~10% larger than a square (20 vs 18 keyline)|
| Tall shapes | Center vertically, may need slight Y offset   |
| Pointed tops| Let point extend slightly above grid boundary  |

Keep stroke width identical across the whole set -- compensate optically with size and position, not by varying stroke. Uneven stroke weights are the most visible sign of an inconsistent set.

---

## Step 4: Icon Styles

### Outline (Stroke-based)
Most versatile. Works at all sizes, scales well, low visual weight. Use `fill="none" stroke="currentColor"`.

### Filled (Solid)
Higher visual weight. Good for active/selected states or small sizes. Use `fill="currentColor"`.

### Duotone (Two-tone)
Primary stroke + secondary filled area at lower opacity. Adds depth without complexity.

```css
.icon-duotone { --icon-primary: currentColor; --icon-secondary: currentColor; }
.icon-duotone .icon-bg { fill: var(--icon-secondary); opacity: 0.15; }
.icon-duotone .icon-fg { stroke: var(--icon-primary); fill: none; }
```

### Rounded vs Sharp
Rounded (stroke-linecap: round) feels friendly and modern. Sharp (stroke-linecap: square/butt) feels precise and technical. Pick one and apply it to the entire icon set. Never mix.

---

## Step 5: Semantic Icon Selection

| Action      | Icon             | Notes                              |
|-------------|------------------|------------------------------------|
| Close       | X                | Always top-right of container      |
| Back        | Arrow left       | Or chevron-left                    |
| Menu        | 3 horizontal bars| Hamburger menu                     |
| Search      | Magnifying glass | Usually in search inputs           |
| Settings    | Gear/cog         | Or sliders for filter settings     |
| User        | Person silhouette| Circle + head shape                |
| Notification| Bell             | With optional dot badge            |
| Delete      | Trash can        | Use with confirmation              |
| Edit        | Pencil           | Or pencil-square                   |
| Add         | Plus             | In circle for FAB                  |
| Share       | Arrow up from box| Or branching arrow                 |
| Download    | Arrow down to bar| Distinct from chevron-down         |
| Check/Done  | Checkmark        | In circle for confirmed state      |
| Info        | i in circle      | Blue semantic color                |
| Warning     | Triangle with !  | Yellow/amber semantic color        |
| Error       | Circle with X    | Red semantic color                 |

---

## Step 6: Custom SVG Icon Techniques

### Path Data Commands
- **M**: Move to, **L**: Line to, **H/V**: Horizontal/Vertical line
- **C**: Cubic bezier, **A**: Arc, **Z**: Close path
- Use lowercase for relative coordinates (often shorter)

### Building from Primitives

```svg
<!-- Home icon from primitives -->
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
     stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
  <polyline points="3 11 12 3 21 11"/>
  <path d="M5 10v9a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1v-9"/>
</svg>
```

---

## Step 7: Icon + Text Alignment

```css
/* Inline alignment */
.icon-text { display: inline-flex; align-items: center; gap: 0.5rem; }
.icon-text .icon { width: 1.25em; height: 1.25em; flex-shrink: 0; }

/* Button with icon */
.btn-icon { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1.25rem; }
.btn-icon .icon { width: 1.25em; height: 1.25em; margin-left: -0.125em; }

/* Icon-only button */
.btn-icon-only { display: inline-grid; place-items: center; width: 2.75rem; height: 2.75rem; padding: 0; border-radius: 0.5rem; } /* 44px target */
```

---

## Step 8: Animated Icons

### Hover Rotation
```css
.icon-interactive { transition: transform 0.2s ease; }
.icon-interactive:hover { transform: rotate(90deg); }
```

### Loading Spinner
```css
.icon-spinner { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
```

### Checkmark Draw-On
`pathLength="1"` normalizes the path length, so you don't need to measure it:

```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
  <path class="draw" pathLength="1" d="M5 12.5l4.5 4.5L19 7.5"/>
</svg>
```
```css
.draw { stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 0.4s var(--ease-out, ease-out) forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
@media (prefers-reduced-motion: reduce) { .draw { animation: none; stroke-dashoffset: 0; } }
```

Wrap hover rotations the same way. A spinner may keep rotating under reduced motion (it conveys state, not decoration), but slow it down or swap to a pulsing opacity.

---

## Step 9: Icon Accessibility

### Rules
1. **Decorative icons** (next to text labels): `aria-hidden="true" focusable="false"`
2. **Meaningful icons** (standalone): provide `aria-label` on the button (and `aria-hidden="true"` on the SVG inside it), or use `<title>` inside SVG with `role="img" aria-labelledby`
3. Never rely on icon alone for critical actions -- always provide a text alternative
4. Icon buttons: 24x24px minimum target is the WCAG 2.2 AA floor (SC 2.5.8); aim for 44x44px (Apple HIG, WCAG AAA 2.5.5) or 48x48dp (Material)
5. Icons that convey meaning need 3:1 contrast against their background (SC 1.4.11)

```css
.icon-button { min-width: 44px; min-height: 44px; display: inline-grid; place-items: center; }
```

---

## Step 10: Common UI Icon Patterns

### Badge Indicator
```css
.icon-with-badge { position: relative; display: inline-block; }
.icon-badge {
  position: absolute; top: -4px; right: -4px;
  width: 10px; height: 10px; background: var(--error-500);
  border-radius: 50%; border: 2px solid var(--bg-primary, white);
}
```

### Status Indicator
```css
.status-icon { position: relative; }
.status-icon::after {
  content: ''; position: absolute; bottom: 0; right: 0;
  width: 8px; height: 8px; border-radius: 50%; border: 2px solid var(--bg-primary, white);
}
.status-icon--online::after  { background: var(--success-500); }
.status-icon--offline::after { background: var(--gray-400); }
.status-icon--busy::after    { background: var(--error-500); }
```

Status dots rely on color alone -- pair them with a text label or `aria-label` ("Online"), and use `var(--bg-primary)` instead of `white` for the ring so it works in dark mode.

---

## Verify the Set

Render every icon on one scratchpad HTML page at 16, 20, 24, and 32px, on light and dark backgrounds, next to a text label, and screenshot it (`npx playwright screenshot --full-page "file://$PWD/icons.html" icons.png`). View the image with Read (also a 4x-zoomed copy for 16px) and check: equal visual weight across icons, identical stroke widths, nothing clipped at the viewBox edge, shapes aligned to the keylines, recognizable at 16px.

---

## Quick Reference

1. Use a consistent viewBox (24x24 default) with 2px padding live area.
2. Pick one style (outline, filled, duotone) and apply it across the entire set.
3. Use `stroke="currentColor"` so icons inherit text color.
4. Keep stroke-width consistent (2px at 24x24).
5. Apply optical corrections for triangles and circles.
6. Size icons with `em` units when inline with text.
7. Always add `aria-hidden="true"` to decorative icons.
8. Always add `aria-label` to icon-only buttons.
9. Aim for 44x44px touch targets (24x24px is the WCAG 2.2 AA minimum).
10. Use `stroke-dasharray` + `stroke-dashoffset` for draw-on animations.
