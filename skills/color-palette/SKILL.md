---
name: color-palette
description: >
  Generate beautiful, accessible color palettes and color systems.
  Trigger phrases: "color palette", "brand colors", "color scheme",
  "generate colors", "dark mode colors", "color tokens", "color system",
  "accessible colors", "contrast ratio", "semantic colors"
license: MIT
---

# Color Palette Generation

Generate harmonious, accessible, and production-ready color systems from any starting point.

## Prerequisites

Before generating colors, check for existing design context:
- Read any design-context files in the project for existing brand colors, themes, or constraints.
- If a design system already exists, extend it rather than replacing it.

---

## Step 1: Understand Color Theory Fundamentals

Use the **HSL** or **OKLCH** color model for palette generation. OKLCH is preferred for perceptual uniformity.

### Color Wheel Relationships

| Harmony        | Angle(s) from base | Feel                        |
|----------------|--------------------|-----------------------------|
| Complementary  | 180°               | High contrast, energetic    |
| Analogous      | ±30°               | Harmonious, natural         |
| Triadic        | 120°, 240°         | Vibrant, balanced           |
| Split-comp.    | 150°, 210°         | Contrast with less tension  |
| Tetradic       | 90°, 180°, 270°    | Rich, needs careful balance |

### Generating Harmonies in OKLCH

```css
:root {
  /* Base brand color in oklch */
  --brand-h: 250;           /* hue angle */
  --brand-s: 0.15;          /* chroma */
  --brand-l: 0.55;          /* lightness */

  --color-primary:       oklch(var(--brand-l) var(--brand-s) var(--brand-h));
  --color-complement:    oklch(var(--brand-l) var(--brand-s) calc(var(--brand-h) + 180));
  --color-analogous-1:   oklch(var(--brand-l) var(--brand-s) calc(var(--brand-h) + 30));
  --color-analogous-2:   oklch(var(--brand-l) var(--brand-s) calc(var(--brand-h) - 30));
  --color-triadic-1:     oklch(var(--brand-l) var(--brand-s) calc(var(--brand-h) + 120));
  --color-triadic-2:     oklch(var(--brand-l) var(--brand-s) calc(var(--brand-h) + 240));
  --color-split-comp-1:  oklch(var(--brand-l) var(--brand-s) calc(var(--brand-h) + 150));
  --color-split-comp-2:  oklch(var(--brand-l) var(--brand-s) calc(var(--brand-h) + 210));
}
```

---

## Step 2: Generate a Full Shade Scale (50-950)

From a single brand color, generate a 19-step lightness scale. In OKLCH, vary lightness while keeping hue stable and slightly reducing chroma at extremes.

### Lightness Map

| Token | OKLCH Lightness | Usage                    |
|-------|-----------------|--------------------------|
| 50    | 0.97            | Tinted background        |
| 100   | 0.93            | Hover background         |
| 200   | 0.87            | Active background        |
| 300   | 0.78            | Borders                  |
| 400   | 0.68            | Placeholder text         |
| 500   | 0.55            | Base / primary actions   |
| 600   | 0.48            | Hover on primary         |
| 700   | 0.40            | Active on primary        |
| 800   | 0.32            | Headings on light bg     |
| 900   | 0.24            | Body text on light bg    |
| 950   | 0.16            | High-contrast text       |

### CSS Implementation

```css
:root {
  --brand-hue: 250;
  --brand-chroma: 0.15;

  --brand-50:  oklch(0.97 calc(var(--brand-chroma) * 0.3) var(--brand-hue));
  --brand-100: oklch(0.93 calc(var(--brand-chroma) * 0.4) var(--brand-hue));
  --brand-200: oklch(0.87 calc(var(--brand-chroma) * 0.5) var(--brand-hue));
  --brand-300: oklch(0.78 calc(var(--brand-chroma) * 0.7) var(--brand-hue));
  --brand-400: oklch(0.68 calc(var(--brand-chroma) * 0.85) var(--brand-hue));
  --brand-500: oklch(0.55 var(--brand-chroma) var(--brand-hue));
  --brand-600: oklch(0.48 var(--brand-chroma) var(--brand-hue));
  --brand-700: oklch(0.40 var(--brand-chroma) var(--brand-hue));
  --brand-800: oklch(0.32 calc(var(--brand-chroma) * 0.9) var(--brand-hue));
  --brand-900: oklch(0.24 calc(var(--brand-chroma) * 0.8) var(--brand-hue));
  --brand-950: oklch(0.16 calc(var(--brand-chroma) * 0.7) var(--brand-hue));
}
```

---

## Step 3: Define Semantic Colors

