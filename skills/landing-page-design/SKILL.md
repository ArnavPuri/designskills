---
name: landing-page-design
description: >
  High-converting landing page design with proven section frameworks and conversion patterns.
  Trigger: user asks to "build a landing page", "create a homepage", "design a marketing page",
  "make a product page", "build a SaaS landing page", "create a signup page", or any
  marketing/conversion-focused web page.
license: MIT
---

# Landing Page Design

## Pre-Flight: Check Design Context

Before generating landing page code:
1. Use `get_design_context` to check for existing brand colors, fonts, or component libraries.
2. If a Figma URL is provided, pull screenshots and metadata to match the design.
3. Ask or infer: What is the product? Who is the audience? What is the single desired action?

---

## 1. Section Framework

Every high-converting landing page follows this flow. You can reorder or omit sections, but this is the proven sequence:

```
1. Hero          — Value prop + primary CTA (above the fold)
2. Social Proof  — Logos, stats, or trust badges
3. Features      — What it does (benefits, not features)
4. How It Works  — 3-step simplicity
5. Testimonials  — Real humans saying real things
6. Pricing       — Clear tiers with obvious recommendation
7. FAQ           — Overcome objections
8. Final CTA     — Repeat the primary action
9. Footer        — Links, legal, secondary nav
```

### Spacing Between Sections
- Use `py-20 md:py-28 lg:py-32` for major sections.
- Alternate between white and subtle gray (`bg-gray-50`) backgrounds.
- Use a `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` container for all content.

---

## 2. Hero Patterns

### Pattern A: Centered Hero (Best for SaaS)
```html
<section class="relative overflow-hidden bg-white pt-24 pb-20 sm:pt-32 sm:pb-28">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
    <!-- Optional: Badge / announcement -->
    <div class="inline-flex items-center gap-2 rounded-full bg-indigo-50 px-3 py-1 text-sm
      font-medium text-indigo-700 ring-1 ring-indigo-600/10 mb-8">
      <span class="h-1.5 w-1.5 rounded-full bg-indigo-600"></span>
      Now in public beta
    </div>

    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-gray-950
      max-w-4xl mx-auto leading-[1.1]">
      The faster way to build
      <span class="text-indigo-600">beautiful products</span>
    </h1>

    <p class="mt-6 text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
      Ship production-ready interfaces in minutes. Stop fighting CSS and start
      delighting your users.
    </p>

    <div class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
      <a href="#" class="w-full sm:w-auto bg-indigo-600 text-white px-8 py-3.5 rounded-xl
        font-semibold text-lg hover:bg-indigo-500 transition-colors shadow-lg
        shadow-indigo-600/25">
        Start free trial
      </a>
      <a href="#" class="w-full sm:w-auto text-gray-700 px-8 py-3.5 rounded-xl font-semibold
        text-lg hover:bg-gray-100 transition-colors flex items-center justify-center gap-2">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><!-- play icon --></svg>
        Watch demo
      </a>
    </div>

    <!-- Trust signals -->
    <p class="mt-8 text-sm text-gray-400">No credit card required. Free for up to 3 projects.</p>
  </div>
</section>
```

### Pattern B: Split Hero (Text Left, Visual Right)
```html
<section class="relative overflow-hidden bg-white">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20 lg:py-28">
    <div class="grid lg:grid-cols-2 gap-12 lg:gap-16 items-center">
      <div>
        <h1 class="text-4xl lg:text-5xl font-extrabold tracking-tight text-gray-950 leading-[1.1]">
          Analytics that actually make sense
        </h1>
        <p class="mt-6 text-lg text-gray-600 leading-relaxed">
          Real-time insights without the learning curve. Understand your users
          in minutes, not months.
        </p>
        <div class="mt-8 flex flex-wrap gap-4">
          <a href="#" class="bg-gray-950 text-white px-6 py-3 rounded-lg font-semibold
            hover:bg-gray-800 transition-colors">Get started</a>
          <a href="#" class="text-gray-700 px-6 py-3 rounded-lg font-semibold
            hover:bg-gray-100 transition-colors">Learn more</a>
        </div>
      </div>
      <div class="relative">
        <div class="rounded-2xl border border-gray-200 shadow-2xl overflow-hidden">
          <img src="/dashboard-preview.png" alt="Dashboard preview"
            class="w-full" loading="lazy" />
        </div>
      </div>
    </div>
  </div>
</section>
```

