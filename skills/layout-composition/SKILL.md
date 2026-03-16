---
name: layout-composition
description: >
  Grid systems, visual hierarchy, and modern layout patterns for web design.
  Trigger phrases: "layout", "grid", "bento grid", "visual hierarchy",
  "page layout", "flexbox layout", "whitespace", "responsive layout",
  "composition", "css grid", "container queries"
license: MIT
---

# Layout and Composition

Build structured, visually compelling layouts using modern CSS.

## Prerequisites

- Read any design-context files for layout preferences, breakpoints, or grid constraints.
- Identify the content types (text-heavy, media-heavy, dashboard, marketing) to choose the right patterns.

---

## Step 1: CSS Grid Patterns

### 12-Column Grid

```css
.grid-12 {
  display: grid; grid-template-columns: repeat(12, 1fr);
  gap: 1.5rem; max-width: 1280px; margin-inline: auto; padding-inline: 1.5rem;
}
.col-full    { grid-column: 1 / -1; }
.col-half    { grid-column: span 6; }
.col-third   { grid-column: span 4; }
.col-quarter { grid-column: span 3; }
@media (max-width: 768px) { .grid-12 > * { grid-column: 1 / -1; } }
```

### Auto-Fit Grid (no media queries needed)

```css
.grid-auto { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }
```

### Named Grid Areas

```css
.page-layout {
  display: grid; grid-template-columns: 250px 1fr 300px;
  grid-template-rows: auto 1fr auto; min-height: 100dvh;
  grid-template-areas: "header header header" "sidebar main aside" "footer footer footer";
}
.header { grid-area: header; } .sidebar { grid-area: sidebar; }
.main { grid-area: main; } .footer { grid-area: footer; }
@media (max-width: 1024px) {
  .page-layout { grid-template-columns: 1fr; grid-template-areas: "header" "main" "sidebar" "aside" "footer"; }
}
```

---

## Step 2: Flexbox Layout Patterns

### Navbar
```css
.navbar { display: flex; align-items: center; justify-content: space-between; padding: 1rem 2rem; gap: 2rem; }
```

### Centered Content Page
```css
.centered-page { display: flex; flex-direction: column; align-items: center; min-height: 100dvh; }
.centered-page main { flex: 1; width: 100%; max-width: 65ch; padding: 2rem; }
```

### Card Row with Equal Heights
```css
.card-row { display: flex; gap: 1.5rem; }
.card-row > * { flex: 1; display: flex; flex-direction: column; }
.card-row .card-footer { margin-top: auto; }
```

---

## Step 3: Bento Grid Layouts

### Basic Bento

```css
.bento { display: grid; grid-template-columns: repeat(4, 1fr); grid-auto-rows: 200px; gap: 1rem; }
.bento-large { grid-column: span 2; grid-row: span 2; }
.bento-wide  { grid-column: span 2; }
.bento-tall  { grid-row: span 2; }
```

### Feature Showcase Bento

```css
.bento-showcase {
  display: grid; grid-template-columns: repeat(6, 1fr);
  grid-template-rows: repeat(4, 180px); gap: 1rem; padding: 1rem;
}
.bento-showcase > :nth-child(1) { grid-column: 1 / 4; grid-row: 1 / 3; }
.bento-showcase > :nth-child(2) { grid-column: 4 / 7; grid-row: 1 / 2; }
.bento-showcase > :nth-child(5) { grid-column: 1 / 3; grid-row: 3 / 5; }
.bento-showcase > * { border-radius: 1rem; padding: 1.5rem; overflow: hidden; background: var(--gray-100); }
@media (max-width: 768px) {
  .bento-showcase { grid-template-columns: 1fr 1fr; grid-template-rows: auto; }
  .bento-showcase > * { grid-column: auto !important; grid-row: auto !important; }
}
```

### Bento Card Styling

```css
.bento-card { border-radius: 1.25rem; padding: 2rem; overflow: hidden; position: relative; display: flex; flex-direction: column; justify-content: space-between; }
.bento-card--gradient { background: linear-gradient(135deg, var(--brand-100), var(--brand-50)); }
.bento-card--dark { background: var(--gray-900); color: var(--gray-50); }
```

---

## Step 4: Whitespace as a Design Element

### Spacing Scale

