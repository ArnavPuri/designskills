---
name: image-generation
description: >
  Foundational skill for AI-powered image generation using Gemini 3.1 Flash Image Preview.
  Handles text-to-image, image editing, multi-turn refinement, and batch generation.
  Trigger phrases: "generate an image", "create an image", "AI image", "Gemini image",
  "generate with Gemini", "image generation", "product image to graphic".
license: MIT
---

# Image Generation with Gemini 3.1 Flash

Foundational skill for generating and editing images using Google's Gemini 3.1 Flash Image Preview model. All graphic design skills reference this skill for the generation pipeline.

---

## Prerequisites

```bash
pip install google-genai Pillow
export GEMINI_API_KEY="your-api-key"
```

---

## Step 1: Choose Generation Mode

| Mode | When to Use | Input |
|------|-------------|-------|
| **Text-to-Image** | Creating from scratch — posters, graphics, illustrations | Text prompt only |
| **Image Edit** | Product shots, mockups, style transfer, adding elements | Image + text prompt |
| **Multi-Turn** | Iterative refinement, exploring variations | Chat session |
| **Batch** | High-volume asset generation (social sets, ad variants) | Multiple prompts via Batch API |

---

## Step 2: Build the Prompt

### Prompt Structure

Every prompt should follow this hierarchy:

```
[FORMAT] + [SUBJECT] + [STYLE] + [COMPOSITION] + [COLOR] + [TYPOGRAPHY] + [MOOD] + [NEGATIVE]
```

**Example — product social post:**
> Create a square social media graphic for a premium headphone launch.
> The headphones are centered on a deep navy (#0d1b2a) to electric blue (#00b4d8) diagonal gradient background.
> Bold white sans-serif text "HEAR EVERYTHING" spans the top third.
> Small coral (#ff6b6b) subtext "Available March 20" below.
> Subtle geometric triangles in the background at 10% opacity.
> Clean, modern, premium feel. No borders, no clip art.

### Key Principles

1. **Describe scenes, not keywords** — "A sneaker floating above a reflective surface with dramatic side lighting" beats "sneaker, cool, modern"
2. **Be specific about colors** — Always include hex codes from design context
3. **Describe spatial layout** — "headline in upper third, product centered, CTA in lower right"
4. **Name the style** — "flat vector", "3D render", "watercolor", "photorealistic", "minimalist Swiss design"
5. **Include typography instructions** — font style, size relationship, color, position
6. **State what to exclude** — "no stock photo watermarks, no beveled effects, no clipart"

### Style-Specific Prompt Patterns

| Style | Prompt Additions |
|-------|-----------------|
| **Minimalist** | "generous whitespace, single accent color, clean sans-serif, no decorative elements" |
| **Bold/Vibrant** | "saturated colors, large impactful typography, geometric shapes, high contrast" |
| **Luxurious** | "dark background, gold or champagne accents, serif typography, subtle texture, elegant" |
| **Playful** | "bright palette, rounded shapes, hand-drawn feel, casual handwriting font" |
| **Corporate** | "structured grid, professional, blue tones, clean hierarchy, balanced composition" |
| **Retro** | "halftone dots, muted vintage palette, serif headlines, film grain texture" |
| **Brutalist** | "raw, high contrast black and white, unconventional layout, oversized type" |

---

## Step 3: Generate

### Text-to-Image

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="[your structured prompt]",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    ),
)

for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save("output.png")
```

### Image Editing (Product Image → Graphic)

The core workflow: user provides a product photo, you generate a complete graphic around it.

```python
from PIL import Image

product = Image.open("product.png")

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[
        product,
        "Transform this product photo into a premium social media graphic. "
        "Place the product on a gradient background (#1a1a2e to #16213e). "
        "Add bold white headline 'JUST DROPPED' above. "
        "Add price '$299' in coral (#e94560) below. "
        "Modern, clean, high-end feel. Square format."
    ],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    ),
)
```

### Multi-Turn Refinement

```python
chat = client.chats.create(
    model="gemini-3.1-flash-image-preview",
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"]),
)

# Generate
r1 = chat.send_message([product_image, "Create a launch graphic for this product..."])
r1.parts[0].as_image().save("v1.png")

# Refine colors
r2 = chat.send_message("Make the background warmer, shift to sunset tones")
r2.parts[0].as_image().save("v2.png")

# Refine text
r3 = chat.send_message("Make the headline larger and add a subtle drop shadow")
r3.parts[0].as_image().save("v3.png")
```

### CLI Tool

```bash
# Text-to-image
python tools/gemini-generate.py --prompt "..." --output graphic.png

# Product image + prompt
python tools/gemini-generate.py --image product.png --prompt "..." --output graphic.png

# With aspect ratio
python tools/gemini-generate.py --prompt "..." --aspect-ratio 1:1 --output square.png

# Multi-turn
python tools/gemini-generate.py --prompt "Create a poster..." --output v1.png \
    --then "Change to dark mode" --output-then v2.png
```

---

## Step 4: Aspect Ratios

| Use Case | Ratio | Notes |
|----------|-------|-------|
| Instagram feed | 1:1 | Safe zone: keep text 100px from edges |
| Instagram story / Reels | 1:4 | Key content in center 60% |
| Twitter/X post | 16:9 | Text readable at small preview size |
| LinkedIn post | 4:3 | Professional, clean layouts |
| Facebook cover | 16:9 | Mobile crops to center |
| Pinterest pin | 1:4 | Vertical, scroll-stopping |
| YouTube thumbnail | 16:9 | High contrast, readable at 168x94px |
| Web banner (leaderboard) | 8:1 | Minimal text, strong CTA |
| Poster / flyer | 3:4 | Print-ready proportions |

---

## Step 5: Quality Checklist

Before delivering any generated image:

- [ ] Text is legible and spelled correctly (Gemini can render text — verify it)
- [ ] Colors match brand context (hex codes specified in prompt)
- [ ] Composition has clear visual hierarchy (one focal point)
- [ ] Sufficient contrast between text and background
- [ ] No unwanted artifacts or distortions
- [ ] Aspect ratio matches intended platform
- [ ] Product image (if used) is cleanly integrated, not distorted
- [ ] Overall aesthetic matches the requested style

If any check fails, use multi-turn refinement to fix specific issues.

---

## Reference: Model Capabilities

| Feature | Gemini 3.1 Flash |
|---------|-----------------|
| Max input images | 14 (10 objects + 4 characters) |
| Output resolutions | 512, 1K, 2K, 4K |
| Aspect ratios | 1:1, 16:9, 3:2, 4:3, 1:4, 4:1, 1:8, 8:1 |
| Text rendering | Supported (specify explicitly in prompt) |
| Thinking mode | On by default, improves complex compositions |
| Batch API | Supported for high-volume generation |
| Watermark | SynthID automatically applied |

---

## Integration with Other Skills

This skill is referenced by all graphic design skills:
- `graphic-design` → primary generation pipeline
- `social-media-graphic` → platform-specific generation
- `poster-design` → poster/flyer generation
- `thumbnail-design` → thumbnail generation
- `ad-creative-design` → ad variant generation
- `product-mockup` → product shot generation
- `banner-design` → banner generation
- `infographic` → infographic generation

Each skill adds domain-specific prompt patterns on top of this foundational generation workflow.
