---
name: ui-design
description: >
  Core UI design patterns and component architecture for building polished interfaces.
  Trigger: user asks to "design a UI", "build a component", "create an interface",
  "style a form", "make it look good", "improve the design", "add hover states",
  "make it accessible", or requests any general UI/UX design work.
license: MIT
---

# UI Design Patterns

## Pre-Flight: Check Design Context

Before generating any UI code, check if the user has an active Figma file or design system context:
1. Use `get_design_context` to retrieve any existing design tokens, color palettes, or component specs.
2. If a Figma URL is provided, pull metadata and screenshots to match the design precisely.
3. If no design context exists, proceed with the opinionated defaults below.

---

## 1. Component Design Principles (Atomic Design)

Build UI in layers. Never start with a full page — start with the smallest pieces.

### Hierarchy
1. **Tokens** — colors, spacing, radii, shadows, typography scale
2. **Atoms** — button, input, badge, avatar, icon
3. **Molecules** — search bar (input + button), form field (label + input + error), card header (avatar + name + timestamp)
4. **Organisms** — navigation bar, hero section, comment thread, pricing table
5. **Templates** — page layouts composed of organisms
6. **Pages** — templates with real data

### Rules
- Every component gets its own set of CSS custom properties scoped to its root.
- Prefer composition over configuration. A `Card` with `children` beats a `Card` with 15 props.
- Components should be stateless by default. Lift state up.

```css
/* Token layer */
:root {
  --color-primary: oklch(65% 0.25 265);
  --color-surface: oklch(98% 0.005 265);
  --radius-md: 0.75rem;
  --shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.05);
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
}
```

---

## 2. Visual Hierarchy Framework

Control where the eye goes. Rank every element by importance and apply these levers:

| Lever | High Emphasis | Medium Emphasis | Low Emphasis |
|-------|--------------|-----------------|--------------|
| **Size** | 2rem+ heading | 1rem body | 0.75rem caption |
| **Weight** | 700–800 bold | 500 medium | 400 regular |
| **Color** | Primary or high-contrast text | Muted text (60% opacity) | Subtle text (40% opacity) |
| **Spacing** | More whitespace around it | Standard spacing | Tighter spacing |
| **Position** | Top-left or center | Mid-page | Bottom or sidebar |

### The Squint Test
Blur your eyes or zoom out to 25%. If you can still identify the primary action and main heading, your hierarchy works.

### Tailwind Implementation
```html
<!-- High emphasis -->
<h1 class="text-4xl font-extrabold tracking-tight text-gray-950">
  Ship faster with AI
</h1>

<!-- Medium emphasis -->
<p class="mt-4 text-lg text-gray-600 max-w-2xl">
  Build production-ready components in minutes, not hours.
</p>

<!-- Low emphasis -->
<span class="text-xs text-gray-400 uppercase tracking-wide">
  Updated 2 hours ago
</span>
```

---

## 3. Interactive States

Every interactive element needs all five states. No exceptions.

### State Definitions
```css
.btn-primary {
  /* Default */
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-4);
  font-weight: 600;
  transition: all 150ms ease;

  /* Hover — subtle lift or brightness shift */
  &:hover {
    filter: brightness(1.1);
    box-shadow: 0 4px 12px oklch(0% 0 0 / 0.15);
    transform: translateY(-1px);
  }

  /* Active — pressed feel */
  &:active {
    transform: translateY(0);
    filter: brightness(0.95);
    box-shadow: var(--shadow-sm);
  }

  /* Focus — visible ring for keyboard users */
  &:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
  }

  /* Disabled — desaturated, no pointer */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }
}
```

### Tailwind Shorthand
```html
<button class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-semibold
  hover:bg-indigo-500 hover:-translate-y-0.5 hover:shadow-lg
  active:translate-y-0 active:bg-indigo-700
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600
  disabled:opacity-50 disabled:cursor-not-allowed
  transition-all duration-150">
  Click me
</button>
```

---

## 4. Feedback Patterns

### Loading States
- **Skeleton screens** over spinners. Show the shape of content that's coming.
- Use `animate-pulse` on placeholder blocks.
- Show loading inline near the action that triggered it.

```html
<!-- Skeleton card -->
<div class="animate-pulse space-y-3">
  <div class="h-48 bg-gray-200 rounded-xl"></div>
  <div class="h-4 bg-gray-200 rounded w-3/4"></div>
  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
</div>
```

### Success State
- Green accent, checkmark icon, brief confirmation text.
- Auto-dismiss after 3–5 seconds.

### Error State
- Red accent, descriptive message, recovery action.
- Never just say "Error." Say what went wrong and what to do.

### Empty State
- Illustration or icon, explanation, primary action to fix it.
```html
<div class="text-center py-16">
  <svg class="mx-auto h-12 w-12 text-gray-400"><!-- inbox icon --></svg>
  <h3 class="mt-4 text-lg font-semibold text-gray-900">No messages yet</h3>
  <p class="mt-2 text-sm text-gray-500">Start a conversation to see messages here.</p>
  <button class="mt-6 bg-indigo-600 text-white px-4 py-2 rounded-lg">
    New message
  </button>
</div>
```

