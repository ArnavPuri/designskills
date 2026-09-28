---
name: image-generation
description: >
  Foundational skill for AI-powered image generation using Gemini 3.1 Flash Image Preview.
  Handles text-to-image, image editing, multi-turn refinement, and batch generation. Use
  directly for one-off images; for posters, ads, thumbnails, social posts, etc. prefer the
  matching graphic design skill, which layers format-specific rules on top of this pipeline.
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

## Step 0: Load Brand Context

Read `.agents/design-context.md` if it exists and pull the hex colors, style archetype, and typography description into the prompt. If it doesn't exist, use the `design-context` defaults and tell the user the output isn't brand-matched yet. If the user has a logo or product photo, pass it as an `--image` reference rather than describing it — the model reproduces references far more faithfully than descriptions.

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
        image_config=types.ImageConfig(aspect_ratio="1:1", image_size="2K"),
    ),
)

# A response can contain text parts and image parts in any order —
# never assume parts[0] is the image.
def save_first_image(response, path):
    for part in response.parts or []:
        if part.inline_data is not None:
            part.as_image().save(path)
            return True
    print("No image returned:", response.text)  # usually a refusal or clarifying question
    return False

save_first_image(response, "output.png")
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
save_first_image(r1, "v1.png")

# Refine colors — change ONE thing per turn and say what to keep
r2 = chat.send_message("Keep the layout and text exactly as is. Make the background warmer, shift to sunset tones")
save_first_image(r2, "v2.png")

# Refine text
r3 = chat.send_message("Keep everything else. Make the headline larger and add a subtle drop shadow")
save_first_image(r3, "v3.png")
```

### CLI Tool

The skill ships its scripts in `scripts/`. Below, `<image-generation>` means this skill's directory (the base directory shown when the skill loads; `skills/image-generation` in a clone of the repo). Run them from the user's project so outputs land there.

```bash
# Text-to-image
python <image-generation>/scripts/gemini-generate.py --prompt "..." --output graphic.png

# Product image + prompt
python <image-generation>/scripts/gemini-generate.py --image product.png --prompt "..." --output graphic.png

# Multiple reference images (product + logo + style reference), up to 14
python <image-generation>/scripts/gemini-generate.py --image product.png --image logo.png --prompt "..." --output graphic.png

# Aspect ratio and resolution
python <image-generation>/scripts/gemini-generate.py --prompt "..." --aspect-ratio 4:5 --size 2K --output feed.png

# Exact pixel size: generate at the nearest supported ratio, then center-crop + resize
python <image-generation>/scripts/gemini-generate.py --prompt "..." --aspect-ratio 8:1 --resize 728x90 --output leaderboard.png

# Long prompts: keep them in a file
python <image-generation>/scripts/gemini-generate.py --prompt-file prompt.txt --aspect-ratio 16:9 --output hero.png

# Multi-turn (--then is repeatable; outputs default to v1_2.png, v1_3.png ...)
python <image-generation>/scripts/gemini-generate.py --prompt "Create a poster..." --output v1.png \
    --then "Change to dark mode" --then "Make the date larger"
```

The script exits non-zero when no image comes back (refusal, safety block, or the model answered with text only) and prints the model's text — read it, adjust the prompt, and retry.

### Exporting Many Sizes From One Master

```bash
# Social set, ad set, or named presets; --focus keeps the subject in frame (x,y as 0-1)
python <image-generation>/scripts/export-sizes.py master.png --group social --out exports/
python <image-generation>/scripts/export-sizes.py master.png --presets og,youtube-thumbnail --focus 0.5,0.4 --out exports/
python <image-generation>/scripts/export-sizes.py master.png --size 300x250 --size 728x90 --out ads/
python <image-generation>/scripts/export-sizes.py --list   # all presets and groups
```

It warns when a crop keeps under half of the master or has to upscale -- generate extreme ratios (8:1, 1:4) separately with the matching `--aspect-ratio` instead. Read a few exports to confirm nothing important was cropped.

---

## Step 4: Aspect Ratios

Supported ratios: `1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 1:4, 4:1, 1:8, 8:1`. Anything else (e.g. 300x250, 1200x628) must be generated at the nearest ratio and cropped with `--resize`.

| Use Case | Ratio | Final size | Notes |
|----------|-------|-----------|-------|
| Instagram feed (portrait) | 4:5 | 1080x1350 | Best feed real estate; grid preview crops to 3:4 center |
| Instagram feed (square) | 1:1 | 1080x1080 | Keep text ~100px from edges |
| Instagram / TikTok Story, Reels | 9:16 | 1080x1920 | Keep text out of top ~250px and bottom ~340px (UI overlays) |
| X / Twitter post | 16:9 | 1600x900 | Text readable at small preview size |
| LinkedIn post | 1:1 or 4:5 | 1200x1200 / 1080x1350 | Link previews are ~1.91:1 (1200x627) — generate 16:9 + `--resize` |
| Facebook / Open Graph link image | 16:9 → crop | 1200x630 | Generate 16:9, `--resize 1200x630` |
| Pinterest pin | 2:3 | 1000x1500 | Vertical, scroll-stopping |
| YouTube thumbnail | 16:9 | 1280x720 | High contrast, readable at 168x94px; avoid bottom-right (timestamp) |
| Web banner (leaderboard) | 8:1 | 728x90 | Minimal text, strong CTA |
| Medium rectangle ad | 5:4 → crop | 300x250 | `--resize 300x250` |
| Poster / flyer | 2:3 or 3:4 | print size | See `poster-design` for bleed and DPI; 4K for print |

---

## Step 5: Look at the Output, Then Check It

Never deliver an image you haven't viewed. Open every generated file (e.g. with the Read tool on the PNG) and inspect it at full size and at the size it will actually be seen (a thumbnail, a feed card).

### Getting text right

Text is the most common failure. To reduce errors:
- Put exact copy in double quotes in the prompt: `headline "HEAR EVERYTHING"`
- Keep rendered text short — a headline, a subline, a CTA. Move long copy (paragraphs, legal, prices that change) into an HTML/CSS overlay instead of the image.
- Spell out unusual words or brand names and say "spelled exactly as written".
- If a word comes back misspelled, fix it in a follow-up turn quoting only that word: `Change "EVERYTHNG" to "EVERYTHING". Change nothing else.`
- After two failed text fixes, generate the image without text and add the text as a code overlay (see `graphic-design`).

Before delivering any generated image:

- [ ] Text is legible and spelled correctly (Gemini can render text — verify it)
- [ ] Colors match brand context (hex codes specified in prompt)
- [ ] Composition has clear visual hierarchy (one focal point)
- [ ] Sufficient contrast between text and background
- [ ] No unwanted artifacts or distortions
- [ ] Aspect ratio matches intended platform
- [ ] Product image (if used) is cleanly integrated, not distorted
- [ ] Overall aesthetic matches the requested style

If any check fails, use multi-turn refinement to fix specific issues — one change per turn, and say what must stay the same. Report to the user which checks you verified and any compromises (e.g. "text added as overlay because the model kept misspelling it").

Also mention that Gemini output carries an invisible SynthID watermark, so it can be identified as AI-generated.

---

## Reference: Model Capabilities

| Feature | Gemini 3.1 Flash |
|---------|-----------------|
| Max input images | 14 (10 objects + 4 characters) |
| Output resolutions | 512, 1K, 2K, 4K |
| Aspect ratios | 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9, 1:4, 4:1, 1:8, 8:1 |
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
