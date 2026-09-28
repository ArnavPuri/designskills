---
name: dashboard-design
description: >
  Data dashboard and admin panel patterns for information-dense interfaces: app shell
  layout, KPI tiles, chart selection, data tables, status badges, real-time indicators,
  and responsive behavior. Use when the user asks to "build a dashboard", "create an admin
  panel", "design analytics", "make a data view", "build a settings page", "create a table
  view", "design a CRM", "build an internal tool", or any data-heavy interface work. For
  general components use ui-design; for marketing KPI/feature cards use card-design; for
  theming details use dark-mode.
license: MIT
---

# Dashboard Design

## Before You Start: Load Design Context

1. **Read `.agents/design-context.md`** (written by the `design-context` skill). If it is missing, look for tokens in `tailwind.config.*` or `:root` CSS variables. If nothing exists, use the defaults (Primary `#2563EB`, Secondary `#7C3AED`, Accent `#F59E0B`, Tailwind gray neutrals, Inter for headings and body, Minimal style) and **tell the user defaults were used** — suggest running `design-context`.
2. **Map tokens to CSS variables once**, then use only the variables: `--color-primary`, `--color-primary-light`, `--color-primary-dark`, `--color-secondary`, `--color-accent`, `--color-neutral-50`…`--color-neutral-900`, `--color-success`/`-warning`/`-error`, `--font-heading`, `--font-body`, `--font-mono`, `--radius`, and the 4px-base spacing scale.
3. **Tailwind:** expose the same variables (v3 `theme.extend`, v4 `@theme`) as `primary`, `primary-light`, `primary-dark`, `secondary`, `accent`, `neutral-*`, `font-heading`, `font-body`. The `indigo-*` / `gray-*` classes in the examples below are placeholders for these tokens.
4. **Figma:** if the user gives a Figma URL, pull it with the Figma MCP (`get_design_context`, `get_screenshot`) and match it; it overrides the context file for that design.
5. Ask or infer: what data is shown, who uses it, what actions they take? Map Success/Warning/Error to the status badges and derive chart colors from Primary/Secondary/Accent (section 3).

---

## 1. Layout Patterns

### Pattern A: Sidebar + Main Content (Most Common)

