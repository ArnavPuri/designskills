import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "tools" / "atlas-generate.py"
SPEC = importlib.util.spec_from_file_location("atlas_generate", SCRIPT)
atlas = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(atlas)


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_args):
        self.close()


def json_response(payload):
    return FakeResponse(json.dumps(payload).encode())


class AtlasGenerateTests(unittest.TestCase):
    def test_text_generation_submits_once_then_polls_and_downloads(self):
        calls = []
        payloads = []
        responses = iter([
            json_response({"data": {"id": "prediction-1", "status": "created"}}),
            json_response({"data": {
                "id": "prediction-1",
                "status": "completed",
                "outputs": ["https://cdn.example/image.png"],
            }}),
            FakeResponse(b"png-bytes"),
        ])

        def fake_urlopen(request, timeout=None):
            if isinstance(request, urllib.request.Request):
                calls.append((request.get_method(), request.full_url))
                if request.full_url.endswith("/model/generateImage"):
                    payloads.append(json.loads(request.data.decode()))
            else:
                calls.append(("GET", request))
            return next(responses)

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "result.png"
            with mock.patch.object(urllib.request, "urlopen", fake_urlopen), \
                    mock.patch.object(atlas.time, "sleep", lambda _delay: None):
                atlas.generate("test-key", "A geometric poster", output, size="1024x768")

            self.assertEqual(output.read_bytes(), b"png-bytes")

        self.assertEqual(
            sum(url.endswith("/model/generateImage") for _method, url in calls), 1
        )
        self.assertEqual(payloads, [{
            "model": "openai/gpt-image-2/text-to-image",
            "prompt": "A geometric poster",
            "size": "1024x768",
            "quality": "medium",
            "output_format": "png",
        }])

    def test_edit_uploads_reference_and_uses_edit_model(self):
        payloads = []
        responses = iter([
            json_response({"data": {"download_url": "https://cdn.example/source.png"}}),
            json_response({"data": {"id": "prediction-2", "status": "created"}}),
        ])

        def fake_urlopen(request, timeout=None):
            if request.full_url.endswith("/model/generateImage"):
                payloads.append(json.loads(request.data.decode()))
            return next(responses)

        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "product.png"
            image.write_bytes(b"source-image")
            with mock.patch.object(urllib.request, "urlopen", fake_urlopen):
                prediction = atlas.submit_once(
                    "test-key", "Use a red background", image_path=image
                )

        self.assertEqual(prediction["id"], "prediction-2")
        self.assertEqual(payloads[0]["model"], "openai/gpt-image-2/edit")
        self.assertEqual(payloads[0]["images"], ["https://cdn.example/source.png"])

    def test_generation_post_failure_is_not_retried(self):
        calls = 0

        def fake_urlopen(request, timeout=None):
            nonlocal calls
            calls += 1
            raise urllib.error.HTTPError(
                request.full_url,
                503,
                "unavailable",
                {},
                io.BytesIO(b'{"message":"busy"}'),
            )

        with mock.patch.object(urllib.request, "urlopen", fake_urlopen):
            with self.assertRaisesRegex(atlas.AtlasError, "HTTP 503"):
                atlas.submit_once("test-key", "A poster")

        self.assertEqual(calls, 1)


if __name__ == "__main__":
    unittest.main()
