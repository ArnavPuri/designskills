---
name: social-media-graphic
description: >
  Platform-specific social media graphic design via AI image generation and code generation.
  Generates correctly-sized visuals for Instagram, Twitter/X, LinkedIn, Facebook, Pinterest,
  and TikTok. Supports Gemini 3.1 Flash Image Preview for AI-generated graphics.
  Trigger phrases: "create a social media post", "design an Instagram graphic",
  "make a Twitter image", "LinkedIn post graphic", "social media design",
  "Instagram story", "carousel design", "social graphic".
license: MIT
---

# Social Media Graphic Design

Generate platform-perfect social media graphics with correct dimensions, safe zones, and platform-specific design patterns. Every graphic is output as production-ready HTML/CSS.

---

## Step 1: Load Design Context

1. Read `.agents/design-context.md` for brand colors, fonts, style
2. If missing, prompt user to run `design-context` skill or use defaults
3. Social media graphics must be strongly on-brand -- consistency builds recognition

---

## Gemini 3.1 Flash Image Preview

For AI image generation, see the `image-generation` skill for the full Gemini pipeline. Below are domain-specific prompt patterns for this skill.

### Example Prompts

- **Instagram Post:** "Create a square Instagram post graphic for [brand]. [product] centered on [color] gradient. Bold [font-style] text '[headline]'. Clean, modern aesthetic."
- **Instagram Story:** "Create a vertical story graphic (9:16) for [brand]. [product/subject] as the focal point with [color scheme] background. Text '[headline]' at top, swipe-up CTA '[action]' at bottom. Trendy, editorial style."
- **LinkedIn Post:** "Create a professional LinkedIn post graphic (1200x627) for [brand]. [topic/statistic] visualized with [chart type or icon]. Headline '[text]' in [font-style]. Corporate blue tones, clean data-driven layout."

---

## Step 2: Identify Platform and Format

### Platform Dimensions Reference

#### Instagram
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Feed Post (Square) | 1080 x 1080 | 1:1 | Standard post |
| Feed Post (Portrait) | 1080 x 1350 | 4:5 | Maximum feed real estate |
| Feed Post (Landscape) | 1080 x 566 | 1.91:1 | Panoramic content |
| Story / Reel Cover | 1080 x 1920 | 9:16 | Full-screen vertical |
| Carousel Slide | 1080 x 1080 | 1:1 | Multi-slide posts |
| Profile Picture | 320 x 320 | 1:1 | Circular crop |

#### Twitter / X
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| In-Feed Image | 1200 x 675 | 16:9 | Standard post image |
| Header / Banner | 1500 x 500 | 3:1 | Profile header |
| Card Image | 1200 x 628 | 1.91:1 | Link preview |

#### LinkedIn
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Feed Post | 1200 x 627 | 1.91:1 | Standard post |
| Feed Post (Square) | 1200 x 1200 | 1:1 | Square post |
| Banner | 1128 x 191 | ~5.9:1 | Profile/company banner |
| Article Cover | 1200 x 644 | 1.86:1 | Article header |

#### Facebook
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Feed Post | 1200 x 630 | 1.91:1 | Standard post |
| Cover Photo | 820 x 312 | 2.63:1 | Page cover |
| Event Cover | 1920 x 1005 | 1.91:1 | Event banner |
| Story | 1080 x 1920 | 9:16 | Story format |

#### Pinterest
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Standard Pin | 1000 x 1500 | 2:3 | Optimal engagement |
| Long Pin | 1000 x 2100 | 1:2.1 | Infographic-style |
| Square Pin | 1000 x 1000 | 1:1 | Alternative format |

#### TikTok
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Video Cover | 1080 x 1920 | 9:16 | Thumbnail/cover |

---

## Step 3: Apply Safe Zones

Every platform has areas where UI elements overlap the content. Keep critical text and visuals inside these safe zones.

### Instagram Feed Post (1080 x 1080)
```
Safe zone: 60px padding on all sides
Bottom: keep text above 980px (like/comment bar overlap in previews)
Top: profile info can overlap top 40px in some views
```

