#!/usr/bin/env python3
"""
Deterministic checks over every skill. Free, fast, no API keys -- run on every change.

    python evals/static_checks.py            # human-readable
    python evals/static_checks.py --json     # machine-readable

Checks:
  script-exists       `<skill>/scripts/<file>` references point at a real bundled script
  script-flags        every --flag used with a bundled script exists in that script
  aspect-ratio        every `--aspect-ratio X` is one Gemini supports
  gemini-model        every gemini-*-image model id matches the generator's MODEL
  python-blocks       ```python fences compile
  json-blocks         ```json fences parse
  js-blocks           ```js / ```javascript fences pass `node --check` (skipped without node)
  context-path        brand context is always `.agents/design-context.md`
  trigger-collisions  no quoted trigger phrase appears in two skills' descriptions
"""

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
GENERATOR = os.path.join(SKILLS, "image-generation", "scripts", "gemini-generate.py")

FENCE = re.compile(r"^```([\w+-]*)[^\n]*\n(.*?)^```", re.M | re.S)
SCRIPT_REF = re.compile(r"<([a-z0-9-]+)>/scripts/([\w.-]+)")
PLACEHOLDER = re.compile(r"\[[A-Za-z][^\]]*\]|\.\.\.|<[a-z-]+>|#X{3,6}")


def load_skills():
    skills = {}
    for name in sorted(os.listdir(SKILLS)):
        path = os.path.join(SKILLS, name, "SKILL.md")
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                skills[name] = f.read()
    return skills


def description(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return ""
    fm = m.group(1)
    d = re.search(r"^description:\s*[>|]?-?\s*(.*?)(?=^\w[\w-]*:|\Z)", fm, re.S | re.M)
    return " ".join(d.group(1).split()) if d else ""


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def generator_constants():
    with open(GENERATOR, encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    consts = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id in ("MODEL", "ASPECT_RATIOS"):
                consts[node.targets[0].id] = ast.literal_eval(node.value)
    return consts


def check(skills):
    failures = []  # (check, skill, line, message)
    consts = generator_constants()
    ratios, model = set(consts["ASPECT_RATIOS"]), consts["MODEL"]
    script_sources = {}

    for name, text in skills.items():
        # Bundled script references and the flags used with them
        for m in SCRIPT_REF.finditer(text):
            owner, script = m.groups()
            path = os.path.join(SKILLS, owner, "scripts", script)
            if not os.path.isfile(path):
                failures.append(("script-exists", name, line_of(text, m.start()), f"<{owner}>/scripts/{script} does not exist"))
                continue
            if path not in script_sources:
                with open(path, encoding="utf-8") as f:
                    script_sources[path] = f.read()
            # flags on the same logical line (follow backslash continuations)
            end = m.end()
            while True:
                nl = text.find("\n", end)
                if nl == -1 or not text[end:nl].rstrip().endswith("\\"):
                    break
                end = nl + 1
            nl = text.find("\n", end)
            rest = text[m.end(): nl if nl != -1 else len(text)]
            rest = re.split(r"`\s", rest)[0]  # stop at the end of an inline code span
            for flag in re.findall(r"(?<![\w-])(--[a-z][a-z0-9-]*)", rest):
                if f"'{flag}'" not in script_sources[path] and f'"{flag}"' not in script_sources[path]:
                    failures.append(("script-flags", name, line_of(text, m.start()), f"{script} has no {flag} option"))

        for m in re.finditer(r"--aspect-ratio[ =]([0-9]+:[0-9]+)", text):
            if m.group(1) not in ratios:
                failures.append(("aspect-ratio", name, line_of(text, m.start()), f"unsupported ratio {m.group(1)}"))

        for m in re.finditer(r"gemini-[\w.-]*image[\w.-]*", text):
            if m.group(0) != model:
                failures.append(("gemini-model", name, line_of(text, m.start()), f"{m.group(0)} != {model}"))

        for m in re.finditer(r"\.agents?/[\w.-]*context[\w.-]*", text):
            if m.group(0) != ".agents/design-context.md":
                failures.append(("context-path", name, line_of(text, m.start()), f"found {m.group(0)}"))

        for m in FENCE.finditer(text):
            lang, body = m.group(1).lower(), m.group(2)
            line = line_of(text, m.start())
            if lang in ("python", "py"):
                try:
                    ast.parse(body)
                except SyntaxError as e:
                    failures.append(("python-blocks", name, line + (e.lineno or 0), f"SyntaxError: {e.msg}"))
            elif lang == "json" and not PLACEHOLDER.search(body):
                try:
                    json.loads(body)
                except json.JSONDecodeError as e:
                    failures.append(("json-blocks", name, line + e.lineno, f"invalid JSON: {e.msg}"))

    failures += check_js(skills)
    failures += check_triggers(skills)
    return failures


def check_js(skills):
    node = shutil.which("node")
    if not node:
        return []
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in skills.items():
            for i, m in enumerate(FENCE.finditer(text)):
                if m.group(1).lower() not in ("js", "javascript", "mjs"):
                    continue
                body = m.group(2)
                if PLACEHOLDER.search(body) and "..." in body:
                    continue  # illustrative fragment
                ext = ".mjs" if re.search(r"^\s*(import|export)\s", body, re.M) else ".cjs"
                path = os.path.join(tmp, f"{name}-{i}{ext}")
                with open(path, "w", encoding="utf-8") as f:
                    f.write(body)
                result = subprocess.run([node, "--check", path], capture_output=True, text=True)
                if result.returncode:
                    msg = next((l for l in result.stderr.splitlines() if "Error" in l), result.stderr.strip()[:120])
                    failures.append(("js-blocks", name, line_of(text, m.start()), msg))
    return failures


def check_triggers(skills):
    owners = {}
    for name, text in skills.items():
        for phrase in re.findall(r'"([^"]{3,})"', description(text)):
            owners.setdefault(phrase.lower(), []).append(name)
    return [("trigger-collisions", ", ".join(names), 0, f'"{phrase}" appears in {len(names)} descriptions')
            for phrase, names in sorted(owners.items()) if len(names) > 1]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    skills = load_skills()
    failures = check(skills)
    if args.json:
        print(json.dumps([dict(zip(("check", "skill", "line", "message"), f)) for f in failures], indent=2))
    else:
        for c, skill, line, msg in failures:
            where = f"skills/{skill}/SKILL.md:{line}" if line else skill
            print(f"FAIL [{c}] {where}  {msg}")
        print(f"\n{len(skills)} skills checked, {len(failures)} problem(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
