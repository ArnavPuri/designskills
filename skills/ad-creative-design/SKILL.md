---
name: ad-creative-design
description: >
  Ad banners and display ad creative design via AI image generation and code generation.
  Covers IAB standard sizes, CTA design, value proposition hierarchy, A/B variations,
  and HTML5 animated ads. Supports Gemini 3.1 Flash Image Preview.
  Trigger phrases: "design an ad", "create a banner ad", "display ad",
  "ad creative", "Google Display ad", "Meta ad", "ad banner",
  "create ad variations", "HTML5 ad".
license: MIT
---

# Ad Creative Design

Design high-converting ad banners and display creatives. Covers all standard IAB sizes, platform requirements, CTA optimization, and A/B testing frameworks. Output as production-ready HTML/CSS with optional animation.

---

## Step 1: Load Design Context

1. Read `.agents/design-context.md` for brand colors, fonts, style
2. If missing, ask user to run `design-context` skill or use defaults
3. Ad creatives must be strictly on-brand -- ads are often the first brand touchpoint

---

## Gemini 3.1 Flash Image Preview

For AI image generation, see the `image-generation` skill for the full Gemini pipeline. Below are domain-specific prompt patterns for this skill.

### Example Prompts

- **Display Ad:** "Create a display ad ([size]). [product/service] visual on [background]. Headline '[text]' in [style]. CTA button '[action]' in [color]. Clean, conversion-focused layout."
- **Social Ad:** "Create a Meta feed ad (1080x1080). [product] photo centered on [background color]. Short headline '[value prop]' above. CTA '[action]' button at bottom in [brand color]. Minimal text, bold imagery."
- **Retargeting Banner:** "Create a 728x90 leaderboard ad. Logo left, '[offer headline]' center in [font-weight] [font-family], CTA '[action]' right in [accent color] pill button. [brand color] background. Urgency-driven."

---

## Step 2: Identify Ad Format and Size

### Standard IAB Ad Sizes

| Name | Dimensions | Type | Performance |
|------|-----------|------|-------------|
| Medium Rectangle | 300 x 250 | Display | Highest inventory |
| Large Rectangle | 336 x 280 | Display | High performance |
| Leaderboard | 728 x 90 | Display | Top of page |
| Mobile Leaderboard | 320 x 50 | Mobile | Mobile standard |
| Large Mobile | 320 x 100 | Mobile | Better engagement |
| Wide Skyscraper | 160 x 600 | Display | Sidebar |
| Half Page | 300 x 600 | Display | High impact |
| Billboard | 970 x 250 | Display | Premium placement |
| Large Leaderboard | 970 x 90 | Display | Wide format |
| Square | 250 x 250 | Display | Compact |

### Social Ad Sizes

| Platform | Format | Dimensions |
|----------|--------|-----------|
| Meta (Feed) | Single Image | 1080 x 1080 or 1200 x 628 |
| Meta (Story) | Full Screen | 1080 x 1920 |
| Google Display | Responsive | Multiple (provide assets) |
| LinkedIn | Sponsored Content | 1200 x 627 |
| Twitter/X | Promoted | 1200 x 675 |

---

## Step 3: Ad Content Hierarchy

Every ad must follow this strict content hierarchy. Limited space means ruthless prioritization.

### The AIDA Framework for Ads

1. **Attention** -- Visual hook (image, color, animation)
2. **Interest** -- Value proposition (what is it, why care)
3. **Desire** -- Benefit statement (what they get)
4. **Action** -- CTA button (what to do next)

### Content Priority by Size

#### Large Formats (300x600, 970x250, 300x250)
```
1. Logo (small, top-left or top-center)
2. Hero image or visual
3. Headline (primary value prop, 5-8 words max)
4. Supporting text (1 line, optional)
5. CTA button
```

#### Medium Formats (728x90, 320x100)
```
1. Logo (left side, compact)
2. Headline (3-5 words)
3. CTA button (right side)
-- No room for supporting text or large visuals
```

#### Small Formats (320x50, 160x600 narrow area)
```
1. Logo or brand name (text only)
2. Headline (2-4 words)
3. CTA (text link or small button)
```

---

## Step 4: CTA Button Design

The CTA is the most important element. It must be unmissable.

### CTA Button Styles

Use one of three patterns: **solid** (high-contrast fill + shadow), **outline** (transparent bg + border), or **pill** (rounded + arrow icon). Key properties:
- `padding: 10-12px 24-28px`, `font-weight: 700`, `text-transform: uppercase`
- Add hover: `translateY(-1px)` + increased shadow or background swap
- Pill variant: `border-radius: 50px` with `::after` arrow content

### CTA Copy Best Practices

| Weak | Strong | Why |
|------|--------|-----|
| Submit | Get Started | Action-oriented |
| Click Here | Shop the Sale | Specific benefit |
| Learn More | See How It Works | Curiosity-driven |
| Buy Now | Claim Your 20% Off | Value-driven |
| Sign Up | Start Free Trial | Low commitment |
| Download | Get Your Free Guide | Ownership language |

### CTA Placement Rules
- **300x250:** Bottom-center or bottom-right
- **728x90:** Right side, vertically centered
- **160x600:** Bottom-center
- **320x50:** Right side
- Always leave at least 8px padding around the CTA
- CTA should occupy 15-25% of the total ad width

---

