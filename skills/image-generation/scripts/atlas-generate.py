#!/usr/bin/env python3
"""Generate or edit images through Atlas Cloud without retrying submissions."""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_BASE = "https://api.atlascloud.ai/api/v1"
TEXT_MODEL = "openai/gpt-image-2/text-to-image"
EDIT_MODEL = "openai/gpt-image-2/edit"
TERMINAL_FAILURES = {"canceled", "cancelled", "failed", "error", "timeout"}
SUPPORTED_SIZES = (
    "1024x1024",
    "1024x768",
    "768x1024",
    "1024x1536",
    "1536x1024",
    "2048x2048",
    "2048x1152",
    "1152x2048",
    "2560x1088",
    "1088x2560",
    "2880x2160",
    "2160x2880",
    "3840x2160",
    "2160x3840",
)


class AtlasError(RuntimeError):
    """Atlas Cloud returned an error or an unexpected response."""


def unwrap(payload):
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        raise AtlasError("Atlas Cloud returned an unexpected response shape")
    return data


def headers(api_key, *, json_body=True):
    result = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": "designskills-atlas/1.0",
    }
    if json_body:
        result["Content-Type"] = "application/json"
    return result


def request_json(api_key, method, route, body=None, timeout=120):
    request = urllib.request.Request(
        f"{API_BASE}{route}",
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers=headers(api_key),
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        raise AtlasError(f"Atlas Cloud HTTP {error.code}: {detail}") from error
    if not isinstance(payload, dict):
        raise AtlasError("Atlas Cloud returned non-object JSON")
    return unwrap(payload)


def upload_image(api_key, image_path):
    image_path = Path(image_path).resolve()
    mime = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    boundary = f"----designskills-atlas-{time.time_ns()}"
    safe_name = image_path.name.replace('"', "_").replace("\r", "_").replace("\n", "_")
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{safe_name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode() + image_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    request = urllib.request.Request(
        f"{API_BASE}/model/uploadMedia",
        data=body,
        headers={
            **headers(api_key, json_body=False),
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")[:500]
        raise AtlasError(f"Atlas upload HTTP {error.code}: {detail}") from error
    url = unwrap(payload).get("download_url")
    if not isinstance(url, str) or not url.startswith("https://"):
        raise AtlasError("Atlas upload returned no HTTPS download URL")
    return url


def output_url(prediction):
    status = str(prediction.get("status") or "").lower()
    if status not in {"completed", "succeeded"}:
        return None
    outputs = prediction.get("outputs") or []
    if not outputs or not isinstance(outputs[0], str) or not outputs[0].startswith("https://"):
        raise AtlasError("Atlas Cloud completed without an HTTPS output URL")
    return outputs[0]


def submit_once(api_key, prompt, *, image_path=None, size="1024x1024", quality="medium"):
    payload = {
        "model": EDIT_MODEL if image_path else TEXT_MODEL,
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "output_format": "png",
    }
    if image_path:
        payload["images"] = [upload_image(api_key, image_path)]

    # This billable POST is intentionally submitted exactly once.
    return request_json(api_key, "POST", "/model/generateImage", payload)


def wait_for_output(api_key, prediction, *, max_polls=60, poll_interval=2.0):
    prediction_id = str(prediction.get("id") or "").strip()
    last_error = None
    for attempt in range(max_polls):
        url = output_url(prediction)
        if url:
            return url
        status = str(prediction.get("status") or "").lower()
        if status in TERMINAL_FAILURES:
            detail = prediction.get("error") or prediction.get("message") or status
            raise AtlasError(f"Atlas generation failed: {detail}")
        if not prediction_id:
            raise AtlasError("Atlas submission returned no prediction ID")
        if attempt + 1 >= max_polls:
            break

        time.sleep(min(poll_interval * (2 ** min(attempt, 3)), 15.0))
        try:
            prediction = request_json(
                api_key,
                "GET",
                f"/model/prediction/{urllib.parse.quote(prediction_id, safe='')}",
                timeout=30,
            )
            last_error = None
        except (AtlasError, urllib.error.URLError) as error:
            # Read-only prediction requests may retry within this bounded loop.
            last_error = error

    detail = f": {last_error}" if last_error else ""
    raise TimeoutError(f"Atlas prediction did not complete after {max_polls} polls{detail}")


def download_image(url, output_path):
    if not url.startswith("https://"):
        raise AtlasError("Refusing to download a non-HTTPS output URL")
    with urllib.request.urlopen(url, timeout=120) as response:
        content = response.read()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)
    print(f"Saved: {output_path}")


def generate(api_key, prompt, output, *, image_path=None, size="1024x1024", quality="medium"):
    prediction = submit_once(
        api_key,
        prompt,
        image_path=image_path,
        size=size,
        quality=quality,
    )
    download_image(wait_for_output(api_key, prediction), output)


def main():
    parser = argparse.ArgumentParser(description="Generate graphics with Atlas Cloud")
    parser.add_argument("--prompt", required=True, help="Text prompt for generation")
    parser.add_argument("--image", help="Input image path for editing")
    parser.add_argument("--output", default="output.png", help="Output image path")
    parser.add_argument("--size", choices=SUPPORTED_SIZES, default="1024x1024")
    parser.add_argument("--quality", choices=("low", "medium", "high"), default="medium")
    parser.add_argument("--then", dest="followup", help="Follow-up edit prompt")
    parser.add_argument("--output-then", default="output_v2.png", help="Follow-up output path")
    args = parser.parse_args()

    api_key = os.environ.get("ATLASCLOUD_API_KEY")
    if not api_key:
        print("Error: ATLASCLOUD_API_KEY environment variable not set.", file=sys.stderr)
        return 1

    try:
        generate(
            api_key,
            args.prompt,
            args.output,
            image_path=args.image,
            size=args.size,
            quality=args.quality,
        )
        if args.followup:
            generate(
                api_key,
                args.followup,
                args.output_then,
                image_path=args.output,
                size=args.size,
                quality=args.quality,
            )
    except (AtlasError, OSError, TimeoutError, urllib.error.URLError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
