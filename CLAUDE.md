# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A collection of AI agent skills for graphic design and UI design. Skills are Markdown files with YAML frontmatter that encode expert design knowledge, enabling Claude Code to produce professional-grade visual output. Modeled after the marketingskills pattern.

## Repository Structure

- `skills/[skill-name]/SKILL.md` — each skill lives in its own directory under `skills/`
- `design-context` is the foundational skill — all other skills reference it for brand/style context
- `image-generation` provides the Gemini 3.1 Flash Image Preview pipeline for AI image generation
- `tools/gemini-generate.py` — CLI utility for generating images via Gemini API
- Skills save persistent context to `.agents/design-context.md`
- Five categories: Foundational (2), Graphic Design (8), UI Design (8), Design Systems (6), Process (4)

## Validation

```bash
bash validate-skills.sh                # validate all skills
bash validate-skills.sh skill-name     # validate a single skill
```

## Skill File Format

Each `SKILL.md` requires:
- YAML frontmatter with `name` (must match directory name), `description` (include trigger phrases), `license: MIT`
- Content under 500 lines
- Step-by-step instructions with opinionated design frameworks
- Reference to `design-context` where applicable

## Key Conventions

- Skill names are lowercase with hyphens, must match their directory name exactly
- Two output modes: AI image generation (Gemini 3.1 Flash) and code generation (HTML/CSS/SVG/React)
- Graphic design skills default to Gemini image generation; UI skills generate code
- The `design-context` skill stores brand parameters that all other skills consume for consistency
- Gemini API requires `GEMINI_API_KEY` env var and `pip install google-genai Pillow`
- Future Glittr integration planned for editable design output