### Pattern C: Video Background Hero
- Use a short (5–15s) looping muted video.
- Dark overlay at 50–60% opacity for text readability.
- Preload poster image for LCP performance.

### Pattern D: Interactive / Animated Hero
- Subtle particle effects, 3D objects, or interactive canvas.
- Keep CPU usage low. Pause animation when off-screen.
- Always have a static fallback for reduced-motion preference.

---

## 3. Social Proof Section

### Logo Bar
```html
<section class="bg-gray-50 py-12 border-y border-gray-100">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <p class="text-center text-sm font-medium text-gray-500 mb-8">
      Trusted by 2,000+ teams worldwide
    </p>
    <div class="flex flex-wrap items-center justify-center gap-x-12 gap-y-6
      grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all">
      <!-- Logos: SVG preferred, max-h-8, auto width -->
      <img src="/logos/stripe.svg" alt="Stripe" class="h-7" />
      <img src="/logos/vercel.svg" alt="Vercel" class="h-7" />
      <!-- ... more logos -->
    </div>
  </div>
</section>
```

### Stats Counters
```html
<div class="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
  <div>
    <div class="text-4xl font-extrabold text-gray-950">10K+</div>
    <div class="mt-1 text-sm text-gray-500">Active users</div>
  </div>
  <div>
    <div class="text-4xl font-extrabold text-gray-950">99.9%</div>
    <div class="mt-1 text-sm text-gray-500">Uptime SLA</div>
  </div>
  <!-- ... -->
</div>
```

---

## 4. Feature Sections

### Bento Grid (Modern, Visual)
```html
<section class="py-20 bg-white">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-16">
      <h2 class="text-3xl sm:text-4xl font-bold text-gray-950">Everything you need</h2>
      <p class="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
        A complete toolkit for modern teams.
      </p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Featured card (spans 2 cols) -->
      <div class="md:col-span-2 bg-gradient-to-br from-indigo-500 to-purple-600
        rounded-2xl p-8 text-white min-h-[300px] flex flex-col justify-end">
        <h3 class="text-2xl font-bold">AI-powered insights</h3>
        <p class="mt-2 text-indigo-100">Automatically surface what matters most.</p>
      </div>
      <!-- Regular cards -->
      <div class="bg-gray-50 rounded-2xl p-8 min-h-[300px] flex flex-col justify-end">
        <div class="w-10 h-10 rounded-lg bg-indigo-100 text-indigo-600 flex items-center
          justify-center mb-4"><!-- icon --></div>
        <h3 class="text-lg font-bold text-gray-950">Real-time sync</h3>
        <p class="mt-2 text-gray-600">Changes appear instantly across all devices.</p>
      </div>
    </div>
  </div>
</section>
```

### Alternating Rows (Classic, Detailed)
- Odd rows: text left, image right.
- Even rows: image left, text right.
- Each row highlights one feature with a heading, description, and visual.

### Icon Grid (Simple, Scannable)
- 3 or 4 columns of icon + heading + short description.
- Icons should be consistent style (outline or filled, not mixed).

---

## 5. CTA Design

### Primary CTA Rules
- **Size**: Minimum 48px tall, 200px+ wide. Larger than any other button on the page.
- **Color**: Highest contrast element on the page. Primary brand color.
- **Copy**: Action-oriented verb. "Start free trial" > "Submit". "Get started" > "Sign up".
- **Urgency**: Optional, but effective. "Start free — no credit card required."
- **Repetition**: Primary CTA appears at least 3 times: hero, mid-page, bottom.

### Sticky CTA (Mobile)
```html
<div class="fixed bottom-0 inset-x-0 bg-white/90 backdrop-blur-lg border-t
  border-gray-200 p-4 sm:hidden z-50">
  <a href="#" class="block w-full bg-indigo-600 text-white text-center py-3.5
    rounded-xl font-semibold text-lg">
    Start free trial
  </a>
</div>
```

### Secondary CTA Patterns
- Ghost button (outline) next to primary.
- Text link with arrow: `Learn more ->`.
- Never two equally-weighted CTAs side by side.

---

## 6. How It Works

