---
name: design-context
description: >
  Foundational design context skill. Establishes brand identity, color system, typography,
  design style, and audience preferences. Trigger phrases: "set up design context",
  "define brand style", "configure design system", "brand guidelines", "design tokens",
  "style guide setup", "initialize design", "set brand colors".
license: MIT
---

# Design Context

The foundational skill for all design work. Every other design skill checks this context first. This skill gathers, stores, and serves brand identity, color systems, typography, and design preferences so that all generated visuals are cohesive and on-brand.

Context is saved to `.agents/design-context.md` for reuse across sessions.

---

## Step 1: Check for Existing Context

Before gathering new information, check for existing design context.

### Auto-Detection Sources

Scan the codebase for existing design tokens in this priority order:

1. **`.agents/design-context.md`** -- previously saved context (highest priority)
2. **`tailwind.config.js` / `tailwind.config.ts`** -- theme.extend.colors, fontFamily, spacing
3. **CSS custom properties** -- `--color-primary`, `--font-heading`, etc. in `:root` or `globals.css`
4. **`package.json`** -- project name, description
5. **Design token files** -- `tokens.json`, `theme.js`, `design-system.*`
6. **Existing components** -- scan for recurring color values, font stacks, spacing patterns
7. **`manifest.json` / `site.webmanifest`** -- theme_color, name
8. **Figma variables** -- if Figma MCP is available, pull variables from connected files

### Auto-Detection Logic

When scanning Tailwind config, extract:
```
colors.primary -> Brand primary color
colors.secondary -> Brand secondary color
colors.accent -> Accent color
fontFamily.sans -> Body font
fontFamily.heading or fontFamily.display -> Heading font
```

When scanning CSS variables, map:
```
--color-primary, --primary -> Primary color
--color-secondary, --secondary -> Secondary color
--color-accent, --accent -> Accent color
--font-heading, --font-display -> Heading font
--font-body, --font-sans -> Body font
--radius, --border-radius -> Border radius preference
```

If context is found, present it to the user for confirmation before proceeding.

---

## Step 2: Gather Brand Identity

If no existing context is found, gather the following conversationally. Ask in natural groupings, not as a checklist dump.

### Brand Core

| Field | Description | Example |
|-------|-------------|---------|
| Brand Name | Official name | "Acme Studio" |
| Tagline | Short brand tagline | "Design without limits" |
| Mission | One-sentence mission | "Empower creators with professional tools" |
| Industry | Primary industry/sector | "SaaS / Creative Tools" |

### Color System

Gather a minimum of 4 color groups. Store as hex codes.

| Role | Purpose | Example |
|------|---------|---------|
| Primary | Main brand color, CTAs, key UI | `#2563EB` |
| Primary Light | Hover states, backgrounds | `#3B82F6` |
| Primary Dark | Active states, text on light | `#1D4ED8` |
| Secondary | Supporting color, secondary actions | `#7C3AED` |
| Accent | Highlights, badges, notifications | `#F59E0B` |
| Neutral 50 | Lightest background | `#FAFAFA` |
| Neutral 100 | Card backgrounds | `#F5F5F5` |
| Neutral 200 | Borders, dividers | `#E5E5E5` |
| Neutral 500 | Placeholder text | `#737373` |
| Neutral 800 | Body text | `#262626` |
| Neutral 900 | Headings | `#171717` |
| Success | Positive states | `#10B981` |
| Warning | Caution states | `#F59E0B` |
| Error | Error states | `#EF4444` |

### Typography

| Field | Description | Example |
|-------|-------------|---------|
| Heading Font | Display/heading typeface | "Inter, sans-serif" |
| Body Font | Body text typeface | "Inter, sans-serif" |
| Mono Font | Code/technical typeface | "JetBrains Mono, monospace" |
| Base Size | Root font size | 16px |
| Scale Ratio | Type scale multiplier | 1.25 (Major Third) |
| Heading Weight | Default heading weight | 700 |
| Body Weight | Default body weight | 400 |

#### Type Scale Reference

Use this scale system (base 16px, ratio 1.25):
```
xs:   12px / 0.75rem
sm:   14px / 0.875rem
base: 16px / 1rem
lg:   18px / 1.125rem
xl:   20px / 1.25rem
2xl:  24px / 1.5rem
3xl:  30px / 1.875rem
4xl:  36px / 2.25rem
5xl:  48px / 3rem
6xl:  60px / 3.75rem
7xl:  72px / 4.5rem
```

### Design Style

Identify the primary style from these archetypes:

