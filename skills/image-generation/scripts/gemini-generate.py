#!/usr/bin/env python3
"""
Gemini Image Generation Utility for designskills.

Uses Gemini 3.1 Flash Image Preview to generate and edit graphics.
Requires: pip install google-genai Pillow

Set GEMINI_API_KEY environment variable before use.

Usage:
    # Text-to-image
    python gemini-generate.py --prompt "A bold product launch poster for a sneaker brand" --output poster.png

    # Image editing (product image + prompt); --image can be repeated (up to 14 references)
    python gemini-generate.py --prompt "Place this product on a gradient background with bold typography" \
        --image product.png --image logo.png --output graphic.png

    # With options
    python gemini-generate.py --prompt "..." --aspect-ratio 1:1 --size 2K --output social.png

    # Prompt from a file (useful for long, structured prompts)
    python gemini-generate.py --prompt-file prompt.txt --output graphic.png

    # Multi-turn editing session (--then can be repeated; outputs are v1.png, v1_2.png, v1_3.png ...)
    python gemini-generate.py --prompt "Create an infographic about cloud computing" --output v1.png \
        --then "Change the color scheme to dark mode" --then "Make the title larger"

    # Exact pixel dimensions (e.g. a 728x90 ad): generate at the nearest ratio, then center-crop + resize
    python gemini-generate.py --prompt "..." --aspect-ratio 8:1 --resize 728x90 --output leaderboard.png

Exit code is non-zero if any requested image was not produced.
"""

import argparse
import os
import sys

MODEL = "gemini-3.1-flash-image-preview"

ASPECT_RATIOS = [
    "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9",
    "1:4", "4:1", "1:8", "8:1",
]
SIZES = ["512", "1K", "2K", "4K"]
MAX_INPUT_IMAGES = 14


def get_client():
    try:
        from google import genai
    except ImportError:
        print("Error: google-genai not installed. Run: pip install google-genai Pillow", file=sys.stderr)
        sys.exit(1)
    return genai.Client()


def load_image(path):
    from PIL import Image
    if not os.path.isfile(path):
        print(f"Error: input image not found: {path}", file=sys.stderr)
        sys.exit(1)
    return Image.open(path)


def build_config(aspect_ratio=None, size=None):
    from google.genai import types

    image_config = {}
    if aspect_ratio:
        image_config["aspect_ratio"] = aspect_ratio
    if size:
        image_config["image_size"] = size

    return types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(**image_config) if image_config else None,
    )


def fit_to_size(image, width, height):
    """Center-crop to the target aspect ratio, then resize to exact pixel dimensions."""
    from PIL import Image

    src_w, src_h = image.size
    target_ratio = width / height
    if src_w / src_h > target_ratio:
        new_w = round(src_h * target_ratio)
        left = (src_w - new_w) // 2
        image = image.crop((left, 0, left + new_w, src_h))
    else:
        new_h = round(src_w / target_ratio)
        top = (src_h - new_h) // 2
        image = image.crop((0, top, src_w, top + new_h))
    return image.resize((width, height), Image.LANCZOS)


def save_image(response, output_path, resize=None):
    """Save the first image in the response. Returns True on success."""
    import io
    from PIL import Image

    parts = getattr(response, "parts", None) or []
    for part in parts:
        if getattr(part, "inline_data", None) is not None:
            image = Image.open(io.BytesIO(part.inline_data.data))
            if resize:
                image = fit_to_size(image, *resize)
            image.save(output_path)
            print(f"Saved: {output_path}")
            return True

    print(f"No image in response for {output_path}.", file=sys.stderr)
    text = getattr(response, "text", None)
    if text:
        print(f"Model response: {text}", file=sys.stderr)
    feedback = getattr(response, "prompt_feedback", None)
    if feedback:
        print(f"Prompt feedback: {feedback}", file=sys.stderr)
    return False


def ensure_parent_dir(path):
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)


def followup_path(base, index):
    root, ext = os.path.splitext(base)
    return f"{root}_{index}{ext or '.png'}"


def run(prompt, image_paths, followups, output, aspect_ratio, size, resize, followup_outputs=()):
    client = get_client()
    config = build_config(aspect_ratio, size)

    contents = [load_image(p) for p in image_paths]
    contents.append(prompt)

    ensure_parent_dir(output)
    ok = True

    if not followups:
        response = client.models.generate_content(model=MODEL, contents=contents, config=config)
        return save_image(response, output, resize)

    chat = client.chats.create(model=MODEL, config=config)
    response = chat.send_message(contents)
    ok &= save_image(response, output, resize)

    for i, followup in enumerate(followups, start=2):
        path = followup_outputs[i - 2] if i - 2 < len(followup_outputs) else followup_path(output, i)
        ensure_parent_dir(path)
        response = chat.send_message(followup)
        ok &= save_image(response, path, resize)

    return ok


def parse_resize(value):
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except ValueError:
        raise argparse.ArgumentTypeError("--resize must look like WIDTHxHEIGHT, e.g. 1080x1350")


def main():
    parser = argparse.ArgumentParser(description="Generate graphics with Gemini 3.1 Flash Image Preview")
    prompt_group = parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt", help="Text prompt for generation")
    prompt_group.add_argument("--prompt-file", help="Read the prompt from a text file")
    parser.add_argument("--image", action="append", default=[],
                        help=f"Input/reference image path (repeatable, max {MAX_INPUT_IMAGES})")
    parser.add_argument("--output", default="output.png", help="Output image path")
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, help="Output aspect ratio")
    parser.add_argument("--size", choices=SIZES, help="Output resolution")
    parser.add_argument("--resize", type=parse_resize,
                        help="Center-crop and resize output to exact WIDTHxHEIGHT pixels")
    parser.add_argument("--then", dest="followups", action="append", default=[],
                        help="Follow-up edit prompt in the same chat (repeatable)")
    parser.add_argument("--output-then", dest="followup_outputs", action="append", default=[],
                        help="Output path for each --then, in order (default: <output>_2.png, _3 ...)")

    args = parser.parse_args()

    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    if len(args.image) > MAX_INPUT_IMAGES:
        print(f"Error: at most {MAX_INPUT_IMAGES} input images are supported.", file=sys.stderr)
        sys.exit(1)

    if args.prompt_file:
        with open(args.prompt_file, encoding="utf-8") as f:
            prompt = f.read().strip()
    else:
        prompt = args.prompt

    ok = run(prompt, args.image, args.followups, args.output,
             args.aspect_ratio, args.size, args.resize, args.followup_outputs)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
