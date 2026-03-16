---
name: image-treatment
description: >
  Photo effects, image composition, and visual treatments with CSS and SVG.
  Trigger phrases: "image effect", "photo filter", "image overlay",
  "duotone", "image mask", "parallax background", "clip-path",
  "blend mode", "image grid", "responsive image", "css filter"
license: MIT
---

# Image Treatment

Apply stunning visual effects to images using CSS filters, blend modes, masks, and SVG filters.

## Prerequisites

- Read any design-context files for brand colors, image style guidelines, or photography direction.
- Identify the mood and purpose: editorial, product, marketing, artistic.

---

## Step 1: CSS Filter Combinations

### Individual Filters

| Filter       | Range        | Effect                          |
|--------------|-------------|---------------------------------|
| brightness() | 0-2+        | Darken (< 1) or lighten (> 1)  |
| contrast()   | 0-2+        | Reduce (< 1) or boost (> 1)    |
| saturate()   | 0-3+        | Desaturate (0) or vivid (> 1)  |
| grayscale()  | 0-1         | Remove color                    |
| sepia()      | 0-1         | Warm vintage tone               |
| hue-rotate() | 0-360deg    | Shift all hues                  |
| blur()       | 0-20px+     | Gaussian blur                   |

### Preset Filter Recipes

```css
.filter-vintage  { filter: sepia(0.3) contrast(1.1) brightness(1.05) saturate(0.9); }
.filter-cool     { filter: saturate(0.85) contrast(1.1) brightness(1.02) hue-rotate(-10deg); }
.filter-bw       { filter: grayscale(1) contrast(1.4) brightness(1.05); }
.filter-dreamy   { filter: brightness(1.1) contrast(0.9) saturate(1.2) blur(0.5px); }
.filter-faded    { filter: contrast(0.85) brightness(1.1) saturate(0.7); }
.filter-moody    { filter: brightness(0.85) contrast(1.2) saturate(0.8); }
.filter-vivid    { filter: contrast(1.15) saturate(1.4) brightness(1.02); }
```

### Hover Effect with Filters

```css
.image-card img { filter: grayscale(0.8) brightness(0.9); transition: filter 0.4s ease; }
.image-card:hover img { filter: grayscale(0) brightness(1); }
```

---

## Step 2: Blend Mode Techniques

### Common Blend Modes

| Mode        | Effect                                         | Use case               |
|-------------|-------------------------------------------------|------------------------|
| multiply    | Darkens (white disappears)                      | Text over light images |
| screen      | Lightens (black disappears)                     | Glow effects           |
| overlay     | Boosts contrast                                 | Color overlays         |
| soft-light  | Subtle overlay                                  | Gentle tinting         |
| color       | Applies hue/sat, preserves luminosity           | Tinting photos         |
| luminosity  | Applies brightness, preserves color of bg       | B&W-like effect        |

### Color Overlay on Image

```css
.image-container { position: relative; }
.image-container::after {
  content: ''; position: absolute; inset: 0;
  background: var(--brand-500); mix-blend-mode: multiply; opacity: 0.6;
}
```

---

## Step 3: Duotone Image Effect

Maps the image's lights to one color and darks to another.

### CSS-Only Duotone

```css
.duotone { position: relative; overflow: hidden; }
.duotone img { filter: grayscale(1) contrast(1.2); mix-blend-mode: luminosity; width: 100%; }
.duotone::before {
  content: ''; position: absolute; inset: 0;
  background: #1a1a2e; z-index: 1; mix-blend-mode: color;
}
.duotone::after {
  content: ''; position: absolute; inset: 0;
  background: #e2b94c; z-index: 2; mix-blend-mode: screen; opacity: 0.5;
}
```

### Popular Duotone Pairs

| Shadow color  | Highlight color | Feel                 |
|---------------|-----------------|----------------------|
| #1a1a2e       | #e2b94c         | Luxury, gold+navy    |
| #0d1b2a       | #3498db         | Tech, cool blue      |
| #2d1b4e       | #ff6b6b         | Creative, bold       |
| #1b3a2a       | #a7f3d0         | Natural, green       |

---

## Step 4: Image Masking

### clip-path Shapes

```css
.clip-circle   { clip-path: circle(50%); }
.clip-rounded  { clip-path: inset(0 round 1rem); }
.clip-diagonal { clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%); }
.clip-hexagon  { clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%); }
```

### mask-image for Gradient Fades

```css
.image-fade-bottom {
  mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
  -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
}
.image-vignette {
  mask-image: radial-gradient(ellipse 70% 70% at center, black 50%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 70% 70% at center, black 50%, transparent 100%);
}
```

### Text-Shaped Mask

```css
.image-text-mask {
  background-image: url('photo.jpg'); background-size: cover;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; font-size: 8rem; font-weight: 900;
}
```

---

