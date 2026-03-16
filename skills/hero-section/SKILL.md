---
name: hero-section
description: >
  Above-the-fold hero section patterns with production-ready code examples.
  Trigger: user asks to "create a hero", "build a hero section", "design above the fold",
  "make a hero banner", "landing page header", "build a homepage hero",
  or any above-the-fold section design.
license: MIT
---

# Hero Section Design

## Pre-Flight: Check Design Context

Before generating hero section code:
1. Use `get_design_context` to check for existing brand colors, fonts, or design tokens.
2. If a Figma URL is provided, pull screenshots and metadata to match the design precisely.
3. Determine: What is the product? What is the primary CTA? What visual style fits?

---

## 1. Headline Hierarchy

Every hero follows this structure, top to bottom:

```
[Optional: Badge / Announcement]
[Headline: Value Proposition]
[Subheadline: Supporting Detail]
[CTA Button(s)]
[Trust Signals]
[Visual: Image, Mockup, or Illustration]
```

### Headline Rules
- **One sentence**. Maximum 10 words.
- State the benefit, not the feature. "Ship faster" > "CI/CD pipeline tool".
- Use `text-4xl sm:text-5xl lg:text-6xl` scale.
- `font-extrabold tracking-tight leading-[1.1]` for impact.

### Subheadline Rules
- 1–2 sentences expanding on the headline.
- `text-lg sm:text-xl text-gray-600 max-w-2xl`.
- Answer: "What is this, and why should I care?"

---

## 2. Hero Pattern: Centered with Gradient Background

The most versatile hero. Works for SaaS, tools, and platforms.

```html
<section class="relative isolate overflow-hidden bg-white">
  <!-- Background gradient -->
  <div class="absolute inset-0 -z-10">
    <div class="absolute inset-0 bg-gradient-to-b from-indigo-50/80 via-white to-white"></div>
    <div class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/4
      w-[800px] h-[600px] rounded-full
      bg-gradient-to-br from-indigo-200/40 via-purple-200/30 to-pink-100/20
      blur-3xl"></div>
  </div>

  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-24 pb-16 sm:pt-32 sm:pb-24
    text-center">
    <!-- Announcement badge -->
    <a href="#" class="inline-flex items-center gap-2 rounded-full bg-indigo-50 px-4 py-1.5
      text-sm font-medium text-indigo-700 ring-1 ring-inset ring-indigo-600/10
      hover:bg-indigo-100 transition-colors mb-8">
      <span class="h-1.5 w-1.5 rounded-full bg-indigo-600 animate-pulse"></span>
      Announcing our Series A
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9 5l7 7-7 7"/>
      </svg>
    </a>

    <!-- Headline -->
    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight
      text-gray-950 max-w-4xl mx-auto leading-[1.1]">
      Build products that
      <span class="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text
        text-transparent">users love</span>
    </h1>

    <!-- Subheadline -->
    <p class="mt-6 text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
      The design-to-code platform that turns your ideas into production-ready
      interfaces in minutes, not weeks.
    </p>

    <!-- CTAs -->
    <div class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
      <a href="#" class="w-full sm:w-auto inline-flex items-center justify-center
        bg-indigo-600 text-white px-8 py-3.5 rounded-xl font-semibold text-lg
        hover:bg-indigo-500 shadow-lg shadow-indigo-600/25
        hover:shadow-xl hover:shadow-indigo-600/30
        hover:-translate-y-0.5 active:translate-y-0
        transition-all duration-200">
        Start building free
      </a>
      <a href="#" class="w-full sm:w-auto inline-flex items-center justify-center gap-2
        text-gray-700 px-8 py-3.5 rounded-xl font-semibold text-lg
        hover:bg-gray-100 transition-colors">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
          <path d="M6.3 2.84A1.5 1.5 0 004 4.11v11.78a1.5 1.5 0 002.3 1.27l9.344-5.891a1.5 1.5 0 000-2.538L6.3 2.841z"/>
        </svg>
        Watch demo
      </a>
    </div>

    <!-- Trust signals -->
    <div class="mt-10 flex flex-wrap items-center justify-center gap-x-6 gap-y-2
      text-sm text-gray-400">
      <span class="flex items-center gap-1.5">
        <svg class="w-4 h-4 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/>
        </svg>
        No credit card required
      </span>
      <span class="flex items-center gap-1.5">
        <svg class="w-4 h-4 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/>
        </svg>
        Free for individuals
      </span>
      <span class="flex items-center gap-1.5">
        <svg class="w-4 h-4 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd"/>
        </svg>
        Setup in 2 minutes
      </span>
    </div>

    <!-- Product screenshot -->
    <div class="mt-16 relative">
      <div class="rounded-2xl border border-gray-200/60 shadow-2xl shadow-gray-900/10
        overflow-hidden bg-white">
        <img src="/dashboard-preview.png" alt="Product dashboard"
          class="w-full" fetchpriority="high" />
      </div>
      <!-- Decorative glow behind image -->
      <div class="absolute -inset-4 -z-10 bg-gradient-to-b from-indigo-100/50
        to-transparent rounded-3xl blur-2xl"></div>
    </div>
  </div>
</section>
```

