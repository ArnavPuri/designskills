#!/usr/bin/env python3
"""
Generate an 11-step OKLCH color scale (50-950) as sRGB hex, with WCAG contrast per step.
No dependencies.

Usage:
    python palette.py 250 0.15                     # hue, chroma -> table
    python palette.py --from "#2563eb"             # derive hue/chroma from a brand color
    python palette.py --from "#2563eb" --name brand --css    # CSS custom properties
    python palette.py 250 0.02 --name gray --json            # JSON for tokens / tooling

Steps keep hue fixed and taper chroma at the light and dark ends; out-of-gamut colors lose
chroma (never lightness or hue) until they fit sRGB. The table marks which steps pass 4.5:1
(normal text) and 3:1 (large text / UI) on white and on black, so you can pick text, border,
and fill steps directly.
"""

import argparse
import json
import math
import re
import sys

# step: (OKLCH lightness, chroma factor)
STOPS = {
    50: (0.97, 0.30), 100: (0.93, 0.40), 200: (0.87, 0.50), 300: (0.78, 0.70),
    400: (0.68, 0.85), 500: (0.55, 1.00), 600: (0.48, 1.00), 700: (0.40, 1.00),
    800: (0.32, 0.90), 900: (0.24, 0.80), 950: (0.16, 0.70),
}


def _linear_rgb(L, C, H):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)


def oklch_to_hex(L, C, H):
    while C > 0 and not all(-1e-4 <= x <= 1 + 1e-4 for x in _linear_rgb(L, C, H)):
        C -= 0.002  # out of sRGB gamut: reduce chroma, keep L and H
    enc = lambda x: 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
    return "#" + "".join(f"{round(min(1, max(0, enc(x))) * 255):02x}" for x in _linear_rgb(L, max(C, 0), H))


def hex_to_oklch(hx):
    m = re.fullmatch(r"#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})", hx.strip())
    if not m:
        raise ValueError(f"expected a hex color like #2563eb, got {hx!r}")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    lin = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m_, s = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m_, s))
    L = 0.2104542553 * l + 0.7936177850 * m_ - 0.0040720468 * s
    a = 1.9779984951 * l - 2.4285922050 * m_ + 0.4505937099 * s
    bb = 0.0259040371 * l + 0.7827717662 * m_ - 0.8086757660 * s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360


def luminance(hx):
    c = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def build_scale(hue, chroma):
    scale = []
    for step, (L, factor) in STOPS.items():
        hx = oklch_to_hex(L, chroma * factor, hue)
        scale.append({
            "step": step,
            "hex": hx,
            "oklch": f"oklch({L:.2f} {chroma * factor:.3f} {hue:.1f})",
            "on_white": round(contrast(hx, "#ffffff"), 2),
            "on_black": round(contrast(hx, "#000000"), 2),
        })
    return scale


def grade(r):
    return "AA" if r >= 4.5 else "large/UI" if r >= 3 else "-"


def main():
    parser = argparse.ArgumentParser(description="Generate an OKLCH color scale")
    parser.add_argument("hue", nargs="?", type=float, help="OKLCH hue in degrees (0-360)")
    parser.add_argument("chroma", nargs="?", type=float, help="Peak OKLCH chroma (0.02 neutral - 0.2 vivid)")
    parser.add_argument("--from", dest="source", help="Derive hue and chroma from a hex color")
    parser.add_argument("--name", default="brand", help="Token name for --css/--json (default: brand)")
    parser.add_argument("--css", action="store_true", help="Print CSS custom properties")
    parser.add_argument("--json", action="store_true", help="Print JSON")
    args = parser.parse_args()

    if args.source:
        try:
            L, chroma, hue = hex_to_oklch(args.source)
        except ValueError as e:
            parser.error(str(e))
        print(f"# {args.source} = oklch({L:.2f} {chroma:.3f} {hue:.1f}); "
              f"closest step is {min(STOPS, key=lambda s: abs(STOPS[s][0] - L))}", file=sys.stderr)
    elif args.hue is not None and args.chroma is not None:
        hue, chroma = args.hue, args.chroma
    else:
        parser.error("give HUE CHROMA or --from HEX")

    scale = build_scale(hue, chroma)
    if args.json:
        print(json.dumps({args.name: scale}, indent=2))
    elif args.css:
        print(":root {")
        for s in scale:
            print(f"  --{args.name}-{s['step']}: {s['hex']};  /* {s['oklch']} */")
        print("}")
    else:
        print(f"{'step':>4}  {'hex':8} {'on white':>14} {'on black':>14}")
        for s in scale:
            print(f"{s['step']:>4}  {s['hex']:8} {s['on_white']:6.2f} {grade(s['on_white']):>7} "
                  f"{s['on_black']:6.2f} {grade(s['on_black']):>7}")


if __name__ == "__main__":
    main()
