---
name: dark-mode
description: >
  Dark theme design and implementation for web UIs: surface elevation, desaturated brand
  colors, text/border tokens, color-scheme, system-preference detection, a no-flash theme
  toggle, and Tailwind dark variants. Use when the user asks to "add dark mode", "create a
  dark theme", "dark mode support", "implement dark/light toggle", "theme switcher",
  "prefers-color-scheme", "design for dark background", "night mode", or any dark theme
  work. For dark mode in HTML email use email-design; for building the full color palette
  use color-palette.
license: MIT
---

# Dark Mode Design

## Before You Start: Load Design Context

1. **Read `.agents/design-context.md`** (written by the `design-context` skill). If it is missing, look for tokens in `tailwind.config.*` or `:root` CSS variables. If nothing exists, use the defaults (Primary `#2563EB`, Secondary `#7C3AED`, Accent `#F59E0B`, Tailwind gray neutrals, Inter for headings and body, Minimal style) and **tell the user defaults were used** — suggest running `design-context`.
2. **Map tokens to CSS variables once**, then use only the variables: `--color-primary`, `--color-primary-light`, `--color-primary-dark`, `--color-secondary`, `--color-accent`, `--color-neutral-50`…`--color-neutral-900`, `--color-success`/`-warning`/`-error`, `--font-heading`, `--font-body`, `--font-mono`, `--radius`, and the 4px-base spacing scale.
3. **Tailwind:** expose the same variables (v3 `theme.extend`, v4 `@theme`) as `primary`, `primary-light`, `primary-dark`, `secondary`, `accent`, `neutral-*`, `font-heading`, `font-body`. The `indigo-*` / `gray-*` classes in the examples below are placeholders for these tokens.
4. **Figma:** if the user gives a Figma URL, pull it with the Figma MCP (`get_design_context`, `get_screenshot`) and match it; it overrides the context file for that design.
5. The context colors are the **light** theme. Derive dark values from them (section 3: raise lightness, lower chroma) instead of inventing a new palette; ask whether this is dark-first or adding dark mode to an existing light UI.

---

## 1. Core Rule: Don't Just Invert

Inverting colors produces harsh, unreadable interfaces. Dark mode requires intentional design decisions.