---

## 3. Hero Pattern: Split (Text Left, Image Right)

Best for products with a strong visual (app screenshots, mockups).

```html
<section class="relative overflow-hidden bg-white">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-20 lg:py-32">
    <div class="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
      <!-- Text -->
      <div class="max-w-xl">
        <div class="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1
          text-sm font-medium text-emerald-700 ring-1 ring-emerald-600/10 mb-6">
          New: AI assistant is here
        </div>
        <h1 class="text-4xl lg:text-5xl xl:text-6xl font-extrabold tracking-tight
          text-gray-950 leading-[1.1]">
          Your finances, finally simple
        </h1>
        <p class="mt-6 text-lg text-gray-600 leading-relaxed">
          Track spending, set budgets, and reach your goals with an app that
          actually makes sense. No jargon, no complexity.
        </p>
        <div class="mt-8 flex flex-wrap gap-4">
          <a href="#" class="bg-gray-950 text-white px-6 py-3 rounded-xl font-semibold
            hover:bg-gray-800 transition-colors">
            Download the app
          </a>
          <a href="#" class="text-gray-700 px-6 py-3 rounded-xl font-semibold
            hover:bg-gray-100 transition-colors flex items-center gap-2">
            See how it works
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 8l4 4m0 0l-4 4m4-4H3"/>
            </svg>
          </a>
        </div>
        <!-- Social proof -->
        <div class="mt-8 flex items-center gap-4">
          <div class="flex -space-x-2">
            <img src="/avatar-1.jpg" class="w-8 h-8 rounded-full ring-2 ring-white" alt="" />
            <img src="/avatar-2.jpg" class="w-8 h-8 rounded-full ring-2 ring-white" alt="" />
            <img src="/avatar-3.jpg" class="w-8 h-8 rounded-full ring-2 ring-white" alt="" />
            <img src="/avatar-4.jpg" class="w-8 h-8 rounded-full ring-2 ring-white" alt="" />
          </div>
          <div class="text-sm text-gray-600">
            <span class="font-semibold text-gray-900">4,000+</span> happy users
          </div>
        </div>
      </div>

      <!-- Visual -->
      <div class="relative lg:ml-auto">
        <div class="relative z-10">
          <img src="/app-mockup.png" alt="App interface"
            class="w-full max-w-md mx-auto rounded-3xl shadow-2xl"
            fetchpriority="high" />
        </div>
        <!-- Background decoration -->
        <div class="absolute -inset-8 bg-gradient-to-tr from-indigo-100 via-purple-50
          to-pink-50 rounded-[2rem] -z-10 blur-sm"></div>
      </div>
    </div>
  </div>
</section>
```

---

## 4. Hero Pattern: Video / Animated Background

```html
<section class="relative h-screen min-h-[600px] max-h-[900px] flex items-center overflow-hidden">
  <!-- Video background -->
  <video
    autoplay muted loop playsinline
    poster="/hero-poster.jpg"
    class="absolute inset-0 w-full h-full object-cover"
  >
    <source src="/hero-bg.mp4" type="video/mp4" />
  </video>

  <!-- Dark overlay -->
  <div class="absolute inset-0 bg-gray-950/60"></div>

  <!-- Content -->
  <div class="relative z-10 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
    <h1 class="text-4xl sm:text-5xl lg:text-7xl font-extrabold tracking-tight
      text-white leading-[1.1]">
      Experience the future
    </h1>
    <p class="mt-6 text-lg sm:text-xl text-white/80 max-w-2xl mx-auto">
      Immersive technology that transforms how you create.
    </p>
    <div class="mt-10">
      <a href="#" class="inline-flex items-center bg-white text-gray-950 px-8 py-4
        rounded-xl font-semibold text-lg hover:bg-gray-100 transition-colors">
        Get early access
      </a>
    </div>
  </div>

  <!-- Scroll indicator -->
  <div class="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
    <svg class="w-6 h-6 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M19 14l-7 7m0 0l-7-7m7 7V3"/>
    </svg>
  </div>
</section>
```