---

## 5. Navigation Patterns

### Sidebar Navigation
- Width: 240–280px desktop, collapsible to 64px (icon-only).
- Group items by category with subtle section headers.
- Active item: filled background, bold text, left accent bar.

### Top Navigation
- Fixed/sticky at top. Height: 56–64px.
- Logo left, nav links center or left, actions right.
- Mobile: collapse to hamburger at `md` breakpoint.

### Tabs
- Use for switching views within the same context.
- Active tab: bottom border (2–3px) in primary color + bold text.
- Never more than 7 tabs. Use dropdown overflow for more.

### Breadcrumbs
- Use `/` or `>` separator.
- Current page is not a link, just text.
- Truncate middle items on long paths.

---

## 6. Form Design

### Rules
1. **Labels above inputs** — not floating, not inline. Always visible.
2. **One column** — multi-column forms reduce completion rate.
3. **Group related fields** with subtle section dividers.
4. **Inline validation** — validate on blur, not on every keystroke.
5. **Error messages below the field**, in red, with specific guidance.
6. **Primary action left-aligned** at form bottom. Secondary action as text link.

```html
<div class="space-y-1.5">
  <label for="email" class="block text-sm font-medium text-gray-700">
    Email address
  </label>
  <input
    type="email"
    id="email"
    class="block w-full rounded-lg border border-gray-300 px-3 py-2
      text-gray-900 placeholder:text-gray-400
      focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20
      transition-colors"
    placeholder="you@example.com"
  />
  <p class="text-sm text-red-600 hidden">Please enter a valid email address.</p>
</div>
```

---

## 7. Accessibility as Design

Accessibility is not an afterthought. It is a design constraint applied from the start.

### Contrast
- **Normal text**: 4.5:1 minimum contrast ratio (WCAG AA).
- **Large text** (18px+ or 14px+ bold): 3:1 minimum.
- **Interactive elements**: 3:1 against adjacent colors.
- Use oklch color space for perceptually uniform contrast adjustments.

### Focus Indicators
- Never remove `outline` without replacing it.
- Use `focus-visible` (not `focus`) to avoid showing rings on mouse click.
- Ring: 2px solid, offset 2px, primary color.

### Semantic Structure
- One `<h1>` per page.
- Headings in order (`h1` > `h2` > `h3`). Never skip levels.
- Use `<nav>`, `<main>`, `<aside>`, `<footer>` landmarks.
- Buttons for actions, links for navigation. Never `<div onclick>`.
- `aria-label` on icon-only buttons.

### Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 8. Responsive Breakpoint Strategy

### Breakpoints (Tailwind defaults)
| Name | Width | Target |
|------|-------|--------|
| `sm` | 640px | Large phones landscape |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large screens |

### Mobile-First Rules
- Start with the mobile layout. Add complexity at larger breakpoints.
- Stack columns on mobile, side-by-side on `md`+.
- Navigation becomes hamburger below `md`.
- Font sizes scale up: `text-2xl md:text-4xl lg:text-5xl`.
- Generous touch padding on mobile: `p-4`, tighten on desktop: `lg:p-2`.

### Container Queries (Modern CSS)
```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}
```

---

## 9. Modern UI Trends

### Glassmorphism
```css
.glass {
  background: oklch(100% 0 0 / 0.1);
  backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid oklch(100% 0 0 / 0.15);
  border-radius: 1rem;
}
```

### Bento Grid
```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: 1rem;
}
.bento .featured {
  grid-column: span 2;
  grid-row: span 2;
}
```

### Aurora / Mesh Gradient Background
```css
.aurora {
  background: linear-gradient(135deg, oklch(85% 0.15 280), oklch(80% 0.2 320), oklch(75% 0.18 200));
  background-size: 400% 400%;
  animation: aurora-shift 8s ease infinite;
}
@keyframes aurora-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

---

## 10. Advanced CSS Techniques

### `:has()` — Parent Selector
```css
/* Highlight form group when input is focused */
.form-group:has(input:focus) {
  background: oklch(97% 0.01 265);
  border-color: var(--color-primary);
}

/* Card changes layout when it contains an image */
.card:has(img) {
  grid-template-rows: 200px 1fr;
}
```

### Subgrid
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* header, body, footer align across cards */
}
```

### Scroll-Driven Animations
```css
.fade-in {
  animation: fade-in linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}
@keyframes fade-in {
  from { opacity: 0; transform: translateY(2rem); }
  to { opacity: 1; transform: translateY(0); }
}
```

---

## Quick Reference: Design Checklist

Before shipping any UI component, verify:

- [ ] Visual hierarchy is clear (squint test passes)
- [ ] All interactive elements have hover, active, focus-visible, and disabled states
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Focus order is logical (tab through the page)
- [ ] Responsive at all breakpoints (320px to 1920px)
- [ ] Loading, empty, and error states are designed
- [ ] Spacing is consistent (using a 4px/8px grid)
- [ ] Typography scale is limited to 4–6 sizes
- [ ] Motion respects `prefers-reduced-motion`
- [ ] Semantic HTML is used (landmarks, headings, button vs. link)