### What Changes
| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Background | White (#fff) | Dark gray (NOT pure black) |
| Text | Near-black | Near-white (NOT pure white) |
| Borders | Gray-200 | White at 8–12% opacity |
| Shadows | Black at 5–15% | Nearly invisible or none |
| Primary color | Full saturation | Reduced saturation |
| Images | Full brightness | Slightly dimmed |
| Elevation | Shadows | Lighter surface color |

### Avoid
- Pure white `#fff` text on pure black `#000` (21:1 — causes halation/glare for many readers, especially with astigmatism).
- Pure black as the default background: it leaves no room to show elevation, and on OLED can cause smearing when scrolling. Reserve true black for an explicit "OLED/true black" option.
- The same shadow values from light mode — shadows barely show on dark surfaces.

---

## 2. Elevation Through Luminance

In light mode, elevation is shown with shadows. In dark mode, elevated surfaces are lighter.

### Surface Hierarchy
```css
:root {
  /* Light mode */
  --bg-base: oklch(100% 0 0);         /* white */
  --bg-surface: oklch(100% 0 0);      /* white */
  --bg-elevated: oklch(100% 0 0);     /* white + shadow */
  --bg-overlay: oklch(100% 0 0);      /* white + deeper shadow */
}

[data-theme="dark"] {
  /* Dark mode — each level gets progressively lighter */
  --bg-base: oklch(13% 0.01 265);     /* darkest: page background */
  --bg-surface: oklch(18% 0.01 265);  /* cards, sidebar */
  --bg-elevated: oklch(23% 0.01 265); /* dropdowns, popovers */
  --bg-overlay: oklch(28% 0.01 265);  /* modals, tooltips */
}
```

### Practical Example
```css
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border);
}
.dropdown {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
}
.modal {
  background: var(--bg-overlay);
}
```

### Material Design Overlay Model (M2)
Each elevation adds a white overlay on the `#121212` base:
- 0dp (base): 0% · 1dp (card): 5% · 4dp (app bar): 9%
- 8dp (menu): 12% · 16dp (nav drawer): 15% · 24dp (dialog): 16%

Material 3 replaces overlays with tonal `surface-container` roles (lowest → highest); the surface tokens above follow the same idea.

---

## 3. Color Saturation Rules

### Reduce Saturation for Dark Backgrounds
Bright, saturated colors on dark backgrounds cause visual vibration and eye strain.

```css
:root {
  --color-primary: oklch(60% 0.25 265);   /* Light mode: full saturation */
  --color-success: oklch(55% 0.20 155);
  --color-error: oklch(55% 0.22 25);
}

[data-theme="dark"] {
  --color-primary: oklch(72% 0.18 265);   /* Dark mode: lighter, less saturated */
  --color-success: oklch(70% 0.15 155);
  --color-error: oklch(70% 0.16 25);
}
```

### Rules
- Increase lightness by 10–15% for dark mode.
- Decrease chroma (saturation) by 15–25%.
- Backgrounds with color (e.g., badges) should use lower opacity.
- Re-check contrast after adjusting: a primary that passes on white often fails with white text in dark mode — use a lighter primary with **dark** text on filled buttons instead (see section 8).

```css
/* Light mode badge */
.badge-success {
  background: oklch(95% 0.05 155);
  color: oklch(35% 0.15 155);
}

/* Dark mode badge */
[data-theme="dark"] .badge-success {
  background: oklch(35% 0.08 155);
  color: oklch(80% 0.12 155);
}
```

---

## 4. Text Contrast Levels

### White-on-Dark Opacity Scale
Use white at different opacities for text hierarchy on dark backgrounds.

| Role | Opacity | Use Case |
|------|---------|----------|
| High emphasis | 87–90% (`oklch(100% 0 0 / 0.87)`) | Headings, primary text |
| Medium emphasis | 60–70% (`oklch(100% 0 0 / 0.70)`) | Body text, secondary, muted |
| Disabled only | 38% (`oklch(100% 0 0 / 0.38)`) | Disabled controls (exempt from contrast rules) |

Anything a user must read — including muted captions and placeholders that carry information — needs **4.5:1** against its surface. Below ~55% white fails on typical dark surfaces.

### Implementation
Use the `--text-primary` / `--text-secondary` / `--text-muted` tokens from the Complete Token System below (`--text-muted` at 62% lightness is the lowest that keeps 4.5:1 on the base and surface colors).

### Tailwind Approach
```html
<!-- High emphasis -->
<h1 class="text-white/90">Main Heading</h1>

<!-- Medium emphasis -->
<p class="text-white/70">Body text content here.</p>

<!-- Low emphasis (not below /60 — /40 fails 4.5:1) -->
<span class="text-white/60">Last updated 2 hours ago</span>
```

---

## 5. Border & Divider Treatment

### Light Borders on Dark
Borders in dark mode should use semi-transparent white, not gray values.

```css
[data-theme="dark"] {
  --border: oklch(100% 0 0 / 0.08);       /* subtle */
  --border-strong: oklch(100% 0 0 / 0.15); /* emphasized */
  --divider: oklch(100% 0 0 / 0.06);       /* section dividers */
}
```

This ensures borders adapt correctly regardless of the underlying surface color. Decorative dividers can be this faint, but **input and control borders need 3:1** against the surface (WCAG 1.4.11) — use `oklch(100% 0 0 / 0.3)` or stronger for form fields.

---

## 6. Image Handling in Dark Mode

### Reduce Image Brightness
```css
[data-theme="dark"] img:not([data-no-dim]) {
  filter: brightness(0.85);
}

/* Restore on hover for galleries */
[data-theme="dark"] img:hover {
  filter: brightness(1);
}
```

### Dark Overlay for Hero Images
```html
<div class="relative">
  <img src="/hero.jpg" alt="" class="w-full" />
  <div class="absolute inset-0 bg-gray-950/30 dark:bg-gray-950/50"></div>
</div>
```

### SVG Icon Adaptation
Icons should use `currentColor` so they inherit text color automatically:
```html
<svg class="w-5 h-5 text-gray-600 dark:text-gray-400" fill="currentColor">
  <!-- icon paths -->
</svg>
```

### Logo Handling
Provide separate logos for light and dark modes:
```html
<img src="/logo-dark.svg" alt="Logo" class="dark:hidden" />
<img src="/logo-light.svg" alt="Logo" class="hidden dark:block" />
```

---

## 7. CSS Implementation

### Always: the `color-scheme` Property
Tells the browser to render native controls, scrollbars, form fields, and the default canvas in the right theme — without it, `<select>`s and scrollbars stay light in dark mode.
```css
:root { color-scheme: light dark; }           /* follow the system */
:root[data-theme="light"] { color-scheme: light; }
:root[data-theme="dark"]  { color-scheme: dark; }
```
Also add `<meta name="color-scheme" content="light dark">` in `<head>` so the page background is right before CSS loads.

### Method 1: `prefers-color-scheme` (System Preference)
```css
:root {
  --bg: oklch(100% 0 0);
  --text: oklch(15% 0 0);
  --surface: oklch(100% 0 0);
  --border: oklch(90% 0 0);
}

@media (prefers-color-scheme: dark) {
  /* :not() lets a manual "light" choice (Method 2) override the system */
  :root:not([data-theme="light"]) {
    --bg: oklch(13% 0.01 265);
    --text: oklch(95% 0 0);
    --surface: oklch(18% 0.01 265);
    --border: oklch(100% 0 0 / 0.08);
  }
}
```

### Method 2: CSS Custom Properties + Class Toggle (User Preference)
```css
:root {
  --bg: oklch(100% 0 0);
  --text: oklch(15% 0 0);
}

[data-theme="dark"] {
  --bg: oklch(13% 0.01 265);
  --text: oklch(95% 0 0);
}

body {
  background: var(--bg);
  color: var(--text);
}
```

```javascript
// Toggle implementation — keeps data-theme, the Tailwind `dark` class, and the button state in sync
function applyTheme(theme) {
  const root = document.documentElement;
  root.setAttribute('data-theme', theme);
  root.classList.toggle('dark', theme === 'dark');
  document.querySelectorAll('[data-theme-toggle]')
    .forEach((btn) => btn.setAttribute('aria-pressed', String(theme === 'dark')));
}
function toggleTheme() {
  const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  try { localStorage.setItem('theme', next); } catch (e) { /* storage blocked: session-only */ }
}
// Follow system changes until the user makes an explicit choice
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
  let saved = null;
  try { saved = localStorage.getItem('theme'); } catch (e) {}
  if (!saved) applyTheme(e.matches ? 'dark' : 'light');
});
```
Initial theme is set by the inline `<head>` script below, not by a function that runs after load. Consider a three-way control (Light / Dark / System) — "System" clears the saved value.

### Method 3: Tailwind `dark:` Variant
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100
  border-gray-200 dark:border-white/10">
  <h2 class="text-gray-950 dark:text-white">Title</h2>
  <p class="text-gray-600 dark:text-gray-400">Description</p>
</div>
```

Tailwind config for class-based dark mode:
```javascript
// tailwind.config.js (v3.4.1+)
module.exports = {
  darkMode: 'selector',                          // `.dark` on <html>
  // darkMode: ['selector', '[data-theme="dark"]'], // or drive it from data-theme
}
```
```css
/* Tailwind v4: in your main CSS file */
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));
```

### Prevent Flash of Wrong Theme (FOUC)
Add this **inline, blocking** script in `<head>` before any stylesheet (not `defer`/`async`, not a bundled module — those run after first paint):
```html
<script>
  (function () {
    var theme = null;
    try { theme = localStorage.getItem('theme'); } catch (e) {}
    if (!theme) theme = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    var root = document.documentElement;
    root.setAttribute('data-theme', theme);
    root.classList.toggle('dark', theme === 'dark');
  })();
