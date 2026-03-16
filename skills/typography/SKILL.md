---
name: typography
description: >
  Master typography for web: type scales, font pairing, responsive text,
  and text effects. Trigger phrases: "typography", "font pairing", "type scale",
  "heading sizes", "responsive text", "font combination", "text style",
  "variable fonts", "fluid typography", "google fonts"
license: MIT
---

# Typography Mastery

Create beautiful, readable, and systematic typography for any web project.

## Prerequisites

Before setting typography, check for existing design context:
- Read any design-context files for existing font choices, brand guidelines, or type preferences.
- If a design system exists, align with its type scale and font stack.

---

## Step 1: Choose a Type Scale Ratio

The type scale ratio determines the mathematical relationship between sizes. Pick based on the content density and visual character of the project.

| Ratio | Name            | Value | Best for                           |
|-------|-----------------|-------|------------------------------------|
| Minor second    | Tight   | 1.067 | Dense data UIs, dashboards         |
| Major second    | Compact | 1.125 | Apps, tools, compact layouts       |
| Minor third     | Default | 1.200 | General web, blogs, marketing      |
| Major third     | Relaxed | 1.250 | Editorial, magazines               |
| Perfect fourth  | Bold    | 1.333 | Marketing sites, landing pages     |
| Augmented fourth| Impact  | 1.414 | Bold headlines, creative sites     |
| Perfect fifth   | Drama   | 1.500 | High-impact hero sections          |
| Golden ratio    | Grand   | 1.618 | Art, luxury, editorial             |

### Generate a Scale

```css
:root {
  --type-ratio: 1.25;   /* major third */
  --type-base: 1rem;    /* 16px */

  --text-xs:   calc(var(--type-base) / var(--type-ratio) / var(--type-ratio)); /* ~0.64rem */
  --text-sm:   calc(var(--type-base) / var(--type-ratio));  /* ~0.80rem */
  --text-base: var(--type-base);                             /* 1rem */
  --text-lg:   calc(var(--type-base) * var(--type-ratio));   /* 1.25rem */
  --text-xl:   calc(var(--type-base) * var(--type-ratio) * var(--type-ratio));  /* 1.563rem */
  --text-2xl:  calc(var(--type-base) * var(--type-ratio) * var(--type-ratio) * var(--type-ratio));  /* 1.953rem */
  --text-3xl:  calc(1rem * 2.441);  /* precomputed for clarity */
  --text-4xl:  calc(1rem * 3.052);
  --text-5xl:  calc(1rem * 3.815);
}
```

---

## Step 2: Font Pairing Rules

### Core Pairing Strategies

1. **Serif headings + Sans body**: Classic editorial feel. High contrast in structure.
2. **Geometric sans headings + Humanist sans body**: Modern but warm.
3. **Slab serif headings + Sans body**: Bold, confident.
4. **Mono headings + Sans body**: Technical, developer-oriented.
5. **Same family, different weights**: Safest option. Use 700+ for headings, 400 for body.

### What to Avoid

- Two fonts from the same category with similar proportions (e.g., two geometric sans).
- More than 2 typefaces on a single page (3 max if one is monospace for code).
- Decorative/display fonts for body text.

---

## Step 3: Curated Google Fonts Pairings

These are tested, production-ready combinations.

### Editorial / Content-heavy

1. **Playfair Display + Source Sans 3**
   Elegant serif headings, clean sans body. Great for magazines, blogs.

2. **Lora + Inter**
   Warm transitional serif + neutral modern sans. Excellent readability.

3. **Fraunces + Commissioner**
   Variable serif with personality + geometric sans. Distinctive editorial.

### Modern / SaaS

4. **Inter + Inter**
   Single-family system. Use 700 for headings, 400 for body. Extremely versatile.

5. **DM Sans + DM Sans**
   Geometric, modern. Slightly more personality than Inter.

6. **Manrope + Source Sans 3**
   Geometric with rounded terminals + humanist sans. Friendly tech feel.

### Bold / Marketing

