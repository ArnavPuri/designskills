---
name: presentation-design
description: >
  Design slide decks as HTML/CSS (custom or reveal.js): slide layouts on a fixed
  16:9 canvas, presentation typography, slide charts, builds and transitions,
  speaker notes, and PDF export. Use for decks presented or shared from the browser;
  for native .pptx files use a PowerPoint-specific tool. Trigger phrases: "presentation",
  "slide deck", "slides", "pitch deck", "keynote", "reveal.js",
  "slide design", "presentation template", "speaker notes"
license: MIT
---

# Presentation Design

Create visually stunning slide decks using HTML and CSS.

## Prerequisites

- Read `.agents/design-context.md` (see `design-context`) for brand colors, heading/body fonts, and style archetype; map them to `--slide-*` variables (Step 9). Use the shared `--brand-*` / `--gray-*` scale from color-palette.
- Identify the audience, purpose, and length of the presentation, and whether it will be projected, screen-shared, or sent as a PDF.
- For photographic backgrounds or illustrations, generate them with the `image-generation` skill (`--aspect-ratio 16:9`) and keep text on a solid or overlaid area, not directly on busy image regions.

---

## Step 1: Slide Layout Templates

### Title Slide

```css
.slide-title {
  display: flex; align-items: center; justify-content: center;
  text-align: center; background: var(--brand-500); color: white;
}
.slide-title .slide-headline { font-size: 4rem; font-weight: 800; line-height: 1.05; letter-spacing: -0.03em; margin-bottom: 1rem; }
.slide-title .slide-subtitle { font-size: 1.5rem; opacity: 0.85; margin-bottom: 2rem; }
.slide-title .slide-meta { display: flex; gap: 2rem; font-size: 1rem; opacity: 0.7; }
```

### Content Slide (Text + Bullets)

```css
.slide-content-layout { display: flex; flex-direction: column; justify-content: center; padding: 4rem 6rem; }
.slide-heading { font-size: 2.5rem; font-weight: 700; margin-bottom: 2rem; color: var(--gray-900); }
.slide-bullets { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 1.25rem; }
.slide-bullets li { font-size: 1.5rem; line-height: 1.4; color: var(--gray-700); padding-left: 2rem; position: relative; }
.slide-bullets li::before { content: ''; position: absolute; left: 0; top: 0.55em; width: 8px; height: 8px; background: var(--brand-500); border-radius: 50%; }
```

### Two-Column Comparison

```css
.slide-columns { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; margin-top: 2rem; }
.slide-col h3 { font-size: 1.5rem; font-weight: 600; margin-bottom: 1rem; padding-bottom: 0.75rem; border-bottom: 3px solid var(--brand-500); }
```

### Quote Slide

```css
.slide-quote { display: grid; place-items: center; padding: 4rem 8rem; background: var(--gray-50); }
.slide-blockquote p { font-size: 2.5rem; font-weight: 500; font-style: italic; line-height: 1.3; text-align: center; margin-bottom: 1.5rem; }
.slide-blockquote cite { display: block; font-size: 1.125rem; font-style: normal; color: var(--brand-500); font-weight: 600; text-align: center; }
```

### Data/Stats Slide

```css
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3rem; margin-top: 3rem; text-align: center; }
.stat-number { display: block; font-size: 4rem; font-weight: 800; color: var(--brand-500); line-height: 1; margin-bottom: 0.5rem; }
.stat-label { font-size: 1.125rem; color: var(--gray-500); }
```

### Image + Text Slide

```css
.slide-image-text { display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
.slide-image-text .slide-image { background-size: cover; background-position: center; }
.slide-image-text .slide-text { display: flex; flex-direction: column; justify-content: center; padding: 4rem; }
```

---

## Step 2: Slide Container (Fixed 16:9 Canvas)

Design every slide on a fixed 1280x720 canvas and scale the whole canvas to the screen. All rem/px sizes in this skill assume that canvas, so type stays proportional on a laptop, a projector, or a PDF page.

```css
html, body { margin: 0; height: 100%; background: black; overflow: hidden; }
.deck { position: fixed; inset: 0; }
.slide {
  position: absolute; left: 50%; top: 50%; width: 1280px; height: 720px;
  transform: translate(-50%, -50%) scale(var(--deck-scale, 1));
  overflow: hidden; font-family: var(--font-body); background: var(--slide-bg, white);
}
.slide-content { padding: 4rem 6rem; } /* Safe margins: keep text out of the outer ~5% */
```

```js
const fit = () => document.documentElement.style.setProperty(
  '--deck-scale', Math.min(innerWidth / 1280, innerHeight / 720));
addEventListener('resize', fit); fit();
```

