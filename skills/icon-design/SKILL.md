---
name: icon-design
description: >
  Design consistent icon systems with SVG: grids, styles, animation,
  and accessibility. Trigger phrases: "icon design", "svg icon", "icon system",
  "custom icons", "icon animation", "icon grid", "icon accessibility",
  "duotone icon", "icon set", "animated icon"
license: MIT
---

# Icon Design

Create consistent, accessible, and beautiful icon systems using SVG and CSS.

## Prerequisites

- Read any design-context files for existing icon libraries, stroke widths, or style preferences.
- If a design system exists, match its icon style (outline, filled, duotone) and sizing grid.

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
| 24x24 | Default UI icons          | 2px          |
| 20x20 | Compact UI, form fields   | 1.5px        |
| 16x16 | Inline text, badges       | 1.5px        |
| 32x32 | Feature icons, navigation | 2px          |
| 48x48 | Illustration icons, hero  | 2px          |

### Grid Zones (24x24)

- **Live area**: 20x20 (2px padding on each side)
- **Trim area**: Full 24x24 for optical adjustments
- Square icons fill the 20x20 live area; circular icons can extend to ~22x22
- Tall/narrow icons stay within 20px height, narrower width

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
| Circle      | Scale up ~2% (circles look smaller than squares)|
| Tall shapes | Center vertically, may need slight Y offset   |
| Pointed tops| Let point extend slightly above grid boundary  |

Circles and curved shapes need slightly thicker strokes to match the visual weight of straight lines. If your system uses stroke-width 2, consider 2.25 for circular elements.

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
     stroke-linecap="round" stroke-linejoin="round">
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
.btn-icon-only { display: inline-grid; place-items: center; width: 2.5rem; height: 2.5rem; padding: 0; border-radius: 0.5rem; }
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
Use `stroke-dasharray` and `stroke-dashoffset` with keyframe animation to create a draw-on effect. Set dasharray to the path length, offset to the same value, then animate offset to 0.

---

## Step 9: Icon Accessibility

### Rules
1. **Decorative icons** (next to text labels): `aria-hidden="true" focusable="false"`
2. **Meaningful icons** (standalone): provide `aria-label` on the button, or use `<title>` inside SVG with `role="img" aria-labelledby`
3. Never rely on icon alone for critical actions -- always provide a text alternative
4. Ensure icon buttons have minimum 44x44px touch target

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
  border-radius: 50%; border: 2px solid white;
}
```

### Status Indicator
```css
.status-icon { position: relative; }
.status-icon::after {
  content: ''; position: absolute; bottom: 0; right: 0;
  width: 8px; height: 8px; border-radius: 50%; border: 2px solid white;
}
.status-icon--online::after  { background: var(--success-500); }
.status-icon--offline::after { background: var(--gray-400); }
.status-icon--busy::after    { background: var(--error-500); }
```

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
9. Ensure 44x44px minimum touch targets.
10. Use `stroke-dasharray` + `stroke-dashoffset` for draw-on animations.
