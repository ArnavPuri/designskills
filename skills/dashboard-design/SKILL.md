---
name: dashboard-design
description: >
  Data dashboard and admin panel design patterns for information-dense interfaces.
  Trigger: user asks to "build a dashboard", "create an admin panel", "design analytics",
  "make a data view", "build a settings page", "create a table view", "design a CRM",
  "build an internal tool", or any data-heavy interface work.
license: MIT
---

# Dashboard Design

## Pre-Flight: Check Design Context

Before generating dashboard code:
1. Use `get_design_context` to check for existing design tokens, component libraries, or dashboard frameworks.
2. If a Figma URL is provided, pull screenshots and metadata to match the design.
3. Determine: What data is being shown? Who is the user? What actions do they need to take?

---

## 1. Layout Patterns

### Pattern A: Sidebar + Main Content (Most Common)

```html
<div class="flex h-screen bg-gray-50">
  <!-- Sidebar -->
  <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
    <!-- Logo -->
    <div class="h-16 flex items-center px-6 border-b border-gray-100">
      <img src="/logo.svg" alt="App" class="h-8" />
    </div>
    <!-- Navigation -->
    <nav class="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
      <!-- Active item -->
      <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg
        bg-indigo-50 text-indigo-700 font-medium text-sm">
        <svg class="w-5 h-5"><!-- icon --></svg>
        Dashboard
      </a>
      <!-- Inactive item -->
      <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg
        text-gray-600 hover:bg-gray-100 hover:text-gray-900 text-sm transition-colors">
        <svg class="w-5 h-5"><!-- icon --></svg>
        Analytics
      </a>
      <!-- Section header -->
      <div class="pt-4 pb-1 px-3 text-xs font-semibold text-gray-400 uppercase tracking-wider">
        Settings
      </div>
    </nav>
    <!-- User section at bottom -->
    <div class="p-4 border-t border-gray-100">
      <div class="flex items-center gap-3">
        <img src="/avatar.jpg" alt="" class="w-8 h-8 rounded-full" />
        <div class="text-sm">
          <div class="font-medium text-gray-900">Jane Doe</div>
          <div class="text-gray-500 text-xs">Admin</div>
        </div>
      </div>
    </div>
  </aside>

  <!-- Main content -->
  <main class="flex-1 overflow-y-auto">
    <!-- Top bar -->
    <header class="h-16 bg-white border-b border-gray-200 flex items-center
      justify-between px-6 sticky top-0 z-10">
      <h1 class="text-lg font-semibold text-gray-900">Dashboard</h1>
      <div class="flex items-center gap-4">
        <!-- Search, notifications, profile -->
      </div>
    </header>
    <!-- Content area -->
    <div class="p-6">
      <!-- Dashboard content here -->
    </div>
  </main>
</div>
```

### Sidebar Behavior
- Desktop (lg+): Always visible, 240–280px wide.
- Tablet (md): Collapsible to icon-only (64px) with tooltip labels.
- Mobile (sm): Hidden, opens as overlay with backdrop.

### Pattern B: Top Nav + Grid
- Best for simpler dashboards with fewer navigation items.
- Horizontal nav bar at top, content fills below.
- Use tabs or pill navigation for sub-sections.

---

## 2. Data Cards (KPI Tiles)

### Standard Stat Card
```html
<div class="bg-white rounded-xl border border-gray-200 p-6">
  <div class="flex items-center justify-between">
    <span class="text-sm font-medium text-gray-500">Total Revenue</span>
    <span class="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600
      flex items-center justify-center">
      <svg class="w-5 h-5"><!-- dollar icon --></svg>
    </span>
  </div>
  <div class="mt-3">
    <span class="text-3xl font-bold text-gray-900">$45,231</span>
  </div>
  <div class="mt-2 flex items-center gap-1.5 text-sm">
    <span class="text-emerald-600 font-medium flex items-center gap-0.5">
      <svg class="w-4 h-4"><!-- arrow-up icon --></svg>
      12.5%
    </span>
    <span class="text-gray-400">vs last month</span>
  </div>
</div>
```

### Card Grid Layout
```html
<div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 md:gap-6">
  <!-- 4 stat cards -->
</div>
```

### Card Variants
- **With sparkline**: Add a small inline chart below the number.
- **With progress bar**: Show completion toward a goal.
- **With mini table**: Top 3 items listed below the stat.
- **Negative trend**: Use red with down-arrow for declining metrics.

---

## 3. Chart Selection Guide

