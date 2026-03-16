---
name: mobile-ui-design
description: >
  Mobile-first interface design for touch-optimized, native-feeling web and app UIs.
  Trigger: user asks to "design for mobile", "build a mobile UI", "make it mobile-friendly",
  "create a mobile app", "build a responsive mobile layout", "design a bottom sheet",
  "mobile navigation", or any mobile-specific interface work.
license: MIT
---

# Mobile UI Design

## Pre-Flight: Check Design Context

Before generating mobile UI code:
1. Use `get_design_context` to check for existing design tokens, platform guidelines, or component libraries.
2. If a Figma URL is provided, pull screenshots and metadata to match the design.
3. Determine: Is this a native app (React Native/Flutter), a PWA, or a responsive website?

---

## 1. Touch Target Sizes

Every interactive element must be large enough to tap reliably.

### Minimum Sizes
| Platform | Minimum Target | Recommended |
|----------|---------------|-------------|
| Apple HIG | 44x44px | 48x48px |
| Material Design | 48x48px | 56x56px |
| WCAG 2.5.8 | 24x24px (AAA: 44px) | 44x44px |

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
<nav class="fixed bottom-0 inset-x-0 bg-white border-t border-gray-200
  safe-area-bottom z-50">
  <div class="flex items-center justify-around h-16">
    <!-- Active tab -->
    <a href="#" class="flex flex-col items-center gap-0.5 text-indigo-600 min-w-[64px]">
      <svg class="w-6 h-6" fill="currentColor"><!-- home icon --></svg>
      <span class="text-[10px] font-medium">Home</span>
    </a>
    <!-- Inactive tab -->
    <a href="#" class="flex flex-col items-center gap-0.5 text-gray-400 min-w-[64px]">
      <svg class="w-6 h-6" fill="none" stroke="currentColor"><!-- search icon --></svg>
      <span class="text-[10px] font-medium">Search</span>
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
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
```

---

## 3. Gesture-Friendly Interactions

### Swipe Actions
```html
<!-- Swipe-to-reveal pattern (conceptual structure) -->
<div class="relative overflow-hidden">
  <!-- Background action (revealed on swipe) -->
  <div class="absolute inset-y-0 right-0 flex items-center bg-red-500 px-6">
    <span class="text-white font-medium">Delete</span>
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

### Common Mobile Gestures
| Gesture | Use Case | Implementation |
|---------|----------|---------------|
| Swipe left/right | Reveal actions, navigate | `touch-action: pan-y` |
| Pull down | Refresh content | Overscroll detection |
| Long press | Context menu, reorder | `@touchstart` with timeout |
| Pinch | Zoom images/maps | `touch-action: manipulation` |
| Swipe up | Dismiss sheet, expand | Drag handle on bottom sheet |

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
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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

The `viewport-fit=cover` is required for `env(safe-area-inset-*)` to work.

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
- Body text minimum 16px on mobile (prevents iOS zoom on input focus).
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
<div class="fixed bottom-0 inset-x-0 p-4 bg-gradient-to-t from-white via-white
  to-transparent pt-12 safe-area-bottom">
  <button class="w-full bg-indigo-600 text-white py-4 rounded-2xl font-semibold
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
  <!-- Backdrop -->
  <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

  <!-- Sheet -->
  <div class="absolute bottom-0 inset-x-0 bg-white rounded-t-3xl
    max-h-[85vh] overflow-y-auto safe-area-bottom">
    <!-- Drag handle -->
    <div class="flex justify-center pt-3 pb-2">
      <div class="w-10 h-1 rounded-full bg-gray-300"></div>
    </div>

    <!-- Content -->
    <div class="px-4 pb-6">
      <h2 class="text-xl font-bold text-gray-900 mb-4">Sheet Title</h2>
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
/* iOS-like spring curve */
--ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);

/* Quick in, slow out (for entering elements) */
--ease-out: cubic-bezier(0.16, 1, 0.3, 1);

/* Slow in, quick out (for exiting elements) */
--ease-in: cubic-bezier(0.55, 0, 1, 0.45);
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
  transition: all 50ms ease;
}
```

### Animation Rules for Mobile
1. Keep animations under 400ms. 200–300ms feels snappy.
2. Use `transform` and `opacity` only for 60fps performance.
3. Add `will-change: transform` sparingly for animated elements.
4. Respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```
5. Provide haptic feedback for important actions (native only).

---

## Mobile Design Checklist

- [ ] All tap targets are 44px+ minimum
- [ ] Bottom navigation with 3–5 tabs and labels
- [ ] Safe areas respected (top, bottom, sides)
- [ ] Body text is 16px+ (no iOS zoom on focus)
- [ ] Primary actions are in the thumb zone (bottom)
- [ ] Forms use correct `inputmode` attributes
- [ ] Sheets have drag handles and dismiss gestures
- [ ] Animations are under 400ms and use GPU-friendly properties
- [ ] `viewport-fit=cover` meta tag is set
- [ ] `prefers-reduced-motion` is respected
- [ ] Content is readable at 320px width
- [ ] No horizontal scroll on any screen
