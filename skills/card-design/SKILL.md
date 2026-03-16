---
name: card-design
description: >
  Card-based layout patterns including product cards, feature cards, and interactive cards.
  Trigger: user asks to "design a card", "build card layout", "create a product card",
  "make a card grid", "design a testimonial card", "blog post card", "feature card",
  "pricing card", or any card-based UI component.
license: MIT
---

# Card Design

## Pre-Flight: Check Design Context

Before generating card components:
1. Use `get_design_context` to check for existing design tokens, border radii, shadow scales, or component libraries.
2. If a Figma URL is provided, pull screenshots and metadata to match the design precisely.
3. Determine: What content goes in the card? What action does the user take?

---

## 1. Card Anatomy

Every card has up to five zones. Not all are required.

```
+---------------------------+
|        [Media]            |  Image, video, or illustration
+---------------------------+
|  [Header]                 |  Title, subtitle, avatar, badge
|                           |
|  [Body]                   |  Description, content, data
|                           |
|  [Actions]                |  Buttons, links, icons
|  [Metadata]               |  Date, author, tags, stats
+---------------------------+
```

### Base Card Style
```css
.card {
  background: white;
  border-radius: 1rem;
  border: 1px solid oklch(92% 0 0);
  overflow: hidden;
  transition: all 200ms ease;
}
```

### Tailwind Base Card
```html
<div class="bg-white rounded-2xl border border-gray-200 overflow-hidden
  shadow-sm hover:shadow-md transition-shadow">
  <!-- content -->
</div>
```

---

## 2. Card Grid Layouts

### Uniform Grid
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  <!-- Equal-sized cards -->
</div>
```

### Featured + Grid
```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <!-- Featured card spans 2 columns -->
  <div class="lg:col-span-2 lg:row-span-2">
    <!-- Large featured card -->
  </div>
  <!-- Smaller cards fill remaining space -->
  <div><!-- card --></div>
  <div><!-- card --></div>
</div>
```

### Masonry Layout (CSS)
```css
.masonry {
  columns: 3;
  column-gap: 1.5rem;
}
.masonry > * {
  break-inside: avoid;
  margin-bottom: 1.5rem;
}

/* Responsive */
@media (max-width: 1024px) { .masonry { columns: 2; } }
@media (max-width: 640px) { .masonry { columns: 1; } }
```

### Horizontal Scroll (Mobile)
```html
<div class="flex gap-4 overflow-x-auto snap-x snap-mandatory pb-4
  scrollbar-hide -mx-4 px-4">
  <div class="snap-start shrink-0 w-72"><!-- card --></div>
  <div class="snap-start shrink-0 w-72"><!-- card --></div>
  <div class="snap-start shrink-0 w-72"><!-- card --></div>
</div>
```

---

## 3. Hover Effects

### Lift Effect (Subtle, Professional)
```html
<div class="bg-white rounded-2xl border border-gray-200 p-6
  hover:-translate-y-1 hover:shadow-lg transition-all duration-200">
```

### Glow Effect
```html
<div class="bg-white rounded-2xl border border-gray-200 p-6
  hover:border-indigo-300 hover:shadow-[0_0_24px_-4px_rgba(99,102,241,0.25)]
  transition-all duration-300">
```

### Border Reveal
```html
<div class="relative bg-white rounded-2xl p-6 border border-transparent
  before:absolute before:inset-0 before:rounded-2xl before:p-px
  before:bg-gradient-to-br before:from-indigo-500 before:to-purple-500
  before:opacity-0 hover:before:opacity-100 before:transition-opacity
  before:-z-10">
```

### Content Slide-Up
```html
<div class="group relative bg-white rounded-2xl overflow-hidden border border-gray-200">
  <img src="/image.jpg" alt="" class="w-full h-48 object-cover" />
  <div class="p-6">
    <h3 class="font-bold text-gray-900">Card Title</h3>
    <p class="mt-2 text-gray-600 text-sm">Description text here.</p>
  </div>
  <!-- Hidden actions that slide up on hover -->
  <div class="absolute bottom-0 inset-x-0 p-4 bg-gradient-to-t from-white via-white
    translate-y-full group-hover:translate-y-0 transition-transform duration-300">
    <button class="w-full bg-indigo-600 text-white py-2 rounded-lg font-medium">
      View details
    </button>
  </div>
</div>
```

### Image Zoom on Hover
```html
<div class="rounded-2xl overflow-hidden border border-gray-200">
  <div class="overflow-hidden">
    <img src="/image.jpg" alt=""
      class="w-full h-48 object-cover transition-transform duration-500
        group-hover:scale-110" />
  </div>
