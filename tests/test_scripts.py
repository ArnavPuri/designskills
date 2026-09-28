"""
Unit tests for the scripts bundled with the skills. Offline: no API keys needed.

    python -m unittest discover tests -v

Browser tests (render.mjs, audit.mjs) run only when Node and Playwright are available.
"""

import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
FIXTURES = os.path.join(ROOT, "tests", "fixtures")


def load(name, relpath):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SKILLS, relpath))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True)


def playwright_available():
    if not shutil.which("node"):
        return False
    probe = ("import('playwright').then(()=>process.exit(0)).catch(()=>{"
             "try{const r=require('child_process').execSync('npm root -g').toString().trim();"
             "require(require('path').join(r,'playwright'));process.exit(0)}catch(e){process.exit(1)}})")
    return subprocess.run(["node", "-e", probe], capture_output=True).returncode == 0


class ContrastTests(unittest.TestCase):
    def setUp(self):
        self.c = load("contrast", "design-context/scripts/contrast.py")

    def test_known_ratios(self):
        self.assertAlmostEqual(self.c.check_pair("#000", "#fff")["ratio"], 21.0)
        self.assertAlmostEqual(self.c.check_pair("#737373", "#ffffff")["ratio"], 4.74, places=2)
        self.assertAlmostEqual(self.c.check_pair("#2563EB", "#FFFFFF")["ratio"], 5.17, places=2)

    def test_color_formats(self):
        for value in ("#fff", "#ffffff", "#ffffffcc", "rgb(255 255 255)", "rgb(255, 255, 255)", "oklch(1 0 0)"):
            self.assertEqual(self.c.to_hex(self.c.parse_color(value)), "#ffffff", value)
        with self.assertRaises(ValueError):
            self.c.parse_color("blue-ish")

    def test_suggestion_passes(self):
        for fg, bg in (("#F59E0B", "#ffffff"), ("#10B981", "#ffffff"), ("#555555", "#000000")):
            result = self.c.check_pair(fg, bg)
            self.assertFalse(result["pass"])
            self.assertTrue(self.c.check_pair(result["suggestion"], bg)["pass"], result)

    def test_context_file(self):
        results, skipped = self.c.check_context(os.path.join(ROOT, "evals", "fixtures", "design-context.md"))
        self.assertEqual(skipped, [])
        self.assertTrue(all(r["pass"] for r in results), [r for r in results if not r["pass"]])

    def test_cli_exit_codes(self):
        script = os.path.join(SKILLS, "design-context", "scripts", "contrast.py")
        self.assertEqual(run(sys.executable, script, "#000", "#fff").returncode, 0)
        self.assertEqual(run(sys.executable, script, "#bbb", "#fff").returncode, 1)
        out = run(sys.executable, script, "--json", "#bbb", "#fff")
        self.assertIn("suggestion", json.loads(out.stdout)["results"][0])


class PaletteTests(unittest.TestCase):
    def setUp(self):
        self.p = load("palette", "color-palette/scripts/palette.py")

    def test_scale_is_monotonic_and_round_trips(self):
        L, C, H = self.p.hex_to_oklch("#2563eb")
        scale = self.p.build_scale(H, C)
        self.assertEqual([s["step"] for s in scale], [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950])
        whites = [s["on_white"] for s in scale]
        self.assertEqual(whites, sorted(whites), "contrast on white should rise with each step")
        step500 = scale[5]["hex"]
        self.assertLess(sum(abs(int(step500[i:i + 2], 16) - int("2563eb"[i - 1:i + 1], 16)) for i in (1, 3, 5)), 12)

    def test_css_output(self):
        out = run(sys.executable, os.path.join(SKILLS, "color-palette", "scripts", "palette.py"),
                  "250", "0.02", "--name", "gray", "--css")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("--gray-500:", out.stdout)


