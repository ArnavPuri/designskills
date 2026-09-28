#!/usr/bin/env python3
"""
Export one master image to many platform sizes (center or focal-point crop + resize).

Requires: pip install Pillow

Usage:
    # Named presets (comma-separated) or preset groups
    python export-sizes.py master.png --presets instagram-feed,instagram-story,og --out exports/
    python export-sizes.py master.png --group social --out exports/

    # Custom sizes
    python export-sizes.py master.png --size 300x250 --size 728x90 --out ads/

    # Keep the subject in frame: focal point as fractions of width,height (default 0.5,0.5)
    python export-sizes.py master.png --group ads --focus 0.5,0.35 --out ads/

    # List presets
    python export-sizes.py --list

Generate the master at the largest ratio you need (e.g. 1:1 or 4:5 at 2K/4K) with the subject
centered and generous margins; extreme crops (8:1, 1:4) from a square master lose most of the
image, so generate those separately with the matching --aspect-ratio instead. The script warns
when a crop keeps less than 50% of the master or when it has to upscale.
"""

import argparse
import os
import sys

PRESETS = {
    # social
    "instagram-feed": (1080, 1350),
    "instagram-square": (1080, 1080),
    "instagram-story": (1080, 1920),
    "tiktok": (1080, 1920),
    "x-post": (1600, 900),
    "linkedin-post": (1200, 1200),
    "linkedin-link": (1200, 627),
    "facebook-feed": (1080, 1350),
    "og": (1200, 630),
    "pinterest": (1000, 1500),
    "youtube-thumbnail": (1280, 720),
    # display ads (IAB)
    "medium-rectangle": (300, 250),
    "large-rectangle": (336, 280),
    "leaderboard": (728, 90),
    "mobile-banner": (320, 50),
    "large-mobile-banner": (320, 100),
    "half-page": (300, 600),
    "wide-skyscraper": (160, 600),
    "billboard": (970, 250),
    # web / email
    "email-header": (1200, 400),
    "hero-desktop": (2560, 1440),
}

GROUPS = {
    "social": ["instagram-feed", "instagram-square", "instagram-story", "x-post",
               "linkedin-post", "og", "pinterest"],
    "ads": ["medium-rectangle", "large-rectangle", "leaderboard", "mobile-banner",
            "half-page", "wide-skyscraper", "billboard"],
    "video": ["youtube-thumbnail", "instagram-story", "tiktok"],
}


def parse_size(value):
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except ValueError:
        raise argparse.ArgumentTypeError(f"size must look like WIDTHxHEIGHT, got {value!r}")


def parse_focus(value):
    try:
        x, y = (float(v) for v in value.split(","))
    except ValueError:
        raise argparse.ArgumentTypeError("focus must look like 0.5,0.4")
    if not (0 <= x <= 1 and 0 <= y <= 1):
        raise argparse.ArgumentTypeError("focus values must be between 0 and 1")
    return x, y


def crop_box(src_w, src_h, width, height, focus=(0.5, 0.5)):
    """Largest box with the target ratio, centered on the focal point, kept inside the image."""
    target = width / height
    if src_w / src_h > target:
        box_w, box_h = round(src_h * target), src_h
    else:
        box_w, box_h = src_w, round(src_w / target)
    left = min(max(round(focus[0] * src_w - box_w / 2), 0), src_w - box_w)
    top = min(max(round(focus[1] * src_h - box_h / 2), 0), src_h - box_h)
    return left, top, left + box_w, top + box_h


def export(image, name, width, height, out_dir, focus, fmt):
    from PIL import Image

    box = crop_box(image.width, image.height, width, height, focus)
    kept = (box[2] - box[0]) * (box[3] - box[1]) / (image.width * image.height)
    warnings = []
    if kept < 0.5:
        warnings.append(f"keeps only {kept:.0%} of the master; consider generating this ratio separately")
    if box[2] - box[0] < width:
        warnings.append(f"upscaled from {box[2] - box[0]}px wide; generate the master larger (--size 2K/4K)")
    result = image.crop(box).resize((width, height), Image.LANCZOS)
    path = os.path.join(out_dir, f"{name}-{width}x{height}.{fmt}")
    if fmt in ("jpg", "jpeg"):
        result.convert("RGB").save(path, quality=90, optimize=True, progressive=True)
    elif fmt == "webp":
        result.save(path, quality=88)
    else:
        result.save(path, optimize=True)
    return path, warnings


def main():
    parser = argparse.ArgumentParser(description="Export a master image to platform sizes")
    parser.add_argument("image", nargs="?", help="Master image path")
    parser.add_argument("--presets", help="Comma-separated preset names")
    parser.add_argument("--group", choices=sorted(GROUPS), action="append", default=[],
                        help="Preset group (repeatable)")
    parser.add_argument("--size", type=parse_size, action="append", default=[], help="Custom WIDTHxHEIGHT")
    parser.add_argument("--focus", type=parse_focus, default=(0.5, 0.5), help="Focal point x,y in 0-1")
    parser.add_argument("--format", default="png", choices=["png", "jpg", "webp"], help="Output format")
    parser.add_argument("--out", default="exports", help="Output directory")
    parser.add_argument("--list", action="store_true", help="List presets and groups")
    args = parser.parse_args()

    if args.list:
        for name, (w, h) in PRESETS.items():
            print(f"{name:22} {w}x{h}")
        for group, names in GROUPS.items():
            print(f"group {group}: {', '.join(names)}")
        return

    if not args.image:
        parser.error("image is required")

    targets = []
    names = [n.strip() for n in (args.presets or "").split(",") if n.strip()]
    for group in args.group:
        names += GROUPS[group]
    for name in dict.fromkeys(names):
        if name not in PRESETS:
            parser.error(f"unknown preset {name!r}; run --list")
        targets.append((name, *PRESETS[name]))
    targets += [("custom", w, h) for w, h in args.size]
    if not targets:
        parser.error("choose --presets, --group, or --size")

    try:
        from PIL import Image
    except ImportError:
        sys.exit("Error: Pillow not installed. Run: pip install Pillow")

    image = Image.open(args.image)
    image.load()
    os.makedirs(args.out, exist_ok=True)
    for name, w, h in targets:
        path, warnings = export(image, name, w, h, args.out, args.focus, args.format)
        print(f"Saved: {path}")
        for warning in warnings:
            print(f"  warning: {warning}", file=sys.stderr)


if __name__ == "__main__":
    main()
