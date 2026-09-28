# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A collection of AI agent skills for graphic design and UI design. Skills are Markdown files with YAML frontmatter that encode expert design knowledge, enabling Claude Code to produce professional-grade visual output. Modeled after the marketingskills pattern.

## Repository Structure

- `skills/[skill-name]/SKILL.md` — each skill lives in its own directory under `skills/`
- `design-context` is the foundational skill — all other skills reference it for brand/style context
- `image-generation` provides the Gemini 3.1 Flash Image Preview pipeline for AI image generation
- `skills/[skill-name]/scripts/` — helper scripts bundled with the skill that uses them (so they ship with `npx skills add`). Skills refer to them as `<skill-name>/scripts/file`, meaning that skill's directory:
  - `image-generation/scripts/gemini-generate.py` (Gemini CLI), `export-sizes.py` (one master → platform sizes)
  - `graphic-design/scripts/render.mjs` (HTML → exact-size PNG/PDF), `design-critique/scripts/audit.mjs` (screenshots + measurements)
  - `design-context/scripts/contrast.py` (WCAG checks), `color-palette/scripts/palette.py` (OKLCH scales)
- `tools/gemini-generate.py` — compatibility wrapper for the generator above
- `evals/` — static checks, skill-routing eval, end-to-end task evals (see `evals/README.md`); `tests/` — script unit tests
- Skills save persistent context to `.agents/design-context.md`
- Five categories: Foundational (2), Graphic Design (8), UI Design (8), Design Systems (6), Process (4)

## Validation

```bash
bash validate-skills.sh                    # frontmatter, names, length, cross-references
python evals/static_checks.py              # flags, aspect ratios, code blocks, trigger collisions
python -m unittest discover tests -v       # bundled scripts
python evals/run_trigger_evals.py          # skill routing (needs Anthropic API access)
python evals/run_task_evals.py --task ID   # end-to-end with headless Claude Code (costs money)
```

Run the first three before every commit (CI runs them too). When changing a skill's description, run the routing eval; when changing a skill's instructions, run its task eval if one exists.

## Skill File Format

Each `SKILL.md` requires:
- YAML frontmatter with `name` (must match directory name), `description` (include trigger phrases), `license: MIT`
- Content under 500 lines
- Step-by-step instructions with opinionated design frameworks
- Reference to `design-context` where applicable

## Key Conventions

- Skill names are lowercase with hyphens, must match their directory name exactly
- Two output modes: AI image generation (Gemini 3.1 Flash) and code generation (HTML/CSS/SVG/React)
- Graphic design skills default to Gemini image generation (except `infographic` and anything with exact numbers or long copy, which default to code); UI skills generate code
- The `design-context` skill stores brand parameters that all other skills consume for consistency
- Gemini API requires `GEMINI_API_KEY` env var and `pip install google-genai Pillow`
- Future Glittr integration planned for editable design output
