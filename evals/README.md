# Evals

Three layers, from free and instant to realistic and paid. Run the cheap ones on every change and the expensive ones when you change what a skill tells the agent to do.

| Layer | Command | Cost | Answers |
|-------|---------|------|---------|
| Static checks | `python evals/static_checks.py` | free, ~2s | Are the skills internally consistent? |
| Skill routing | `python evals/run_trigger_evals.py` | ~$0.50 per run (60 cases) | Does each request load the right skill? |
| Task evals | `python evals/run_task_evals.py` | ~$1-3 per task | Does the skill produce good work end to end? |

`validate-skills.sh` (frontmatter and structure) and `python -m unittest discover tests` (the bundled scripts) complete the fast checks. CI runs all fast checks on every push and PR.

## Static checks

Deterministic lint across all `SKILL.md` files:

- `<skill>/scripts/...` references point at real files, and every `--flag` used with them exists
- `--aspect-ratio` values are ones Gemini supports; Gemini model ids match the generator
- ```` ```python ````, ```` ```json ```` and ```` ```js ```` blocks parse (`node --check` for JS)
- The brand context path is always `.agents/design-context.md`
- No quoted trigger phrase appears in two skills' descriptions (ambiguous routing)

## Skill routing — `triggers.jsonl`

One case per line: a realistic request and the skill(s) that should handle it. `expected` can hold several skills when a request is genuinely ambiguous; `[]` means no design skill should load.

```json
{"prompt": "Make a YouTube thumbnail for my video 'I Tried Every Budget Keyboard'.", "expected": ["thumbnail-design"]}
```

```bash
python evals/run_trigger_evals.py                       # api mode (default)
python evals/run_trigger_evals.py --mode claude-code    # real Claude Code triggering
python evals/run_trigger_evals.py --only dark-mode,none --model claude-sonnet-5
python evals/run_trigger_evals.py --dry-run             # print the routing prompt
```

- **api mode** gives Claude the same name + description list Claude Code sees and asks it to choose one (structured output). Fast and cheap; use it while tuning descriptions. Needs `pip install anthropic` and API access.
- **claude-code mode** runs `claude -p` in a scratch project with the skills installed and records the first skill loaded. Only the Skill tool is allowed, and each run stops as soon as a skill loads, so it costs little per case. Use it to confirm before shipping description changes.

Output lists every miss, per-skill recall, and precision by chosen skill; the full results go to `evals/results/`. The run fails below `--min-accuracy` (default 0.85).

**When you edit a description:** add 2–3 cases for any new trigger phrase, plus a near-miss that should go to a sibling skill. The most useful cases sit on the boundary between two skills: banner vs ad vs social, hero vs landing page, color-palette vs design-system.

## Task evals — `tasks/*.json`

Each task is a realistic request run by headless Claude Code in a throwaway project that has the skills in `.claude/skills/` and the seed files copied in. The output is then graded.

```json
{
  "id": "hero-section",
  "skill": "hero-section",
  "prompt": "Build the hero section for our homepage as a single self-contained index.html ...",
  "seed": {".agents/design-context.md": "evals/fixtures/design-context.md"},
  "budget_usd": 3,
  "checks": [
    {"type": "skill_loaded", "skill": "hero-section", "required": true},
    {"type": "brand_colors", "glob": "index.html", "min": 2},
    {"type": "audit", "glob": "index.html", "no_overflow": true, "max_contrast_failures": 0, "no_lazy_above_fold": true}
  ],
  "rubric": ["One clear focal point; the headline is the most prominent text", "..."]
}
```

```bash
python evals/run_task_evals.py --task hero-section --keep   # keep the workspace to inspect
python evals/run_task_evals.py --judge                      # also score screenshots against the rubric
python evals/run_task_evals.py --baseline                   # same tasks without skills, for comparison
python evals/run_task_evals.py --grade-only <workspace> --task hero-section   # re-grade, no new run
```

**Checks** are deterministic. The `audit` check renders the page with `design-critique/scripts/audit.mjs` and measures it: overflow at 390px, WCAG contrast (light and dark), lazy images above the fold, reduced motion, `lang`, and tap targets. See the docstring in `run_task_evals.py` for every check type. A task passes when all `required` checks pass and at least 80% of all checks do.

**The judge** (`--judge`) sends screenshots and the rubric to Claude and asks for a strict 1–5 score per criterion, with one sentence of evidence for each. Treat judge scores as a trend across runs, not as absolute truth. Read the screenshots whenever a score moves.

**Measure skill value with `--baseline`.** The difference between runs with and without skills is what the skills contribute. If a task scores the same either way, the skill isn't pulling its weight on that task.

**Isolation:** every run gets a throwaway `HOME` and skill sync turned off, so the only extra skills Claude Code sees are the ones in the workspace. Skills built into Claude Code itself are present on both sides, so the baseline is Claude Code as shipped.

## Showcase for the README

`evals/showcase.py` runs each task that has a `showcase` block twice, with and without skills. Both sides get the same prompt, seed files and tools, including `tools/gemini-generate.py` for the Gemini tasks. It then renders both outputs and composes a labelled side-by-side image:

```bash
python evals/showcase.py --task hero-section,email-design      # code tasks
python evals/showcase.py --task poster-gemini,youtube-thumbnail-gemini,instagram-post-gemini   # needs GEMINI_API_KEY
python evals/showcase.py --compose-only                          # rebuild images + README from saved results
```

Results are merged into `docs/showcase/results.json`, so tasks can run in separate sessions. Images go to `docs/showcase/`, and the README section between `<!-- showcase:start -->` and `<!-- showcase:end -->` is regenerated each time.

### Current tasks

| Task | Skill | What it checks |
|------|-------|----------------|
| `hero-section` | hero-section | Brand colors and fonts, no lazy LCP image, contrast, reduced motion, mobile overflow |
| `dark-mode` | dark-mode | System default, `color-scheme`, persisted accessible toggle, dark-mode contrast |
| `email-design` | email-design | Table layout, no flex/grid, 600px, unsubscribe, under 102KB |
| `social-graphic-code` | social-media-graphic | Exact 1080x1350 PNG export, brand colors, copy present |
| `design-context-detect` | design-context | Colors, fonts and name detected from Tailwind + package.json; saved palette passes contrast |
| `design-critique` | design-critique | Finds the flaws planted in `tests/fixtures/flawed-page.html`, prioritizes them, leaves the file untouched |
| `color-palette` | color-palette | Palette written back to design context without clobbering other fields; passes contrast |
| `poster-gemini` | poster-design | Portrait print ratio, at least 1000px wide (needs `GEMINI_API_KEY`) |
| `youtube-thumbnail-gemini` | thumbnail-design | Exactly 1280x720 (needs `GEMINI_API_KEY`) |
| `instagram-post-gemini` | social-media-graphic | Exactly 1080x1350 (needs `GEMINI_API_KEY`) |

### Adding a task

1. Write the prompt the way a user would, including the constraints that matter ("must work in Outlook").
2. Put seed files in `fixtures/` and map them in `seed`.
3. Prefer checks that catch real failures you've seen, and mark only the non-negotiables `required`.
4. Add a `rubric` for the things only a human eye can judge.
5. Run it 2–3 times. A check that flips between runs is either too strict or catching a real inconsistency, so work out which.

Tasks with `"requires_env": ["GEMINI_API_KEY"]` are skipped when the key isn't set, so the suite still runs anywhere. `social-graphic-code` covers the graphic path without Gemini.