| Data Type | Best Chart | When to Use |
|-----------|-----------|-------------|
| Trend over time | **Line chart** | Revenue, users, performance over days/months |
| Comparison | **Bar chart** | Compare categories, A/B results |
| Composition | **Pie / Donut** | Budget breakdown, traffic sources (max 5 slices) |
| Volume over time | **Area chart** | Bandwidth, cumulative metrics |
| Distribution | **Histogram** | Age ranges, price ranges |
| Relationship | **Scatter plot** | Correlation between two variables |
| Progress | **Progress bar / Gauge** | Goal completion, quotas |
| Ranking | **Horizontal bar** | Top pages, top products |

### Chart Design Rules
1. **Title every chart** with what it shows, not how to read it.
2. **Label axes** clearly. Include units.
3. **Limit colors** to 5–6 max. Use your primary palette.
4. **Start Y-axis at zero** for bar charts. Line charts can have non-zero baselines.
5. **Add tooltips** for exact values on hover.
6. **Use grid lines sparingly** — light dashed lines, not solid.
7. **Responsive**: Charts should resize, not overflow.

### Chart Color Palette
```css
:root {
  --chart-1: oklch(65% 0.2 265);   /* primary blue */
  --chart-2: oklch(70% 0.2 165);   /* teal */
  --chart-3: oklch(75% 0.2 320);   /* pink */
  --chart-4: oklch(80% 0.15 80);   /* amber */
  --chart-5: oklch(65% 0.15 145);  /* green */
}
```

---

## 4. Table Design

### Full-Featured Data Table
```html
<div class="bg-white rounded-xl border border-gray-200 overflow-hidden">
  <!-- Table header / toolbar -->
  <div class="px-6 py-4 border-b border-gray-100 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <h2 class="font-semibold text-gray-900">Recent Orders</h2>
      <span class="bg-gray-100 text-gray-600 text-xs font-medium px-2.5 py-0.5 rounded-full">
        2,847
      </span>
    </div>
    <div class="flex items-center gap-2">
      <!-- Search input -->
      <input type="text" placeholder="Search..."
        class="text-sm border border-gray-200 rounded-lg px-3 py-1.5 w-56
        focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500/20" />
      <!-- Filter button -->
      <button class="text-sm text-gray-600 border border-gray-200 rounded-lg
        px-3 py-1.5 hover:bg-gray-50 flex items-center gap-1.5">
        <svg class="w-4 h-4"><!-- filter icon --></svg>
        Filters
      </button>
    </div>
  </div>

  <!-- Table -->
  <table class="w-full text-sm">
    <thead>
      <tr class="border-b border-gray-100 text-left">
        <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
          <button class="flex items-center gap-1 hover:text-gray-700">
            Customer
            <svg class="w-3 h-3"><!-- sort icon --></svg>
          </button>
        </th>
        <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
          Status
        </th>
        <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider
          text-right">
          Amount
        </th>
        <th class="px-6 py-3 w-12"></th>
      </tr>
    </thead>
    <tbody class="divide-y divide-gray-50">
      <tr class="hover:bg-gray-50 transition-colors">
        <td class="px-6 py-4">
          <div class="flex items-center gap-3">
            <img src="/avatar.jpg" alt="" class="w-8 h-8 rounded-full" />
            <div>
              <div class="font-medium text-gray-900">Jane Cooper</div>
              <div class="text-gray-500 text-xs">jane@example.com</div>
            </div>
          </div>
        </td>
        <td class="px-6 py-4">
          <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full
            text-xs font-medium bg-emerald-50 text-emerald-700">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
            Completed
          </span>
        </td>
        <td class="px-6 py-4 text-right font-medium text-gray-900">$2,500.00</td>
        <td class="px-6 py-4">
          <button class="text-gray-400 hover:text-gray-600">
            <svg class="w-5 h-5"><!-- dots icon --></svg>
          </button>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- Pagination -->
  <div class="px-6 py-4 border-t border-gray-100 flex items-center justify-between text-sm">
    <span class="text-gray-500">Showing 1-10 of 2,847</span>
    <div class="flex gap-1">
      <button class="px-3 py-1.5 rounded-lg border border-gray-200 text-gray-600
        hover:bg-gray-50 disabled:opacity-50" disabled>Previous</button>
      <button class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white">1</button>
      <button class="px-3 py-1.5 rounded-lg border border-gray-200 text-gray-600
        hover:bg-gray-50">2</button>
      <button class="px-3 py-1.5 rounded-lg border border-gray-200 text-gray-600
        hover:bg-gray-50">Next</button>
    </div>
  </div>
</div>
```

### Table Design Rules
- Align numbers right, text left.
- Use row hover highlight (`hover:bg-gray-50`).
- Sticky header on scroll (`sticky top-0`).
- Zebra striping is optional; subtle dividers are preferred.
- Row actions: icon button (three dots) that opens a dropdown.

---

## 5. Status Indicators