## Step 5: Background Image Techniques

### Full Cover Background

```css
.hero-bg {
  background: url('hero.jpg') center/cover no-repeat;
  min-height: 80vh;
}
```

### Fixed / Parallax Background

```css
.parallax-section {
  background: url('bg.jpg') center/cover no-repeat;
  background-attachment: fixed;
  min-height: 60vh;
}
@media (hover: none) {
  .parallax-section { background-attachment: scroll; }
}
```

### Multiple Background Layers

```css
.layered-bg {
  background:
    linear-gradient(to bottom, rgba(0,0,0,0.4), rgba(0,0,0,0.7)),
    url('pattern.svg') repeat center / 64px 64px,
    url('photo.jpg') no-repeat center / cover;
}
```

---

## Step 6: Image Overlay Patterns

### Gradient Overlay (for text readability)

```css
.image-overlay-gradient { position: relative; }
.image-overlay-gradient::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.3) 40%, transparent 100%);
}
.image-overlay-gradient .content { position: relative; z-index: 1; color: white; }
```

### Hover Reveal Overlay

```css
.card-image { position: relative; overflow: hidden; }
.card-image .overlay {
  position: absolute; inset: 0;
  background: oklch(from var(--brand-500) l c h / 0.85);
  display: grid; place-items: center; opacity: 0; transition: opacity 0.3s ease;
}
.card-image:hover .overlay { opacity: 1; }
```

---

## Step 7: Image Grid and Collage Layouts

### Masonry-Style Grid

```css
.image-grid-masonry { columns: 3; column-gap: 1rem; }
.image-grid-masonry img { width: 100%; margin-bottom: 1rem; border-radius: 0.5rem; break-inside: avoid; }
@media (max-width: 768px) { .image-grid-masonry { columns: 2; } }
@media (max-width: 480px) { .image-grid-masonry { columns: 1; } }
```

### CSS Grid Collage

```css
.image-collage {
  display: grid; grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 200px); gap: 0.5rem;
}
.image-collage img:nth-child(1) { grid-column: 1 / 3; grid-row: 1 / 3; }
.image-collage img { width: 100%; height: 100%; object-fit: cover; border-radius: 0.5rem; }
```

---

## Step 8: Responsive Image Art Direction

### The `<picture>` Element

```html
<picture>
  <source media="(max-width: 640px)" srcset="hero-mobile.avif" type="image/avif">
  <source media="(max-width: 640px)" srcset="hero-mobile.webp" type="image/webp">
  <source srcset="hero-desktop.avif" type="image/avif">
  <source srcset="hero-desktop.webp" type="image/webp">
  <img src="hero-desktop.jpg" alt="Hero image" width="1600" height="900" loading="eager">
</picture>
```

### Key Rules

1. Always include `width` and `height` attributes to prevent layout shift.
2. Use `loading="lazy"` for below-fold images, `loading="eager"` for hero images.
3. Use `decoding="async"` to avoid blocking the main thread.
4. Prefer AVIF > WebP > JPEG for file size.

---

## Step 9: SVG Filters for Advanced Effects

### Frosted Glass
```css
.frosted-glass { backdrop-filter: blur(12px) saturate(180%); background: rgba(255,255,255,0.7); }
```

### Noise/Grain Texture
```html
<svg width="0" height="0">
  <filter id="noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
    <feBlend in="SourceGraphic" mode="multiply"/>
  </filter>
</svg>
```

### Drop Shadow (Following Shape)
```css
.shaped-shadow { filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2)); }
```

---

## Step 10: Object-Fit and Object-Position

| Value      | Behavior                                              |
|------------|-------------------------------------------------------|
| cover      | Fills container, crops excess (most common)           |
| contain    | Fits entirely, may have empty space                   |
| fill       | Stretches to fill (distorts)                          |
| scale-down | Like contain but never scales up                      |

```css
.card-image { width: 100%; height: 200px; object-fit: cover; object-position: center; }
.portrait   { object-fit: cover; object-position: center top; }
.thumbnail  { aspect-ratio: 1; object-fit: cover; border-radius: 0.75rem; }
```

---

## Quick Reference

1. Use CSS `filter` for quick photo effects (combine brightness, contrast, saturate).
2. Use `mix-blend-mode: multiply` for color overlays on images.
3. Duotone = grayscale image + two-color blend layers.
4. `clip-path` for geometric masks; `mask-image` for gradient fades.
5. Always disable `background-attachment: fixed` on mobile (`@media (hover: none)`).
6. Layer overlays: gradient bottom-to-top for text readability on images.
7. Use `<picture>` for art direction (different crops per breakpoint).
8. Always include `width`, `height`, `loading`, and `alt` on images.
9. `object-fit: cover` + `aspect-ratio` for consistent image containers.
10. SVG filters (noise, goo, displacement) for effects CSS cannot achieve.
