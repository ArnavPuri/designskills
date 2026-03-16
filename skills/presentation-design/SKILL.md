---
name: presentation-design
description: >
  Design slide decks and presentations with HTML/CSS: layouts, typography,
  data visualization, and transitions. Trigger phrases: "presentation",
  "slide deck", "slides", "pitch deck", "keynote", "reveal.js",
  "slide design", "presentation template", "speaker notes"
license: MIT
---

# Presentation Design

Create visually stunning slide decks using HTML and CSS.

## Prerequisites

- Read any design-context files for brand colors, fonts, or presentation templates.
- Identify the audience, purpose, and length of the presentation.

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

## Step 2: Slide Container (16:9)

```css
.slide {
  width: 100%; aspect-ratio: 16 / 9; max-width: 1280px; max-height: 720px;
  overflow: hidden; position: relative; font-family: var(--font-body);
}
.presentation { width: 100vw; height: 100vh; display: flex; align-items: center; justify-content: center; background: black; }
.presentation .slide { width: 100vw; height: 56.25vw; max-height: 100vh; max-width: 177.78vh; }
.slide-content { padding: 4rem 6rem; } /* Safe margins */
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
.chart-bars { display: flex; align-items: flex-end; gap: 2rem; height: 300px; padding-top: 2rem; }
.bar { flex: 1; height: calc(var(--value) * 1%); background: var(--brand-500); border-radius: 0.5rem 0.5rem 0 0; position: relative; transition: height 0.6s var(--ease-out); }
.bar-value { position: absolute; top: -2rem; font-weight: 700; font-size: 1.25rem; }
.bar-label { position: absolute; bottom: -2rem; font-size: 1rem; color: var(--gray-500); }
```

### CSS Donut Chart

```css
.donut { width: 200px; height: 200px; border-radius: 50%; background: conic-gradient(var(--brand-500) 0% 65%, var(--gray-200) 65% 100%); display: grid; place-items: center; }
.donut::after { content: '65%'; width: 140px; height: 140px; background: white; border-radius: 50%; display: grid; place-items: center; font-size: 2rem; font-weight: 800; }
```

### Rules for Slide Charts
1. Minimize gridlines and labels -- communicate a trend, not precise data
2. Highlight the key data point (larger, different color, label it)
3. Animate chart elements on slide entrance for impact

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
.stat-number { animation: count-up 2s var(--ease-out) forwards; counter-reset: num var(--num); }
.stat-number::after { content: counter(num) '%'; }
@keyframes count-up { from { --num: 0; } to { --num: 65; } }
```

---

## Step 7: Speaker Notes

```html
<section class="slide" data-notes="Explain the key metric here."><!-- slide content --></section>
```

```css
.speaker-notes { display: none; }
@media print, screen and (min-width: 1800px) {
  .presentation-wrapper { display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; }
  .speaker-notes { display: block; padding: 2rem; font-size: 1.125rem; line-height: 1.6; border-left: 3px solid var(--brand-500); }
}
```

---

## Step 8: Slide Framework Setup

### Custom Slide System (No Framework)

```css
.deck { width: 100vw; height: 100vh; overflow: hidden; position: relative; }
.slide { position: absolute; inset: 0; display: flex; opacity: 0; pointer-events: none; transition: opacity 0.4s ease; }
.slide.is-active { opacity: 1; pointer-events: auto; }
```

```js
let current = 0;
const slides = document.querySelectorAll('.slide');
function goTo(index) {
  slides[current].classList.remove('is-active');
  current = Math.max(0, Math.min(index, slides.length - 1));
  slides[current].classList.add('is-active');
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ') goTo(current + 1);
  if (e.key === 'ArrowLeft') goTo(current - 1);
});
goTo(0);
```

For Reveal.js, load from CDN and customize with CSS variables (`--r-heading-font`, `--r-main-color`, `--r-link-color`).

---

## Step 9: Brand-Consistent Templates

```css
.deck {
  --slide-bg: white; --slide-heading-color: var(--gray-900);
  --slide-text-color: var(--gray-600); --slide-accent: var(--brand-500);
  font-family: var(--slide-font);
}
.slide::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: var(--slide-accent); }
.slide-number { position: absolute; bottom: 1.5rem; right: 2rem; font-size: 0.875rem; color: var(--gray-400); font-variant-numeric: tabular-nums; }
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