### Badge Styles
```html
<!-- Success / Active -->
<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs
  font-medium bg-emerald-50 text-emerald-700">
  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>Active
</span>

<!-- Warning / Pending -->
<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs
  font-medium bg-amber-50 text-amber-700">
  <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>Pending
</span>

<!-- Error / Failed -->
<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs
  font-medium bg-red-50 text-red-700">
  <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>Failed
</span>

<!-- Neutral / Draft -->
<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs
  font-medium bg-gray-100 text-gray-600">
  <span class="w-1.5 h-1.5 rounded-full bg-gray-400"></span>Draft
</span>
```

### Progress Bars
```html
<div class="w-full bg-gray-100 rounded-full h-2">
  <div class="bg-indigo-600 h-2 rounded-full transition-all duration-500"
    style="width: 65%"></div>
</div>
```

---

## 6. Dark Mode Dashboard

Dashboards often look better in dark mode — it reduces eye strain for data-heavy views.

### Surface Hierarchy (Dark)
```css
:root[data-theme="dark"] {
  --bg-base: oklch(15% 0.01 265);      /* page background */
  --bg-surface: oklch(20% 0.01 265);   /* cards */
  --bg-elevated: oklch(25% 0.01 265);  /* dropdowns, modals */
  --border: oklch(30% 0.01 265);       /* borders */
  --text-primary: oklch(95% 0 0);      /* headings */
  --text-secondary: oklch(70% 0 0);    /* body text */
  --text-muted: oklch(50% 0 0);        /* captions */
}
```

### Rules
- Elevation is shown through lighter surfaces, not shadows.
- Reduce chart color saturation by ~15%.
- Use semi-transparent borders (`oklch(100% 0 0 / 0.08)`).
- Active sidebar item: lighter background, not colored.

---

## 7. Real-Time Data Indicators

### Live Pulse Dot
```html
<span class="relative flex h-2.5 w-2.5">
  <span class="animate-ping absolute inline-flex h-full w-full rounded-full
    bg-emerald-400 opacity-75"></span>
  <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
</span>
```

### Last Updated Timestamp
```html
<span class="text-xs text-gray-400 flex items-center gap-1.5">
  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
  Live — Updated 3s ago
</span>
```

### Auto-Refresh Pattern
- Show a subtle countdown or progress bar before refresh.
- Animate changed values (flash green for increase, red for decrease).
- Never refresh the entire page — update individual data points.

---

## 8. Dense Information Without Clutter

### Techniques
1. **Progressive disclosure**: Show summary, expand for details.
2. **Tabbed sections**: Don't show everything at once.
3. **Collapsible panels**: Let users hide what they don't need.
4. **Tooltips over labels**: Save space, add context on hover.
5. **Consistent spacing**: Use a strict 4px grid (4, 8, 12, 16, 24, 32, 48).
6. **Smaller base font**: Dashboard body text can be 13–14px.
7. **Monospace for data**: Numbers in tables use tabular-nums.

```css
.data-table td {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}
```

---

## 9. Responsive Dashboard Layouts

### Breakpoint Strategy
- **Mobile (< 768px)**: Single column. Cards stack. Tables become card lists. Sidebar hidden.
- **Tablet (768–1024px)**: 2-column grid. Sidebar collapsed to icons. Simplified charts.
- **Desktop (1024px+)**: Full layout. Sidebar expanded. Multi-column grids.
- **Wide (1536px+)**: Add extra column or widen content area. Don't stretch beyond 1440px max.

### Mobile Table Alternative
On mobile, convert tables to stacked cards:
```html
<!-- Desktop: table row -->
<!-- Mobile: card with label-value pairs -->
<div class="sm:hidden bg-white rounded-xl border border-gray-200 p-4 space-y-2">
  <div class="flex justify-between">
    <span class="text-gray-500 text-sm">Customer</span>
    <span class="font-medium text-gray-900 text-sm">Jane Cooper</span>
  </div>
  <div class="flex justify-between">
    <span class="text-gray-500 text-sm">Status</span>
    <span class="bg-emerald-50 text-emerald-700 text-xs px-2 py-0.5 rounded-full">Active</span>
  </div>
  <div class="flex justify-between">
    <span class="text-gray-500 text-sm">Amount</span>
    <span class="font-medium text-gray-900 text-sm">$2,500.00</span>
  </div>
</div>
```

---

## Dashboard Design Checklist

- [ ] Sidebar navigation with clear active state and section grouping
- [ ] KPI cards at top with trend indicators
- [ ] Charts have titles, labels, and tooltips
- [ ] Tables have sort, search, filter, and pagination
- [ ] Status badges use consistent color coding
- [ ] Responsive: works on tablet and mobile
- [ ] Loading skeletons for all async data
- [ ] Empty states for tables and charts with no data
- [ ] Dark mode considered (especially for monitoring dashboards)
- [ ] Numbers use tabular-nums for alignment
