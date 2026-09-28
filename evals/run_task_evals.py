#!/usr/bin/env python3
"""
End-to-end task evals: run real headless Claude Code on design tasks with the skills
installed, then grade what it produced.

For each evals/tasks/*.json:
  1. Create a throwaway project: skills copied to .claude/skills/, seed files copied in.
  2. Run `claude -p "<prompt>"` there (stream-json, acceptEdits, per-task --max-budget-usd).
  3. Grade the workspace with deterministic checks (below). Optionally (--judge) have
     Claude score screenshots against the task's rubric.

Usage:
    python evals/run_task_evals.py                         # all tasks
    python evals/run_task_evals.py --task hero-section,dark-mode --keep
    python evals/run_task_evals.py --judge                 # add rubric grading (Anthropic API)
    python evals/run_task_evals.py --grade-only /tmp/ws --task hero-section   # re-grade a kept workspace
    python evals/run_task_evals.py --baseline              # same tasks WITHOUT skills, for comparison

Needs: the `claude` CLI (logged in), Node + Playwright with Chromium (for audit/screenshot
checks), and for --judge `pip install anthropic`. Each task has a budget_usd cap. Results go to
evals/results/ (gitignored).

Check types (a check with "required": true fails the whole task):
  skill_loaded       {skill}                       the run invoked that skill
  file_exists        {glob}
  file_contains      {glob, pattern, flags?}       regex over the matched files; flags "i" = ignore case
  file_not_contains  {glob, pattern, flags?}
  file_unchanged     {glob}                        seed file left untouched
  max_file_kb        {glob, kb}
  brand_colors       {glob, min}                   at least `min` hex colors from the seeded design context
  image_size         {glob, width, height}         PNG/JPG exact pixel size
  image_aspect       {glob, ratios, min_width?}    aspect ratio within 2% of one of `ratios` ("2:3", ...)
  audit              {glob, ...thresholds}         runs design-critique/scripts/audit.mjs; thresholds:
                     no_overflow, max_contrast_failures, max_dark_contrast_failures,
                     no_lazy_above_fold, reduced_motion, require_lang, max_small_targets
  command            {run, expect_exit?}           shell command in the workspace; {skills} = skills dir
  response_contains  {pattern, flags?}             regex over Claude's final message
"""

import argparse
import base64
import concurrent.futures
import datetime
import glob as globlib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")
TASKS_DIR = os.path.join(ROOT, "evals", "tasks")
RESULTS = os.path.join(ROOT, "evals", "results")
AUDIT = os.path.join(SKILLS_DIR, "design-critique", "scripts", "audit.mjs")
RENDER = os.path.join(SKILLS_DIR, "graphic-design", "scripts", "render.mjs")


def load_tasks(selected=None):
    tasks = []
    for path in sorted(globlib.glob(os.path.join(TASKS_DIR, "*.json"))):
        with open(path, encoding="utf-8") as f:
            task = json.load(f)
        if not selected or task["id"] in selected:
            tasks.append(task)
    if selected and len(tasks) != len(selected):
        missing = selected - {t["id"] for t in tasks}
        sys.exit(f"unknown task(s): {', '.join(sorted(missing))}")
    return tasks


# --- workspace + run -----------------------------------------------------------------------

def make_workspace(task, with_skills=True):
    ws = tempfile.mkdtemp(prefix=f"designskills-{task['id']}-")
    if with_skills:
        target = os.path.join(ws, ".claude", "skills")
        os.makedirs(target)
        names = sorted(os.listdir(SKILLS_DIR)) if task.get("all_skills", True) else \
            [task["skill"], "design-context", "image-generation", *task.get("include_skills", [])]
        for name in dict.fromkeys(names):
            src = os.path.join(SKILLS_DIR, name)
            if os.path.isdir(src):
                shutil.copytree(src, os.path.join(target, name))
    for dest, src in task.get("seed", {}).items():
        out = os.path.join(ws, dest)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy(os.path.join(ROOT, src), out)
    return ws


def parse_stream(lines):
    skills, final, cost = [], "", None
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    skills.append(block.get("input", {}).get("skill", "").split(":")[-1].strip("/"))
        elif event.get("type") == "result":
            final = event.get("result") or ""
            cost = event.get("total_cost_usd")
    return {"skills": skills, "final": final, "cost_usd": cost}


