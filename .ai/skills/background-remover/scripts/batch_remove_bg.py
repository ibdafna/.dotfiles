#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10,<3.11"
# dependencies = ["rembg", "pillow", "onnxruntime"]
# ///
"""
Batch remove backgrounds from multiple images.

Usage:
    uv run batch_remove_bg.py input_folder/ -o output_folder/
    uv run batch_remove_bg.py *.png -o processed/
    uv run batch_remove_bg.py photos/ --model birefnet-portrait
"""

import argparse
import sys
from pathlib import Path


def batch_remove_background(
    input_paths: list,
    output_dir: str = "output",
    model: str = "birefnet-general",
    alpha_matting: bool = False,
) -> list:
    """
    Remove backgrounds from multiple images.

    Args:
        input_paths: List of input image paths or a directory
        output_dir: Directory for output images
        model: Model to use for segmentation
        alpha_matting: Enable alpha matting for better edges

    Returns:
        List of (input_path, output_path, success) tuples
    """
    from PIL import Image
    from rembg import remove, new_session

    # Collect all image files
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif'}
    files_to_process = []

    for path_str in input_paths:
        path = Path(path_str)
        if path.is_dir():
            for ext in image_extensions:
                files_to_process.extend(path.glob(f"*{ext}"))
                files_to_process.extend(path.glob(f"*{ext.upper()}"))
        elif path.is_file() and path.suffix.lower() in image_extensions:
            files_to_process.append(path)

    if not files_to_process:
        print("Error: No image files found")
        sys.exit(1)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Processing {len(files_to_process)} images with model: {model}")
    print(f"Output directory: {output_dir}")
    print("-" * 50)

    # Create session once for efficiency
    session = new_session(model)

    results = []
    for i, input_file in enumerate(files_to_process, 1):
        output_file = output_path / f"{input_file.stem}_nobg.png"
        print(f"[{i}/{len(files_to_process)}] {input_file.name}...", end=" ")

        try:
            input_image = Image.open(input_file)
            output_image = remove(
                input_image,
                session=session,
                alpha_matting=alpha_matting,
            )
            output_image.save(output_file)
            print("done")
            results.append((str(input_file), str(output_file), True))
        except Exception as e:
            print(f"failed: {e}")
            results.append((str(input_file), None, False))

    # Summary
    successful = sum(1 for _, _, success in results if success)
    print("-" * 50)
    print(f"Completed: {successful}/{len(files_to_process)} images processed")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch remove backgrounds from images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s photos/                     # Process all images in folder
  %(prog)s *.jpg -o transparent/       # Process all JPGs
  %(prog)s img1.png img2.png -o out/   # Process specific files
  %(prog)s photos/ --model birefnet-portrait  # Use portrait model
        """,
    )

    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input images or directories",
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Output directory (default: output)",
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
            "silueta",
            "bria-rmbg",
        ],
        help="Model to use (default: birefnet-general)",
    )
    parser.add_argument(
        "--alpha-matting",
        action="store_true",
        help="Enable alpha matting for better edge quality (slower)",
    )

    args = parser.parse_args()

    batch_remove_background(
        input_paths=args.inputs,
        output_dir=args.output,
        model=args.model,
        alpha_matting=args.alpha_matting,
    )


if __name__ == "__main__":
    main()
