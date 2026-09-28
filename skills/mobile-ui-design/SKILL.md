---
name: mobile-ui-design
description: >
  Touch-first mobile UI for native-feeling web apps, PWAs, and React Native/Flutter screens:
  touch targets, bottom navigation, gestures, safe areas, thumb zones, sheets, mobile forms,
  and motion. Use when the user asks to "design for mobile", "build a mobile UI", "make it
  mobile-friendly", "create a mobile app", "build a responsive mobile layout", "design a
  bottom sheet", "mobile navigation", "iOS/Android style", or any mobile-specific work. For
  general responsive rules on desktop-first sites use ui-design; for app-store screenshots
  or device mockups use product-mockup.
license: MIT
---

# Mobile UI Design

## Before You Start: Load Design Context

1. **Read `.agents/design-context.md`** (written by the `design-context` skill). If it is missing, look for tokens in `tailwind.config.*` or `:root` CSS variables. If nothing exists, use the defaults (Primary `#2563EB`, Secondary `#7C3AED`, Accent `#F59E0B`, Tailwind gray neutrals, Inter for headings and body, Minimal style) and **tell the user defaults were used** — suggest running `design-context`.
2. **Map tokens to CSS variables once**, then use only the variables: `--color-primary`, `--color-primary-light`, `--color-primary-dark`, `--color-secondary`, `--color-accent`, `--color-neutral-50`…`--color-neutral-900`, `--color-success`/`-warning`/`-error`, `--font-heading`, `--font-body`, `--font-mono`, `--radius`, and the 4px-base spacing scale.
3. **Tailwind:** expose the same variables (v3 `theme.extend`, v4 `@theme`) as `primary`, `primary-light`, `primary-dark`, `secondary`, `accent`, `neutral-*`, `font-heading`, `font-body`. The `indigo-*` / `gray-*` classes in the examples below are placeholders for these tokens.
4. **Figma:** if the user gives a Figma URL, pull it with the Figma MCP (`get_design_context`, `get_screenshot`) and match it; it overrides the context file for that design.
5. Ask whether this is a native app (React Native/Flutter: map tokens into the theme object instead of CSS variables), a PWA, or a responsive website.

---

## 1. Touch Target Sizes

Every interactive element must be large enough to tap reliably.

### Minimum Sizes
| Source | Minimum Target | Notes |
|--------|---------------|-------|
| Apple HIG | 44×44pt | = 44×44 CSS px on the web |
| Material Design | 48×48dp | ≈ 48×48 CSS px; visual icon can be 24dp |
| WCAG 2.2 SC 2.5.8 (AA) | 24×24 CSS px | Legal floor, not a design target |
| WCAG 2.2 SC 2.5.5 (AAA) | 44×44 CSS px | |

**Rule for this skill:** 44×44px minimum for every touch target (48×48 on Android-styled UIs).

### Implementation
```css
/* Ensure tap targets even on small visual elements */
.icon-button {
  width: 24px;
  height: 24px;
  /* Expand tap target with padding or pseudo-element */
  position: relative;
}
.icon-button::after {
  content: '';
  position: absolute;
  inset: -12px; /* extends tap area to 48x48 */
}
```

### Spacing Between Targets
Minimum 8px gap between tappable elements. 12px+ is preferred. This prevents accidental taps.

---

## 2. Bottom Navigation

The thumb reaches the bottom of the screen most easily. Put primary navigation there.

### Standard Bottom Tab Bar
```html
<nav aria-label="Main" class="fixed bottom-0 inset-x-0 bg-white border-t border-gray-200
  safe-area-bottom z-50">
  <div class="flex items-center justify-around h-16">
    <!-- Active tab -->
    <a href="#" aria-current="page" class="flex flex-col items-center justify-center gap-0.5
      text-indigo-600 min-w-[64px] min-h-[48px]">
      <svg class="w-6 h-6" fill="currentColor" aria-hidden="true"><!-- home icon --></svg>
      <span class="text-xs font-medium">Home</span>
    </a>
    <!-- Inactive tab (gray-500, not gray-400: labels need 4.5:1) -->
    <a href="#" class="flex flex-col items-center justify-center gap-0.5
      text-gray-500 min-w-[64px] min-h-[48px]">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" aria-hidden="true"><!-- search icon --></svg>
      <span class="text-xs font-medium">Search</span>
    </a>
    <!-- ... 3-5 tabs total -->
  </div>
</nav>
```