Map purpose-driven tokens to your palette or define independent hues.

### Recommended Semantic Hues

| Role    | Hue (OKLCH) | Rationale              |
|---------|-------------|------------------------|
| Success | 145         | Green, universal "go"  |
| Warning | 85          | Amber/yellow, caution  |
| Error   | 25          | Red, urgency           |
| Info    | 230         | Blue, neutral info     |

```css
:root {
  /* Semantic: success */
  --success-50:  oklch(0.97 0.04 145);
  --success-500: oklch(0.55 0.16 145);
  --success-700: oklch(0.40 0.14 145);

  /* Semantic: warning */
  --warning-50:  oklch(0.97 0.04 85);
  --warning-500: oklch(0.60 0.16 85);
  --warning-700: oklch(0.45 0.14 85);

  /* Semantic: error */
  --error-50:  oklch(0.97 0.04 25);
  --error-500: oklch(0.55 0.18 25);
  --error-700: oklch(0.40 0.16 25);

  /* Semantic: info */
  --info-50:  oklch(0.97 0.04 230);
  --info-500: oklch(0.55 0.14 230);
  --info-700: oklch(0.40 0.12 230);
}
```

---

## Step 4: Generate a Neutral Scale

Neutrals are the backbone. Add a slight hue tint from the brand for warmth.

```css
:root {
  --neutral-hue: var(--brand-hue);
  --neutral-chroma: 0.01; /* barely tinted */

  --gray-50:  oklch(0.98 var(--neutral-chroma) var(--neutral-hue));
  --gray-100: oklch(0.96 var(--neutral-chroma) var(--neutral-hue));
  --gray-200: oklch(0.90 var(--neutral-chroma) var(--neutral-hue));
  --gray-300: oklch(0.83 var(--neutral-chroma) var(--neutral-hue));
  --gray-400: oklch(0.71 var(--neutral-chroma) var(--neutral-hue));
  --gray-500: oklch(0.55 var(--neutral-chroma) var(--neutral-hue));
  --gray-600: oklch(0.45 var(--neutral-chroma) var(--neutral-hue));
  --gray-700: oklch(0.37 var(--neutral-chroma) var(--neutral-hue));
  --gray-800: oklch(0.27 var(--neutral-chroma) var(--neutral-hue));
  --gray-900: oklch(0.20 var(--neutral-chroma) var(--neutral-hue));
  --gray-950: oklch(0.13 var(--neutral-chroma) var(--neutral-hue));
}
```

---

## Step 5: Ensure WCAG Accessibility

### Contrast Requirements

| Level    | Normal text | Large text (18px+ bold, 24px+) |
|----------|-------------|-------------------------------|
| WCAG AA  | 4.5:1       | 3:1                           |
| WCAG AAA | 7:1         | 4.5:1                         |

### Practical Rules

- **Body text on light bg**: use 900 or 950 shade (always passes AA).
- **Body text on dark bg**: use 50 or 100 shade.
- **Primary buttons**: white text on 500+ shade; verify 4.5:1 contrast.
- **Disabled states**: use 400 shade on light bg. Disabled elements are exempt from WCAG but should still be distinguishable.
- **Links**: must be distinguishable from surrounding text by more than color alone (underline or 3:1 contrast with surrounding text).

### Quick Contrast Check via OKLCH Lightness

A lightness difference of 0.40+ in OKLCH **usually** meets AA for normal text. Always verify with a tool, but this is a fast heuristic.

```
text lightness: 0.20  |  bg lightness: 0.97  |  diff: 0.77 -> passes AAA
text lightness: 0.55  |  bg lightness: 0.97  |  diff: 0.42 -> likely passes AA for large text
```

---

## Step 6: Dark Mode Adaptation

Do NOT simply invert the scale. Instead, remap semantic usage.

### Dark Mode Strategy

```css
[data-theme="dark"] {
  /* Backgrounds: use 900/950 instead of 50/white */
  --bg-primary:   var(--gray-950);
  --bg-secondary: var(--gray-900);
  --bg-tertiary:  var(--gray-800);

  /* Text: use 50/100 instead of 900/950 */
  --text-primary:   var(--gray-50);
  --text-secondary: var(--gray-300);
  --text-tertiary:  var(--gray-400);

  /* Surfaces: slightly lighter than bg */
  --surface:       var(--gray-900);
  --surface-hover: var(--gray-800);

  /* Borders: use 700 instead of 200 */
  --border: var(--gray-700);

  /* Brand colors: increase lightness for dark bg */
  --brand-primary: var(--brand-400); /* lighter than 500 */

  /* Semantic: bump to lighter shades */
  --color-success: var(--success-400);
  --color-error:   var(--error-400);
}
```