class GeneratorTests(unittest.TestCase):
    """gemini-generate.py against a stubbed client, using the real google-genai types when installed."""

    def setUp(self):
        try:
            import google.genai  # noqa: F401
            from PIL import Image  # noqa: F401
        except ImportError:
            self.skipTest("google-genai / Pillow not installed")
        self.g = load("gen", "image-generation/scripts/gemini-generate.py")
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def fake_client(self, calls, with_image=True):
        from PIL import Image
        buf = io.BytesIO()
        Image.new("RGB", (1600, 200), "red").save(buf, "PNG")
        image_part = types.SimpleNamespace(inline_data=types.SimpleNamespace(data=buf.getvalue()))
        text_part = types.SimpleNamespace(inline_data=None)
        response = types.SimpleNamespace(parts=[text_part, image_part] if with_image else [text_part],
                                         text="model text", prompt_feedback=None)

        class Chat:
            def send_message(self, contents):
                calls.append(("chat", contents))
                return response

        def generate_content(**kwargs):
            calls.append(("generate", kwargs))
            return response

        return types.SimpleNamespace(models=types.SimpleNamespace(generate_content=generate_content),
                                     chats=types.SimpleNamespace(create=lambda **kw: Chat()))

    def test_config_carries_ratio_and_size(self):
        config = self.g.build_config("16:9", "2K")
        self.assertEqual((config.image_config.aspect_ratio, config.image_config.image_size), ("16:9", "2K"))
        self.assertIsNone(self.g.build_config().image_config)

    def test_resize_to_exact_pixels(self):
        from PIL import Image
        calls = []
        self.g.get_client = lambda: self.fake_client(calls)
        out = os.path.join(self.tmp, "nested", "ad.png")
        self.assertTrue(self.g.run("prompt", [], [], out, "8:1", None, (728, 90)))
        self.assertEqual(Image.open(out).size, (728, 90))
        self.assertEqual(calls[0][1]["config"].image_config.aspect_ratio, "8:1")

    def test_multi_turn_outputs(self):
        calls = []
        self.g.get_client = lambda: self.fake_client(calls)
        base = os.path.join(self.tmp, "v1.png")
        custom = os.path.join(self.tmp, "custom.png")
        self.assertTrue(self.g.run("p", [], ["a", "b"], base, None, None, None, [custom]))
        self.assertTrue(os.path.exists(custom))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "v1_3.png")))
        self.assertEqual(len(calls), 3)

    def test_no_image_is_a_failure(self):
        calls = []
        self.g.get_client = lambda: self.fake_client(calls, with_image=False)
        self.assertFalse(self.g.run("p", [], [], os.path.join(self.tmp, "x.png"), None, None, None))

    def test_fit_to_size_keeps_center(self):
        from PIL import Image
        img = Image.new("RGB", (300, 100), "white")
        img.paste((255, 0, 0), (100, 0, 200, 100))  # red center third
        out = self.g.fit_to_size(img, 100, 100)
        self.assertEqual(out.size, (100, 100))
        self.assertEqual(out.getpixel((50, 50)), (255, 0, 0))