def isolated_env(ws):
    """Environment for the child Claude Code: a throwaway HOME and no skill sync, so the only
    extra skills it sees are the ones in the workspace (built-in skills remain on both sides)."""
    env = dict(os.environ)
    env.pop("CLAUDE_CODE_SYNC_SKILLS", None)
    home = os.path.join(ws, ".eval-home")
    os.makedirs(home, exist_ok=True)
    env["HOME"] = home
    return env


def missing_env(task):
    return [name for name in task.get("requires_env", []) if not os.environ.get(name)]


def run_claude(task, ws, model, timeout):
    cmd = ["claude", "-p", task["prompt"], "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project", "--permission-mode", "acceptEdits",
           "--allowedTools", "Skill,Read,Write,Edit,Glob,Grep,Bash",
           "--no-session-persistence", "--max-budget-usd", str(task.get("budget_usd", 3))]
    if model:
        cmd += ["--model", model]
    try:
        proc = subprocess.run(cmd, cwd=ws, env=isolated_env(ws), capture_output=True, text=True, timeout=timeout)
        out, err = proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        out, err = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""), "timeout"
    with open(os.path.join(ws, ".eval-transcript.jsonl"), "w", encoding="utf-8") as f:
        f.write(out)
    run = parse_stream(out.splitlines())
    run["stderr"] = (err or "")[-500:]
    return run


# --- graders -------------------------------------------------------------------------------

def files(ws, pattern):
    return sorted(p for p in globlib.glob(os.path.join(ws, pattern), recursive=True) if os.path.isfile(p))


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def regex(check):
    return re.compile(check["pattern"], re.I if "i" in check.get("flags", "") else 0)


def context_colors(task):
    src = task.get("seed", {}).get(".agents/design-context.md")
    if not src:
        return set()
    return {h.lower() for h in re.findall(r"\|\s*(#[0-9a-fA-F]{6})\s*\|", read(os.path.join(ROOT, src)))}


def run_audit(ws, path, cache):
    if path in cache:
        return cache[path]
    out = os.path.join(ws, ".eval-audit", os.path.basename(path))
    proc = subprocess.run(["node", AUDIT, path, out, "--widths", "390,1440", "--no-axe"],
                          capture_output=True, text=True, timeout=180)
    report = json.loads(proc.stdout) if proc.returncode == 0 and proc.stdout.strip() else {"error": proc.stderr[-300:]}
    cache[path] = (report, out)
    return cache[path]


