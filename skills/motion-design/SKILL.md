---
name: motion-design
description: >
  Animation and micro-interactions for UI: easing, transitions, scroll
  animations, and performance. Trigger phrases: "animation", "micro-interaction",
  "motion design", "page transition", "scroll animation", "loading animation",
  "css animation", "hover effect", "skeleton loader", "stagger animation"
license: MIT
---

# Motion Design

Add purposeful animation and micro-interactions that enhance UX without compromising performance.

## Prerequisites

- Read any design-context files for animation preferences, timing tokens, or easing curves.
- If a design system exists, use its transition tokens.
- Always respect `prefers-reduced-motion`.

---

## Step 1: Animation Principles for UI

### The Three Rules
1. **Every animation must have a purpose**: Guide attention, provide feedback, show relationships, or convey state change.
2. **Faster is almost always better**: UI animations should be 100-500ms.
3. **Animate what changes**: Only animate properties that are actually changing.

### Duration Guidelines

| Action                    | Duration    |
|---------------------------|-------------|
| Button hover/press        | 100-150ms   |
| Toggle/switch             | 200ms       |
| Dropdown/menu open        | 200-250ms   |
| Modal/dialog appear       | 250-300ms   |
| Page transition           | 300-400ms   |
| Expand/collapse           | 250-350ms   |
| Loading spinner cycle     | 800-1200ms  |

### Easing Functions

```css
:root {
  --ease-out: cubic-bezier(0, 0, 0.2, 1);        /* Decelerate: ENTER */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);          /* Accelerate: EXIT */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);    /* Standard: MOVE */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);    /* Bouncy overshoot */
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.27, 1.55); /* Strong bounce */
}
```

Use ease-out for entrances, ease-in for exits, ease-in-out for moves, spring for playful feedback.

---

## Step 2: Micro-Interaction Patterns

### Button Press

```css
.btn {
  transition: transform 0.1s var(--ease-out), background-color 0.15s var(--ease-out), box-shadow 0.15s var(--ease-out);
}
.btn:hover { box-shadow: 0 4px 12px oklch(from var(--interactive-primary) l c h / 0.3); }
.btn:active { transform: scale(0.97); }
```

### Toggle Switch

```css
.toggle-track { width: 44px; height: 24px; background: var(--gray-300); border-radius: 12px; padding: 2px; cursor: pointer; transition: background-color 0.2s var(--ease-out); }
.toggle-thumb { width: 20px; height: 20px; background: white; border-radius: 50%; transition: transform 0.2s var(--ease-spring); }
.toggle-input:checked + .toggle-track { background: var(--brand-500); }
.toggle-input:checked + .toggle-track .toggle-thumb { transform: translateX(20px); }
```

### Like/Heart Animation

```css
.like-btn.is-liked .heart-icon { animation: like-pop 0.4s var(--ease-spring); color: #ef4444; fill: currentColor; }
@keyframes like-pop { 0% { transform: scale(1); } 30% { transform: scale(1.3); } 60% { transform: scale(0.9); } 100% { transform: scale(1); } }
```

---

## Step 3: Page Transition Animations

### Slide Up and Fade