### Video Hero Rules
- Keep video 5–15 seconds, looping.
- File size under 5MB. Use WebM + MP4 for compatibility.
- Always provide a `poster` image for LCP.
- Use `playsinline` for iOS.
- Text must have sufficient contrast against the overlay.

---

## 5. Hero Pattern: Minimal Typography

For premium brands, agencies, and portfolios.

```html
<section class="min-h-screen flex items-center bg-gray-950">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-32">
    <h1 class="text-5xl sm:text-7xl lg:text-9xl font-extrabold text-white
      tracking-tighter leading-[0.9]">
      We design<br />
      <span class="text-gray-500">digital</span><br />
      experiences
    </h1>
    <div class="mt-12 flex items-center gap-6">
      <a href="#" class="text-white border border-white/20 px-6 py-3 rounded-full
        hover:bg-white hover:text-gray-950 transition-all font-medium">
        View our work
      </a>
      <a href="#" class="text-gray-400 hover:text-white transition-colors font-medium">
        Contact us
      </a>
    </div>
  </div>
</section>
```

---

## 6. Background Techniques

### Mesh Gradient
```css
.mesh-gradient {
  background-color: oklch(97% 0.01 265);
  background-image:
    radial-gradient(at 20% 20%, oklch(90% 0.12 280 / 0.4) 0px, transparent 50%),
    radial-gradient(at 80% 10%, oklch(90% 0.10 320 / 0.3) 0px, transparent 50%),
    radial-gradient(at 50% 80%, oklch(90% 0.12 200 / 0.3) 0px, transparent 50%);
}
```

### Animated Gradient
```css
.animated-gradient {
  background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
  background-size: 400% 400%;
  animation: gradient-shift 15s ease infinite;
}
@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

### Dot Grid Pattern
```css
.dot-grid {
  background-image: radial-gradient(circle, #d1d5db 1px, transparent 1px);
  background-size: 24px 24px;
}
```

### Noise Texture
```css
.noise {
  position: relative;
}
.noise::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
}
```

---

## 7. Responsive Hero Strategy

### Breakpoint Adjustments
```
Mobile (< 640px):
  - h1: text-3xl to text-4xl
  - Stack CTAs vertically (flex-col)
  - Hide decorative elements
  - Full-width buttons
  - Product image below text

Tablet (640–1024px):
  - h1: text-4xl to text-5xl
  - Horizontal CTAs (flex-row)
  - Product image scales down

Desktop (1024px+):
  - h1: text-5xl to text-6xl
  - Split layout becomes side-by-side
  - Full decorative elements visible
```

### Image Handling
```html
<picture>
  <source media="(min-width: 1024px)" srcset="/hero-desktop.webp" />
  <source media="(min-width: 640px)" srcset="/hero-tablet.webp" />
  <img src="/hero-mobile.webp" alt="Product preview"
    class="w-full rounded-2xl" fetchpriority="high" />
</picture>
```

---

## 8. LCP Performance

The hero is almost always the Largest Contentful Paint element. Optimize it.

### Rules
1. **Preload the hero image**: `<link rel="preload" href="/hero.webp" as="image" />`
2. **Use `fetchpriority="high"`** on the hero image tag.
3. **Never lazy-load** the hero image.
4. **Inline critical CSS** for the hero section.
5. **Use WebP/AVIF** format with fallback.
6. **Size appropriately**: Don't serve a 4000px image for a 1200px container.

```html
<head>
  <link rel="preload" href="/hero.webp" as="image"
    imagesrcset="/hero-400.webp 400w, /hero-800.webp 800w, /hero-1200.webp 1200w"
    imagesizes="100vw" />
</head>
```

---

## Hero Section Checklist

- [ ] Headline is under 10 words and states the benefit
- [ ] Subheadline expands on the value in 1–2 sentences
- [ ] Primary CTA is large, high-contrast, and action-oriented
- [ ] Secondary CTA is visually subordinate
- [ ] Trust signals appear near the CTA
- [ ] Hero image/visual is preloaded with `fetchpriority="high"`
- [ ] Responsive: text scales, layout adapts, images swap
- [ ] Background adds visual interest without competing with content
- [ ] Animation respects `prefers-reduced-motion`
- [ ] Above the fold loads in under 2.5s (LCP target)