def grade_check(check, task, ws, run, cache):
    kind = check["type"]
    label = check.get("label") or f"{kind} {check.get('glob') or check.get('skill') or check.get('pattern') or ''}".strip()
    matched = files(ws, check["glob"]) if "glob" in check else []

    def result(ok, detail=""):
        return {"check": label, "type": kind, "pass": bool(ok), "required": check.get("required", False), "detail": detail}

    if kind == "skill_loaded":
        return result(check["skill"] in run["skills"], f"loaded: {run['skills'] or 'none'}")
    if kind == "file_exists":
        return result(matched, ", ".join(os.path.relpath(p, ws) for p in matched) or "no match")
    if kind in ("file_contains", "file_not_contains"):
        if not matched:
            return result(False, "no matching file")
        hits = [os.path.relpath(p, ws) for p in matched if regex(check).search(read(p))]
        return result(bool(hits) if kind == "file_contains" else not hits, f"matches in: {hits or 'none'}")
    if kind == "file_unchanged":
        src = os.path.join(ROOT, task["seed"][check["glob"]])
        digest = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
        return result(matched and digest(matched[0]) == digest(src))
    if kind == "max_file_kb":
        if not matched:
            return result(False, "no matching file")
        size = max(os.path.getsize(p) for p in matched) / 1024
        return result(size <= check["kb"], f"{size:.1f} KB")
    if kind == "brand_colors":
        colors = context_colors(task)
        found = {c for p in matched for c in colors if c in read(p).lower()}
        return result(len(found) >= check["min"], f"{len(found)} brand colors: {sorted(found)}")
    if kind == "image_size":
        if not matched:
            return result(False, "no matching file")
        from PIL import Image
        size = Image.open(matched[0]).size
        return result(size == (check["width"], check["height"]), f"{size[0]}x{size[1]}")
    if kind == "image_aspect":
        if not matched:
            return result(False, "no matching file")
        from PIL import Image
        w, h = Image.open(matched[0]).size
        ok = any(abs(w / h - int(a) / int(b)) <= 0.02 * int(a) / int(b)
                 for a, b in (r.split(":") for r in check["ratios"]))
        return result(ok and w >= check.get("min_width", 0), f"{w}x{h}")
    if kind == "audit":
        if not matched:
            return result(False, "no matching file")
        report, _ = run_audit(ws, matched[0], cache)
        if "error" in report:
            return result(False, report["error"])
        problems = []
        widths = report.get("widths", {}).values()
        structure = report.get("structure", {})
        if check.get("no_overflow") and any(w["horizontalOverflow"] for w in widths):
            problems.append("horizontal overflow")
        if "max_contrast_failures" in check:
            n = max((len(w["contrastFailures"]) for w in widths), default=0)
            if n > check["max_contrast_failures"]:
                worst = min((f for w in widths for f in w["contrastFailures"]), key=lambda f: f["ratio"])
                problems.append(f"{n} contrast failures (worst {worst['ratio']}:1 on \"{worst['text'][:24]}\")")
        if "max_dark_contrast_failures" in check:
            n = len(report.get("darkMode", {}).get("contrastFailures", []))
            if n > check["max_dark_contrast_failures"]:
                problems.append(f"{n} dark-mode contrast failures")
        if check.get("no_lazy_above_fold") and structure.get("lazyImagesAboveFold"):
            problems.append("lazy image above the fold")
        if check.get("reduced_motion") and structure.get("animationWithoutReducedMotion"):
            problems.append("animation without prefers-reduced-motion")
        if check.get("require_lang") and not structure.get("lang"):
            problems.append("missing lang")
        if "max_small_targets" in check:
            n = max((len(w["smallTargets"]) for w in widths), default=0)
            if n > check["max_small_targets"]:
                problems.append(f"{n} tap targets under 24px")
        return result(not problems, "; ".join(problems) or "clean")
    if kind == "command":
        cmd = check["run"].replace("{skills}", SKILLS_DIR)
        proc = subprocess.run(cmd, shell=True, cwd=ws, capture_output=True, text=True, timeout=120)
        return result(proc.returncode == check.get("expect_exit", 0), (proc.stdout + proc.stderr)[-300:].strip())
    if kind == "response_contains":
        return result(regex(check).search(run.get("final", "")))
    return result(False, f"unknown check type {kind}")


# --- optional rubric judge -----------------------------------------------------------------

def screenshots_for(task, ws, cache):
    shots = []
    for pattern in task.get("screenshots", []):
        shots += files(ws, pattern)
    if not shots:
        html = next((p for c in task["checks"] if c["type"] == "audit" for p in files(ws, c["glob"])), None)
        if html:
            _, out = run_audit(ws, html, cache)
            shots = [p for p in (os.path.join(out, "desktop-fold.png"), os.path.join(out, "mobile-fold.png"),
                                 os.path.join(out, "desktop-dark-fold.png")) if os.path.exists(p)]
    return shots[:4]


def judge(task, ws, cache, model):
    import anthropic

    shots = screenshots_for(task, ws, cache)
    if not shots:
        return {"error": "no screenshots to judge"}
    content = []
    for path in shots:
        content.append({"type": "text", "text": f"Screenshot: {os.path.relpath(path, ws)}"})
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                                     "data": base64.b64encode(open(path, "rb").read()).decode()}})
    criteria = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(task["rubric"]))
    content.append({"type": "text", "text": f"Task given to the designer:\n{task['prompt']}\n\n"
                    f"Score each criterion 1-5 (5 = excellent, 3 = acceptable, 1 = fails) strictly "
                    f"from what is visible, with one sentence of evidence each.\n{criteria}"})
    schema = {
        "type": "object",
        "properties": {"scores": {"type": "array", "items": {
            "type": "object",
            "properties": {"criterion": {"type": "integer"}, "score": {"type": "integer"}, "evidence": {"type": "string"}},
            "required": ["criterion", "score", "evidence"], "additionalProperties": False}}},
        "required": ["scores"], "additionalProperties": False,
    }
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model, max_tokens=4096,
        system="You are a senior product designer grading design work against a rubric. Be strict and specific.",
        messages=[{"role": "user", "content": content}],
        output_config={"format": {"type": "json_schema", "schema": schema}},
    )
    if response.stop_reason == "refusal":
        return {"error": "judge refused"}
    data = json.loads(next(b.text for b in response.content if b.type == "text"))
    scores = [s["score"] for s in data["scores"]]
    return {"mean": round(sum(scores) / len(scores), 2), "scores": data["scores"]}