---

## Step 3: One Idea Per Slide

Each slide communicates exactly ONE concept. Structure:
1. **Headline**: The one takeaway (1 line, 6-8 words max)
2. **Support**: Visual or 3-4 bullet points reinforcing the headline
3. **Visual anchor**: An image, chart, icon, or number

Cut: paragraphs of text, more than 4-5 bullets, busy diagrams. Split or simplify.

---

## Step 4: Typography for Presentations

| Element   | Size          | Weight | Notes                        |
|-----------|---------------|--------|------------------------------|
| Headline  | 3-4.5rem      | 700-800| 1 line, max 2 lines         |
| Subhead   | 1.5-2rem      | 500    | Supporting context            |
| Body      | 1.25-1.5rem   | 400    | Bullets, descriptions         |
| Caption   | 1-1.125rem    | 400    | Attribution, fine print       |
| Stat      | 4-6rem        | 800    | Key metrics, big numbers     |

### Dark Background Contrast

```css
.slide-dark { background: var(--gray-900); color: var(--gray-50); }
.slide-dark .slide-heading { color: white; }
.slide-dark .slide-body { color: var(--gray-300); }
```

Use `font-display: block` for presentation fonts to avoid FOUT during live presentation.

---

## Step 5: Data Visualization for Slides

### CSS Bar Chart

```css
.chart-bars { display: flex; align-items: flex-end; gap: 2rem; height: 300px; padding-top: 2rem; margin-bottom: 2.5rem; /* room for .bar-label */ }
.bar { flex: 1; height: calc(var(--value) * 1%); background: var(--brand-500); border-radius: 0.5rem 0.5rem 0 0; position: relative; transition: height 0.6s var(--ease-out); }
.bar-value, .bar-label { position: absolute; left: 0; right: 0; text-align: center; }
.bar-value { top: -2rem; font-weight: 700; font-size: 1.25rem; }
.bar-label { bottom: -2rem; font-size: 1rem; color: var(--gray-600); }
```

```html
<div class="chart-bars" role="img" aria-label="Revenue by quarter: Q1 40%, Q2 55%, Q3 70%, Q4 90%">
  <div class="bar" style="--value: 40"><span class="bar-value">40%</span><span class="bar-label">Q1</span></div>
  <!-- ... -->
</div>
```

### CSS Donut Chart

```css
.donut { --pct: 65%; width: 200px; height: 200px; border-radius: 50%; background: conic-gradient(var(--brand-500) 0 var(--pct), var(--gray-200) var(--pct) 100%); display: grid; place-items: center; }
.donut-label { width: 140px; height: 140px; background: var(--slide-bg, white); border-radius: 50%; display: grid; place-items: center; font-size: 2rem; font-weight: 800; }
```

```html
<div class="donut" style="--pct: 65%" role="img" aria-label="65% of customers renewed"><span class="donut-label" aria-hidden="true">65%</span></div>
```

For anything beyond one or two series, use a real chart library (see the `dataviz` guidance if available) rather than CSS shapes.

### Rules for Slide Charts
1. Minimize gridlines and labels -- communicate a trend, not precise data
2. Highlight the key data point (larger, different color, label it)
3. Chart marks need 3:1 contrast against the slide background (WCAG 1.4.11); label values directly instead of relying on a color legend
4. Animate chart elements on slide entrance for impact

---

## Step 6: Transition and Build Animations

### Slide Transitions

```css
.slide { opacity: 0; transition: opacity 0.4s ease; }
.slide.is-active { opacity: 1; }
```

### Progressive Build (Bullet Reveal)

```css
.slide-bullets li { opacity: 0; transform: translateX(-20px); transition: opacity 0.3s var(--ease-out), transform 0.3s var(--ease-out); }
.slide-bullets li.is-revealed { opacity: 1; transform: translateX(0); }
```

### Number Count-Up

```css
@property --num { syntax: '<integer>'; initial-value: 0; inherits: false; }
.stat-countup { --target: 65; animation: count-up 2s var(--ease-out) forwards; counter-reset: num var(--num); }
.stat-countup::after { content: counter(num) '%'; }
@keyframes count-up { from { --num: 0; } to { --num: var(--target); } }
@media (prefers-reduced-motion: reduce) { .stat-countup { animation: none; --num: var(--target); } }
```

Keep the element empty (the number is generated) and give it `aria-label="65%"`, since screen readers may skip or announce every frame of generated content.

---

## Step 7: Speaker Notes

Put notes in an `<aside class="notes">` inside each slide -- the same markup reveal.js uses, so decks can move between the custom system and reveal.js.

