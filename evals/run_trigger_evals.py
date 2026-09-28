#!/usr/bin/env python3
"""
Skill-routing eval: does each prompt in evals/triggers.jsonl pick the right skill?

Two modes:

  api          Ask Claude, via the Anthropic API, to choose one skill from the skill
               names + descriptions (the same text Claude Code sees). Fast and cheap; the
               best signal for tuning descriptions. Needs `pip install anthropic` and an
               API key (ANTHROPIC_API_KEY or an `ant auth login` profile).

  claude-code  Run real headless Claude Code (`claude -p`) in a throwaway project with the
               skills installed under .claude/skills, and record which skill it loads first.
               Slower and costs more, but measures actual triggering. Only the Skill tool is
               allowed, and each run is stopped as soon as a skill loads (or --max-budget-usd).

Usage:
    python evals/run_trigger_evals.py                          # api mode, all cases
    python evals/run_trigger_evals.py --mode claude-code --limit 10
    python evals/run_trigger_evals.py --only dark-mode,ui-design --model claude-sonnet-5
    python evals/run_trigger_evals.py --dry-run                # print the routing prompt, no calls

Scoring: a case passes when the chosen skill is in `expected` (several are acceptable for
genuinely ambiguous prompts); `expected: []` means no design skill should load. Results are
written to evals/results/ (gitignored). Exit code is 1 if accuracy is below --min-accuracy.
"""

import argparse
import concurrent.futures
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")
CASES = os.path.join(ROOT, "evals", "triggers.jsonl")
RESULTS = os.path.join(ROOT, "evals", "results")

sys.path.insert(0, os.path.join(ROOT, "evals"))
from static_checks import description, load_skills  # noqa: E402

ROUTER_SYSTEM = """You route user requests to skills. A skill is a packaged set of expert \
instructions; loading the right one makes the result much better, loading the wrong one \
makes it worse. Pick the single skill whose description best matches the request, or \
"none" if no skill applies (for example, the request is not about design).

Available skills:
{catalog}"""


def load_cases(only=None, limit=None):
    cases = []
    with open(CASES, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            case = json.loads(line)
            case["id"] = i
            if only and not (set(case["expected"]) & only or (not case["expected"] and "none" in only)):
                continue
            cases.append(case)
    return cases[:limit] if limit else cases


def catalog(skills):
    return "\n".join(f"- {name}: {description(text)}" for name, text in skills.items())


# --- api mode ------------------------------------------------------------------------------

def route_api(client, model, system, names, prompt):
    schema = {
        "type": "object",
        "properties": {
            "skill": {"type": "string", "enum": names + ["none"]},
            "reason": {"type": "string"},
        },
        "required": ["skill", "reason"],
        "additionalProperties": False,
    }
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system,
        messages=[{"role": "user", "content": prompt}],
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": schema}},
    )
    if response.stop_reason == "refusal":
        return None, "refused"
    text = next((b.text for b in response.content if b.type == "text"), "{}")
    data = json.loads(text)
    return (None if data["skill"] == "none" else data["skill"]), data.get("reason", "")


# --- claude-code mode ----------------------------------------------------------------------

def make_workspace(skill_names):
    tmp = tempfile.mkdtemp(prefix="designskills-trigger-")
    target = os.path.join(tmp, ".claude", "skills")
    os.makedirs(target)
    for name in skill_names:
        shutil.copytree(os.path.join(SKILLS_DIR, name), os.path.join(target, name))
    return tmp


def first_skill_from_stream(lines):
    """Return (skill or None, saw_result) from Claude Code stream-json lines."""
    for line in lines:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use" and block.get("name") == "Skill":
                    skill = block.get("input", {}).get("skill", "")
                    return skill.split(":")[-1].strip("/"), False
        if event.get("type") == "result":
            return None, True
    return None, False


