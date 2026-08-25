#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai", "pillow"]
# ///
"""
Generate images from text prompts using Nano Banana (Google Gemini Image models).

Usage:
    python generate_image.py "A sunset over mountains" -o sunset.png
    python generate_image.py "A logo for a coffee shop" --model pro --aspect 1:1 --size 2K
    python generate_image.py "A cat in space" --aspect 16:9 --show
"""

import argparse
import os
import sys
from pathlib import Path


def get_client():
    """Initialize and return the Gemini client."""
    try:
        from google import genai
    except ImportError:
        print("Error: google-genai package not installed.")
        print("Install with: pip install google-genai pillow")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Set it with: export GEMINI_API_KEY='your-api-key'")
        sys.exit(1)

    return genai.Client(api_key=api_key)


def generate_image(
    prompt: str,
    output_path: str = "generated_image.png",
    model: str = "pro",
    aspect_ratio: str = "1:1",
    image_size: str = None,
    show: bool = False,
) -> str:
    """
    Generate an image from a text prompt.

    Args:
        prompt: Text description of the image to generate
        output_path: Path to save the generated image
        model: Model to use ('flash' or 'pro')
        aspect_ratio: Aspect ratio (e.g., '1:1', '16:9', '9:16')
        image_size: Resolution ('1K', '2K', '4K')
        show: Whether to display the image after generation

    Returns:
        Path to the saved image
    """
    from google.genai import types

    client = get_client()

    # Select model
    model_id = (
        "gemini-3-pro-image-preview"
        if model == "pro"
        else "gemini-2.5-flash-image"
    )

    # Build image config
    image_config_kwargs = {"aspect_ratio": aspect_ratio}
    if image_size:
        image_config_kwargs["image_size"] = image_size

    print(f"Generating image with {model_id}...")
    print(f"Prompt: {prompt}")
    print(f"Aspect ratio: {aspect_ratio}")
    if image_size:
        print(f"Resolution: {image_size}")

    response = client.models.generate_content(
        model=model_id,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(**image_config_kwargs),
        ),
    )

    # Extract and save the image
    for part in response.parts:
        if part.inline_data:
            image = part.as_image()
            image.save(output_path)
            print(f"Image saved to: {output_path}")

            if show:
                image.show()

            return output_path

    # Check for safety blocks
    if response.candidates and response.candidates[0].finish_reason:
        reason = response.candidates[0].finish_reason
        if reason in ["IMAGE_SAFETY", "IMAGE_PROHIBITED_CONTENT"]:
            print(f"Error: Content blocked by safety filters ({reason})")
            sys.exit(1)

    print("Error: No image was generated")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Nano Banana (Google Gemini Image models)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "A sunset over mountains"
  %(prog)s "A coffee shop logo" --model pro --aspect 1:1 --size 2K
  %(prog)s "A cat astronaut" -o cat_space.png --aspect 16:9 --show

Aspect Ratios:
  1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9

Resolutions:
  1K (1024px), 2K (2048px), 4K (4096px, Pro model only)
        """,
    )

    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument(
        "-o", "--output",
        default="generated_image.png",
        help="Output file path (default: generated_image.png)",
    )
    parser.add_argument(
        "-m", "--model",
        choices=["pro", "flash"],
        default="pro",
        help="Model to use: 'pro' (high quality, default) or 'flash' (fast)",
    )
    parser.add_argument(
        "-a", "--aspect",
        default="1:1",
        choices=["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"],
        help="Aspect ratio (default: 1:1)",
    )
    parser.add_argument(
        "-s", "--size",
        choices=["1K", "2K", "4K"],
        help="Image resolution (default: model default; 4K requires Pro model)",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the image after generation",
    )

    args = parser.parse_args()

    # Validate 4K is only used with Pro model
    if args.size == "4K" and args.model != "pro":
        print("Error: 4K resolution requires the 'pro' model")
        print("Use: --model pro --size 4K")
        sys.exit(1)

    generate_image(
        prompt=args.prompt,
        output_path=args.output,
        model=args.model,
        aspect_ratio=args.aspect,
        image_size=args.size,
        show=args.show,
    )


if __name__ == "__main__":
    main()