</script>
```
With SSR frameworks (Next.js etc.), add `suppressHydrationWarning` to `<html>` since the attribute differs from the server render.

---

## 8. Component-Specific Dark Mode Patterns

### Input Fields
```html
<input class="bg-white border-gray-300 text-gray-900 placeholder:text-gray-400
  focus:border-indigo-500 focus:ring-indigo-500/20
  dark:bg-white/5 dark:border-white/30 dark:text-gray-100 dark:placeholder:text-gray-400
  dark:focus:border-indigo-400 dark:focus:ring-indigo-400/20" />
```

### Cards
```html
<div class="bg-white border border-gray-200 shadow-sm
  dark:bg-white/5 dark:border-white/10 dark:shadow-none">
```

### Buttons
```html
<!-- Primary: stays bold in both modes -->
<!-- In dark, a lighter primary with dark text keeps 4.5:1 (white on indigo-500 is only ~4.4:1) -->
<button class="bg-indigo-600 text-white hover:bg-indigo-500
  dark:bg-indigo-400 dark:text-indigo-950 dark:hover:bg-indigo-300">
  Primary
</button>

<!-- Secondary: adapts background -->
<button class="bg-gray-100 text-gray-700 hover:bg-gray-200
  dark:bg-white/10 dark:text-gray-200 dark:hover:bg-white/15">
  Secondary
</button>
```

### Dropdowns / Popovers
```html
<div class="bg-white border border-gray-200 shadow-lg rounded-xl
  dark:bg-gray-800 dark:border-white/10 dark:shadow-2xl dark:shadow-black/20">
```

### Tables
```html
<tr class="border-b border-gray-100 hover:bg-gray-50
  dark:border-white/5 dark:hover:bg-white/5">
