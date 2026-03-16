---
name: design-critique
description: >
  Evaluate and improve existing designs with structured analysis and
  actionable code fixes. Trigger phrases: "design critique", "review design",
  "improve design", "design audit", "design feedback", "evaluate UI",
  "design score", "accessibility audit", "visual review", "design assessment"
license: MIT
---

# Design Critique

Systematically evaluate existing designs and provide specific, actionable improvements with code.

## Prerequisites

Before critiquing, check for existing design context:
- Read any design-context files for brand guidelines, design system tokens, or stated goals.
- Understand the project's purpose, audience, and constraints before making recommendations.

---

## Step 1: Visual Hierarchy Assessment

Evaluate how effectively the design guides the user's eye.

### Checklist

- [ ] **Primary focal point**: Is there one clear element that draws attention first?
- [ ] **Secondary elements**: Can you identify a clear 2nd and 3rd level of importance?
- [ ] **Size contrast**: Is the most important element the largest? Is there enough size difference between levels?
- [ ] **Color contrast**: Does the primary CTA use the strongest color? Are secondary elements visually receded?
- [ ] **Weight contrast**: Do headings feel heavier than body text?
- [ ] **Whitespace**: Does the most important element have the most breathing room?
- [ ] **Reading flow**: Does the layout follow an F-pattern (content) or Z-pattern (landing page)?

### Common Fixes

```css
/* Problem: All elements same visual weight */
/* Fix: Create clear hierarchy with size and color */

/* Before: flat hierarchy */
.heading { font-size: 1.5rem; color: #333; }
.subheading { font-size: 1.25rem; color: #333; }
.body { font-size: 1rem; color: #333; }

/* After: clear hierarchy */
.heading { font-size: 2.5rem; font-weight: 800; color: var(--gray-900); letter-spacing: -0.02em; }
.subheading { font-size: 1.25rem; font-weight: 500; color: var(--gray-500); }
.body { font-size: 1rem; font-weight: 400; color: var(--gray-700); line-height: 1.65; }
```

---

## Step 2: Color Usage Evaluation

### Checklist

- [ ] **Palette cohesion**: Are all colors from the same family/system or do some feel random?
- [ ] **Meaningful color**: Does each color serve a purpose (brand, semantic, decorative)?
- [ ] **Color count**: Are there too many colors? (Aim for 1-2 brand + 4 semantic + neutrals.)
- [ ] **Contrast ratios**: Does all text meet WCAG AA (4.5:1 for normal, 3:1 for large)?
- [ ] **Consistent semantic colors**: Is red always error? Green always success?
- [ ] **Dark mode**: If present, are colors adapted (not just inverted)?
- [ ] **Color-only information**: Is any information conveyed by color alone? (It should not be.)

### Common Fixes

```css
/* Problem: Text fails contrast check */
/* Before: light gray on white */
.muted-text { color: #aaa; } /* ~2.3:1 on white -- FAILS AA */

/* Fix: darken until AA passes */
.muted-text { color: #737373; } /* ~4.6:1 on white -- passes AA */

/* Problem: Link indistinguishable from text */
/* Fix: underline + color */
a { color: var(--brand-500); text-decoration: underline; text-underline-offset: 2px; }
```

---

## Step 3: Typography Consistency Check

### Checklist

- [ ] **Font count**: Max 2 typefaces (3 with monospace). More feels chaotic.
- [ ] **Size scale**: Do sizes follow a consistent scale ratio or are they arbitrary?
- [ ] **Weight usage**: Are only 2-3 weights used? (400, 600, 700 is a good set.)
- [ ] **Line height**: Is body text 1.5-1.75? Are headings 1.1-1.3?
- [ ] **Line length**: Is body text constrained to 45-75 characters per line?
- [ ] **Consistency**: Same element types use same styles throughout?
- [ ] **Text wrap**: Are headings using `text-wrap: balance`?
- [ ] **Responsive**: Does text scale appropriately on mobile?

### Common Fixes

```css
/* Problem: Line length too long */
/* Before: text spans full 1400px container */
.content { max-width: 1400px; }

/* Fix: constrain prose */
.content { max-width: 1400px; }
.content .prose { max-width: 65ch; }

/* Problem: Arbitrary font sizes */
/* Fix: implement a scale */
:root {
  --scale: 1.25;
  --text-sm: calc(1rem / var(--scale));
  --text-base: 1rem;
  --text-lg: calc(1rem * var(--scale));
  --text-xl: calc(1rem * var(--scale) * var(--scale));
}
```

---

## Step 4: Spacing and Alignment Audit

### Checklist