</div>
```

---

## 4. Product Card

```html
<div class="group bg-white rounded-2xl border border-gray-200 overflow-hidden
  hover:shadow-lg transition-all duration-200">
  <!-- Image -->
  <div class="relative overflow-hidden">
    <img src="/product.jpg" alt="Product name"
      class="w-full h-56 object-cover group-hover:scale-105 transition-transform duration-500" />
    <!-- Badge -->
    <span class="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold
      px-2.5 py-1 rounded-full">-20%</span>
    <!-- Wishlist button -->
    <button class="absolute top-3 right-3 w-9 h-9 bg-white/90 backdrop-blur rounded-full
      flex items-center justify-center text-gray-600 hover:text-red-500
      opacity-0 group-hover:opacity-100 transition-all">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
      </svg>
    </button>
  </div>

  <!-- Content -->
  <div class="p-4">
    <!-- Category -->
    <span class="text-xs font-medium text-indigo-600 uppercase tracking-wide">Electronics</span>
    <!-- Title -->
    <h3 class="mt-1 font-semibold text-gray-900 line-clamp-2">
      Wireless Noise-Cancelling Headphones Pro Max
    </h3>
    <!-- Rating -->
    <div class="mt-2 flex items-center gap-1.5">
      <div class="flex text-amber-400">
        <!-- 4.5 stars -->
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
        <!-- repeat for remaining stars -->
      </div>
      <span class="text-sm text-gray-500">(128)</span>
    </div>
    <!-- Price -->
    <div class="mt-3 flex items-baseline gap-2">
      <span class="text-xl font-bold text-gray-900">$249</span>
      <span class="text-sm text-gray-400 line-through">$319</span>
    </div>
  </div>

  <!-- Action -->
  <div class="px-4 pb-4">
    <button class="w-full bg-gray-950 text-white py-2.5 rounded-xl font-medium
      hover:bg-gray-800 active:bg-gray-900 transition-colors">
      Add to cart
    </button>
  </div>
</div>
```

---

## 5. Feature / Benefit Card

```html
<div class="bg-white rounded-2xl border border-gray-200 p-6
  hover:border-indigo-200 hover:shadow-md transition-all duration-200">
  <!-- Icon -->
  <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600
    flex items-center justify-center">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M13 10V3L4 14h7v7l9-11h-7z"/>
    </svg>
  </div>
  <!-- Content -->
  <h3 class="mt-4 text-lg font-semibold text-gray-900">Lightning Fast</h3>
  <p class="mt-2 text-gray-600 text-sm leading-relaxed">
    Built on edge infrastructure for sub-100ms response times worldwide.
    Your users won't wait.
  </p>
  <!-- Optional link -->
  <a href="#" class="mt-4 inline-flex items-center gap-1 text-sm font-medium
    text-indigo-600 hover:text-indigo-500 transition-colors">
    Learn more
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M17 8l4 4m0 0l-4 4m4-4H3"/>
    </svg>
  </a>
</div>
```

---

## 6. Testimonial Card

```html
<div class="bg-white rounded-2xl border border-gray-200 p-6">
  <!-- Stars -->
  <div class="flex gap-0.5 text-amber-400 mb-4">
    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
    <!-- repeat 5x -->
  </div>
  <!-- Quote -->
  <blockquote class="text-gray-700 leading-relaxed">
    "This tool saved our team 20 hours per week. The onboarding was seamless
    and we saw results from day one. Can't imagine going back."
  </blockquote>
  <!-- Author -->
  <div class="mt-6 flex items-center gap-3">
    <img src="/avatar.jpg" alt="" class="w-10 h-10 rounded-full" />
    <div>
      <div class="font-semibold text-gray-900 text-sm">Alex Rivera</div>
      <div class="text-gray-500 text-sm">VP Engineering, Acme Inc</div>
    </div>
  </div>
</div>
```

---

## 7. Blog Post Card

```html
<a href="/blog/post-slug" class="group block bg-white rounded-2xl border border-gray-200
  overflow-hidden hover:shadow-lg transition-all duration-200">
  <!-- Image -->
  <div class="overflow-hidden">
    <img src="/blog-cover.jpg" alt=""
      class="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-500" />
  </div>
  <!-- Content -->
  <div class="p-5">
    <!-- Meta -->
    <div class="flex items-center gap-2 text-sm text-gray-500 mb-3">
      <span class="bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full text-xs font-medium">
        Engineering
      </span>
      <span>5 min read</span>
    </div>
    <!-- Title -->
    <h3 class="font-bold text-gray-900 text-lg group-hover:text-indigo-600
      transition-colors line-clamp-2">
      How We Reduced Our Build Times by 80%
    </h3>
    <!-- Excerpt -->
    <p class="mt-2 text-gray-600 text-sm line-clamp-3 leading-relaxed">
      A deep dive into our migration to incremental builds and how it
      transformed our developer experience across 12 teams.
    </p>
    <!-- Author -->
    <div class="mt-4 flex items-center gap-2">
      <img src="/avatar.jpg" alt="" class="w-6 h-6 rounded-full" />
      <span class="text-sm text-gray-600">Sarah Kim</span>
      <span class="text-sm text-gray-400">Mar 15, 2026</span>
    </div>
  </div>
