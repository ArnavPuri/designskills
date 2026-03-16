# designskills

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Design skills for Claude Code and AI agents — powered by Gemini 3.1 Flash Image Preview.**

Skills that make AI agents produce professional-grade graphic design, UI design, and visual content. Give it a product image and a one-line prompt, and get an eye-catching graphic back. These skills encode expert design knowledge — composition, color theory, typography, prompt engineering — that results in 10x better visual output.

**Two output modes:**
- **AI Image Generation** — Uses Gemini 3.1 Flash Image Preview to generate pixel-perfect graphics from prompts and reference images
- **Code Generation** — Produces production-ready HTML/CSS/SVG for web-native, interactive graphics

## Skills

### Foundational

| Skill | Description |
|-------|-------------|
| `design-context` | Establish brand identity, style, and audience context for all other skills |
| `image-generation` | Gemini 3.1 Flash Image Preview pipeline — text-to-image, image editing, multi-turn refinement |

### Graphic Design

| Skill | Description |
|-------|-------------|
| `graphic-design` | Core graphic design principles and generation framework |
| `social-media-graphic` | Platform-specific social media graphics (Instagram, Twitter, LinkedIn, etc.) |
| `poster-design` | Event posters, promotional flyers, announcements |
| `thumbnail-design` | YouTube thumbnails, video covers, article headers |
| `ad-creative-design` | Ad banners, display ads, retargeting creatives |
| `product-mockup` | Product shots, device mockups, packaging visualization |
| `infographic` | Data visualization, process diagrams, comparison graphics |
| `banner-design` | Website banners, email headers, event banners |

### UI Design

| Skill | Description |
|-------|-------------|
| `ui-design` | Core UI design patterns and component design |
| `landing-page-design` | High-converting landing pages with strong visual hierarchy |
| `dashboard-design` | Data dashboards, admin panels, analytics views |
| `mobile-ui-design` | Mobile-first interface design for iOS and Android |
| `hero-section` | Above-the-fold hero sections that convert |
| `card-design` | Card-based layouts, product cards, feature cards |
| `dark-mode` | Dark theme design with proper contrast and color adaptation |
| `email-design` | HTML email templates that render across clients |

### Design Systems

| Skill | Description |
|-------|-------------|
| `color-palette` | Color theory, palette generation, accessibility-compliant colors |
| `typography` | Font pairing, type hierarchy, responsive type scales |
| `layout-composition` | Grid systems, visual hierarchy, whitespace management |
| `brand-identity` | Logo systems, brand guidelines, visual identity |
| `icon-design` | Icon sets, icon systems, consistent iconography |
| `design-system` | Component libraries, design tokens, systematic design |

### Process

| Skill | Description |
|-------|-------------|
| `design-critique` | Evaluate and improve existing designs |
| `motion-design` | Animation principles, micro-interactions, transitions |
| `presentation-design` | Slide decks, pitch decks, keynote presentations |
| `image-treatment` | Photo effects, overlays, filters, image composition |

## Installation

### Prerequisites (for AI image generation)

```bash
pip install google-genai Pillow
export GEMINI_API_KEY="your-api-key"
```

### Using npx (recommended)

```bash
npx skills install designskills
```

### Manual clone

```bash
git clone https://github.com/arnavpuri/designskills.git ~/.claude/skills/designskills
```

### Git submodule

```bash
git submodule add https://github.com/arnavpuri/designskills.git .claude/skills/designskills
```

## Quick Start

Start by establishing design context, then invoke a specific skill:

```
1. Use the design-context skill to define your brand, audience, and style guidelines.
2. Then use a specific skill like graphic-design or landing-page-design for the task at hand.
```

**Example — product image to social graphic:**

```
> /design-context Set up brand context for a fintech startup targeting millennials.
  Uses navy/teal palette, modern sans-serif type, clean minimal aesthetic.

> /graphic-design Here's our product image [product.png]. Create an Instagram
  post announcing the launch with headline "Now Available".
```

The agent will:
1. Load brand context (colors, fonts, style)
2. Craft an optimized Gemini prompt with your brand parameters
3. Generate the graphic using Gemini 3.1 Flash Image Preview with your product image
4. Deliver a polished, on-brand graphic

The `design-context` skill stores brand parameters that all other skills reference, ensuring consistency across every asset you generate.

## Glittr Integration

Future releases will support [Glittr](https://glittr.com) for editable design output. This will allow you to take AI-generated designs and refine them in a visual editor, bridging the gap between AI generation and manual polish.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on creating and submitting new skills.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
