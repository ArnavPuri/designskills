---
name: graphic-design
description: >
  Core graphic design skill for generating eye-catching visuals via Gemini 3.1 Flash image
  generation and/or HTML/CSS/SVG code. Covers composition, color theory, typography treatment,
  prompt engineering for AI image generation, and advanced CSS techniques.
  Trigger phrases: "design a graphic", "create a visual", "make a graphic",
  "design an image", "create artwork", "generate a graphic", "visual design".
license: MIT
---

# Graphic Design

The primary skill for generating stunning visual graphics. Supports two output modes:

1. **AI Image Generation** (default) — Uses Gemini 3.1 Flash Image Preview to generate pixel-perfect graphics from prompts and reference images
2. **Code Generation** — Produces production-ready HTML/CSS/SVG for web-native graphics

Choose AI generation for social posts, posters, ads, and rich visuals. Choose code for interactive web graphics, animated elements, or when the output must be editable HTML.

---

## Step 1: Load Design Context

Before any design work:

1. Read `.agents/design-context.md` for brand colors, fonts, style archetype
2. If no context exists, ask the user to run the `design-context` skill or proceed with defaults
3. Extract: primary color, secondary color, accent, heading font, body font, design style

---

## Step 2: Analyze the Brief

Determine the graphic's purpose:

| Intent | Approach | Key Elements |
|--------|----------|--------------|
| **Promotional** | Bold, attention-grabbing | Large headline, CTA, product image |
| **Informational** | Clear hierarchy, readable | Structured content, icons, data |
| **Emotional** | Mood-driven, atmospheric | Photography, color mood, minimal text |
| **Celebratory** | Energetic, festive | Dynamic shapes, bright colors, confetti/particles |
| **Announcement** | Clean, authoritative | Date/details prominent, professional |
| **Brand Awareness** | On-brand, memorable | Logo prominent, brand colors dominant |

Identify required elements:
- Headline text
- Subheadline or supporting text
- Product image or visual focal point
- CTA or action text
- Brand elements (logo, colors)
- Dimensions / aspect ratio

---

## Step 2b: Gemini Image Generation Path

When generating graphics as images (not code), use Gemini 3.1 Flash Image Preview:

### Craft the Prompt

Build a structured prompt from the brief. **Describe the scene narratively — don't just list keywords.**

**Prompt template:**
```
Create a [style] [format] for [purpose].

Scene: [Describe the composition — what's in the foreground, background, how elements are arranged]
Style: [Design style — minimalist, bold, luxurious, retro, etc.]
Colors: [Specific colors from brand context — "navy blue #1a2b4a background with coral #ff6b6b accents"]
Typography: [Describe text treatment — "large bold sans-serif headline reading '[TEXT]' in white"]
Mood: [Emotional tone — energetic, calm, professional, playful]
Details: [Specific design elements — gradients, geometric shapes, textures, shadows]
```

### With a Product Image

Pass the product image + prompt to Gemini. See `image-generation` skill for full API details and CLI usage.

