"""
ASCII Art Generator
Converts images to ASCII art text.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageEnhance
except ImportError:
    print("Error: Pillow is required. Run: pip install Pillow")
    sys.exit(1)


# Character ramps from darkest to lightest
CHAR_SETS = {
    "simple": " .:-=+*#%@",
    "standard": " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
    "blocks": " ░▒▓█",
    "binary": " █",
    "retro": " .oO",
}


def get_image_path() -> str:
    """Get image path from user input if not provided via arguments."""
    return input("Enter the path to an image: ").strip()


def load_image(path: str) -> Image.Image:
    """Load an image from the given path."""
    image_path = Path(path)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    return Image.open(image_path)


def resize_image(image: Image.Image, width: int, auto_scale: bool = True) -> Image.Image:
    """
    Resize image to target width while maintaining aspect ratio.
    Accounts for the fact that characters are taller than they are wide.
    """
    orig_width, orig_height = image.size
    aspect_ratio = orig_height / orig_width

    # Characters are roughly 2x as tall as they are wide, so we compensate
    if auto_scale:
        new_height = int(width * aspect_ratio * 0.55)
    else:
        new_height = int(width * aspect_ratio)

    # Ensure minimum dimensions
    new_height = max(new_height, 1)
    width = max(width, 1)

    return image.resize((width, new_height), Image.Resampling.LANCZOS)


def image_to_grayscale(image: Image.Image) -> Image.Image:
    """Convert image to grayscale."""
    return image.convert("L")


def map_pixels_to_ascii(image: Image.Image, char_set: str) -> str:
    """Map grayscale pixel values to ASCII characters."""
    pixels = list(image.get_flattened_data())
    chars = list(char_set)
    char_range = len(chars) - 1

    # Map 0-255 to character index
    ascii_chars = [chars[min(int(pixel / 255 * char_range), char_range)] for pixel in pixels]
    return "".join(ascii_chars)


def format_ascii_art(ascii_str: str, width: int) -> str:
    """Format ASCII string into lines of given width."""
    lines = [ascii_str[i : i + width] for i in range(0, len(ascii_str), width)]
    return "\n".join(lines)


def enhance_image(image: Image.Image, contrast: float = 1.0, brightness: float = 1.0) -> Image.Image:
    """Apply contrast and brightness adjustments."""
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)
    return image


def generate_ascii_art(
    image_path: str,
    width: int = 100,
    char_set: str = "standard",
    contrast: float = 1.0,
    brightness: float = 1.0,
    auto_scale: bool = True,
    invert: bool = False,
) -> str:
    """
    Main function to generate ASCII art from an image.

    Args:
        image_path: Path to the input image
        width: Target width in characters
        char_set: Name of character set to use
        contrast: Contrast enhancement factor
        brightness: Brightness enhancement factor
        auto_scale: Whether to auto-scale for character aspect ratio
        invert: Whether to invert the colors

    Returns:
        ASCII art string
    """
    image = load_image(image_path)
    return generate_ascii_art_from_image(
        image,
        width=width,
        char_set=char_set,
        contrast=contrast,
        brightness=brightness,
        auto_scale=auto_scale,
        invert=invert,
    )


def generate_ascii_art_from_image(
    image: Image.Image,
    width: int = 100,
    char_set: str = "standard",
    contrast: float = 1.0,
    brightness: float = 1.0,
    auto_scale: bool = True,
    invert: bool = False,
) -> str:
    """
    Generate ASCII art from an in-memory PIL Image.

    Args:
        image: PIL Image object
        width: Target width in characters
        char_set: Name of character set to use
        contrast: Contrast enhancement factor
        brightness: Brightness enhancement factor
        auto_scale: Whether to auto-scale for character aspect ratio
        invert: Whether to invert the colors

    Returns:
        ASCII art string
    """
    image = resize_image(image, width, auto_scale)
    image = enhance_image(image, contrast, brightness)
    image = image_to_grayscale(image)

    chars = CHAR_SETS.get(char_set, CHAR_SETS["standard"])
    if invert:
        chars = chars[::-1]

    ascii_str = map_pixels_to_ascii(image, chars)
    result = format_ascii_art(ascii_str, image.width)

    # Strip leading/trailing blank lines to avoid empty space at top/bottom
    lines = result.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def save_ascii_art(ascii_art: str, output_path: str) -> None:
    """Save ASCII art to a text file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ascii_art)
    print(f"Saved to: {output_path}")