- [ ] **Consistent spacing**: Are gaps between similar elements the same?
- [ ] **Spacing scale**: Do spacings use a base unit (4px or 8px multiples)?
- [ ] **Alignment**: Are elements aligned to a grid? Left edges lining up?
- [ ] **Proximity**: Are related items closer together than unrelated items?
- [ ] **Padding balance**: Is internal padding consistent within components?
- [ ] **Vertical rhythm**: Is there a consistent rhythm to the vertical spacing?
- [ ] **Edge consistency**: Are page margins consistent across sections?

### Common Fixes

```css
/* Problem: Inconsistent spacing */
/* Before: random pixel values */
.card { padding: 17px; margin-bottom: 23px; }
.section { padding: 45px 30px; }

/* Fix: use a 4px/8px scale */
.card { padding: var(--space-5); margin-bottom: var(--space-6); }
.section { padding: var(--space-12) var(--space-8); }

/* Problem: Misaligned elements */
/* Fix: use consistent padding and max-width */
.container {
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: var(--space-6);
}
```

---

## Step 5: Accessibility Review

### Contrast

- [ ] Normal text (< 18px): 4.5:1 minimum contrast ratio.
- [ ] Large text (18px+ bold, 24px+): 3:1 minimum.
- [ ] UI components (borders, icons): 3:1 against adjacent colors.
- [ ] Focus indicators: 3:1 against adjacent background.

### Keyboard Navigation

- [ ] All interactive elements are focusable.
- [ ] Focus order follows visual order.
- [ ] Focus indicator is visible and has sufficient contrast.
- [ ] No keyboard traps (user can always tab away).
- [ ] Skip-to-content link exists.

### Screen Reader

- [ ] Images have meaningful alt text (or `alt=""` if decorative).
- [ ] Form inputs have associated labels.
- [ ] Icon-only buttons have `aria-label`.
- [ ] Headings form a logical outline (no skipped levels).
- [ ] Dynamic content changes are announced (aria-live regions).

### Common Fixes

```css
/* Problem: Custom focus style removed */
/* Before */
*:focus { outline: none; } /* NEVER DO THIS */

/* Fix: custom but visible focus */
*:focus-visible {
  outline: 2px solid var(--brand-500);
  outline-offset: 2px;
}

/* Problem: No skip link */
/* Fix: */
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  padding: 0.5rem 1rem;
  background: var(--brand-500);
  color: white;
  z-index: 9999;
}

.skip-link:focus {
  top: 0;
}
```

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

---

## Step 6: Responsive Behavior Check

### Checklist

- [ ] **Mobile layout**: Does the layout stack sensibly on small screens?
- [ ] **Touch targets**: Are all interactive elements at least 44x44px on mobile?
- [ ] **Text readability**: Is body text at least 16px on mobile (no zoom needed)?
- [ ] **Horizontal scroll**: Is there any horizontal overflow?
- [ ] **Images**: Do images resize appropriately (max-width: 100%)?
- [ ] **Navigation**: Is mobile navigation accessible and usable?
- [ ] **Breakpoints**: Do layouts transition smoothly between breakpoints?

### Common Fixes

```css
/* Problem: Fixed widths cause overflow */
/* Before */
.card { width: 400px; }

/* Fix: flexible with max */
.card { width: 100%; max-width: 400px; }

/* Problem: Small touch targets */
/* Before */
.icon-button { width: 24px; height: 24px; }

/* Fix: larger touch target */
.icon-button {
  width: 24px;
  height: 24px;
  padding: 10px;    /* Increases touch target to 44px */
  margin: -10px;    /* Prevents layout shift */
}

/* Problem: Images overflow container */
img {
  max-width: 100%;
  height: auto;
}
```

---

## Step 7: Performance Impact Assessment

### Checklist

- [ ] **Font loading**: Using `font-display: swap`? Preloading critical fonts?
- [ ] **Image formats**: Using WebP/AVIF with fallbacks?
- [ ] **Image sizing**: Are images sized appropriately (not 4000px for a 400px display)?
- [ ] **Animation performance**: Animations using only `transform` and `opacity`?
- [ ] **CSS efficiency**: Any redundant or overriding styles?
- [ ] **Layout shifts**: Are dimensions reserved for images/embeds (aspect-ratio, width/height)?
- [ ] **Excessive shadows/blurs**: Are there complex box-shadows on frequently painted elements?

### Common Fixes

```css
/* Problem: Animation causes layout recalculation */
/* Before */
.card:hover { margin-top: -5px; }  /* triggers layout */

/* Fix: use transform */
.card:hover { transform: translateY(-5px); }  /* GPU composited */

/* Problem: Layout shift from images */
/* Fix: reserve space */
img {
  aspect-ratio: 16 / 9;
  width: 100%;
  object-fit: cover;
}
```

---

