# Versions

## v1.1.0

**Release date:** 2026-09-28

- Reviewed all 28 skills: corrected platform specs, Gemini aspect ratios, WCAG thresholds, and broken code; every skill reads `.agents/design-context.md`; generated output is rendered and checked before delivery
- Bundled helper scripts in `skills/<name>/scripts/`: `gemini-generate.py` (now honors aspect ratio/size, supports multiple reference images, exact-pixel resize), `export-sizes.py`, `render.mjs`, `audit.mjs`, `contrast.py`, `palette.py`
- Evals: static consistency checks, skill-routing eval, end-to-end task evals with a rubric judge
- Unit tests for the scripts and a CI workflow

## v1.0.0

**Release date:** 2026-03-16

Initial release of designskills.

- 26 design skills across 5 categories: Foundational, Graphic Design, UI Design, Design Systems, and Process
- Validation script for skill format checking
- Contributing guidelines and issue templates
- MIT license