class ExportSizesTests(unittest.TestCase):
    def setUp(self):
        try:
            from PIL import Image  # noqa: F401
        except ImportError:
            self.skipTest("Pillow not installed")
        self.e = load("export_sizes", "image-generation/scripts/export-sizes.py")

    def test_crop_box_respects_focus_and_bounds(self):
        self.assertEqual(self.e.crop_box(1000, 1000, 1600, 900), (0, 219, 1000, 781))
        top = self.e.crop_box(1000, 1000, 1600, 900, focus=(0.5, 0.0))
        self.assertEqual(top[1], 0)
        bottom = self.e.crop_box(1000, 1000, 1600, 900, focus=(0.5, 1.0))
        self.assertEqual(bottom[3], 1000)

    def test_cli_exports_presets(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            master = os.path.join(tmp, "master.png")
            Image.new("RGB", (2048, 2048), "navy").save(master)
            script = os.path.join(SKILLS, "image-generation", "scripts", "export-sizes.py")
            out = run(sys.executable, script, master, "--presets", "og,instagram-story,leaderboard",
                      "--size", "300x250", "--out", os.path.join(tmp, "out"))
            self.assertEqual(out.returncode, 0, out.stderr)
            sizes = sorted(Image.open(os.path.join(tmp, "out", f)).size for f in os.listdir(os.path.join(tmp, "out")))
            self.assertEqual(sizes, [(300, 250), (728, 90), (1080, 1920), (1200, 630)])
            self.assertIn("keeps only", out.stderr)  # 8:1 crop from a square master warns
            self.assertEqual(out.stderr.count("keeps only"), 1)  # 9:16 keeps 56%, no warning


@unittest.skipUnless(playwright_available(), "Node + Playwright not available")
class BrowserScriptTests(unittest.TestCase):
    def test_render_exact_size(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "ad.png")
            proc = run("node", os.path.join(SKILLS, "graphic-design", "scripts", "render.mjs"),
                       os.path.join(FIXTURES, "overlay.html"), "--size", "300x250", "--scale", "2", "--out", out)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(Image.open(out).size, (600, 500))

    def test_render_warns_on_overflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = run("node", os.path.join(SKILLS, "graphic-design", "scripts", "render.mjs"),
                       os.path.join(FIXTURES, "flawed-page.html"), "--widths", "390", "--out",
                       os.path.join(tmp, "page.png"))
            self.assertEqual(proc.returncode, 3)
            self.assertIn("wider than", proc.stderr)

    def test_audit_finds_planted_flaws(self):
        with tempfile.TemporaryDirectory() as tmp:
            proc = run("node", os.path.join(SKILLS, "design-critique", "scripts", "audit.mjs"),
                       os.path.join(FIXTURES, "flawed-page.html"), tmp, "--widths", "390,1440", "--no-axe")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            report = json.loads(proc.stdout)
            mobile, structure = report["widths"]["mobile"], report["structure"]
            self.assertTrue(mobile["horizontalOverflow"])
            self.assertTrue(any(f["text"] == "Low contrast text" for f in mobile["contrastFailures"]))
            self.assertTrue(mobile["smallTargets"])
            self.assertIsNone(structure["lang"])
            self.assertEqual(structure["skippedHeadingLevels"], 1)
            self.assertTrue(structure["imagesMissingAlt"])
            self.assertTrue(structure["unlabeledControls"])
            self.assertTrue(structure["lazyImagesAboveFold"])
            self.assertTrue(structure["animationWithoutReducedMotion"])
            for name in ("mobile-fold.png", "desktop-full.png", "desktop-dark-fold.png", "report.json"):
                self.assertTrue(os.path.exists(os.path.join(tmp, name)), name)


class StaticChecksTests(unittest.TestCase):
    def test_repo_is_clean(self):
        proc = run(sys.executable, os.path.join(ROOT, "evals", "static_checks.py"))
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_trigger_cases_reference_real_skills(self):
        names = set(os.listdir(SKILLS))
        with open(os.path.join(ROOT, "evals", "triggers.jsonl"), encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if line.strip():
                    case = json.loads(line)
                    self.assertTrue(set(case["expected"]) <= names, f"line {n}: {case['expected']}")

    def test_task_files_are_valid(self):
        tasks_dir = os.path.join(ROOT, "evals", "tasks")
        known = {"skill_loaded", "file_exists", "file_contains", "file_not_contains", "file_unchanged",
                 "max_file_kb", "brand_colors", "image_size", "image_aspect", "audit", "command", "response_contains"}
        for name in os.listdir(tasks_dir):
            with open(os.path.join(tasks_dir, name), encoding="utf-8") as f:
                task = json.load(f)
            self.assertEqual(task["id"] + ".json", name)
            self.assertTrue(os.path.isdir(os.path.join(SKILLS, task["skill"])), name)
            for src in task.get("seed", {}).values():
                self.assertTrue(os.path.exists(os.path.join(ROOT, src)), f"{name}: {src}")
            for check in task["checks"]:
                self.assertIn(check["type"], known, name)


if __name__ == "__main__":
    unittest.main()