```

---

## 9. Smooth Mode Transition

### CSS Transition Between Modes
Don't put a permanent `* { transition: … }` rule in your CSS — it overrides every component's own transitions (button transforms, sheet slides) and animates colors on first paint. Apply a temporary class only while switching:
```css
@media (prefers-reduced-motion: no-preference) {
  .theme-transition,
  .theme-transition *,
  .theme-transition *::before,
  .theme-transition *::after {
    transition: background-color 200ms ease, border-color 200ms ease,
      color 200ms ease, fill 200ms ease, stroke 200ms ease !important;
  }
}
```
```javascript
// In toggleTheme(), wrap the switch:
const root = document.documentElement;
root.classList.add('theme-transition');
applyTheme(next);
setTimeout(() => root.classList.remove('theme-transition'), 250);
```
Alternative: `document.startViewTransition(() => applyTheme(next))` where supported, for a cross-fade.

### Toggle Button UI
```html
<!-- aria-pressed is kept in sync by applyTheme(); the name stays constant -->
<button type="button" data-theme-toggle aria-pressed="false" aria-label="Dark mode"
  onclick="toggleTheme()" class="relative w-14 h-7 rounded-full
  bg-gray-500 dark:bg-indigo-500 transition-colors
  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500">
  <span class="absolute top-0.5 left-0.5 w-6 h-6 rounded-full bg-white shadow
    motion-safe:transition-transform dark:translate-x-7 flex items-center justify-center">
    <!-- Sun icon (light mode) -->
    <svg class="w-4 h-4 text-amber-500 dark:hidden" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
      <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/>
    </svg>
    <!-- Moon icon (dark mode) -->
    <svg class="w-4 h-4 text-indigo-500 hidden dark:block" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true">
      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
    </svg>
  </span>
</button>
```

---

## Complete Token System

### Recommended Dark Mode Palette
Shared by all UI skills (dashboard-design reuses these). Derive `--color-primary` and status colors from the design-context values per section 3; the oklch values below are the defaults for Primary `#2563EB`.
```css
[data-theme="dark"] {
  color-scheme: dark;

  /* Surfaces */
  --bg-base: oklch(13% 0.01 265);
  --bg-surface: oklch(18% 0.01 265);
  --bg-elevated: oklch(23% 0.01 265);
  --bg-overlay: oklch(28% 0.01 265);

  /* Text */
  --text-primary: oklch(95% 0 0);
  --text-secondary: oklch(75% 0 0);
  --text-muted: oklch(62% 0 0);        /* ≥ 4.5:1 on base and surface */

  /* Borders */
  --border: oklch(100% 0 0 / 0.08);     /* decorative dividers */
  --border-strong: oklch(100% 0 0 / 0.15);
  --border-input: oklch(100% 0 0 / 0.30); /* form controls: ≥ 3:1 */

  /* Interactive */
  --color-primary: oklch(72% 0.18 265);
  --color-primary-hover: oklch(78% 0.16 265);

  /* Status */
  --color-success: oklch(70% 0.15 155);
  --color-warning: oklch(75% 0.15 80);
  --color-error: oklch(70% 0.16 25);
  --color-info: oklch(72% 0.15 230);
}
```

---

## Verify: Render and Check

Don't hand over code you haven't looked at. After generating it:
1. Screenshot it at mobile and desktop widths, e.g. `npx playwright screenshot --full-page --viewport-size=390,844 file://$PWD/index.html mobile.png`, then again with `--viewport-size=1440,900` (or point at the dev server URL).
2. Open both images and check: no horizontal scroll or clipped/overlapping text, hierarchy reads at a glance, brand tokens are applied, images load at the right aspect ratio.
3. Tab through once: every interactive element gets a visible focus ring, in a logical order.
4. Screenshot **both** themes (Playwright `--color-scheme=dark` / `light`), reload in dark mode to confirm there is no flash of the light theme, and contrast-check muted text and borders in dark.
5. Fix what you find and re-screenshot before reporting done.

---

## Dark Mode Checklist

- [ ] Background is dark gray, text is off-white (no pure #fff on pure #000)
- [ ] `color-scheme` is set (CSS property + meta tag) so native controls match
- [ ] Elevation uses lighter surfaces, not shadows
- [ ] Primary colors are desaturated and lightened
- [ ] Borders use semi-transparent white
- [ ] Images are slightly dimmed
- [ ] Logos have light variants
- [ ] No flash of the wrong theme on load (inline blocking `<head>` script)
- [ ] System preference is detected and respected
- [ ] User preference is persisted in localStorage
- [ ] Theme transition is temporary (not a global `*` rule) and skipped under reduced motion
- [ ] Contrast still meets WCAG AA in dark: 4.5:1 text (including muted), 3:1 input borders, icons, and focus rings
- [ ] Toggle is a real `<button>` with an accessible name and `aria-pressed`
- [ ] Both themes rendered and screenshotted (see Verify)
