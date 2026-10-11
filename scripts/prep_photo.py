#!/usr/bin/env python3
"""
prep_photo.py — Isolates subject and prepares high-contrast grayscale image for ASCII rendering.
"""

import sys
from PIL import Image, ImageOps

def prep(input_path="source-photo.jpg", output_path="source-prepped.png"):
    img = Image.open(input_path).convert("RGB")
    # Grayscale conversion
    gray = ImageOps.grayscale(img)
    # Autocontrast to maximize dynamic range
    contrasted = ImageOps.autocontrast(gray, cutoff=2)
    contrasted.save(output_path)
    print(f"Saved {output_path}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep(src)
