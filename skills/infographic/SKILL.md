---
name: infographic
description: >
  Data visualization and infographic design via AI image generation and code generation.
  Process flows, comparison charts, statistics highlights, timelines, and SVG-based
  charts. Supports Gemini 3.1 Flash Image Preview.
  Trigger phrases: "create an infographic", "design a chart", "data visualization",
  "process flow", "comparison infographic", "timeline design", "stats graphic",
  "infographic design", "visualize data".
license: MIT
---

# Infographic Design

Create compelling data visualizations and infographics as HTML/CSS/SVG. Transform numbers, processes, and comparisons into visually engaging graphics.

---

## Step 1: Load Design Context

1. Read `.agents/design-context.md` for brand colors, fonts, style
2. If missing, ask user to run `design-context` skill or use defaults
3. Infographics rely heavily on a consistent color system for data categories

---

## Gemini 3.1 Flash Image Preview

For AI image generation, see the `image-generation` skill for the full Gemini pipeline. Below are domain-specific prompt patterns for this skill.

### Example Prompts

- **Statistics Infographic:** "Create an infographic showing [topic] statistics. [number] key metrics displayed as large numbers with icons. [color palette] color scheme. Clean grid layout with section headers. Professional, data-driven design."
- **Process Flow:** "Create a process flow infographic for [process name]. [number] steps connected by arrows. Each step has an icon, title, and one-line description. [color] gradient progression from start to finish. Vertical layout, modern style."
- **Timeline:** "Create a timeline infographic for [subject]. [number] milestones from [start year] to [end year]. Alternating left-right layout along a vertical line. [color palette]. Key dates and brief descriptions at each point."

---

## Step 2: Identify Infographic Type

| Type | Best For | Layout |
|------|----------|--------|
| **Process Flow** | Step-by-step procedures | Horizontal or vertical chain |
| **Comparison** | Two or more options | Columns or split layout |
| **Statistics** | Key numbers and metrics | Grid of stat cards |
| **Timeline** | Chronological events | Vertical or horizontal line |
| **List / Ranking** | Top N items | Numbered vertical list |
| **Data Chart** | Quantitative data | Bar, pie, line via SVG |
| **Icon Grid** | Category overview | Grid of icon + label pairs |

---

## Step 3: Color Coding System

Assign colors systematically. Never use random colors for data categories.

### Palette Types

```css
/* Sequential (ordered data) */
:root { --data-1: #EFF6FF; --data-2: #BFDBFE; --data-3: #60A5FA; --data-4: #2563EB; --data-5: #1E40AF; }

/* Categorical (distinct categories) */
:root { --cat-a: #6366F1; --cat-b: #EC4899; --cat-c: #F59E0B; --cat-d: #10B981; --cat-e: #8B5CF6; --cat-f: #EF4444; }

/* Diverging (positive/negative) */
:root { --neg-strong: #EF4444; --neg-light: #FCA5A5; --neutral: #E5E7EB; --pos-light: #86EFAC; --pos-strong: #22C55E; }
```

### Color Rules
- Use brand primary for the most important data point
- Use neutrals (gray scale) for context/baseline data
- Maintain at least 3:1 contrast between adjacent colors
- Maximum 6 distinct colors in a single chart

---

## Step 4: Process Flow Diagrams

### Horizontal Process Flow

```css
.process-flow { display: flex; align-items: flex-start; gap: 0; padding: 40px; }
.step { flex: 1; text-align: center; position: relative; padding: 0 20px; }
.step-icon {
  width: 48px; height: 48px; border-radius: 50%; background: var(--primary);
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 700; margin: 0 auto 16px; position: relative; z-index: 2;
}
.step-connector {
  position: absolute; top: 24px; left: calc(50% + 24px); right: calc(-50% + 24px);
  height: 2px; background: var(--primary); opacity: 0.3; z-index: 1;
}
.step:last-child .step-connector { display: none; }
```

### Vertical Process Flow
Use `flex-direction: column` with a `::before` pseudo-element as the connecting line (absolute positioned left of items).

---

## Step 5: Comparison Charts

### Side-by-Side Feature Comparison

```css
.comparison-table { width: 100%; border-collapse: separate; border-spacing: 0; }
.comparison-table thead th { padding: 20px; font-size: 18px; font-weight: 700; text-align: center; border-bottom: 2px solid #E5E7EB; }
.comparison-table thead th.highlighted { background: var(--primary); color: #fff; border-radius: 12px 12px 0 0; }
.comparison-table td { padding: 14px 20px; text-align: center; border-bottom: 1px solid #F3F4F6; font-size: 14px; }
.check { color: #22C55E; } .cross { color: #D1D5DB; }
```