```html
<div class="flex h-screen bg-gray-50">
  <!-- Sidebar -->
  <!-- Hidden below lg; open as an overlay drawer via a menu button (see Sidebar Behavior) -->
  <aside class="hidden lg:flex w-64 shrink-0 bg-white border-r border-gray-200 flex-col">
    <!-- Logo -->
    <div class="h-16 flex items-center px-6 border-b border-gray-100">
      <img src="/logo.svg" alt="App" class="h-8" />
    </div>
    <!-- Navigation -->
    <nav aria-label="Main" class="flex-1 py-4 px-3 space-y-1 overflow-y-auto">
      <!-- Active item -->
      <a href="#" aria-current="page" class="flex items-center gap-3 px-3 py-2 rounded-lg
        bg-indigo-50 text-indigo-700 font-medium text-sm">
        <svg class="w-5 h-5" aria-hidden="true"><!-- icon --></svg>
        Dashboard
      </a>
      <!-- Inactive item -->
      <a href="#" class="flex items-center gap-3 px-3 py-2 rounded-lg
        text-gray-600 hover:bg-gray-100 hover:text-gray-900 text-sm transition-colors">
        <svg class="w-5 h-5" aria-hidden="true"><!-- icon --></svg>
        Analytics
      </a>
      <!-- Section header -->
      <div class="pt-4 pb-1 px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
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
  <main class="flex-1 min-w-0 overflow-y-auto">
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
- Mobile (< md): Hidden, opens as an overlay drawer with backdrop from a labelled menu button (`aria-expanded`, focus moved into the drawer, Esc closes).
- Breakpoints follow the Tailwind defaults in ui-design (md 768, lg 1024, xl 1280, 2xl 1536).

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
      <svg class="w-5 h-5" aria-hidden="true"><!-- dollar icon --></svg>
    </span>
  </div>
  <div class="mt-3">
    <span class="text-3xl font-bold text-gray-900">$45,231</span>
  </div>
  <div class="mt-2 flex items-center gap-1.5 text-sm">
    <span class="text-emerald-600 font-medium flex items-center gap-0.5">
      <svg class="w-4 h-4" aria-hidden="true"><!-- arrow-up icon --></svg>
      <span class="sr-only">Up</span> +12.5%
    </span>
    <span class="text-gray-500">vs last month</span>
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
- **Negative trend**: Use red with down-arrow and a minus sign — never color alone (color-blind users).
- Loading: show a skeleton tile of the same size, not a spinner, so the grid doesn't shift.

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
3. **Limit colors** to 5–6 max, derived from the brand tokens. Each series color needs 3:1 contrast against the chart background (WCAG 1.4.11); add direct labels or patterns so color isn't the only cue.
4. **Start Y-axis at zero** for bar charts. Line charts can have non-zero baselines.
5. **Add tooltips** for exact values on hover.
6. **Use grid lines sparingly** — light dashed lines, not solid.
7. **Responsive**: Charts should resize, not overflow.

### Chart Color Palette
```css
:root {
  /* Lightness ≤ ~65% keeps ≥ 3:1 against white; lighten ~10–15% for dark backgrounds */
  --chart-1: var(--color-primary);
  --chart-2: oklch(58% 0.12 185);  /* teal */
  --chart-3: oklch(58% 0.19 350);  /* pink */
  --chart-4: oklch(64% 0.15 60);   /* amber/orange */
  --chart-5: oklch(55% 0.14 145);  /* green */
}
```
If a data-visualization skill (such as dataviz) is installed, follow it for chart marks, legends, and tooltips.

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
      <input type="search" placeholder="Search orders…" aria-label="Search orders"
        class="text-sm border border-gray-300 rounded-lg px-3 py-1.5 w-full sm:w-56
        focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20" />
      <!-- Filter button -->
      <button type="button" class="text-sm text-gray-600 border border-gray-300 rounded-lg
        px-3 py-1.5 hover:bg-gray-50 flex items-center gap-1.5">
        <svg class="w-4 h-4" aria-hidden="true"><!-- filter icon --></svg>
        Filters
      </button>
    </div>
  </div>

  <!-- Table: horizontal scroll wrapper so wide tables never break the page -->
  <div class="overflow-x-auto">
  <table class="w-full text-sm">
    <caption class="sr-only">Recent orders</caption>
    <thead>
      <tr class="border-b border-gray-100 text-left">
        <th scope="col" aria-sort="ascending" class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
          <button type="button" class="flex items-center gap-1 hover:text-gray-700">
            Customer
            <svg class="w-3 h-3" aria-hidden="true"><!-- sort icon --></svg>
          </button>
        </th>
        <th scope="col" class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
          Status
        </th>
        <th scope="col" class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider
          text-right">
          Amount
        </th>
        <th scope="col" class="px-6 py-3 w-12"><span class="sr-only">Actions</span></th>
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
          <button type="button" aria-label="Actions for Jane Cooper" aria-haspopup="menu"
            class="p-1.5 rounded-md text-gray-500 hover:text-gray-700 hover:bg-gray-100">
            <svg class="w-5 h-5" aria-hidden="true"><!-- dots icon --></svg>
          </button>
        </td>
      </tr>
    </tbody>
  </table>
  </div>

  <!-- Pagination -->
  <nav aria-label="Pagination" class="px-6 py-4 border-t border-gray-100 flex items-center justify-between text-sm">
    <span class="text-gray-500">Showing 1-10 of 2,847</span>
    <div class="flex gap-1">
      <button class="px-3 py-1.5 rounded-lg border border-gray-200 text-gray-600
        hover:bg-gray-50 disabled:opacity-50" disabled>Previous</button>
      <button class="px-3 py-1.5 rounded-lg bg-indigo-600 text-white" aria-current="page">1</button>
      <button class="px-3 py-1.5 rounded-lg border border-gray-200 text-gray-600
        hover:bg-gray-50">2</button>
      <button class="px-3 py-1.5 rounded-lg border border-gray-200 text-gray-600
        hover:bg-gray-50">Next</button>
    </div>
  </nav>
</div>
```

### Table Design Rules
- Align numbers right, text left.
- Use row hover highlight (`hover:bg-gray-50`).
- Sticky header on scroll (`sticky top-0` on `<th>` with a solid background, or it shows rows through it).
- Sortable columns: `<button>` inside `<th>`, with `aria-sort` on the sorted column.
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

Monitoring and ops dashboards are often used in dark mode. Use the surface, text, and border tokens from the **dark-mode** skill's Complete Token System (`--bg-base` / `--bg-surface` / `--bg-elevated`, `--text-*`, `--border`) — don't define a second set here.