```css
.page-enter { animation: slideUpFade 0.4s var(--ease-out) both; }
@keyframes slideUpFade {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### View Transitions API (Modern)

```css
@view-transition { navigation: auto; }
::view-transition-old(root) { animation: fade-out 0.2s ease-in both; }
::view-transition-new(root) { animation: fade-in 0.3s ease-out both; }
.hero-image { view-transition-name: hero; }
```

---

## Step 4: Scroll-Triggered Animations

### CSS-Only with `animation-timeline`

```css
.scroll-reveal { animation: reveal linear both; animation-timeline: view(); animation-range: entry 0% entry 100%; }
@keyframes reveal { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
```

### Intersection Observer Approach

```css
.reveal { opacity: 0; transform: translateY(30px); transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out); }
.reveal.is-visible { opacity: 1; transform: translateY(0); }
```

```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```

---

## Step 5: Loading Animations

### Skeleton Loader

```css
.skeleton { background: var(--gray-200); border-radius: var(--radius-md); position: relative; overflow: hidden; }
.skeleton::after {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(90deg, transparent, oklch(1 0 0 / 0.4), transparent);
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer { from { transform: translateX(-100%); } to { transform: translateX(100%); } }
.skeleton-text { height: 1em; margin-bottom: 0.75em; }
.skeleton-text:last-child { width: 60%; }
.skeleton-avatar { width: 48px; height: 48px; border-radius: 50%; }
```

### Spinner

```css
.spinner { width: 24px; height: 24px; border: 3px solid var(--gray-200); border-top-color: var(--brand-500); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
```

### Three-Dot Bounce

```css
.dots-loader { display: flex; gap: 4px; }
.dots-loader span { width: 8px; height: 8px; background: var(--brand-500); border-radius: 50%; animation: dot-bounce 1.2s ease-in-out infinite; }
.dots-loader span:nth-child(2) { animation-delay: 0.15s; }
.dots-loader span:nth-child(3) { animation-delay: 0.3s; }
@keyframes dot-bounce { 0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; } 40% { transform: scale(1); opacity: 1; } }
```

---

## Step 6: CSS Animation Techniques

### Transition vs Animation
- **`transition`**: For state changes (hover, focus, class toggle). A-to-B.
- **`animation`**: For multi-step sequences, continuous effects, or entrance animations.

### Animation Fill Modes

| Value     | Behavior                                              |
|-----------|-------------------------------------------------------|
| none      | Reverts to original state after animation             |
| forwards  | Stays at the last keyframe                            |
| backwards | Applies first keyframe during delay period            |
| both      | Combines forwards + backwards. Usually what you want  |

---

## Step 7: Spring Physics with CSS

```css
:root {
  --spring-gentle: cubic-bezier(0.34, 1.2, 0.64, 1);   /* Slight overshoot */
  --spring-medium: cubic-bezier(0.34, 1.56, 0.64, 1);   /* Noticeable bounce */
  --spring-strong: cubic-bezier(0.22, 1.8, 0.36, 1);    /* Dramatic bounce */
  --spring-snappy: cubic-bezier(0.075, 0.82, 0.165, 1); /* Fast in, controlled settle */
}
```

For multi-bounce, use keyframes:

```css
@keyframes spring-bounce {
  0% { transform: scale(0.8); } 40% { transform: scale(1.08); }
  60% { transform: scale(0.97); } 80% { transform: scale(1.02); } 100% { transform: scale(1); }
}
```

---

## Step 8: Reduced Motion

### Global Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important; scroll-behavior: auto !important;
  }
}
```

Preferred approach: replace motion with non-motion transitions (e.g., opacity changes instead of transforms).

---

## Step 9: Performance Optimization

### The Golden Rule
Only animate `transform` and `opacity`. These are GPU-composited and do not trigger layout or paint.

### Property Cost

| Property        | Layout | Paint | Composite | Performance |
|-----------------|--------|-------|-----------|-------------|
| transform       | No     | No    | Yes       | Excellent   |
| opacity         | No     | No    | Yes       | Excellent   |
| filter          | No     | Yes   | No        | Good        |
| box-shadow      | No     | Yes   | No        | Moderate    |
| width/height    | Yes    | Yes   | No        | Poor        |
| top/left        | Yes    | Yes   | No        | Poor        |

Use `will-change` sparingly -- only on elements about to animate, remove when done. Do NOT set on many elements permanently.

---

## Step 10: Stagger Animations for Lists

### Dynamic Stagger with Custom Properties

```css
.stagger-list > * {
  animation: stagger-in 0.4s var(--ease-out) both;
  animation-delay: calc(var(--index, 0) * 60ms);
}
@keyframes stagger-in { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
```

```html
<ul class="stagger-list">
  <li style="--index: 0">Item 1</li>
  <li style="--index: 1">Item 2</li>
  <li style="--index: 2">Item 3</li>
</ul>
```

### Stagger Rules
- Total stagger time should not exceed 600ms
- Per-item delay: 40-80ms between items
- Cap the delay after 8-10 items (they can all appear together)

---

## Quick Reference

1. Every animation needs a purpose: feedback, guidance, or state change.
2. Keep durations short: 100-400ms for most UI interactions.
3. Use ease-out for entrances, ease-in for exits, ease-in-out for moves.
4. Only animate `transform` and `opacity` for best performance.
5. Always implement `prefers-reduced-motion`.
6. Use skeleton loaders for content loading, spinners for actions.
7. Stagger list animations at 50-80ms intervals, total under 600ms.
8. Use `animation: ... both` to maintain end state.
9. Spring easings (`cubic-bezier` with values >1) add personality.
10. Test on low-end devices -- animation that jitters is worse than no animation.