### Rules
- Maximum 5 tabs. 3–4 is ideal.
- Active tab: filled icon + primary color. Inactive: outline icon + gray.
- Labels are required. Icon-only tabs have poor discoverability.
- Never use a hamburger menu as a tab bar replacement.
- Account for bottom safe area on notched devices.

### Safe Area CSS
```css
/* Only for elements with no bottom padding of their own */
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
/* Elements that already have padding: ADD the inset, don't replace the padding */
.pb-safe-4 {
  padding-bottom: calc(1rem + env(safe-area-inset-bottom));
}
```
Also pad the scrolling content (e.g. `pb-[calc(4rem+env(safe-area-inset-bottom))]` on `<main>`) so the last item isn't hidden behind the tab bar.

---

## 3. Gesture-Friendly Interactions

### Swipe Actions
```html
<!-- Swipe-to-reveal pattern (conceptual structure) -->
<div class="relative overflow-hidden">
  <!-- Background action (revealed on swipe). A real button, also reachable without swiping -->
  <div class="absolute inset-y-0 right-0 flex items-center bg-red-600 px-6">
    <button type="button" class="text-white font-medium">Delete</button>
  </div>
  <!-- Foreground content (swipeable) -->
  <div class="bg-white px-4 py-3 transform transition-transform touch-pan-y">
    <div class="font-medium text-gray-900">List Item</div>
    <div class="text-sm text-gray-500">Swipe left for actions</div>
  </div>
</div>
```

### Pull-to-Refresh
- Indicator appears at top as user pulls down.
- Use a spinner or custom animation.
- Trigger refresh at ~80px pull distance.
- Provide haptic feedback if possible (native only).
- On the web, set `overscroll-behavior-y: contain` on the scroller so the browser's own pull-to-refresh doesn't fire too.

### Common Mobile Gestures
| Gesture | Use Case | Implementation |
|---------|----------|---------------|
| Swipe left/right | Reveal actions, navigate | `touch-action: pan-y` |
| Pull down | Refresh content | Overscroll detection |
| Long press | Context menu, reorder | `pointerdown` + ~500ms timeout, cancel on `pointermove`/`pointerup` |
| Pinch | Zoom images/maps | `touch-action: none` on the zoomable element + Pointer Events |
| Swipe up | Dismiss sheet, expand | Drag handle on bottom sheet |

`touch-action: manipulation` on buttons and links removes double-tap-zoom delay; it does *not* enable custom pinch handling. **Every gesture needs a visible single-tap alternative** (button, menu item) — WCAG 2.5.1 and discoverability both require it.

---

## 4. iOS vs Android Design Language

### Key Differences
| Element | iOS (Human Interface) | Android (Material) |
|---------|----------------------|-------------------|
| Navigation | Tab bar at bottom | Bottom navigation bar |
| Back | Swipe from left edge / text "Back" | Arrow icon top-left |
| Titles | Large title that collapses | Centered or left-aligned |
| Buttons | Rounded rect, no elevation | Rounded, with elevation |
| Switches | Green/white toggle | Track + thumb with ripple |
| Sheets | Rounded top, drag handle | Full-width, drag handle |
| Typography | SF Pro (system) | Roboto (system) |
| Spacing | 16px margins | 16px margins |

### Cross-Platform Approach
When building for both, lean toward iOS patterns for polish and Material patterns for interaction feedback. Use system fonts:

```css
/* Use the design-context body font if set; otherwise the platform font */
font-family: var(--font-body, system-ui), -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

---

## 5. Safe Areas

### Device Considerations
```css
/* Status bar area */
.top-safe {
  padding-top: env(safe-area-inset-top);
}

/* Home indicator / gesture bar */
.bottom-safe {
  padding-bottom: env(safe-area-inset-bottom);
}