### Three-Step Pattern
```html
<section class="py-20 bg-gray-50">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <h2 class="text-3xl font-bold text-center text-gray-950 mb-16">
      Get started in minutes
    </h2>
    <div class="grid md:grid-cols-3 gap-12">
      <div class="text-center">
        <div class="w-12 h-12 rounded-full bg-indigo-100 text-indigo-600 font-bold
          text-lg flex items-center justify-center mx-auto">1</div>
        <h3 class="mt-4 text-lg font-semibold text-gray-950">Connect your data</h3>
        <p class="mt-2 text-gray-600">Import from 50+ sources with one click.</p>
      </div>
      <!-- Steps 2 and 3 follow same pattern -->
    </div>
  </div>
</section>
```

Keep it to 3 steps. If your process has more, simplify or group.

---

## 7. Testimonials

### Card Grid
```html
<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
    <div class="flex gap-1 text-amber-400 mb-4">
      <!-- 5 star icons -->
    </div>
    <blockquote class="text-gray-700 leading-relaxed">
      "This completely changed how our team works. We shipped 3x faster in the
      first month."
    </blockquote>
    <div class="mt-4 flex items-center gap-3">
      <img src="/avatars/sarah.jpg" alt="" class="w-10 h-10 rounded-full" />
      <div>
        <div class="font-semibold text-gray-950 text-sm">Sarah Chen</div>
        <div class="text-gray-500 text-sm">CTO, Acme Corp</div>
      </div>
    </div>
  </div>
</div>
```

### Rules
- Real photos, real names, real companies.
- Include role/title for authority.
- Star ratings add visual credibility.
- Highlight specific outcomes ("3x faster", "saved 20 hours/week").

---

## 8. Pricing Section

### Three-Tier Pattern
- **Free/Basic** — anchor price, limited features.
- **Pro** (recommended) — highlighted with border, badge, or shadow. Most features.
- **Enterprise** — "Contact sales", unlimited everything.

### Design Rules
- Highlight the recommended plan with `ring-2 ring-indigo-600 scale-105`.
- Use a "Most Popular" badge.
- Annual/monthly toggle with savings callout.
- Feature list: checkmarks for included, dashes or X for excluded.
- Price: large number, small period (e.g., **$29**/mo).

---

## 9. Trust Signals

Place these throughout the page, not just in one section:
- **Security badges**: SSL, SOC 2, GDPR
- **Money-back guarantee**: "30-day full refund, no questions asked"
- **Support**: "24/7 support" or "Avg. response time: 2 hours"
- **Social proof**: "Join 10,000+ teams" near CTA buttons
- **Press logos**: "As seen in TechCrunch, Forbes..."

---

## 10. Performance Priorities

### Above-the-Fold (LCP Optimization)
- Hero image/video is the likely LCP element. Preload it.
- Inline critical CSS for the hero section.
- No lazy-loading above the fold.

```html
<link rel="preload" href="/hero-image.webp" as="image" />
```

### Below-the-Fold
- Lazy-load all images: `loading="lazy"`.
- Use `srcset` for responsive images.
- Defer non-critical JS.
- Use `content-visibility: auto` on far-down sections.

```html
<img
  src="/feature.webp"
  srcset="/feature-400.webp 400w, /feature-800.webp 800w, /feature-1200.webp 1200w"
  sizes="(max-width: 768px) 100vw, 50vw"
  loading="lazy"
  alt="Feature description"
  class="rounded-2xl"
/>
```

---

## 11. Conversion-Focused Spacing & Flow

### Visual Flow Rules
1. **F-pattern** for text-heavy pages (eyes scan top-left to right, then down-left).
2. **Z-pattern** for minimal pages (eyes zigzag across the page).
3. **Each section answers one question** then guides to the next.
4. **White space is a feature** — cramped pages feel untrustworthy.

### Section Spacing Scale
- Between major sections: `py-20 lg:py-32`
- Between subsections: `py-12 lg:py-16`
- Between heading and content: `mb-12 lg:mb-16`
- Between content items: `gap-6 lg:gap-8`

### Page-Level Checklist

- [ ] Single clear CTA (repeated 3+ times)
- [ ] Hero loads fast (preloaded LCP image)
- [ ] Social proof within first scroll
- [ ] Benefits over features in copy
- [ ] Mobile-optimized (sticky CTA, stacked layout)
- [ ] Fast page load (< 2s on 3G)
- [ ] No competing navigation (minimal header on landing pages)