### Instagram Story (1080 x 1920)
```
Top safe: 200px from top (status bar + story header)
Bottom safe: 280px from bottom (reply bar + swipe indicator)
Left/Right safe: 60px from edges
Content zone: 960w x 1440h centered
```

### Twitter/X (1200 x 675)
```
Safe zone: 40px padding all sides
Text should be centered -- edges may crop on mobile
Keep key content in center 1120 x 595
```

### LinkedIn (1200 x 627)
```
Safe zone: 50px padding all sides
Bottom-left: avoid -- engagement buttons overlap
Center the main message
```

### Facebook Cover (820 x 312)
```
Mobile safe zone: center 640 x 312 (edges hidden on mobile)
Profile photo overlaps bottom-left 170px area
Keep text center-right
```

### Pinterest Pin (1000 x 1500)
```
Top safe: 80px (pin title overlay)
Bottom safe: 100px (save button area)
Logo/branding: bottom 100px or top-left corner
```

---

## Step 4: Platform-Specific Design Trends

### Instagram
- Clean, editorial layouts with generous whitespace
- Muted color palettes with one pop of color
- Consistent carousel templates (same frame, changing content)
- Sans-serif typography dominates
- Photo-forward with text overlays at 60-80% opacity backgrounds
- Rounded corners on inner elements (12-16px radius)

### Twitter / X
- Bold, high-contrast designs (dark mode is common)
- Large readable text -- viewed at small sizes in feed
- Data visualizations and chart-style graphics perform well
- Thread-style sequential graphics
- Minimal decoration, content-forward

### LinkedIn
- Professional, corporate-leaning aesthetic
- Blue tones naturally blend with the platform
- Clean data presentation, statistics, and insights
- Headshot + quote format for thought leadership
- Subtle gradients rather than loud colors

### Facebook
- Warm, approachable design language
- Photo-centric with overlay text
- Event and community-focused layouts
- Cover photos should tell a story without text (text < 20% of area)
- Groups and communities prefer authentic over polished

### Pinterest
- Vertical format maximizes screen real estate
- Text overlay on lifestyle imagery
- Step-by-step tutorial formats
- List-style pins with clear numbered sections
- Warm, aspirational color palettes
- Bold, readable text at small sizes

### TikTok
- Bold, energetic, trend-driven
- High contrast for small-screen readability
- Emoji and casual typography
- Thumbnail must convey content in under 1 second

---

## Step 5: Template Structures

### Quote Post (Instagram 1080x1080)
```html
<div class="canvas" style="width:1080px;height:1080px;position:relative;overflow:hidden;
  background:linear-gradient(135deg, var(--primary), var(--secondary));
  display:flex;align-items:center;justify-content:center;padding:80px;">

  <div style="text-align:center;">
    <div style="font-size:72px;line-height:1.1;margin-bottom:8px;opacity:0.3;
      font-family:Georgia,serif;">"</div>
    <p style="font-family:var(--font-heading);font-size:42px;font-weight:700;
      color:#fff;line-height:1.3;text-wrap:balance;">
      The quote text goes here, keep it under 120 characters for readability.
    </p>
    <div style="margin-top:40px;display:flex;align-items:center;justify-content:center;gap:12px;">
      <div style="width:40px;height:2px;background:rgba(255,255,255,0.5);"></div>
      <span style="font-family:var(--font-body);font-size:18px;color:rgba(255,255,255,0.8);
        text-transform:uppercase;letter-spacing:0.1em;">Author Name</span>
      <div style="width:40px;height:2px;background:rgba(255,255,255,0.5);"></div>
    </div>
  </div>
</div>
```

### Announcement Post (LinkedIn 1200x627)
```
Layout structure:
- Left 60%: Headline (bold, 48px) + Body text (20px) + CTA badge
- Right 40%: Visual element (icon, illustration, or abstract shape)
- Top bar: Brand color accent line (4px)
- Bottom: Logo + URL in small text
- Background: White or very light neutral
```

