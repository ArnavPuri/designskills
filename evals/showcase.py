#!/usr/bin/env python3
"""
Build a with/without-skills showcase for the README.

For each task that has a "showcase" block (evals/tasks/*.json), run it twice with headless
Claude Code, once with the skills installed and once without (same prompt, same seed files,
same tools), render both outputs, and compose a labeled side-by-side image.

    python evals/showcase.py                                  # every showcase task
    python evals/showcase.py --task hero-section,email-design
    python evals/showcase.py --compose-only                   # rebuild images + README from saved results

Outputs (commit these):
    docs/showcase/<task>.jpg          side-by-side comparison
    docs/showcase/raw/<task>-{baseline,skills}.png
    docs/showcase/results.json        scores, checks, cost, model, date per side (merged across runs,
                                      so tasks can be run in separate sessions)
    README.md                         section between <!-- showcase:start --> and <!-- showcase:end -->

Tasks with "requires_env" (e.g. GEMINI_API_KEY) are skipped when the variable is missing.
Each run costs real money (see budget_usd per task); one run per side is anecdotal, so the
README section states the model and date and links to the raw results.
"""

import argparse
import concurrent.futures
import datetime
import glob as globlib
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "evals"))
import run_task_evals as rte  # noqa: E402

OUT = os.path.join(ROOT, "docs", "showcase")
RAW = os.path.join(OUT, "raw")
RESULTS = os.path.join(OUT, "results.json")
README = os.path.join(ROOT, "README.md")
START, END = "<!-- showcase:start -->", "<!-- showcase:end -->"
SIDES = ("baseline", "skills")
LABELS = {"baseline": "Without skills", "skills": "With designskills"}
PANEL_HEIGHT = 900