### Key Principles

1. Reduce contrast slightly -- pure white on pure black is harsh. Use gray-50 on gray-950.
2. Reduce chroma slightly in dark mode -- saturated colors glow on dark backgrounds.
3. Elevations in dark mode use lighter surfaces (opposite of light mode shadows).

---

## Step 7: Color Psychology by Industry

| Industry      | Primary colors          | Why                               |
|---------------|------------------------|------------------------------------|
| Finance       | Navy, dark blue, green | Trust, stability, growth           |
| Health        | Blue, teal, white      | Calm, cleanliness, trust           |
| Food          | Red, orange, yellow    | Appetite, energy, warmth           |
| Tech/SaaS     | Blue, violet, cyan     | Innovation, reliability            |
| Luxury        | Black, gold, deep purple| Elegance, exclusivity             |
| Eco/Green     | Green, earth tones     | Nature, sustainability             |
| Education     | Blue, orange, green    | Trust, enthusiasm, growth          |
| Creative      | Bold primaries, neons  | Energy, expression, fun            |

---

## Step 8: Gradient Combinations

### Rules for Effective Gradients

1. Stay within 60 degrees of hue rotation for subtle gradients.
2. Use 90-180 degrees for vibrant, energetic gradients.
3. Avoid crossing 0/360 boundary in HSL (causes muddy midpoints). OKLCH handles this correctly.
4. Add a slight chroma boost at midpoint to avoid the "gray dead zone."

```css
/* Subtle brand gradient */
.gradient-subtle {
  background: linear-gradient(
    135deg,
    oklch(0.55 0.15 250),
    oklch(0.55 0.15 280)
  );
}

/* Vibrant hero gradient */
.gradient-vibrant {
  background: linear-gradient(
    135deg,
    oklch(0.65 0.20 280),
    oklch(0.60 0.22 330),
    oklch(0.65 0.20 20)
  );
}

/* Mesh gradient (modern trend) */
.gradient-mesh {
  background:
    radial-gradient(at 0% 0%, oklch(0.70 0.15 280) 0%, transparent 50%),
    radial-gradient(at 100% 0%, oklch(0.70 0.15 200) 0%, transparent 50%),
    radial-gradient(at 100% 100%, oklch(0.70 0.15 330) 0%, transparent 50%),
    oklch(0.97 0.01 250);
}
```

---

## Step 9: Tailwind Config Generation

```js
// tailwind.config.js
const brand = {
  50:  'oklch(0.97 0.045 250)',
  100: 'oklch(0.93 0.06 250)',
  200: 'oklch(0.87 0.075 250)',
  300: 'oklch(0.78 0.105 250)',
  400: 'oklch(0.68 0.1275 250)',
  500: 'oklch(0.55 0.15 250)',
  600: 'oklch(0.48 0.15 250)',
  700: 'oklch(0.40 0.15 250)',
  800: 'oklch(0.32 0.135 250)',
  900: 'oklch(0.24 0.12 250)',
  950: 'oklch(0.16 0.105 250)',
};

module.exports = {
  theme: {
    extend: {
      colors: {
        brand,
        success: { /* ... same pattern, hue 145 */ },
        warning: { /* ... same pattern, hue 85 */ },
        error:   { /* ... same pattern, hue 25 */ },
        info:    { /* ... same pattern, hue 230 */ },
      },
    },
  },
};
```

---

## Step 10: CSS Custom Properties Architecture

Structure tokens in three layers:

```css
/* Layer 1: Primitive (raw values) */
:root {
  --blue-500: oklch(0.55 0.15 250);
  --red-500:  oklch(0.55 0.18 25);
}

/* Layer 2: Semantic (purpose) */
:root {
  --color-primary:    var(--blue-500);
  --color-danger:     var(--red-500);
  --color-bg:         var(--gray-50);
  --color-text:       var(--gray-900);
}

/* Layer 3: Component (scoped) */
.btn-primary {
  background: var(--color-primary);
  color: white;
}
```

This three-layer approach makes theming and dark mode trivial -- you only remap Layer 2.

---

## Quick Reference: Palette from a Single Hex

1. Convert hex to OKLCH.
2. Extract hue. This is your brand hue.
3. Generate 50-950 scale using the lightness map in Step 2.
4. Generate neutrals tinted with brand hue (Step 4).
5. Pick semantic hues (Step 3).
6. Verify contrast (Step 5).
7. Build dark mode remap (Step 6).
8. Export as CSS custom properties or Tailwind config.