### Tip Carousel (Instagram 1080x1080, multi-slide)
```
Slide 1 (Cover):
- Bold headline: "5 Tips for [Topic]"
- Subtext: "Swipe to learn more →"
- Eye-catching gradient or image background
- Brand logo bottom-center

Slides 2-6 (Content):
- Tip number: large, semi-transparent in background (like "01")
- Tip headline: 32px bold
- Tip description: 20px, 2-3 lines max
- Consistent background across all slides
- Progress indicator dots at bottom

Slide 7 (CTA):
- "Found this helpful?"
- Follow CTA + handle
- Share/save prompt
- Brand logo
```

### Before/After (Instagram 1080x1350)
```
Layout:
- Top half: "Before" label + image/state
- Divider: thin line or diagonal cut with label
- Bottom half: "After" label + image/state
- Keep dimensions equal for both halves
- Use subtle color shift (gray/muted for before, vibrant for after)
```

### Data/Stat Post (Twitter 1200x675)
```
Layout:
- Large number: 72-96px, bold, gradient or accent color
- Context line: 24px below the number
- Supporting text: 18px, 2 lines max
- Source attribution: 14px, bottom-right
- Background: clean gradient or subtle pattern
- Brand mark: small, bottom-left
```

---

## Step 6: Carousel Design System

For multi-slide carousels, maintain consistency:

```css
/* Shared carousel variables */
:root {
  --slide-bg: #0F172A;
  --slide-text: #F8FAFC;
  --slide-accent: #6366F1;
  --slide-padding: 80px;
  --slide-radius: 0; /* carousels are edge-to-edge */
}

/* Consistent header bar across slides */
.slide-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--slide-accent);
}

/* Progress indicator */
.progress-dots {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}
.progress-dots .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
}
.progress-dots .dot.active {
  background: var(--slide-accent);
  width: 24px;
  border-radius: 4px;
}

/* Swipe hint on first slide */
.swipe-hint {
  position: absolute;
  right: 40px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  writing-mode: vertical-rl;
  opacity: 0.6;
}
```

---

## Step 7: Engagement Optimization

### Text Readability Rules
- **Maximum 6 words per line** for headlines on social
- **Maximum 3 lines** for any text block on a social graphic
- **Minimum font size:** 24px for Instagram, 20px for Twitter/LinkedIn
- **Contrast:** white text on dark overlay OR dark text on light overlay, never mid-tone on mid-tone

### Attention-Grabbing Techniques
1. **Asymmetric layouts** -- break the grid slightly for visual tension
2. **One bold color** against a muted palette
3. **Oversized numbers or single words** as anchors
4. **Negative space** that frames the message
5. **Diagonal elements** that create movement
6. **Border or frame** around the canvas edge (8-12px inset)

### Platform-Specific CTAs
- Instagram: "Save this for later", "Share to your story", "Double tap if you agree"
- Twitter: "RT if you agree", "Reply with your take", "Bookmark this thread"
- LinkedIn: "Agree? Share your perspective below", "Follow for more insights"
- Pinterest: "Save this pin", "Click through for the full guide"

---

## Step 8: Output Production-Ready Code

Generate the graphic as a self-contained HTML file. Include:

1. Correct `width` and `height` on the canvas element
2. Google Fonts loaded via `<link>` tag
3. All colors from design-context
4. CSS custom properties for easy adjustment
5. Comments marking editable sections (text, colors, images)

### Exporting Tips

Include a comment in the output:
```html
<!-- To export as an image:
     1. Open this file in a browser
     2. Use browser DevTools > screenshot (Cmd+Shift+P > "Capture node screenshot")
     3. Or use a tool like html2canvas, Puppeteer, or Screenshot API
     4. Verify dimensions match the target platform -->
```

---

## Quality Checklist

- [ ] Dimensions exactly match the target platform
- [ ] Text is within safe zones
- [ ] Font size is readable at the platform's display size
- [ ] Brand colors and fonts are applied consistently
- [ ] Visual hierarchy is clear -- one focal point
- [ ] No text-heavy areas (social graphics are visual-first)
- [ ] CTA or action prompt is included where appropriate
- [ ] Code is self-contained with no external dependencies except fonts
