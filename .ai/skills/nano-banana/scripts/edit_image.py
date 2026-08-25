#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai", "pillow"]
# ///
"""
Edit images using Nano Banana (Google Gemini Image models).

Usage:
    python edit_image.py input.jpg "Remove the background" -o output.png
    python edit_image.py photo.png "Make it look like a watercolor painting" --model pro
    python edit_image.py image.jpg "Add a sunset in the background" --show
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


def edit_image(
    input_path: str,
    instruction: str,
    output_path: str = None,
    model: str = "pro",
    show: bool = False,
    include_text: bool = False,
) -> str:
    """
    Edit an image based on text instructions.

    Args:
        input_path: Path to the input image
        instruction: Text description of edits to make
        output_path: Path to save the edited image
        model: Model to use ('flash' or 'pro')
        show: Whether to display the image after editing
        include_text: Whether to include text description of changes

    Returns:
        Path to the saved image
    """
    from google.genai import types
    from PIL import Image

    client = get_client()

    # Determine output path
    if output_path is None:
        input_file = Path(input_path)
        output_path = str(input_file.parent / f"{input_file.stem}_edited.png")

    # Load input image
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    input_image = Image.open(input_path)

    # Select model
    model_id = (
        "gemini-3-pro-image-preview"
        if model == "pro"
        else "gemini-2.5-flash-image"
    )

    # Set response modalities
    modalities = ["TEXT", "IMAGE"] if include_text else ["IMAGE"]

    print(f"Editing image with {model_id}...")
    print(f"Input: {input_path}")
    print(f"Instruction: {instruction}")

    response = client.models.generate_content(
        model=model_id,
        contents=[input_image, instruction],
        config=types.GenerateContentConfig(
            response_modalities=modalities,
        ),
    )

    # Extract and save the image
    image_saved = False
    for part in response.parts:
        if part.text and include_text:
            print(f"\nModel response: {part.text}")
        if part.inline_data:
            image = part.as_image()
            image.save(output_path)
            print(f"Edited image saved to: {output_path}")
            image_saved = True

            if show:
                image.show()

    if image_saved:
        return output_path

    # Check for safety blocks
    if response.candidates and response.candidates[0].finish_reason:
        reason = response.candidates[0].finish_reason
        if reason in ["IMAGE_SAFETY", "IMAGE_PROHIBITED_CONTENT"]:
            print(f"Error: Content blocked by safety filters ({reason})")
            sys.exit(1)

    print("Error: No edited image was generated")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Edit images using Nano Banana (Google Gemini Image models)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s photo.jpg "Remove the background"
  %(prog)s portrait.png "Add a blurred background" -o portrait_blur.png
  %(prog)s scene.jpg "Change from day to night" --model pro --show
  %(prog)s image.png "Make it look vintage" --text

Common edit instructions:
  - "Remove the background"
  - "Replace the background with [description]"
  - "Add [object] to the image"
  - "Remove the [object]"
  - "Change the lighting to [description]"
  - "Apply [style] style"
  - "Convert to black and white"
  - "Make the colors more vibrant"
        """,
    )

    parser.add_argument("input", help="Path to the input image")
    parser.add_argument("instruction", help="Text description of edits to make")
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: input_edited.png)",
    )
    parser.add_argument(
        "-m", "--model",
        choices=["pro", "flash"],
        default="pro",
        help="Model to use: 'pro' (high quality, default) or 'flash' (fast)",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the image after editing",
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Include text description of changes made",
    )

    args = parser.parse_args()

    edit_image(
        input_path=args.input,
        instruction=args.instruction,
        output_path=args.output,
        model=args.model,
        show=args.show,
        include_text=args.text,
    )


if __name__ == "__main__":
    main()
