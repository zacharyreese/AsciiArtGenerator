"""
ASCII Art Generator - Web UI
Flask backend for the ASCII art web interface.
"""

import io
import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from PIL import Image

from ascii_art import CHAR_SETS, generate_ascii_art_from_image

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max upload


@app.route("/")
def index():
    """Render the main web UI."""
    return render_template("index.html", char_sets=list(CHAR_SETS.keys()))


@app.route("/convert", methods=["POST"])
def convert():
    """Handle image upload and return ASCII art."""
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image provided"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    # Parse options
    try:
        width = int(request.form.get("width", 100))
        width = max(10, min(width, 500))  # Clamp between 10 and 500
    except ValueError:
        width = 100

    char_set = request.form.get("charset", "standard")
    if char_set not in CHAR_SETS:
        char_set = "standard"

    try:
        contrast = float(request.form.get("contrast", 1.0))
    except ValueError:
        contrast = 1.0

    try:
        brightness = float(request.form.get("brightness", 1.0))
    except ValueError:
        brightness = 1.0

    invert = request.form.get("invert", "false").lower() == "true"
    auto_scale = request.form.get("auto_scale", "true").lower() == "true"

    try:
        # Read image from upload
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Convert to RGB if necessary (handles PNG with alpha, GIF, etc.)
        if image.mode in ("RGBA", "P", "LA", "L"):
            if image.mode == "P":
                image = image.convert("RGBA")
            if image.mode in ("RGBA", "LA"):
                # Create white background for transparency
                bg = Image.new("RGB", image.size, (255, 255, 255))
                if image.mode == "RGBA":
                    bg.paste(image, mask=image.split()[3])
                else:
                    bg.paste(image, mask=image.split()[1])
                image = bg
            else:
                image = image.convert("RGB")

        ascii_art = generate_ascii_art_from_image(
            image,
            width=width,
            char_set=char_set,
            contrast=contrast,
            brightness=brightness,
            auto_scale=auto_scale,
            invert=invert,
        )

        lines = ascii_art.split("\n")
        return jsonify({
            "success": True,
            "ascii_art": ascii_art,
            "width": len(lines[0]) if lines else 0,
            "height": len(lines),
            "char_set": char_set,
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