## Step 5: Value Proposition Framework

### Headline Formulas

1. **Benefit-first:** "Save 3 Hours Every Week"
2. **Problem-solution:** "Tired of [Problem]? Try [Product]"
3. **Social proof:** "Join 50,000+ [Users] Who..."
4. **Urgency:** "Last Day: 40% Off Everything"
5. **Curiosity:** "The [Tool] Top Companies Use for [Result]"
6. **Numbers:** "3x Faster [Task] Starting Today"

### Copy Constraints by Size

| Size | Headline Max | Body Max | CTA Max |
|------|-------------|----------|---------|
| 300x250 | 8 words | 12 words | 3 words |
| 728x90 | 5 words | 0 (no room) | 2 words |
| 160x600 | 6 words | 10 words | 2 words |
| 300x600 | 8 words | 15 words | 3 words |
| 320x50 | 4 words | 0 | 2 words |

---

## Step 6: Layout Templates by Size

### Layout Patterns by Size

- **300x250**: Flex column. Logo top (12px padding), visual area (flex:1), content bottom (16px padding, centered). Headline 18px/700.
- **728x90**: Flex row, `align-items: center`, 20px gap. Logo left (28px height), headline (flex:1, 20px/700), CTA right.
- **160x600**: Flex column, centered text. Logo top, visual middle (flex:1), headline 16px/700, body 12px, CTA at bottom (`margin-top: auto`).
- **320x50**: Flex row on brand-color bg. Text (flex:1, 13px/700 white), CTA right (white bg, brand-color text, 6px 14px padding).

All sizes: `position: relative; overflow: hidden; border: 1px solid #E5E7EB;`

---

## Step 7: A/B Testing Variation Framework

Always generate at least 2 variations when possible. Test these dimensions:

### Variation Axes

| Axis | Variation A | Variation B |
|------|------------|------------|
| **Headline** | Benefit-focused | Urgency-focused |
| **CTA Color** | Brand primary | High-contrast accent |
| **CTA Copy** | "Get Started" | "Try Free" |
| **Layout** | Image top, text bottom | Text left, image right |
| **Background** | Light/white | Dark/brand color |
| **Visual** | Product screenshot | Abstract/lifestyle |

### Generating Variations

When creating an ad, produce:
- **Version A:** The primary design
- **Version B:** Same content, one variable changed (CTA color, headline, or layout)

Label each variation clearly in the output:
```html
<!-- VARIATION A: Benefit headline, primary CTA -->
<div class="ad variation-a">...</div>

<!-- VARIATION B: Urgency headline, accent CTA -->
<div class="ad variation-b">...</div>
```

---

## Step 8: Platform-Specific Requirements

### Google Display Network
- File size: max 150KB (HTML5), images under 150KB each
- Animation: max 30 seconds, max 3 loops
- Must include a visible border (1px solid #ccc if background is white)
- Click area must cover the entire ad
- No auto-playing audio

### Meta (Facebook/Instagram) Ads
- Text on image: keep under 20% of the image area (not enforced but affects delivery)
- Primary text: 125 characters
- Headline: 40 characters
- Square (1:1) and vertical (4:5) perform best on mobile
- Video thumbnails follow same rules

### LinkedIn Ads
- Professional tone -- avoid clickbait
- Statistics and data-driven headlines perform well
- Blue tones blend with platform; use contrasting colors
- Company logo must be visible

### Programmatic Display
- Must degrade gracefully (backup static image)
- All assets loaded from relative paths or data URIs
- Click tag implementation required

```html
<!-- Standard click tag -->
<script>
var clickTag = "https://example.com";
</script>
<a href="javascript:void(window.open(clickTag))" style="position:absolute;inset:0;z-index:999;">
</a>
```

---

## Step 9: HTML5 Animation for Ads

### Animation Patterns

**Staggered entry**: Use `fadeSlideIn` (opacity 0->1, translateY 10px->0) with 0.2s staggered delays for logo, visual, headline, CTA. Add a subtle `ctaPulse` (scale 1->1.03) after entry completes.

**Multi-frame rotation**: Position frames absolutely, use a shared `@keyframes frame` with opacity in/out, stagger by `total-duration / num-frames`. Max 3 frames over 10-15s.

### Animation Guidelines
- Total animation: 15-30 seconds max, max 3 loops
- End on a static frame with CTA visible
- No more than 3 frames/scenes
- Avoid fast flashing (accessibility)
- Final frame must show: headline + CTA + logo

---

## Step 10: Ad Border and Container

Every display ad needs a clear boundary:

- `border: 1px solid #E5E7EB; border-radius: 0; overflow: hidden; position: relative;`
- Full-bleed click area: `position: absolute; inset: 0; z-index: 100; cursor: pointer;`

---

## Quality Checklist

- [ ] Dimensions exactly match the target ad size
- [ ] Clear visual hierarchy: Visual > Headline > CTA
- [ ] CTA is prominent and clearly clickable
- [ ] Copy is concise and within character limits
- [ ] Brand colors and fonts from design-context
- [ ] 1px border present (required for display ads)
- [ ] File size is reasonable (aim for under 150KB total)
- [ ] Animation (if any) ends on a static frame with visible CTA
- [ ] At least 2 variations provided for A/B testing
- [ ] No text below 10px font size
- [ ] Sufficient contrast ratios for accessibility