7. **Space Grotesk + General Sans** (self-hosted) or **Space Grotesk + DM Sans**
   Monospace-influenced sans + clean geometric. Techy and bold.

8. **Bricolage Grotesque + Inter**
   Quirky variable sans for headings + reliable body text. Playful but professional.

9. **Cabinet Grotesk** (self-hosted) **+ Satoshi** (self-hosted)
   Modern geometric pair. Premium startup aesthetic.

### Specialized

10. **JetBrains Mono + Inter**
    Monospace headings/code + sans body. Developer tools, documentation.

11. **Instrument Serif + Instrument Sans**
    Matched serif/sans superfamily. Seamless pairing guaranteed.

12. **Sora + Newsreader**
    Geometric sans headings + readable serif body. Inverted classic pattern.

### CSS Import Pattern

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
```

```css
:root {
  --font-heading: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

---

## Step 4: Heading Hierarchy

### Recommended Defaults (1.25 ratio, base 16px)

```css
h1 {
  font-family: var(--font-heading);
  font-size: var(--text-5xl);   /* ~3.8rem / 61px */
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.025em;
  margin-bottom: 0.5em;
}

h2 {
  font-family: var(--font-heading);
  font-size: var(--text-4xl);   /* ~3.05rem / 49px */
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.02em;
  margin-bottom: 0.5em;
}

h3 {
  font-family: var(--font-heading);
  font-size: var(--text-3xl);   /* ~2.44rem / 39px */
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.015em;
  margin-bottom: 0.5em;
}

h4 {
  font-size: var(--text-2xl);   /* ~1.95rem / 31px */
  font-weight: 600;
  line-height: 1.25;
  letter-spacing: -0.01em;
}

h5 {
  font-size: var(--text-xl);    /* ~1.56rem / 25px */
  font-weight: 600;
  line-height: 1.3;
}

h6 {
  font-size: var(--text-lg);    /* ~1.25rem / 20px */
  font-weight: 600;
  line-height: 1.4;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### Key Rules

- Negative letter-spacing for large headings (-0.01em to -0.03em).
- Tighter line-height for headings (1.1-1.3) than body text.
- Skip heading levels sparingly -- h1 to h3 is fine for most pages.

---

## Step 5: Body Text Optimization

### The Golden Rules

- **Font size**: 16px minimum, 18px preferred for long-form content.
- **Line height**: 1.5 for UI, 1.6-1.75 for long-form reading.
- **Line length**: 45-75 characters per line (65ch is ideal).
- **Paragraph spacing**: 1em-1.5em between paragraphs.

```css
body {
  font-family: var(--font-body);
  font-size: 1.125rem;        /* 18px */
  line-height: 1.65;
  color: var(--gray-900);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

.prose {
  max-width: 65ch;
  margin-inline: auto;
}

.prose p + p {
  margin-top: 1.25em;
}

.prose > * + * {
  margin-top: 1em;
}
```

---

## Step 6: Responsive Typography with clamp()

Use `clamp()` for fluid scaling between breakpoints without media queries.

### Formula

```
clamp(min, preferred, max)
preferred = viewport-relative unit (e.g., 2.5vw + a rem base)
```

### Practical Fluid Scale

```css
:root {
  --text-base: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
  --text-lg:   clamp(1.125rem, 0.75vw + 0.9rem, 1.35rem);
  --text-xl:   clamp(1.25rem, 1vw + 0.95rem, 1.75rem);
  --text-2xl:  clamp(1.5rem, 1.5vw + 1rem, 2.25rem);
  --text-3xl:  clamp(1.875rem, 2vw + 1.1rem, 3rem);
  --text-4xl:  clamp(2.25rem, 3vw + 1rem, 4rem);
  --text-5xl:  clamp(2.75rem, 4vw + 1rem, 5.5rem);
}
```

### Hero Headline Pattern

```css
.hero-title {
  font-size: clamp(2.5rem, 5vw + 1rem, 6rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.03em;
  text-wrap: balance; /* prevents orphans */
}
```

---

## Step 7: Text Treatments and Effects

### Gradient Text

```css
.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Outlined / Stroke Text

```css
.outlined-text {
  -webkit-text-stroke: 2px currentColor;
  -webkit-text-fill-color: transparent;
  font-weight: 800;
  font-size: 5rem;
}
```

### Text Shadow for Depth

```css
.text-shadow-soft {
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.text-shadow-hard {
  text-shadow: 3px 3px 0 rgba(0,0,0,0.15);
}

/* Neon glow */
.text-neon {
  text-shadow:
    0 0 7px #fff,
    0 0 10px #fff,
    0 0 21px #fff,
    0 0 42px #0fa,
    0 0 82px #0fa;
}
```

### Text Over Images

```css
.text-over-image {
  text-shadow: 0 2px 16px rgba(0,0,0,0.5);
  /* OR use a backdrop */
}

.text-backdrop {
  background: rgba(0,0,0,0.5);
  backdrop-filter: blur(4px);
  padding: 0.5em 1em;
  border-radius: 0.25em;
}
```

---

## Step 8: Variable Fonts

### Common Axes

| Axis  | CSS property      | Range (typical) |
|-------|-------------------|-----------------|
| wght  | font-weight       | 100-900         |
| wdth  | font-stretch      | 75%-125%        |
| slnt  | font-style        | -12 to 0        |
| ital  | font-style        | 0 or 1          |
| opsz  | font-optical-sizing| 8-144          |

```css
@font-face {
  font-family: 'Inter Variable';
  src: url('/fonts/InterVariable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}

.heading {
  font-family: 'Inter Variable', sans-serif;
  font-weight: 750;           /* precise weight */
  font-variation-settings: 'wdth' 110;  /* slightly wider */
}
```

---

## Step 9: Letter-Spacing and Word-Spacing Guidelines

| Context              | letter-spacing | Rationale                    |
|----------------------|----------------|------------------------------|
| Large headings (3rem+)| -0.02 to -0.03em | Tighten for visual density|
| Small headings        | -0.01em        | Slight tightening            |
| Body text             | normal (0)     | Default is optimized         |
| All-caps text         | +0.05 to +0.1em| Caps need room to breathe   |
| Small/caption text    | +0.01 to +0.02em| Improve legibility at small sizes|
| Monospace             | normal         | Already evenly spaced        |

```css
.caps-label {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: var(--text-sm);
  font-weight: 600;
}
```

---

## Step 10: Font Loading Strategy

### Recommended Approach

```html
<!-- Preconnect to font CDN -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload critical font file -->
<link rel="preload" as="font" type="font/woff2"
      href="/fonts/inter-var.woff2" crossorigin>
```

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter-var.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;  /* Show fallback immediately, swap when loaded */
}
```

### font-display Values

| Value    | Behavior                              | Use when                      |
|----------|---------------------------------------|-------------------------------|
| swap     | Fallback shown immediately, swaps     | Body text, most cases         |
| optional | Brief block, may skip custom font     | Non-critical decorative fonts |
| fallback | Short block, short swap period        | Balance of swap + optional    |
| block    | Invisible text for up to 3s           | Icon fonts only               |

### System Font Stack Fallback

```css
:root {
  --font-system: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI',
                 Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}
```

### Preventing Layout Shift

Use `size-adjust`, `ascent-override`, and `descent-override` to match fallback metrics:

```css
@font-face {
  font-family: 'Inter Fallback';
  src: local('Arial');
  size-adjust: 107%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

---

## Quick Reference Checklist

1. Pick a type scale ratio appropriate to the project.
2. Choose max 2 typefaces (3 if including monospace).
3. Set body text to 16-18px with 1.5-1.75 line-height.
4. Constrain line length to 45-75 characters.
5. Use `clamp()` for fluid responsive sizing.
6. Apply negative letter-spacing to large headings.
7. Use positive letter-spacing for uppercase text.
8. Preload critical fonts; use `font-display: swap`.
9. Set up a system font fallback stack.
10. Use `text-wrap: balance` on headings to avoid orphans.
