---
name: image-treatment
description: >
  Treat existing images in code: CSS filters, blend modes, duotone, masks and
  clip-paths, overlays for text legibility, collages, SVG filters, and responsive
  delivery (picture/srcset/sizes, AVIF/WebP). Use when styling or serving photos on
  a page; to CREATE new images use image-generation. Trigger phrases: "image effect", "photo filter", "image overlay",
  "duotone", "image mask", "parallax background", "clip-path",
  "blend mode", "image grid", "responsive image", "css filter"
license: MIT
---

# Image Treatment

Apply stunning visual effects to images using CSS filters, blend modes, masks, and SVG filters.

## Prerequisites

- Read `.agents/design-context.md` (see `design-context`) for brand colors (duotone and overlay colors should come from the Color System), style archetype, and imagery direction. Colors below use the shared `--brand-*` / `--gray-*` scale.
- Identify the mood and purpose: editorial, product, marketing, artistic.
- If source images don't exist yet, create them with the `image-generation` skill (`python <image-generation>/scripts/gemini-generate.py`), then treat them here. For treatments that must be baked into the file (social images, email, OG images), apply them with Pillow instead of CSS.

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
| multiply    | Darkens (white disappears)                      | Color tints, knocking out white backgrounds |
| screen      | Lightens (black disappears)                     | Glow effects           |
| overlay     | Boosts contrast                                 | Color overlays         |
| soft-light  | Subtle overlay                                  | Gentle tinting         |
| color       | Applies hue/sat, preserves luminosity           | Tinting photos         |
| luminosity  | Takes brightness from the layer, hue/saturation from what's below | Recoloring textures |

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

Grayscale image **multiplied** onto the highlight color (white → highlight, black → black), then the shadow color **lightens** the darks (black → shadow). The highlight must be lighter than the shadow in every RGB channel.

```css
.duotone { position: relative; isolation: isolate; background: #e2b94c; /* highlight */ }
.duotone img { display: block; width: 100%; filter: grayscale(1) contrast(1.2); mix-blend-mode: multiply; }
.duotone::after {
  content: ''; position: absolute; inset: 0; pointer-events: none;
  background: #1a1a2e; /* shadow */ mix-blend-mode: lighten;
}
```

### SVG Filter Duotone (exact mapping, works on any element)

`tableValues` are each channel of shadow → highlight in 0-1 (hex ÷ 255): `#1a1a2e` → `#e2b94c`.

```html
<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <filter id="duotone-gold" color-interpolation-filters="sRGB">
    <feColorMatrix type="matrix" values="0.2126 0.7152 0.0722 0 0  0.2126 0.7152 0.0722 0 0  0.2126 0.7152 0.0722 0 0  0 0 0 1 0"/>
    <feComponentTransfer>
      <feFuncR type="table" tableValues="0.102 0.886"/>
      <feFuncG type="table" tableValues="0.102 0.725"/>
      <feFuncB type="table" tableValues="0.180 0.298"/>
    </feComponentTransfer>
  </filter>
</svg>
<img src="photo.jpg" alt="…" style="filter: url(#duotone-gold)">
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
  color: transparent; /* fallback if background-clip: text is unsupported */
}
```

