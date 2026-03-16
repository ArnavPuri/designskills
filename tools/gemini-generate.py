#!/usr/bin/env python3
"""
Gemini Image Generation Utility for designskills.

Uses Gemini 3.1 Flash Image Preview to generate and edit graphics.
Requires: pip install google-genai Pillow

Set GEMINI_API_KEY environment variable before use.

Usage:
    # Text-to-image
    python gemini-generate.py --prompt "A bold product launch poster for a sneaker brand" --output poster.png

    # Image editing (product image + prompt)
    python gemini-generate.py --prompt "Place this product on a gradient background with bold typography" \
        --image product.png --output graphic.png

    # With options
    python gemini-generate.py --prompt "..." --aspect-ratio 1:1 --size 2K --output social.png

    # Multi-turn editing session
    python gemini-generate.py --prompt "Create an infographic about cloud computing" --output v1.png \
        --then "Change the color scheme to dark mode" --output-then v2.png
"""

import argparse
import base64
import os
import sys

MODEL = "gemini-3.1-flash-image-preview"


def get_client():
    try:
        from google import genai
        return genai.Client()
    except ImportError:
        print("Error: google-genai not installed. Run: pip install google-genai", file=sys.stderr)
        sys.exit(1)


def load_image(path):
    from PIL import Image
    return Image.open(path)


def save_image(response, output_path):
    for part in response.parts:
        if part.inline_data is not None:
            image = part.as_image()
            image.save(output_path)
            print(f"Saved: {output_path}")
            return True
    print("No image in response.", file=sys.stderr)
    if response.text:
        print(f"Model response: {response.text}", file=sys.stderr)
    return False


def generate(prompt, image_path=None, aspect_ratio=None, size=None, output="output.png"):
    from google.genai import types

    client = get_client()

    config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    )

    contents = []
    if image_path:
        contents.append(load_image(image_path))
    contents.append(prompt)

    response = client.models.generate_content(
        model=MODEL,
        contents=contents,
        config=config,
    )

    return save_image(response, output)


def generate_multi_turn(prompt1, prompt2, image_path=None, output1="v1.png", output2="v2.png"):
    from google.genai import types

    client = get_client()

    chat = client.chats.create(
        model=MODEL,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        ),
    )

    contents = []
    if image_path:
        contents.append(load_image(image_path))
    contents.append(prompt1)

    response1 = chat.send_message(contents)
    save_image(response1, output1)

    response2 = chat.send_message(prompt2)
    save_image(response2, output2)


def main():
    parser = argparse.ArgumentParser(description="Generate graphics with Gemini 3.1 Flash Image Preview")
    parser.add_argument("--prompt", required=True, help="Text prompt for generation")
    parser.add_argument("--image", help="Input image path for editing")
    parser.add_argument("--output", default="output.png", help="Output image path")
    parser.add_argument("--aspect-ratio", help="Aspect ratio (e.g., 1:1, 16:9, 4:3)")
    parser.add_argument("--size", help="Image size (512, 1K, 2K, 4K)")
    parser.add_argument("--then", dest="followup", help="Follow-up edit prompt (multi-turn)")
    parser.add_argument("--output-then", default="output_v2.png", help="Output path for follow-up")

    args = parser.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    if args.followup:
        generate_multi_turn(
            args.prompt, args.followup,
            image_path=args.image,
            output1=args.output,
            output2=args.output_then,
        )
    else:
        generate(
            args.prompt,
            image_path=args.image,
            aspect_ratio=args.aspect_ratio,
            size=args.size,
            output=args.output,
        )


if __name__ == "__main__":
    main()