```html
<section class="slide">
  <!-- slide content -->
  <aside class="notes">Explain the key metric here. Pause for questions.</aside>
</section>
```

```css
.notes { display: none; }
/* Press N (see Step 8 JS) to show notes as an overlay while rehearsing */
.show-notes .slide.is-active .notes {
  display: block; position: absolute; inset: auto 0 0 0; max-height: 35%; overflow: auto;
  padding: 1.5rem 2rem; background: oklch(0.2 0 0 / 0.92); color: white; font-size: 1.25rem; line-height: 1.5;
}
```

For a real presenter view on a second screen, use reveal.js (press `S`).

---

## Step 8: Slide Framework Setup

### Custom Slide System (No Framework)

Uses the Step 2 canvas; inactive slides are hidden with `inert` so their links aren't tabbable and screen readers only see the current slide.

```css
.slide { display: flex; opacity: 0; pointer-events: none; transition: opacity 0.4s ease; }
.slide.is-active { opacity: 1; pointer-events: auto; }
```

```js
let current = 0;
const slides = document.querySelectorAll('.slide');
function goTo(index) {
  current = Math.max(0, Math.min(index, slides.length - 1));
  slides.forEach((s, i) => { s.classList.toggle('is-active', i === current); s.inert = i !== current; });
  history.replaceState(null, '', '#' + (current + 1)); // deep-linkable
}
document.addEventListener('keydown', (e) => {
  if (['ArrowRight', 'PageDown', ' '].includes(e.key)) { e.preventDefault(); goTo(current + 1); }
  if (['ArrowLeft', 'PageUp'].includes(e.key)) goTo(current - 1);
  if (e.key.toLowerCase() === 'n') document.body.classList.toggle('show-notes');
});
goTo((parseInt(location.hash.slice(1), 10) || 1) - 1);
```

For Reveal.js, load from CDN and customize with CSS variables (`--r-heading-font`, `--r-main-color`, `--r-link-color`).

---

## Step 9: Brand-Consistent Templates

```css
.deck {
  --slide-bg: white; --slide-heading-color: var(--gray-900);
  --slide-text-color: var(--gray-600); --slide-accent: var(--brand-500);
  font-family: var(--font-body); /* design-context Body Font; headings use --font-heading */
}
.slide::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: var(--slide-accent); }
.slide-number { position: absolute; bottom: 1.5rem; right: 2rem; font-size: 0.875rem; color: var(--gray-500); font-variant-numeric: tabular-nums; }
.slide-logo { position: absolute; bottom: 1.5rem; left: 2rem; width: 80px; opacity: 0.3; }
```

---

## Step 10: Closing / CTA Slide

The last slide stays up longest during Q&A. Include:
1. A clear next step / CTA (URL, QR code)
2. Contact information
3. Optionally: key takeaway in one line

```css
.slide-closing { display: grid; place-items: center; text-align: center; background: var(--gray-900); color: white; }
.closing-headline { font-size: 4rem; font-weight: 800; margin-bottom: 2rem; }
.closing-link { font-size: 2rem; color: var(--brand-300); font-weight: 600; }
.closing-contact { font-size: 1.125rem; opacity: 0.6; display: flex; gap: 2rem; }
```

---

## Quick Reference

1. Use 16:9 aspect ratio with generous padding (4-6rem).
2. One idea per slide. Split complex slides.
3. Headlines: 3-4.5rem, max 8 words.
4. Body text: 1.25-1.5rem minimum (readable from back of room).
5. Use brand colors consistently. Max 3 colors per slide.
6. Animate builds progressively. Do not animate everything.
7. Data visualizations: simplify, highlight the key point.
8. Include speaker notes for every content slide.
9. Closing slide: CTA + contact. Keep it on screen during Q&A.
10. Test on a projector or large screen -- colors appear washed out.

## Verify and Export

1. **Screenshot every slide** at 1920x1080 with Playwright (loop over `#1…#N`, `page.goto(url + '#' + n)`, `page.screenshot({ path: 'slide-' + n + '.png' })`) and view each with Read. Check: no text overflowing or clipped by `overflow: hidden`, one idea per slide, headline readable at thumbnail size, consistent margins and slide-number position, brand colors correct.
2. **Contrast**: text on brand-color and image backgrounds must meet 4.5:1 (3:1 for ≥24px text); projectors lower contrast further, so aim higher.
3. **PDF**: for the custom system, add `@media print { .slide { position: relative; transform: none; left: 0; top: 0; break-after: page; opacity: 1; } }` and `@page { size: 1280px 720px; margin: 0; }`, then `page.pdf({ path: 'deck.pdf', preferCSSPageSize: true, printBackground: true })`. For reveal.js, open with `?print-pdf` first.