### Versus Comparison
Use a three-column grid: `grid-template-columns: 1fr auto 1fr` with a large "VS" element centered between two option cards.

---

## Step 6: Statistics and Number Highlights

### Big Number Card

```css
.stat-card { text-align: center; padding: 32px; border-radius: 16px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
.stat-number {
  font-size: 56px; font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  line-height: 1; margin-bottom: 8px;
}
.stat-label { font-size: 14px; font-weight: 500; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.05em; }
```

### Progress Indicators

```css
/* Percentage bar */
.percent-bar { height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden; }
.percent-bar .fill { height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent)); border-radius: 4px; animation: fillBar 1.5s ease-out; }
@keyframes fillBar { from { width: 0; } }

/* Circular progress - use conic-gradient with --progress custom property */
.circle-progress {
  width: 120px; height: 120px; border-radius: 50%;
  background: conic-gradient(var(--primary) 0deg, var(--primary) calc(var(--progress) * 3.6deg), #E5E7EB calc(var(--progress) * 3.6deg));
  display: flex; align-items: center; justify-content: center;
}
```

---

## Step 7: Timeline Infographics

### Vertical Timeline

```css
.timeline { position: relative; padding: 20px 0; max-width: 600px; margin: 0 auto; }
.timeline::before {
  content: ''; position: absolute; left: 50%; top: 0; bottom: 0; width: 2px;
  background: linear-gradient(180deg, transparent, var(--primary), var(--primary), transparent);
  transform: translateX(-50%);
}
.timeline-item { display: flex; align-items: flex-start; margin-bottom: 40px; position: relative; }
.timeline-item:nth-child(odd) { padding-right: calc(50% + 30px); text-align: right; }
.timeline-item:nth-child(even) { flex-direction: row-reverse; padding-left: calc(50% + 30px); text-align: left; }
.timeline-dot {
  position: absolute; left: 50%; transform: translateX(-50%);
  width: 16px; height: 16px; border-radius: 50%; background: var(--primary);
  border: 3px solid var(--bg-color); z-index: 2;
}
.timeline-content { padding: 16px 20px; background: rgba(255,255,255,0.05); border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); }
```

### Horizontal Timeline
Use `display: flex` with a `::before` horizontal line. Each item has a dot and content below.

---

## Step 8: SVG-Based Charts

### Bar Chart
Use `<rect>` elements positioned on a y-axis baseline. Add `<animate>` for entrance animation on height/y attributes. Include `<text>` for axis labels and `<line>` for gridlines.

### Donut Chart
Use `<circle>` elements with `stroke-dasharray` and `stroke-dashoffset` to create segments. Transform with `rotate(-90)` to start from top. Add center `<text>` for the key metric.

### Line Chart
Use `<polyline>` for the data line, `<path>` with `fill` for the area beneath, and `<circle>` elements for data points. Add a `<linearGradient>` for the area fill.

Key pattern for all SVG charts:
```html
<svg viewBox="0 0 400 250" width="400" height="250" xmlns="http://www.w3.org/2000/svg">
  <!-- Grid lines, axes, labels -->
  <!-- Data elements with optional <animate> -->
  <!-- Gradient definitions in <defs> -->
</svg>
```

---

## Step 9: Icon-Driven Data Points

### Icon + Stat Layout

```css
.icon-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 32px; padding: 40px; }
.icon-stat { display: flex; align-items: flex-start; gap: 16px; }
.icon-stat .icon-circle {
  width: 48px; height: 48px; border-radius: 12px;
  background: rgba(var(--primary-rgb), 0.1); display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.icon-stat .value { font-size: 28px; font-weight: 800; line-height: 1; margin-bottom: 4px; }
.icon-stat .label { font-size: 13px; color: #6B7280; }
```

---

## Step 10: Infographic Layout Templates

### Long-Form Vertical
Width: 800px (web) or 1000px (print). Structure: Header > Section 1 > Divider > Section 2 > Divider > Section 3 > Takeaway > Footer. Use 60px spacing between sections.

### Dashboard-Style Grid

```css
.info-dashboard { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; padding: 40px; }
.info-dashboard .header { grid-column: 1 / -1; }
.info-dashboard .chart-main { grid-column: 1 / 3; }
.info-dashboard .chart-side { grid-column: 3; }
.info-dashboard .footer { grid-column: 1 / -1; }
```

---

## Quality Checklist

- Data is accurately represented (numbers match visuals)
- Color coding is consistent and meaningful (max 6 colors)
- Clear labels on all data points
- Visual hierarchy guides the reader through the information
- Source attribution included where appropriate
- Brand colors from design-context applied
- SVG charts have proper viewBox and are responsive
- Animations are subtle and enhance understanding
- Sufficient whitespace between sections
