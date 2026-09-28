#!/usr/bin/env python3
"""
WCAG 2.x contrast checker for designskills. No dependencies.

Usage:
    # Check one or more foreground/background pairs
    python contrast.py "#737373" "#ffffff"
    python contrast.py "#fff" "#2563eb" "oklch(0.55 0.2 260)" "#fafafa"

    # Check the standard pairings in a saved design context (exit 1 on any failure)
    python contrast.py --context .agents/design-context.md

    # Machine-readable output
    python contrast.py --json "#737373" "#ffffff"

Accepted colors: #rgb, #rrggbb, #rrggbbaa (alpha ignored), rgb(r g b) / rgb(r, g, b),
oklch(L C H) with L as 0-1 or a percentage.

Thresholds (WCAG 2.2): normal text 4.5:1, large text (>=24px, or >=18.66px bold) 3:1,
non-text UI (borders of inputs, icons, focus rings) 3:1. For every failing pair the script
suggests the nearest passing foreground, found by moving OKLCH lightness only, so hue and
chroma (the brand feel) are kept.
"""

import argparse
import json
import math
import re
import sys

NORMAL, LARGE, UI = 4.5, 3.0, 3.0


# --- color parsing and conversion -------------------------------------------------------

def parse_color(value):
    """Return (r, g, b) floats in 0-1 sRGB."""
    v = value.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        elif len(h) in (6, 8):
            h = h[:6]
        else:
            raise ValueError(f"bad hex color: {value}")
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+).*\)", v)
    if m:
        return tuple(min(float(x), 255) / 255 for x in m.groups())
    m = re.fullmatch(r"oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)(?:deg)?\s*(?:/.*)?\)", v)
    if m:
        lightness = float(m.group(1)) / (100 if m.group(2) else 1)
        return oklch_to_srgb(lightness, float(m.group(3)), float(m.group(4)))
    raise ValueError(f"unrecognized color: {value}")


def to_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02x}" for c in rgb)


def _linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _gamma(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def luminance(rgb):
    r, g, b = (_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    l1, l2 = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def srgb_to_oklch(rgb):
    r, g, b = (_linear(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def oklch_to_srgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bl = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return tuple(max(0.0, min(1.0, _gamma(max(0.0, c)))) for c in (r, g, bl))


def suggest(fg, bg, target):
    """Nearest foreground (by OKLCH lightness only) reaching `target` against bg."""
    L, C, H = srgb_to_oklch(fg)
    darker = luminance(bg) > 0.18  # light background -> darken the text
    step = -0.005 if darker else 0.005
    for i in range(1, 200):
        candidate = to_hex(oklch_to_srgb(min(1, max(0, L + step * i)), C, H))
        if ratio(parse_color(candidate), bg) >= target:  # check the rounded hex, not the float
            return candidate
    return "#000000" if darker else "#ffffff"


# --- checks ------------------------------------------------------------------------------

def check_pair(fg_str, bg_str, target=NORMAL, label=None):
    fg, bg = parse_color(fg_str), parse_color(bg_str)
    r = ratio(fg, bg)
    result = {
        "label": label or f"{fg_str} on {bg_str}",
        "foreground": to_hex(fg),
        "background": to_hex(bg),
        "ratio": round(r, 2),
        "normal_text": r >= NORMAL,
        "large_text": r >= LARGE,
        "ui": r >= UI,
        "required": target,
        "pass": r >= target,
    }
    if not result["pass"]:
        result["suggestion"] = suggest(fg, bg, target)
    return result


# Standard pairings checked for a design context: (label, fg role, bg role, required ratio)
CONTEXT_PAIRS = [
    ("Body text on page background", "Neutral 800", "Neutral 50", NORMAL),
    ("Body text on white", "Neutral 800", "#ffffff", NORMAL),
    ("Headings on page background", "Neutral 900", "Neutral 50", NORMAL),
    ("Muted text on white", "Neutral 500", "#ffffff", NORMAL),
    ("White text on primary button", "#ffffff", "Primary", NORMAL),
    ("White text on primary hover", "#ffffff", "Primary Dark", NORMAL),
    ("Primary as link text on white", "Primary", "#ffffff", NORMAL),
    ("Primary as focus ring / icon on white", "Primary", "#ffffff", UI),
    # Semantic colors are usually fills/icons; text needs a darker shade (see design-context).
    ("Error as icon/border on white", "Error", "#ffffff", UI),
    ("Success as icon/border on white", "Success", "#ffffff", UI),
    ("Warning as icon/border on white", "Warning", "#ffffff", UI),
]


def parse_context(path):
    """Read `| Role | #hex | ... |` rows from a design-context.md color table."""
    roles = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and re.fullmatch(r"#[0-9a-fA-F]{3,8}", cells[1]):
                roles[cells[0]] = cells[1]
    return roles


def check_context(path):
    roles = parse_context(path)
    if not roles:
        raise SystemExit(f"No color table rows like '| Primary | #2563EB | ... |' found in {path}")
    results, skipped = [], []
    for label, fg, bg, target in CONTEXT_PAIRS:
        fg_val, bg_val = roles.get(fg, fg), roles.get(bg, bg)
        if not fg_val.startswith("#") or not bg_val.startswith("#"):
            skipped.append(label)
            continue
        results.append(check_pair(fg_val, bg_val, target, label))
    return results, skipped


def print_table(results):
    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        line = (f"{status}  {r['ratio']:>5.2f}:1  (needs {r['required']}:1)  {r['label']}"
                f"  [{r['foreground']} on {r['background']}]")
        if not r["pass"]:
            line += f"  -> try {r['suggestion']}"
        print(line)


def main():
    parser = argparse.ArgumentParser(description="WCAG 2.x contrast checker")
    parser.add_argument("colors", nargs="*", help="foreground background [foreground background ...]")
    parser.add_argument("--context", help="Check the standard pairings in a design-context.md file")
    parser.add_argument("--large", action="store_true", help="Judge pairs as large text / UI (3:1)")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args()

    skipped = []
    if args.context:
        results, skipped = check_context(args.context)
    else:
        if not args.colors or len(args.colors) % 2:
            parser.error("pass colors in foreground/background pairs, or use --context")
        target = LARGE if args.large else NORMAL
        try:
            results = [check_pair(args.colors[i], args.colors[i + 1], target)
                       for i in range(0, len(args.colors), 2)]
        except ValueError as e:
            parser.error(str(e))

    if args.json:
        print(json.dumps({"results": results, "skipped": skipped}, indent=2))
    else:
        print_table(results)
        for label in skipped:
            print(f"SKIP  {label} (role missing from context)")
    sys.exit(0 if all(r["pass"] for r in results) else 1)


if __name__ == "__main__":
    main()