/* Notch / Dynamic Island on landscape */
.side-safe {
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

/* Full-bleed safe wrapper */
.safe-area {
  padding: env(safe-area-inset-top) env(safe-area-inset-right)
    env(safe-area-inset-bottom) env(safe-area-inset-left);
}
```

### Viewport Meta
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
```

The `viewport-fit=cover` is required for `env(safe-area-inset-*)` to return non-zero values. Never add `maximum-scale=1` or `user-scalable=no` — it blocks pinch-zoom (WCAG 1.4.4).

### Viewport Height
`100vh` is taller than the visible area when mobile browser toolbars are showing. Use `100dvh` (tracks toolbars) for full-screen app shells and sheets, `100svh` for heroes that shouldn't resize while scrolling (Tailwind: `h-dvh`, `h-svh`).

---

## 6. Mobile Typography Scale

### Recommended Scale
| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| Large title | 34px | 700 | 1.2 |
| Title 1 | 28px | 700 | 1.2 |
| Title 2 | 22px | 700 | 1.25 |
| Title 3 | 20px | 600 | 1.25 |
| Headline | 17px | 600 | 1.3 |
| Body | 17px | 400 | 1.5 |
| Callout | 16px | 400 | 1.4 |
| Subhead | 15px | 400 | 1.4 |
| Footnote | 13px | 400 | 1.3 |
| Caption | 12px | 400 | 1.3 |

### Rules
- Body text minimum 16px on mobile for readability.
- Inputs, selects, and textareas must be ≥16px — iOS Safari auto-zooms into any field with a smaller font.
- Line length: 35–50 characters max for comfortable mobile reading.
- Use `rem` units based on 16px root.

---

## 7. Thumb Zone Optimization

### The Thumb Zone Map
```
+-----------------------------+
|     Hard to reach           |  <- Top 25%: Put secondary actions, titles
|                             |
|-----------------------------|
|     Comfortable stretch     |  <- Middle 50%: Content, scrollable lists
|                             |
|-----------------------------|
|     Easy / Natural          |  <- Bottom 25%: Primary actions, nav, FAB
+-----------------------------+
```

### Practical Rules
- **Primary actions at bottom**: CTA buttons, submit buttons, navigation.
- **Search bars**: Consider bottom placement (like iOS Safari).
- **FAB (Floating Action Button)**: Bottom-right corner, 56px, with shadow.
- **Destructive actions at top**: Harder to reach = harder to accidentally trigger.

```html
<!-- Bottom-anchored CTA -->
<div class="fixed bottom-0 inset-x-0 px-4 pt-12 pb-safe-4 bg-gradient-to-t from-white via-white
  to-transparent">
  <button type="button" class="w-full bg-indigo-600 text-white py-4 rounded-2xl font-semibold
    text-lg active:bg-indigo-700 transition-colors">
    Continue
  </button>
</div>
```

---

## 8. Sheet / Bottom Drawer Patterns

### Bottom Sheet Structure
```html
<div class="fixed inset-0 z-50">
  <!-- Backdrop: tap to dismiss -->
  <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" data-dismiss></div>

  <!-- Sheet: a modal dialog — trap focus, close on Esc, return focus to the trigger.
       A native <dialog> opened with showModal() gives you most of this for free. -->
  <div role="dialog" aria-modal="true" aria-labelledby="sheet-title"
    class="absolute bottom-0 inset-x-0 bg-white rounded-t-3xl
    max-h-[85dvh] overflow-y-auto overscroll-contain pb-safe-4">
    <!-- Drag handle (visual only) -->
    <div class="flex justify-center pt-3 pb-2" aria-hidden="true">
      <div class="w-10 h-1 rounded-full bg-gray-300"></div>
    </div>

    <!-- Content -->
    <div class="px-4 pb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 id="sheet-title" class="text-xl font-bold text-gray-900">Sheet Title</h2>
        <button type="button" aria-label="Close" class="w-11 h-11 -mr-2 rounded-full
          flex items-center justify-center text-gray-500">✕</button>
      </div>
      <!-- Sheet content -->
    </div>
  </div>
</div>
```

### Sheet Variants
- **Peek sheet**: Shows 30% of content, drag to expand.
- **Action sheet**: List of options (iOS-style).
- **Full-screen sheet**: Slides up to cover entire screen with close button.
- **Map sheet**: Persistent bottom sheet over a map (Google Maps style).

### Sheet Rules
- Always include a drag handle (40px wide, 4px tall, centered, rounded).
- Max height: 85% of viewport. Let it scroll internally.
- Dismiss: swipe down, tap backdrop, or explicit close button.
- Snap points: collapsed, half, expanded.

---

## 9. Mobile Form Design

### Rules
1. **Large inputs**: Minimum 48px height, 16px+ font (avoids iOS zoom).
2. **Full-width inputs**: Edge-to-edge within the container.
3. **Smart keyboard types**: Use `inputmode` attribute.
4. **Sticky submit button**: Fixed at bottom of screen.
5. **Single column only**: Never side-by-side fields on mobile.

### Input Mode Attribute
```html
<!-- Phone number: numeric keyboard -->
<input type="tel" inputmode="tel" />

<!-- Email: keyboard with @ and . -->
<input type="email" inputmode="email" />

<!-- Number: numeric keypad -->
<input type="text" inputmode="numeric" pattern="[0-9]*" />

<!-- URL: keyboard with / and .com -->
<input type="url" inputmode="url" />

<!-- Search: keyboard with search/go button -->
<input type="search" inputmode="search" />
```

### Mobile-Optimized Input
```html
<div class="space-y-1.5">
  <label for="phone" class="block text-sm font-medium text-gray-700">
    Phone number
  </label>
  <input
    type="tel"
    id="phone"
    inputmode="tel"
    autocomplete="tel"
    class="block w-full h-12 rounded-xl border border-gray-300 px-4
      text-base text-gray-900 placeholder:text-gray-400
      focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
    placeholder="+1 (555) 000-0000"
  />
</div>
```

---

## 10. Native-Feeling Animations

### Timing Functions
```css
:root {
  /* iOS-like spring curve (slight overshoot) */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  /* Quick in, slow out (for entering elements) */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
  /* Slow in, quick out (for exiting elements) */
  --ease-in: cubic-bezier(0.55, 0, 1, 0.45);
}
```

### Common Transitions
```css
/* Page transition: slide from right */
.page-enter {
  transform: translateX(100%);
  animation: slide-in 350ms var(--ease-out) forwards;
}
@keyframes slide-in {
  to { transform: translateX(0); }
}

/* Sheet reveal: slide up */
.sheet-enter {
  transform: translateY(100%);
  animation: sheet-up 400ms var(--ease-out) forwards;
}
@keyframes sheet-up {
  to { transform: translateY(0); }
}

/* Tap feedback */
.tap-feedback:active {
  transform: scale(0.97);
  opacity: 0.8;
  transition: transform 50ms ease, opacity 50ms ease;
}
```

### Animation Rules for Mobile
1. Keep animations under 400ms. 200–300ms feels snappy.
2. Use `transform` and `opacity` only for 60fps performance.
3. Add `will-change: transform` sparingly for animated elements.
4. Respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
5. Provide haptic feedback for important actions (native only).

---

## Verify: Render and Check

Don't hand over code you haven't looked at. After generating it:
1. Screenshot it at mobile and desktop widths, e.g. `npx playwright screenshot --full-page --viewport-size=390,844 file://$PWD/index.html mobile.png`, then again with `--viewport-size=1440,900` (or point at the dev server URL).
2. Open both images and check: no horizontal scroll or clipped/overlapping text, hierarchy reads at a glance, brand tokens are applied, images load at the right aspect ratio.
3. Tab through once: every interactive element gets a visible focus ring, in a logical order.
4. Also screenshot at 320px and in landscape; fixed bars must clear the safe areas. Headless browsers don't emulate notches, so confirm in code that every fixed top/bottom bar adds `env(safe-area-inset-*)` (or check in the iOS Simulator if available).
5. Fix what you find and re-screenshot before reporting done.

---

## Mobile Design Checklist

- [ ] All tap targets are 44×44px+ (48×48 for Material), never below WCAG's 24×24
- [ ] Bottom navigation with 3–5 tabs and labels
- [ ] Safe areas respected (top, bottom, sides)
- [ ] Body text is 16px+ (no iOS zoom on focus)
- [ ] Primary actions are in the thumb zone (bottom)
- [ ] Forms use correct `inputmode` attributes
- [ ] Sheets have drag handles and dismiss gestures
- [ ] Animations are under 400ms and use GPU-friendly properties
- [ ] `viewport-fit=cover` meta tag is set; zoom is not disabled
- [ ] Full-height layouts use `dvh`/`svh`, not `100vh`
- [ ] Every gesture has a tap alternative; sheets are labelled dialogs with focus management
- [ ] `prefers-reduced-motion` is respected
- [ ] Content is readable at 320px width
- [ ] No horizontal scroll on any screen
- [ ] Rendered and screenshotted at 320px, 390px, and landscape (see Verify)