| Style | Characteristics |
|-------|----------------|
| **Minimal** | Generous whitespace, restrained palette, clean lines, subtle shadows |
| **Bold** | Saturated colors, large typography, strong contrast, geometric shapes |
| **Playful** | Bright colors, rounded corners, illustrations, casual tone |
| **Corporate** | Structured grids, blue/gray palette, professional imagery, formal |
| **Luxurious** | Dark backgrounds, metallic accents, serif fonts, fine details |
| **Retro** | Vintage palettes, halftone textures, serif/slab type, warm tones |
| **Brutalist** | Raw aesthetic, high contrast, monospace type, unconventional layout |
| **Organic** | Earth tones, natural textures, flowing shapes, warm neutrals |

### Audience and Tone

| Field | Description | Example |
|-------|-------------|---------|
| Primary Audience | Who sees these designs | "Tech-savvy professionals 25-40" |
| Aesthetic Preferences | What resonates with them | "Clean, modern, data-driven" |
| Tone | Communication style | "Professional but approachable" |
| Formality | Scale of 1-5 | 3 (balanced) |

### Brand Marks

| Field | Description | Example |
|-------|-------------|---------|
| Logo Description | Describe the logo visually | "Geometric 'A' mark in primary blue" |
| Logo Usage | Where/how to use it | "Top-left, min 32px height" |
| Icon Style | Preferred icon style | "Outlined, 2px stroke, rounded caps" |

### Platform Preferences

| Platform | Priority | Notes |
|----------|----------|-------|
| Web | High/Medium/Low | Responsive, modern browsers |
| Mobile | High/Medium/Low | Touch-friendly, safe areas |
| Print | High/Medium/Low | CMYK considerations |
| Social | High/Medium/Low | Platform-specific sizes |

---

## Step 3: Save Context

Save the gathered context to `.agents/design-context.md` using this template:

```markdown
# Design Context

## Brand Identity
- **Name:** [Brand Name]
- **Tagline:** [Tagline]
- **Mission:** [Mission]
- **Industry:** [Industry]

## Color System
| Role | Hex | Usage |
|------|-----|-------|
| Primary | #XXXXXX | CTAs, key elements |
| Primary Light | #XXXXXX | Hover, backgrounds |
| Primary Dark | #XXXXXX | Active, dark text |
| Secondary | #XXXXXX | Supporting elements |
| Accent | #XXXXXX | Highlights, badges |
| Neutral 50 | #XXXXXX | Light backgrounds |
| Neutral 100 | #XXXXXX | Card backgrounds |
| Neutral 200 | #XXXXXX | Borders |
| Neutral 500 | #XXXXXX | Muted text |
| Neutral 800 | #XXXXXX | Body text |
| Neutral 900 | #XXXXXX | Headings |
| Success | #XXXXXX | Positive |
| Warning | #XXXXXX | Caution |
| Error | #XXXXXX | Error |

## Typography
- **Heading Font:** [Font stack]
- **Body Font:** [Font stack]
- **Mono Font:** [Font stack]
- **Base Size:** [size]
- **Scale Ratio:** [ratio]
- **Heading Weight:** [weight]
- **Body Weight:** [weight]

## Design Style
- **Primary Style:** [Style archetype]
- **Border Radius:** [value]
- **Shadow Style:** [subtle/medium/dramatic/none]
- **Spacing System:** [4px/8px base grid]

## Audience
- **Primary:** [Description]
- **Aesthetic:** [Preferences]
- **Tone:** [Tone description]

## Brand Marks
- **Logo:** [Description]
- **Icon Style:** [Description]

## Platform Priority
- Web: [priority]
- Mobile: [priority]
- Social: [priority]
- Print: [priority]
```

---

## Step 4: Using Context in Other Skills

When any other design skill activates, it must:

1. Read `.agents/design-context.md` first
2. Apply the color system -- never use arbitrary colors
3. Use the specified typography -- load Google Fonts if needed via `<link>` tag
4. Match the design style archetype
5. Respect the tone and audience preferences

### Quick Context Snippet for Other Skills

Other skills should include this check at the top of their workflow:

```
Before generating any visual:
1. Read .agents/design-context.md
2. Extract: primary color, secondary color, accent, heading font, body font, style archetype
3. If no context file exists, ask the user to run the design-context skill first,
   or use sensible defaults and note that output may not be on-brand
```

---

## Step 5: Context Updates

When the user wants to update context:

1. Read the existing `.agents/design-context.md`
2. Ask what they want to change
3. Update only the changed fields
4. Confirm the changes
5. Save the updated file

Never overwrite the entire file for a single field change.

---

## Default Fallbacks

If no context is set and the user wants to proceed anyway, use these defaults:

```
Primary: #2563EB (blue-600)
Secondary: #7C3AED (violet-600)
Accent: #F59E0B (amber-500)
Neutral: Tailwind gray scale
Heading Font: Inter
Body Font: Inter
Style: Minimal
Tone: Professional
```

Always note in the output that defaults were used and recommend setting up proper design context.