**Example prompt for product image editing:**
> Place this product on a bold gradient background (#1a2b4a to #ff6b6b). Add a large headline 'NEW ARRIVAL' in white bold sans-serif at the top. Add geometric accent shapes. Eye-catching for Instagram (1:1).

### Prompt Engineering for Design Quality

| Technique | Example |
|-----------|---------|
| **Specify style explicitly** | "flat vector illustration style" not "nice looking" |
| **Name colors with hex codes** | "deep navy #0a1628 background" not "dark background" |
| **Describe spatial layout** | "product centered in lower third, text in upper third" |
| **Reference design movements** | "Swiss/International style grid layout" |
| **Describe typography style** | "bold geometric sans-serif, tightly tracked" not "nice font" |
| **Include lighting/texture** | "soft gradient lighting from top-left, subtle noise texture" |
| **Specify what NOT to include** | "no borders, no drop shadows, no clip art" |

### Iterative Refinement

Use multi-turn chat (see `image-generation` skill) to refine: adjust colors, reposition elements, change text, add/remove details. Each refinement builds on the previous result.

---

## Step 3: Analyze Product Image (If Provided)

When the user provides a product image:

1. **Identify dominant colors** -- extract 3-5 key colors from the image
2. **Assess composition** -- where is the subject, where is negative space
3. **Determine mood** -- warm/cool, energetic/calm, luxurious/casual
4. **Plan integration** -- how the image fits into the overall graphic layout
5. **Choose complement strategy:**
   - Harmonious: use colors from the image in the background/text
   - Contrasting: use complementary colors to make the image pop
   - Monochromatic: desaturate and overlay with brand color

---

## Step 4: Apply Composition Principles

### Rule of Thirds
Divide the canvas into a 3x3 grid. Place key elements at intersection points.

```css
/* Visual guide for rule of thirds placement */
.canvas {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr;
}
.focal-point {
  grid-column: 2;
  grid-row: 1 / 3; /* Upper-center area for primary content */
}
```

### Golden Ratio (1:1.618)
Use for sizing relationships between elements:
- If headline is 48px, subheadline should be ~30px (48 / 1.618)
- If main content area is 600px, sidebar/accent area should be ~370px

### Focal Point Hierarchy
Every graphic needs ONE clear focal point. Layer importance:

1. **Primary focal point** -- the thing the eye hits first (largest, most contrasted)
2. **Secondary elements** -- supporting info (medium size, moderate contrast)
3. **Tertiary details** -- fine print, logos, decorative (smallest, lowest contrast)

### Z-Pattern (for text-heavy graphics)
Eye moves: top-left -> top-right -> diagonal to bottom-left -> bottom-right

### F-Pattern (for information-dense layouts)
Eye scans horizontally across top, then drops down and scans shorter horizontal lines.

---

## Step 5: Color Scheme Selection

Start from the design-context colors, then apply these strategies:

### Complementary Enhancement
```
Primary + its complement for maximum contrast
Use 60-30-10 rule: 60% dominant, 30% secondary, 10% accent
```

### Gradient Techniques

```css
/* Smooth multi-stop gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Mesh-style gradient (multiple radials) */
background:
  radial-gradient(at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
  radial-gradient(at 80% 20%, rgba(255, 119, 115, 0.3) 0%, transparent 50%),
  radial-gradient(at 50% 50%, rgba(76, 29, 149, 1) 0%, rgba(15, 23, 42, 1) 100%);

/* Conic gradient for unique effects */
background: conic-gradient(from 45deg, #12c2e9, #c471ed, #f64f59, #12c2e9);

/* Animated gradient */
background: linear-gradient(270deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
background-size: 400% 400%;
animation: gradientShift 8s ease infinite;

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

### Color Overlay on Images
```css
.image-with-overlay {
  position: relative;
}
.image-with-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.7), rgba(124, 58, 237, 0.7));
  mix-blend-mode: multiply;
}
```

---

## Step 6: Typography Treatment

### Headline Hierarchy

```css
/* Display headline -- the main event */
.headline {
  font-family: var(--font-heading);
  font-size: clamp(2.5rem, 6vw, 5rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.02em;
  text-wrap: balance;
}

/* Subheadline -- supporting context */
.subheadline {
  font-family: var(--font-body);
  font-size: clamp(1rem, 2vw, 1.5rem);
  font-weight: 400;
  line-height: 1.4;
  opacity: 0.85;
}

/* Detail text -- dates, fine print */
.detail {
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
```

### Text Effects

- **Gradient text**: `background: linear-gradient(...)` + `background-clip: text` + `-webkit-text-fill-color: transparent`
- **Outlined text**: `-webkit-text-stroke: 2px currentColor` + `-webkit-text-fill-color: transparent`
- **Glowing text**: Multi-layer `text-shadow` at increasing blur/spread with decreasing opacity
- **Embossed**: Transparent color + light text-shadow + dark bg-clip text
- **Depth/3D text**: Stacked 1px-offset text-shadows in progressively darker shades

---

## Step 7: Generate the Graphic

### Output Structure

Always generate as a self-contained HTML file with embedded CSS:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=[HeadingFont]:wght@700;800&family=[BodyFont]:wght@400;500&display=swap" rel="stylesheet">
  <style>
    /* Reset and canvas setup */
    *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

    .canvas {
      width: [WIDTH]px;
      height: [HEIGHT]px;
      position: relative;
      overflow: hidden;
      /* Background, gradients, etc. */
    }

    /* Layer structure */
    .background-layer { /* gradients, patterns, images */ }
    .content-layer { /* text, CTAs, key elements */ }
    .decoration-layer { /* shapes, accents, overlays */ }
  </style>
</head>
<body>
  <div class="canvas">
    <div class="background-layer">...</div>
    <div class="content-layer">...</div>
    <div class="decoration-layer">...</div>
  </div>
</body>
</html>
```

### Advanced CSS Techniques

#### Creative Shapes with clip-path
```css
/* Diagonal section */
.diagonal { clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%); }

/* Blob shape */
.blob { clip-path: polygon(30% 0%, 70% 0%, 100% 30%, 100% 70%, 70% 100%, 30% 100%, 0% 70%, 0% 30%); }

/* Circle reveal */
.circle-reveal { clip-path: circle(40% at 50% 50%); }

/* Custom wave */
.wave-bottom {
  clip-path: path('M0,200 C150,250 350,150 500,200 L500,0 L0,0 Z');
}
```

#### Glassmorphism
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
}
```

#### Blend Modes for Image Integration
```css
.image-overlay {
  background-image: url('product.jpg');
  background-size: cover;
  background-blend-mode: overlay; /* or multiply, screen, soft-light */
  background-color: rgba(37, 99, 235, 0.5);
}
```

#### SVG Filters
Use inline `<svg>` with `<filter>` for noise (`feTurbulence` + `feColorMatrix` + `feBlend multiply`) and glow (`feGaussianBlur` + `feMerge`).

#### Decorative Elements
- **Floating circles**: Absolute-positioned, radial gradient, `filter: blur(40px)`
- **Grid/dot patterns**: `background-image` with `linear-gradient` or `radial-gradient` at low opacity, small `background-size`

#### Subtle Animations
- **Float**: `translateY(0 -> -10px -> 0)` over 4s ease-in-out infinite
- **Pulse glow**: `box-shadow` alternating intensity over 2-3s
- **Shimmer**: Linear gradient at 200% background-size, animate `background-position` from -200% to 200%

---

## Step 8: Style-Specific Frameworks

### Minimalist
```css
.minimalist-canvas {
  background: #FAFAFA;
  padding: 60px;
}
.minimalist-canvas .headline {
  font-size: 3rem;
  font-weight: 300;
  color: #171717;
  letter-spacing: -0.03em;
}
/* Single accent color, generous whitespace, thin rules */
/* Use negative space as a design element */
/* Max 2 colors plus neutrals */
```

### Bold / Vibrant
```css
.bold-canvas {
  background: linear-gradient(135deg, #FF6B6B, #FFE66D);
}
.bold-canvas .headline {
  font-size: 5rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.04em;
}
/* Saturated gradients, oversized type, geometric overlays */
/* High contrast, thick borders, strong shadows */
```

### Luxurious
```css
.luxury-canvas {
  background: #0A0A0A;
  color: #F5F0E8;
}
.luxury-canvas .headline {
  font-family: 'Playfair Display', serif;
  font-size: 3.5rem;
  font-weight: 400;
  letter-spacing: 0.05em;
}
.luxury-canvas .accent {
  color: #D4AF37; /* Gold */
  border: 1px solid rgba(212, 175, 55, 0.3);
}
/* Dark backgrounds, gold/silver accents, serif fonts */
/* Subtle gradients, thin lines, refined spacing */
```

### Playful
```css
.playful-canvas {
  background: #FFF8F0;
  border-radius: 24px;
}
.playful-canvas .headline {
  font-family: 'Fredoka One', cursive;
  font-size: 3rem;
  color: #FF6B6B;
  transform: rotate(-2deg);
}
/* Bright colors, rounded everything, hand-drawn feel */
/* Bouncy animations, emoji accents, organic shapes */
```

### Corporate
```css
.corporate-canvas {
  background: #FFFFFF;
  font-family: 'Inter', sans-serif;
}
.corporate-canvas .headline {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1E3A5F;
}
/* Blue/gray palette, structured 12-column grid */
/* Professional photography, clean data presentation */
```

### Retro
```css
.retro-canvas {
  background: #F4E8C1;
  color: #2D1B00;
}
.retro-canvas .headline {
  font-family: 'Playfair Display', serif;
  font-size: 4rem;
  font-weight: 900;
}
/* Halftone overlay with SVG filter, warm palette */
/* Vintage color: #C84B31, #2D1B00, #F4E8C1, #ECDBBA */
/* Distressed textures, stamp effects */
```

### Brutalist
```css
.brutalist-canvas {
  background: #FFFFFF;
  border: 4px solid #000000;
}
.brutalist-canvas .headline {
  font-family: 'Space Mono', monospace;
  font-size: 4rem;
  font-weight: 700;
  text-transform: uppercase;
  mix-blend-mode: difference;
}
/* High contrast B&W, raw borders, monospace type */
/* Overlapping elements, unconventional alignment */
/* Visible grid, exposed structure */
```

---

## Step 9: Quality Checklist

Before delivering any graphic, verify:

- [ ] Colors match the design-context palette
- [ ] Typography uses specified fonts (loaded via Google Fonts if needed)
- [ ] Clear visual hierarchy -- eye knows where to look first
- [ ] Text is readable -- sufficient contrast ratio (4.5:1 minimum for body, 3:1 for large text)
- [ ] Proper spacing -- nothing feels cramped
- [ ] Dimensions match the requested size
- [ ] Code is self-contained -- no external dependencies except fonts
- [ ] Decorative elements enhance, not distract
- [ ] The design matches the intended style archetype
- [ ] All text content is accurate and spelled correctly

---

## Pro Tips

1. **Start with the background** -- get the mood right before adding content
2. **Use opacity** -- 0.05 to 0.15 opacity shapes create depth without distraction
3. **Layer gradients** -- multiple semi-transparent gradients create rich, unique backgrounds
4. **Constrain your palette** -- 3 colors maximum for most graphics, plus neutrals
5. **Size contrast** -- make the headline at least 3x larger than body text
6. **Whitespace is design** -- empty space is not wasted space, it is breathing room
7. **Test at actual size** -- open the HTML file and view at 100% to verify readability
8. **Use CSS custom properties** -- define colors once, reference everywhere for consistency