def load_results():
    if os.path.exists(RESULTS):
        with open(RESULTS, encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": {}}


def save_results(results):
    os.makedirs(OUT, exist_ok=True)
    with open(RESULTS, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


def comparable_checks(outcome):
    """Checks that apply to both sides (skill_loaded only makes sense with skills)."""
    return [c for c in outcome.get("checks", []) if c["type"] != "skill_loaded"]


# --- capture one side -----------------------------------------------------------------------

def capture(task, ws, dest):
    """Write a PNG of the task's output to dest. Returns a short note or None on success."""
    from PIL import Image

    spec = task["showcase"]
    if "image" in spec:
        matches = rte.files(ws, spec["image"]) or sorted(
            globlib.glob(os.path.join(ws, "*.png")), key=os.path.getsize, reverse=True)
        if not matches:
            return "no image produced"
        img = Image.open(matches[0]).convert("RGB")
        img.thumbnail((1600, 1600))
        img.save(dest)
        return None if rte.files(ws, spec["image"]) else f"used {os.path.basename(matches[0])}"

    matches = rte.files(ws, spec["html"]) or rte.files(ws, "*.html")
    if not matches:
        return "no HTML produced"
    cmd = ["node", rte.RENDER, matches[0], "--out", dest]
    cmd += ["--size", spec["size"]] if "size" in spec else ["--widths", str(spec.get("width", 1280))]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if proc.returncode not in (0, 3) or not os.path.exists(dest):
        return f"render failed: {proc.stderr[-200:]}"
    if "max_height" in spec:
        img = Image.open(dest)
        if img.height > spec["max_height"]:
            img.crop((0, 0, img.width, spec["max_height"])).save(dest)
    return None


def run_side(task, side, args):
    ns = argparse.Namespace(grade_only=None, baseline=(side == "baseline"), model=args.model,
                            timeout=args.timeout, judge=False, keep=True, pass_ratio=0.8)
    outcome = rte.evaluate(task, ns)
    if outcome.get("skipped"):
        return {"skipped": outcome["skipped"]}
    os.makedirs(RAW, exist_ok=True)
    dest = os.path.join(RAW, f"{task['id']}-{side}.png")
    note = capture(task, outcome["workspace"], dest)
    checks = comparable_checks(outcome)
    record = {
        "passed": sum(c["pass"] for c in checks),
        "total": len(checks),
        "checks": [{k: c[k] for k in ("check", "pass", "detail")} for c in checks],
        "skills_loaded": outcome["skills_loaded"],
        "cost_usd": outcome["cost_usd"],
        "image": os.path.relpath(dest, ROOT) if os.path.exists(dest) else None,
        "note": note,
        "model": args.model or "Claude Code default",
        "date": datetime.date.today().isoformat(),
    }
    if not args.keep:
        shutil.rmtree(outcome["workspace"], ignore_errors=True)
    else:
        record["workspace"] = outcome["workspace"]
    return record


# --- compose --------------------------------------------------------------------------------

def font(size, bold=False):
    from PIL import ImageFont
    for path in (f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
                 f"/Library/Fonts/Arial{' Bold' if bold else ''}.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def panel(record, side):
    from PIL import Image, ImageDraw
    if record and record.get("image") and os.path.exists(os.path.join(ROOT, record["image"])):
        img = Image.open(os.path.join(ROOT, record["image"])).convert("RGB")
        img = img.resize((round(img.width * PANEL_HEIGHT / img.height), PANEL_HEIGHT), Image.LANCZOS)
        if img.width > 1600:
            img = img.crop((0, 0, 1600, PANEL_HEIGHT))
    else:
        img = Image.new("RGB", (675, PANEL_HEIGHT), "#f1f1f1")
        ImageDraw.Draw(img).text((40, PANEL_HEIGHT // 2), (record or {}).get("note") or "Not run yet",
                                 fill="#666", font=font(28))
    header = 110
    canvas = Image.new("RGB", (img.width, img.height + header), "white")
    canvas.paste(img, (0, header))
    draw = ImageDraw.Draw(canvas)
    draw.text((0, 12), LABELS[side], fill="#111", font=font(40, bold=True))
    if record and record.get("total"):
        draw.text((0, 64), f"{record['passed']}/{record['total']} checks passed", fill="#555", font=font(28))
    return canvas


def compose(task, results):
    from PIL import Image, ImageDraw
    entry = results["tasks"].get(task["id"], {})
    left, right = panel(entry.get("baseline"), "baseline"), panel(entry.get("skills"), "skills")
    gap, margin, title_h = 60, 48, 90
    width = left.width + right.width + gap + 2 * margin
    height = max(left.height, right.height) + title_h + 2 * margin
    out = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(out)
    draw.text((margin, margin - 8), task["showcase"].get("title", task["id"]), fill="#111", font=font(48, bold=True))
    out.paste(left, (margin, margin + title_h))
    out.paste(right, (margin + left.width + gap, margin + title_h))
    x = margin + left.width + gap // 2
    draw.line([(x, margin + title_h), (x, height - margin)], fill="#ddd", width=2)
    dest = os.path.join(OUT, f"{task['id']}.jpg")
    if out.width > 2400:
        out = out.resize((2400, round(out.height * 2400 / out.width)), Image.LANCZOS)
    out.save(dest, quality=85, optimize=True, progressive=True)
    return dest


def readme_section(tasks, results):
    lines = [START, "## With vs. without skills", "",
             "Same prompt, same brand context, same tools. The only difference is whether the skills "
             "are installed. Each side was generated by headless Claude Code via `evals/showcase.py`; "
             "checks are the automated ones in `evals/tasks/` (brand colors, contrast, exact export "
             "size, and so on). One run per side, so treat these as examples, not benchmarks.", ""]
    for task in tasks:
        entry = results["tasks"].get(task["id"])
        if not entry or not os.path.exists(os.path.join(OUT, f"{task['id']}.jpg")):
            continue
        b, s = entry.get("baseline") or {}, entry.get("skills") or {}
        score = lambda r: f"{r['passed']}/{r['total']}" if r.get("total") else "n/a"
        lines += [f"**{task['showcase'].get('title', task['id'])}**: checks {score(b)} without skills, "
                  f"{score(s)} with skills", "",
                  f"![{task['id']}: without vs with skills](docs/showcase/{task['id']}.jpg)", ""]
    meta = sorted({(r.get("model"), r.get("date")) for e in results["tasks"].values()
                   for r in e.values() if isinstance(r, dict) and r.get("date")})
    if meta:
        lines += ["<sub>Generated " + "; ".join(f"{d} with {m}" for m, d in meta) +
                  ". Raw outputs and per-check results: [docs/showcase](docs/showcase/results.json).</sub>", ""]
    lines.append(END)
    return "\n".join(lines)


def update_readme(section):
    with open(README, encoding="utf-8") as f:
        text = f.read()
    if START in text and END in text:
        text = text[:text.index(START)] + section + text[text.index(END) + len(END):]
    else:
        anchor = "## Installation"
        text = text.replace(anchor, section + "\n\n" + anchor, 1) if anchor in text else text + "\n" + section + "\n"
    with open(README, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser(description="With/without-skills showcase")
    parser.add_argument("--task", help="Comma-separated task ids (default: all tasks with a showcase block)")
    parser.add_argument("--model", help="Model for Claude Code (default: CLI default)")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--keep", action="store_true", help="Keep workspaces")
    parser.add_argument("--compose-only", action="store_true", help="Skip runs; rebuild images and README")
    parser.add_argument("--no-readme", action="store_true", help="Don't touch README.md")
    args = parser.parse_args()

    all_tasks = [t for t in rte.load_tasks() if t.get("showcase")]
    wanted = set(args.task.split(",")) if args.task else None
    tasks = [t for t in all_tasks if not wanted or t["id"] in wanted]
    if wanted and len(tasks) != len(wanted):
        sys.exit(f"not showcase tasks: {', '.join(sorted(wanted - {t['id'] for t in tasks}))}")

    results = load_results()
    if not args.compose_only:
        if not shutil.which("claude"):
            sys.exit("claude CLI not found")
        jobs = [(t, side) for t in tasks for side in SIDES]
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(run_side, t, side, args): (t, side) for t, side in jobs}
            for fut in concurrent.futures.as_completed(futures):
                task, side = futures[fut]
                try:
                    record = fut.result()
                except Exception as e:
                    record = {"note": f"error: {type(e).__name__}: {e}"}
                if record.get("skipped"):
                    print(f"SKIP  {task['id']:<26} {side:<8} {record['skipped']}")
                    continue
                results["tasks"].setdefault(task["id"], {})[side] = record
                save_results(results)  # save as we go; runs are expensive
                cost = f"${record['cost_usd']:.2f}" if record.get("cost_usd") else ""
                print(f"DONE  {task['id']:<26} {side:<8} {record.get('passed', 0)}/{record.get('total', 0)} checks "
                      f"{cost} {record.get('note') or ''}")

    composed = [t for t in all_tasks if t["id"] in results["tasks"]]
    for task in composed:
        print(f"Composed {os.path.relpath(compose(task, results), ROOT)}")
    if composed and not args.no_readme:
        update_readme(readme_section(all_tasks, results))
        print("Updated README.md showcase section")


if __name__ == "__main__":
    main()