def route_claude_code(workspace, model, budget, prompt, timeout=180):
    cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--setting-sources", "project", "--allowedTools", "Skill",
           "--disallowedTools", "Bash,Write,Edit,NotebookEdit,WebFetch,WebSearch,Agent",
           "--no-session-persistence", "--max-budget-usd", str(budget)]
    if model:
        cmd += ["--model", model]
    proc = subprocess.Popen(cmd, cwd=workspace, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    lines = []
    try:
        deadline = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
        for line in proc.stdout:
            lines.append(line)
            skill, done = first_skill_from_stream([line])
            if skill or done or datetime.datetime.now() > deadline:
                return skill, "stream"
        return first_skill_from_stream(lines)[0], "stream"
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(5)
            except subprocess.TimeoutExpired:
                proc.kill()


# --- scoring -------------------------------------------------------------------------------

def score(results):
    total = len(results)
    passed = sum(r["pass"] for r in results)
    per_skill = {}
    for r in results:
        for skill in r["expected"] or ["none"]:
            s = per_skill.setdefault(skill, {"cases": 0, "hits": 0})
            s["cases"] += 1
            s["hits"] += r["pass"]
    chosen = {}
    for r in results:
        chosen.setdefault(r["chosen"] or "none", []).append(r["pass"])
    precision = {k: round(sum(v) / len(v), 2) for k, v in chosen.items()}
    return {"total": total, "passed": passed, "accuracy": round(passed / total, 3) if total else 0,
            "per_skill": per_skill, "precision_by_chosen": precision}


def main():
    parser = argparse.ArgumentParser(description="Skill-routing eval")
    parser.add_argument("--mode", choices=["api", "claude-code"], default="api")
    parser.add_argument("--model", help="Model id (api default: claude-opus-5; claude-code default: CLI default)")
    parser.add_argument("--only", help="Comma-separated expected skills to include (use 'none' for negatives)")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--budget", type=float, default=0.25, help="claude-code: max USD per case")
    parser.add_argument("--min-accuracy", type=float, default=0.85)
    parser.add_argument("--dry-run", action="store_true", help="Print the routing prompt and cases; no calls")
    args = parser.parse_args()

    skills = load_skills()
    names = list(skills)
    cases = load_cases(set(args.only.split(",")) if args.only else None, args.limit)
    for case in cases:
        unknown = set(case["expected"]) - set(names)
        if unknown:
            sys.exit(f"triggers.jsonl line {case['id']}: unknown skill(s) {sorted(unknown)}")
    system = ROUTER_SYSTEM.format(catalog=catalog(skills))

    if args.dry_run:
        print(system)
        print(f"\n{len(cases)} cases")
        return

    if args.mode == "api":
        try:
            import anthropic
        except ImportError:
            sys.exit("pip install anthropic")
        client = anthropic.Anthropic()
        model = args.model or "claude-opus-5"
        route = lambda prompt: route_api(client, model, system, names, prompt)
    else:
        if not shutil.which("claude"):
            sys.exit("claude CLI not found (npm i -g @anthropic-ai/claude-code)")
        workspace = make_workspace(names)
        model = args.model
        route = lambda prompt: route_claude_code(workspace, model, args.budget, prompt)

    def run(case):
        try:
            chosen, reason = route(case["prompt"])
        except Exception as e:  # keep going; report the error as a failed case
            chosen, reason = None, f"error: {type(e).__name__}: {e}"
        ok = (chosen in case["expected"]) if case["expected"] else chosen is None
        if reason.startswith("error"):
            ok = False
        return {**case, "chosen": chosen, "reason": reason, "pass": ok}

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(run, cases))

    summary = score(results)
    for r in results:
        if not r["pass"]:
            expected = ", ".join(r["expected"]) or "none"
            print(f"MISS  #{r['id']:<3} expected {expected:<32} got {r['chosen'] or 'none':<22} {r['prompt'][:60]}")
    print(f"\n{args.mode} / {model or 'default model'}: {summary['passed']}/{summary['total']} "
          f"= {summary['accuracy']:.0%}")
    weak = {k: v for k, v in summary["per_skill"].items() if v["hits"] < v["cases"]}
    if weak:
        print("Skills with misses: " + ", ".join(f"{k} {v['hits']}/{v['cases']}" for k, v in sorted(weak.items())))

    os.makedirs(RESULTS, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out = os.path.join(RESULTS, f"triggers-{args.mode}-{stamp}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"mode": args.mode, "model": model, "summary": summary, "results": results}, f, indent=2)
    print(f"Saved {os.path.relpath(out, ROOT)}")
    sys.exit(0 if summary["accuracy"] >= args.min_accuracy else 1)


if __name__ == "__main__":
    main()
