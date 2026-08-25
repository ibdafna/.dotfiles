#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10,<3.11"
# dependencies = ["rembg", "pillow", "onnxruntime"]
# ///
"""
Remove background from images using rembg.

Usage:
    uv run remove_bg.py input.png -o output.png
    uv run remove_bg.py photo.jpg --model isnet-general-use
    uv run remove_bg.py image.png --mask-only -o mask.png
    uv run remove_bg.py input.png --bgcolor 255,255,255 -o white_bg.png
"""

import argparse
import sys
from pathlib import Path


def remove_background(
    input_path: str,
    output_path: str = None,
    model: str = "birefnet-general",
    mask_only: bool = False,
    bgcolor: tuple = None,
    alpha_matting: bool = False,
) -> str:
    """
    Remove background from an image.

    Args:
        input_path: Path to input image
        output_path: Path for output image (default: input_nobg.png)
        model: Model to use for segmentation
        mask_only: Return only the mask instead of the processed image
        bgcolor: Background color as (R, G, B) tuple, None for transparent
        alpha_matting: Enable alpha matting for better edges

    Returns:
        Path to the output image
    """
    from PIL import Image
    from rembg import remove, new_session

    # Determine output path
    if output_path is None:
        input_file = Path(input_path)
        suffix = "_mask.png" if mask_only else "_nobg.png"
        output_path = str(input_file.parent / f"{input_file.stem}{suffix}")

    # Load input image
    if not Path(input_path).exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    input_image = Image.open(input_path)

    print(f"Processing: {input_path}")
    print(f"Model: {model}")
    if bgcolor:
        print(f"Background color: RGB{bgcolor}")

    # Create session for the model
    session = new_session(model)

    # Remove background
    output_image = remove(
        input_image,
        session=session,
        only_mask=mask_only,
        alpha_matting=alpha_matting,
        bgcolor=bgcolor,
    )

    # Save output
    output_image.save(output_path)
    print(f"Saved: {output_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Remove background from images using rembg",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s photo.png                           # Output: photo_nobg.png
  %(prog)s photo.jpg -o transparent.png        # Specify output
  %(prog)s photo.png --model u2net             # Use specific model
  %(prog)s photo.png --mask-only               # Output mask only
  %(prog)s photo.png --bgcolor 255,255,255     # White background
  %(prog)s photo.png --alpha-matting           # Better edge quality

Available models:
  birefnet-general   - BiRefNet general (default, best quality)
  birefnet-portrait  - BiRefNet optimized for portraits
  isnet-general-use  - ISNet general purpose
  isnet-anime        - ISNet for anime/illustrations
  u2net              - U2Net general purpose
  u2netp             - U2Net lightweight (faster)
  u2net_human_seg    - U2Net for human segmentation
  silueta            - Lightweight model (43MB)
  bria-rmbg          - BRIA AI model
        """,
    )

    parser.add_argument("input", help="Path to input image")
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: input_nobg.png)",
    )
    parser.add_argument(
        "-m", "--model",
        default="birefnet-general",
        choices=[
            "birefnet-general",
            "birefnet-portrait",
            "isnet-general-use",
            "isnet-anime",
            "u2net",
            "u2netp",
            "u2net_human_seg",
            "u2net_cloth_seg",
            "silueta",
            "bria-rmbg",
        ],
        help="Model to use (default: birefnet-general)",
    )
    parser.add_argument(
        "--mask-only",
        action="store_true",
        help="Output only the segmentation mask",
    )
    parser.add_argument(
        "--bgcolor",
        help="Background color as R,G,B (e.g., 255,255,255 for white)",
    )
    parser.add_argument(
        "--alpha-matting",
        action="store_true",
        help="Enable alpha matting for better edge quality (slower)",
    )

    args = parser.parse_args()

    # Parse background color
    bgcolor = None
    if args.bgcolor:
        try:
            parts = [int(x.strip()) for x in args.bgcolor.split(",")]
            if len(parts) != 3 or not all(0 <= x <= 255 for x in parts):
                raise ValueError()
            bgcolor = tuple(parts)
        except ValueError:
            print("Error: --bgcolor must be R,G,B format (e.g., 255,255,255)")
            sys.exit(1)

    remove_background(
        input_path=args.input,
        output_path=args.output,
        model=args.model,
        mask_only=args.mask_only,
        bgcolor=bgcolor,
        alpha_matting=args.alpha_matting,
    )


if __name__ == "__main__":
    main()
