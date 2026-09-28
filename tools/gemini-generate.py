#!/usr/bin/env python3
"""Compatibility wrapper: the generator now ships inside the image-generation skill
(skills/image-generation/scripts/gemini-generate.py) so it is available when skills are
installed individually. All arguments are passed through unchanged."""

import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "skills", "image-generation", "scripts", "gemini-generate.py")

sys.argv[0] = TARGET
runpy.run_path(TARGET, run_name="__main__")