## Step 8: Specific Improvement Recommendations

When providing feedback, always follow this structure:

### Recommendation Format

```
### Issue: [What's wrong]
**Severity**: High / Medium / Low
**Category**: Hierarchy | Color | Typography | Spacing | Accessibility | Responsive | Performance

**Problem**: [1-2 sentences describing what's wrong and why it matters]

**Fix**:
[Specific CSS/HTML code to resolve it]

**Impact**: [What improves -- readability, usability, aesthetics, performance]
```

### Example

```
### Issue: Hero section lacks visual hierarchy
**Severity**: High
**Category**: Hierarchy

**Problem**: The hero headline, subheadline, and CTA button are all similar
in visual weight. Users cannot quickly identify the primary message or action.

**Fix**:
```

```css
.hero-headline {
  font-size: clamp(2.5rem, 5vw + 1rem, 5rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.03em;
  color: var(--gray-900);
  margin-bottom: var(--space-4);
}

.hero-subtitle {
  font-size: var(--text-xl);
  color: var(--gray-500);   /* Receded from headline */
  max-width: 50ch;
  margin-bottom: var(--space-8);
}

.hero-cta {
  font-size: var(--text-lg);
  padding: var(--space-3) var(--space-8);
  background: var(--brand-500);
  color: white;
  font-weight: 600;
}
```

```
**Impact**: Users immediately see the headline, understand the value proposition
from the subtitle, and have a clear next action.
```

---

## Step 9: Before/After Comparison Approach

When suggesting changes, provide both states for comparison.

### Structure

1. Identify the specific element or section.
2. Show the current CSS (before).
3. Show the improved CSS (after).
4. Explain what changed and why.

```css
/* BEFORE: Flat, low contrast card */
.card {
  padding: 20px;
  border: 1px solid #eee;
  background: white;
}

.card h3 {
  font-size: 18px;
  margin-bottom: 8px;
}

.card p {
  font-size: 14px;
  color: #666;
}

/* AFTER: Elevated, clear hierarchy */
.card {
  padding: var(--space-6);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-secondary);
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card h3 {
  font-size: var(--text-xl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.card p {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  line-height: 1.6;
}

/* Changes: added border-radius, hover elevation, better spacing tokens,
   stronger heading weight, improved line-height for readability */
```

---

## Step 10: Scoring Framework

Rate the design across these dimensions (1-10 scale):

### Categories

| Category       | Weight | What to evaluate                                  |
|----------------|--------|---------------------------------------------------|
| **Hierarchy**  | 25%    | Clear focal points, scannable, directed flow       |
| **Consistency**| 25%    | Spacing scale, color system, type system, patterns |
| **Aesthetics** | 25%    | Color harmony, whitespace, polish, modern feel     |
| **Usability**  | 25%    | Accessibility, responsiveness, clarity, performance|

### Scoring Rubric

| Score | Meaning                                               |
|-------|-------------------------------------------------------|
| 1-2   | Fundamentally broken. Major rework needed.            |
| 3-4   | Significant issues. Multiple areas need attention.    |
| 5-6   | Functional but unpolished. Clear improvement areas.   |
| 7-8   | Good. Minor refinements would elevate it.             |
| 9-10  | Excellent. Professional quality, well-executed.       |

### Report Template

```
## Design Critique Report

### Overall Score: X/10

| Category    | Score | Notes                                |
|-------------|-------|--------------------------------------|
| Hierarchy   | X/10  | [brief note]                         |
| Consistency | X/10  | [brief note]                         |
| Aesthetics  | X/10  | [brief note]                         |
| Usability   | X/10  | [brief note]                         |

### Top 3 Strengths
1. [What's working well]
2. [What's working well]
3. [What's working well]

### Top 3 Improvements (with code)
1. [Highest impact fix -- include CSS]
2. [Second highest impact fix -- include CSS]
3. [Third highest impact fix -- include CSS]

### Quick Wins (< 5 min each)
- [Small change, big impact]
- [Small change, big impact]
```

---

## Critique Process Summary

1. **Read design context** and understand goals.
2. **Assess visual hierarchy**: Is there a clear 1-2-3 priority?
3. **Evaluate colors**: Cohesive? Accessible? Purposeful?
4. **Check typography**: Consistent scale? Good line length? Readable?
5. **Audit spacing**: Using a system? Aligned? Consistent?
6. **Review accessibility**: Contrast, focus, labels, keyboard?
7. **Test responsive**: Mobile stacking, touch targets, overflow?
8. **Check performance**: Animations efficient? Images sized? Fonts loaded?
9. **Provide specific fixes**: Always include code, never just describe.
10. **Score and prioritize**: Give an overall score and rank recommendations by impact.
