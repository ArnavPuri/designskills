# Design Skills for AI Agents

This repository contains design skills that can be used by Claude Code and other AI agents to produce professional-grade graphic design and UI output.

## How Skills Work

Each skill in `skills/` follows a standardized format with YAML frontmatter and structured instructions. Skills are activated based on trigger phrases in their descriptions.

## Foundational Skills

Always check `design-context` first — it establishes brand identity, color systems, typography, and audience context that all other skills reference.

The `image-generation` skill provides the Gemini 3.1 Flash Image Preview pipeline that all graphic design skills use for AI image generation.

## Bundled Scripts

Some skills ship helper scripts in their `scripts/` folder. `<skill-name>/scripts/file` in a skill means that skill's directory, which is the base directory shown when the skill loads. Run the scripts from the user's project so outputs land there.

## Skill Categories

- **Foundational:** design-context, image-generation
- **Graphic Design:** graphic-design, social-media-graphic, poster-design, thumbnail-design, ad-creative-design, product-mockup, infographic, banner-design
- **UI Design:** ui-design, landing-page-design, dashboard-design, mobile-ui-design, hero-section, card-design, dark-mode, email-design
- **Design Systems:** color-palette, typography, layout-composition, brand-identity, icon-design, design-system
- **Process:** design-critique, motion-design, presentation-design, image-treatment