# --- main ----------------------------------------------------------------------------------

def evaluate(task, args):
    if missing_env(task) and not args.grade_only:
        return {"id": task["id"], "workspace": None, "skills_loaded": [], "cost_usd": None, "checks": [],
                "score": 0, "pass": False, "skipped": f"missing env: {', '.join(missing_env(task))}"}
    if args.grade_only:
        ws, run = args.grade_only, {"skills": [], "final": "", "cost_usd": None}
        transcript = os.path.join(ws, ".eval-transcript.jsonl")
        if os.path.exists(transcript):
            run = parse_stream(read(transcript).splitlines())
    else:
        ws = make_workspace(task, with_skills=not args.baseline)
        run = run_claude(task, ws, args.model, args.timeout)

    cache = {}
    checks = [grade_check(c, task, ws, run, cache) for c in task["checks"]
              if not (args.baseline and c["type"] == "skill_loaded")]
    passed = sum(c["pass"] for c in checks)
    outcome = {
        "id": task["id"], "workspace": ws, "skills_loaded": run["skills"], "cost_usd": run.get("cost_usd"),
        "checks": checks, "score": round(passed / len(checks), 2) if checks else 0,
        "pass": all(c["pass"] for c in checks if c["required"]) and passed / max(len(checks), 1) >= args.pass_ratio,
    }
    if args.judge and task.get("rubric"):
        try:
            outcome["judge"] = judge(task, ws, cache, args.judge_model)
        except Exception as e:
            outcome["judge"] = {"error": f"{type(e).__name__}: {e}"}
    if not args.keep and not args.grade_only:
        shutil.rmtree(ws, ignore_errors=True)
        outcome["workspace"] = None
    return outcome


def main():
    parser = argparse.ArgumentParser(description="End-to-end task evals")
    parser.add_argument("--task", help="Comma-separated task ids (default: all)")
    parser.add_argument("--model", help="Model for Claude Code (default: CLI default)")
    parser.add_argument("--judge", action="store_true", help="Also grade screenshots against each task's rubric")
    parser.add_argument("--judge-model", default="claude-opus-5")
    parser.add_argument("--baseline", action="store_true", help="Run without skills installed")
    parser.add_argument("--grade-only", metavar="WORKSPACE", help="Grade an existing workspace (one --task)")
    parser.add_argument("--keep", action="store_true", help="Keep workspaces for inspection")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=900, help="Seconds per task")
    parser.add_argument("--pass-ratio", type=float, default=0.8, help="Share of checks needed to pass a task")
    args = parser.parse_args()

    tasks = load_tasks(set(args.task.split(",")) if args.task else None)
    if args.grade_only and len(tasks) != 1:
        sys.exit("--grade-only needs exactly one --task")
    if not args.grade_only and not shutil.which("claude"):
        sys.exit("claude CLI not found (npm i -g @anthropic-ai/claude-code)")

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        outcomes = list(pool.map(lambda t: evaluate(t, args), tasks))

    for o in outcomes:
        if o.get("skipped"):
            print(f"SKIP  {o['id']:<24} {o['skipped']}")
            continue
        cost = f"  ${o['cost_usd']:.2f}" if o.get("cost_usd") else ""
        judge_txt = f"  judge {o['judge']['mean']}/5" if o.get("judge", {}).get("mean") else ""
        print(f"{'PASS' if o['pass'] else 'FAIL'}  {o['id']:<24} {o['score']:.0%} checks{judge_txt}{cost}")
        for c in o["checks"]:
            if not c["pass"]:
                print(f"      x {c['check']}{' (required)' if c['required'] else ''}: {c['detail'][:220]}")
        if o.get("judge", {}).get("error"):
            print(f"      judge: {o['judge']['error']}")
        if o["workspace"]:
            print(f"      workspace: {o['workspace']}")
    passed = sum(o["pass"] for o in outcomes)
    print(f"\n{passed}/{len(outcomes)} tasks passed{' (baseline, no skills)' if args.baseline else ''}")

    os.makedirs(RESULTS, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = os.path.join(RESULTS, f"tasks-{'baseline' if args.baseline else 'skills'}-{stamp}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"model": args.model, "baseline": args.baseline, "outcomes": outcomes}, f, indent=2)
    print(f"Saved {os.path.relpath(out, ROOT)}")
    sys.exit(0 if passed == len(outcomes) else 1)


if __name__ == "__main__":
    main()