</a>
```

---

## 8. Interactive Cards

### Expandable Card
```html
<details class="group bg-white rounded-2xl border border-gray-200 overflow-hidden">
  <summary class="flex items-center justify-between p-6 cursor-pointer
    list-none hover:bg-gray-50 transition-colors">
    <div>
      <h3 class="font-semibold text-gray-900">Card Title</h3>
      <p class="text-sm text-gray-500 mt-1">Click to expand</p>
    </div>
    <svg class="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform"
      fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M19 9l-7 7-7-7"/>
    </svg>
  </summary>
  <div class="px-6 pb-6 text-gray-600 text-sm leading-relaxed">
    Expanded content appears here. This can contain additional details,
    images, or nested components.
  </div>
</details>
```

### Flippable Card
```html
<div class="group [perspective:1000px] h-64 w-full">
  <div class="relative h-full w-full transition-transform duration-500
    [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]">
    <!-- Front -->
    <div class="absolute inset-0 bg-white rounded-2xl border border-gray-200
      p-6 flex flex-col items-center justify-center [backface-visibility:hidden]">
      <div class="w-16 h-16 rounded-2xl bg-indigo-100 text-indigo-600
        flex items-center justify-center text-2xl mb-4">
        <svg class="w-8 h-8"><!-- icon --></svg>
      </div>
      <h3 class="font-bold text-gray-900">Feature Name</h3>
      <p class="mt-2 text-sm text-gray-500 text-center">Hover to learn more</p>
    </div>
    <!-- Back -->
    <div class="absolute inset-0 bg-indigo-600 rounded-2xl p-6
      flex flex-col items-center justify-center text-white text-center
      [backface-visibility:hidden] [transform:rotateY(180deg)]">
      <p class="text-sm leading-relaxed">
        Detailed description of this feature. Includes specific benefits
        and use cases for your team.
      </p>
      <button class="mt-4 bg-white text-indigo-600 px-4 py-2 rounded-lg
        font-medium text-sm">Learn more</button>
    </div>
  </div>
</div>
```

---

## 9. Skeleton Loading States

```html
<!-- Skeleton card mimics the final card structure -->
<div class="bg-white rounded-2xl border border-gray-200 overflow-hidden animate-pulse">
  <!-- Image placeholder -->
  <div class="h-48 bg-gray-200"></div>
  <!-- Content placeholders -->
  <div class="p-5 space-y-3">
    <div class="h-3 bg-gray-200 rounded-full w-1/4"></div>
    <div class="h-5 bg-gray-200 rounded-full w-3/4"></div>
    <div class="space-y-2">
      <div class="h-3 bg-gray-200 rounded-full w-full"></div>
      <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
    </div>
    <div class="flex items-center gap-2 pt-2">
      <div class="w-6 h-6 bg-gray-200 rounded-full"></div>
      <div class="h-3 bg-gray-200 rounded-full w-20"></div>
    </div>
  </div>
</div>
```

### Skeleton Rules
1. Match the exact layout of the real card (same heights, widths, spacing).
2. Use `animate-pulse` on the container (not individual elements).
3. Use `rounded-full` for text placeholders, `rounded-lg` for images.
4. Show 3–6 skeleton cards while loading, matching the expected grid.
5. Transition from skeleton to real content without layout shift.

---

## Card Design Checklist

- [ ] Card has clear visual boundaries (border, shadow, or background contrast)
- [ ] Content hierarchy: media > title > description > actions
- [ ] Hover effect provides feedback (lift, glow, or border change)
- [ ] Interactive cards are keyboard accessible (`tabindex`, `focus-visible`)
- [ ] Text is truncated with `line-clamp` where needed
- [ ] Grid is responsive (3 cols desktop, 2 tablet, 1 mobile)
- [ ] Loading skeleton matches card layout
- [ ] Images have proper `alt` text and `object-cover`
- [ ] Card links wrap the entire card (or use `::after` pseudo-element)
- [ ] Consistent border radius, padding, and spacing across all cards