```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
  --space-5: 1.5rem; --space-6: 2rem; --space-8: 3rem; --space-10: 4rem;
  --space-12: 6rem; --space-16: 8rem;
}
section { padding-block: clamp(4rem, 8vw, 8rem); }
.hero { padding-block: clamp(6rem, 12vw, 12rem); }
```

### Density Guidelines
- Dense UI (dashboards): 4-8px gaps, 12-16px padding
- Standard UI (apps): 8-16px gaps, 16-24px padding
- Marketing / editorial: 16-32px gaps, 32-64px section padding
- Luxury / premium: double everything

---

## Step 5: Visual Hierarchy Techniques

Ranked by impact (strongest to weakest):

1. **Size** -- Make the most important element the largest
2. **Color and Contrast** -- High contrast draws the eye; brand color for CTAs, muted grays for secondary
3. **Weight and Typeface** -- Bold signals importance
4. **Position** -- Top-left gets read first (LTR); place key content above the fold
5. **Proximity and Grouping** -- Related items close together, clear separation for unrelated
6. **Negative Space** -- Whitespace increases visual weight

### Section Header Pattern

```css
.section-header { max-width: 600px; margin-inline: auto; text-align: center; margin-bottom: var(--space-10); }
.section-label { font-size: var(--text-sm); font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--brand-500); margin-bottom: var(--space-3); }
.section-title { font-size: var(--text-4xl); font-weight: 800; line-height: 1.1; color: var(--gray-900); margin-bottom: var(--space-4); }
.section-description { font-size: var(--text-lg); color: var(--gray-500); line-height: 1.6; }
```

---

## Step 6: Reading Patterns

### F-Pattern (Text-Heavy Pages)
Users scan across the top, partway across the middle, then down the left. Place key info in first two paragraphs, start sections with bold keywords, use left-aligned headings.

### Z-Pattern (Landing Pages)
Users scan: top-left logo > top-right nav > diagonal to center CTA > bottom. Build landing pages along this diagonal.

---

## Step 7: Rule of Thirds and Asymmetric Layouts

Place focal points at 1/3 intersections, not dead center. Slightly off-center placement feels more dynamic.

```css
.hero-content { display: grid; grid-template-columns: 2fr 1fr; align-items: center; min-height: 80vh; }
```

### Asymmetric Split (60/40)

```css
.asymmetric { display: grid; grid-template-columns: 1.5fr 1fr; gap: 4rem; align-items: center; }
.asymmetric--reversed { grid-template-columns: 1fr 1.5fr; }
```

### Offset Grid

```css
.offset-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; }
.offset-grid > :nth-child(3n+2) { transform: translateY(3rem); }
```

---

## Step 8: Responsive Strategies

### Stack Pattern (auto-responsive)
```css
.layout { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 350px), 1fr)); gap: 1.5rem; }
```

### Reflow Pattern
```css
.reflow { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; }
@media (max-width: 768px) { .reflow { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .reflow { grid-template-columns: 1fr; } }
```

---

## Step 9: Container Query Layouts

```css
.card-container { container-type: inline-size; container-name: card; }
.card { display: flex; flex-direction: column; }
@container card (min-width: 500px) {
  .card { flex-direction: row; align-items: center; gap: 2rem; }
  .card-image { flex: 0 0 200px; }
}
```

---

## Step 10: Aspect Ratio for Consistent Media

```css
.thumbnail { aspect-ratio: 16 / 9; object-fit: cover; border-radius: 0.75rem; width: 100%; }
.avatar { aspect-ratio: 1; object-fit: cover; border-radius: 50%; }
/* Common ratios: 1:1 avatars, 4:3 cards, 16:9 video, 3:2 photos, 21:9 cinematic */
```

---

## Quick Reference: Layout Selection Guide

| Content type          | Recommended layout                 |
|-----------------------|------------------------------------|
| Landing page          | Single column + full-width sections|
| Blog / article        | Centered single column, max 65ch   |
| Dashboard             | 12-column grid or sidebar + main   |
| Feature showcase      | Bento grid                         |
| Card listing          | Auto-fit grid                      |
| Portfolio             | Masonry or offset grid             |
| Documentation         | Sidebar nav + centered content     |
| E-commerce product    | 2-col asymmetric (image + details) |