### Dashboard-Specific Rules
- Elevation is shown through lighter surfaces, not shadows.
- Reduce chart color saturation by ~15% and raise lightness so series still hit 3:1 on the dark surface.
- Use semi-transparent borders (`oklch(100% 0 0 / 0.08)`).
- Active sidebar item: lighter background, not colored.

---

## 7. Real-Time Data Indicators

### Live Pulse Dot
```html
<span class="relative flex h-2.5 w-2.5" aria-hidden="true">
  <span class="motion-safe:animate-ping absolute inline-flex h-full w-full rounded-full
    bg-emerald-400 opacity-75"></span>
  <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
</span>
```

### Last Updated Timestamp
```html
<span class="text-xs text-gray-500 flex items-center gap-1.5" role="status">
  <span class="w-1.5 h-1.5 rounded-full bg-emerald-500" aria-hidden="true"></span>
  Live — Updated 3s ago
</span>
```

### Auto-Refresh Pattern
- Show a subtle countdown or progress bar before refresh.
- Animate changed values (flash green for increase, red for decrease).
- Never refresh the entire page — update individual data points.
- Don't put fast-changing numbers in an `aria-live` region (it floods screen readers); announce only meaningful events (e.g. "3 new orders").

---

## 8. Dense Information Without Clutter

### Techniques
1. **Progressive disclosure**: Show summary, expand for details.
2. **Tabbed sections**: Don't show everything at once.
3. **Collapsible panels**: Let users hide what they don't need.
4. **Tooltips for extra context, not essential labels**: they must also open on keyboard focus and tap.
5. **Consistent spacing**: Use the 4px-base scale from ui-design (4, 8, 12, 16, 24, 32, 48, 64).
6. **Smaller base font**: Dashboard body text can be 13–14px (never below 12px).
7. **Tabular figures for data**: Numbers in tables and KPIs use `tabular-nums` so digits align.

```css
.data-table td {
  font-variant-numeric: tabular-nums; /* Tailwind: tabular-nums */
}
```

---

## 9. Responsive Dashboard Layouts

### Breakpoint Strategy
- **Mobile (< 768px)**: Single column. Cards stack. Tables become card lists. Sidebar hidden.
- **Tablet (768–1024px)**: 2-column grid. Sidebar collapsed to icons. Simplified charts.
- **Desktop (1024px+)**: Full layout. Sidebar expanded. Multi-column grids.
- **Wide (1536px+)**: Add an extra column rather than stretching; cap text-heavy content at ~1440px (`max-w-screen-2xl` or similar).

### Mobile Table Alternative
Below `md` (768px), hide the table (`hidden md:block` on its wrapper) and render each row as a card:
```html
<!-- Mobile only: one card per row, label-value pairs -->
<dl class="md:hidden bg-white rounded-xl border border-gray-200 p-4 space-y-2 text-sm">
  <div class="flex justify-between">
    <dt class="text-gray-500">Customer</dt>
    <dd class="font-medium text-gray-900">Jane Cooper</dd>
  </div>
  <div class="flex justify-between">
    <dt class="text-gray-500">Status</dt>
    <dd><span class="bg-emerald-50 text-emerald-700 text-xs px-2 py-0.5 rounded-full">Active</span></dd>
  </div>
  <div class="flex justify-between">
    <dt class="text-gray-500">Amount</dt>
    <dd class="font-medium text-gray-900">$2,500.00</dd>
  </div>
</dl>
```

---

## Verify: Render and Check

Don't hand over code you haven't looked at. After generating it:
1. Screenshot it at mobile and desktop widths, e.g. `npx playwright screenshot --full-page --viewport-size=390,844 file://$PWD/index.html mobile.png`, then again with `--viewport-size=1440,900` (or point at the dev server URL).
2. Open both images and check: no horizontal scroll or clipped/overlapping text, hierarchy reads at a glance, brand tokens are applied, images load at the right aspect ratio.
3. Tab through once: every interactive element gets a visible focus ring, in a logical order.
4. Also screenshot at 768px: sidebar collapses, tables scroll or become cards, charts resize instead of overflowing. Check the dark theme if you built one.
5. Fix what you find and re-screenshot before reporting done.

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
- [ ] Icon-only buttons and search inputs have accessible names; trends don't rely on color alone
- [ ] Rendered and screenshotted at 390px, 768px, and 1440px (see Verify)