Only for display-size decorative text; the photo under the letters must still give 3:1 contrast with the page background, and the element keeps real text for screen readers.

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
@media (hover: none), (prefers-reduced-motion: reduce) {
  .parallax-section { background-attachment: scroll; } /* iOS ignores fixed; parallax can trigger vestibular issues */
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

Text over images must still meet WCAG contrast (4.5:1, or 3:1 for ≥24px / ≥18.66px bold) against the **lightest** pixels behind it. Check the region under the text in the rendered screenshot, not the average of the image; strengthen the overlay until it passes.

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
.image-grid-masonry img { display: block; width: 100%; margin-bottom: 1rem; border-radius: 0.5rem; break-inside: avoid; }
/* Note: columns flow top-to-bottom, so DOM/reading order runs down each column, not across rows */
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

### Resolution Switching (same crop, many sizes)

`w` descriptors list each file's real pixel width; `sizes` tells the browser how wide the image will be *displayed* so it can pick before layout. Without `sizes`, the browser assumes `100vw`.

```html
<img src="card-800.jpg"
     srcset="card-400.jpg 400w, card-800.jpg 800w, card-1200.jpg 1200w, card-1600.jpg 1600w"
     sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 400px"
     alt="Team reviewing designs at a whiteboard" width="800" height="600"
     loading="lazy" decoding="async">
```

### Art Direction + Modern Formats (`<picture>`)

Browsers take the **first** matching `<source>`, so order by media query, then by format (AVIF before WebP). Each source gets its own `srcset`/`sizes`; `width`/`height` on `<source>` handle a different aspect ratio per breakpoint.

```html
<picture>
  <source media="(max-width: 640px)" type="image/avif"
          srcset="hero-mobile-640.avif 640w, hero-mobile-1280.avif 1280w" sizes="100vw" width="1280" height="1600">
  <source media="(max-width: 640px)" type="image/webp"
          srcset="hero-mobile-640.webp 640w, hero-mobile-1280.webp 1280w" sizes="100vw" width="1280" height="1600">
  <source type="image/avif" srcset="hero-1600.avif 1600w, hero-2400.avif 2400w" sizes="100vw">
  <source type="image/webp" srcset="hero-1600.webp 1600w, hero-2400.webp 2400w" sizes="100vw">
  <img src="hero-1600.jpg" alt="Describe what the hero shows" width="1600" height="900"
       fetchpriority="high" decoding="async">
</picture>
```

### Key Rules

1. Always include `width` and `height` attributes (the intrinsic aspect ratio) to prevent layout shift; CSS can still make it fluid with `width: 100%; height: auto`.
2. Use `loading="lazy"` for below-fold images. Never lazy-load the LCP/hero image -- leave it eager (the default) and add `fetchpriority="high"`.
3. Use `decoding="async"` so decode doesn't block rendering.
4. Formats: AVIF (smallest, supported in all current major browsers) → WebP → JPEG fallback in `<img src>`. Use PNG/SVG only for graphics needing transparency or sharp edges; quality ~50-65 for AVIF and ~75-80 for WebP is a good start.
5. `alt` describes the image's purpose; decorative images use `alt=""`.

### Generate the Variants

```python
from PIL import Image  # pip install Pillow  (AVIF built in since Pillow 11.2; check features.check("avif"))
src = Image.open("hero.png").convert("RGB")
for w in (640, 1280, 1600, 2400):
    im = src.resize((w, round(src.height * w / src.width)), Image.LANCZOS)
    im.save(f"hero-{w}.webp", quality=78)
    im.save(f"hero-{w}.avif", quality=55)
    im.save(f"hero-{w}.jpg", quality=82, optimize=True, progressive=True)
```

---

## Step 9: SVG Filters for Advanced Effects

### Frosted Glass
```css
.frosted-glass { backdrop-filter: blur(12px) saturate(180%); background: rgba(255,255,255,0.7); }
@supports not (backdrop-filter: blur(1px)) { .frosted-glass { background: rgba(255,255,255,0.92); } } /* keep text readable */
```

### Noise/Grain Texture
```html
<svg width="0" height="0" aria-hidden="true" style="position:absolute">
  <filter id="noise">
    <feTurbulence type="fractalNoise" baseFrequency="0.65" numOctaves="3" stitchTiles="stitch"/>
    <feColorMatrix type="saturate" values="0"/>
    <feBlend in="SourceGraphic" mode="multiply"/>
  </filter>
</svg>
<!-- apply with: .grain { filter: url(#noise); } -->
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
8. Always include `width`, `height`, `alt`, and `srcset` + `sizes` on content images; lazy-load only below the fold.
9. `object-fit: cover` + `aspect-ratio` for consistent image containers.
10. SVG filters (noise, goo, displacement) for effects CSS cannot achieve.

## Verify the Treatment

Render the page and screenshot it (`npx playwright screenshot --full-page "file://$PWD/index.html" out.png`, plus `--viewport-size=375,800` for mobile and `--color-scheme=dark`), then view the images with Read. Check: faces and products aren't cropped by `object-fit`/`clip-path` at any width, text over images passes contrast in its worst spot, duotone/filters still look on-brand (not muddy), and nothing looks broken where a blend mode or filter is unsupported. In the browser, confirm the right `srcset` candidate loads (`img.currentSrc`) and that the hero is not lazy-loaded.