def print_preview(ascii_art: str, max_lines: int = 50) -> None:
    """Print ASCII art with optional truncation for preview."""
    lines = ascii_art.split("\n")
    if len(lines) > max_lines:
        print("\n".join(lines[:max_lines]))
        print(f"\n... ({len(lines) - max_lines} more lines)")
    else:
        print(ascii_art)


def interactive_mode() -> None:
    """Run in interactive mode, prompting the user for inputs."""
    print("=== ASCII Art Generator ===\n")

    image_path = get_image_path()

    try:
        width = int(input("Enter desired width in characters (default 100): ") or "100")
    except ValueError:
        width = 100

    print("\nAvailable character sets:")
    for name in CHAR_SETS:
        print(f"  - {name}")
    char_set = input("Choose character set (default: standard): ").strip() or "standard"

    try:
        contrast = float(input("Contrast adjustment (1.0 = none, default 1.5): ") or "1.5")
    except ValueError:
        contrast = 1.5

    invert_input = input("Invert colors? (y/N): ").strip().lower()
    invert = invert_input in ("y", "yes")

    print("\nGenerating ASCII art...")
    try:
        ascii_art = generate_ascii_art(
            image_path=image_path,
            width=width,
            char_set=char_set,
            contrast=contrast,
            invert=invert,
        )
        print("\n" + "=" * 40)
        print_preview(ascii_art)
        print("=" * 40 + "\n")

        save_input = input("Save to file? (y/N): ").strip().lower()
        if save_input in ("y", "yes"):
            default_name = Path(image_path).stem + "_ascii.txt"
            output_path = input(f"Enter output filename (default: {default_name}): ").strip() or default_name
            save_ascii_art(ascii_art, output_path)

    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert images to ASCII art",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ascii_art.py image.jpg
  python ascii_art.py image.png -w 80 -c simple --contrast 2.0
  python ascii_art.py image.jpg -o output.txt --invert
        """,
    )
    parser.add_argument("image", nargs="?", help="Path to input image")
    parser.add_argument("-w", "--width", type=int, default=100, help="Output width in characters (default: 100)")
    parser.add_argument("-c", "--charset", choices=list(CHAR_SETS.keys()), default="standard", help="Character set to use")
    parser.add_argument("--contrast", type=float, default=1.0, help="Contrast enhancement (default: 1.0)")
    parser.add_argument("--brightness", type=float, default=1.0, help="Brightness enhancement (default: 1.0)")
    parser.add_argument("--invert", action="store_true", help="Invert the colors")
    parser.add_argument("--no-scale", action="store_true", help="Disable auto-scaling for character aspect ratio")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--preview", type=int, metavar="N", help="Show first N lines as preview")

    args = parser.parse_args()

    if args.interactive or (not args.image and not sys.stdin.isatty()):
        interactive_mode()
        return

    if not args.image:
        parser.print_help()
        sys.exit(1)

    try:
        ascii_art = generate_ascii_art(
            image_path=args.image,
            width=args.width,
            char_set=args.charset,
            contrast=args.contrast,
            brightness=args.brightness,
            auto_scale=not args.no_scale,
            invert=args.invert,
        )

        if args.output:
            save_ascii_art(ascii_art, args.output)
        else:
            if args.preview:
                print_preview(ascii_art, args.preview)
            else:
                print(ascii_art)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
