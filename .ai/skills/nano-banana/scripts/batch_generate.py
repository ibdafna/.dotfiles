#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai", "pillow"]
# ///
"""
Batch generate images from a list of prompts using Nano Banana.

Usage:
    python batch_generate.py prompts.txt -o output_dir/
    python batch_generate.py prompts.txt --model pro --aspect 16:9

prompts.txt format (one prompt per line):
    A sunset over mountains
    A cat playing piano
    A futuristic city at night
"""

import argparse
import os
import sys
import time
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


def sanitize_filename(prompt: str, max_length: int = 50) -> str:
    """Convert a prompt to a safe filename."""
    # Take first part of prompt
    filename = prompt[:max_length].strip()
    # Replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    # Replace spaces and multiple underscores
    filename = '_'.join(filename.split())
    return filename


def batch_generate(
    prompts_file: str,
    output_dir: str = "generated_images",
    model: str = "pro",
    aspect_ratio: str = "1:1",
    image_size: str = None,
    delay: float = 1.0,
) -> list:
    """
    Generate images from a file containing prompts.

    Args:
        prompts_file: Path to file with one prompt per line
        output_dir: Directory to save generated images
        model: Model to use ('flash' or 'pro')
        aspect_ratio: Aspect ratio for all images
        image_size: Resolution ('1K', '2K', '4K')
        delay: Delay between requests in seconds

    Returns:
        List of (prompt, output_path, success) tuples
    """
    from google.genai import types

    client = get_client()

    # Read prompts
    if not os.path.exists(prompts_file):
        print(f"Error: Prompts file not found: {prompts_file}")
        sys.exit(1)

    with open(prompts_file, 'r') as f:
        prompts = [line.strip() for line in f if line.strip()]

    if not prompts:
        print("Error: No prompts found in file")
        sys.exit(1)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

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

    print(f"Generating {len(prompts)} images with {model_id}")
    print(f"Output directory: {output_dir}")
    print(f"Aspect ratio: {aspect_ratio}")
    if image_size:
        print(f"Resolution: {image_size}")
    print("-" * 50)

    results = []

    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] Generating: {prompt[:60]}...")

        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    image_config=types.ImageConfig(**image_config_kwargs),
                ),
            )

            # Extract and save the image
            saved = False
            for part in response.parts:
                if part.inline_data:
                    filename = f"{i:03d}_{sanitize_filename(prompt)}.png"
                    filepath = output_path / filename
                    image = part.as_image()
                    image.save(str(filepath))
                    print(f"  Saved: {filename}")
                    results.append((prompt, str(filepath), True))
                    saved = True
                    break

            if not saved:
                # Check for safety blocks
                reason = None
                if response.candidates and response.candidates[0].finish_reason:
                    reason = response.candidates[0].finish_reason
                print(f"  Failed: No image generated (reason: {reason})")
                results.append((prompt, None, False))

        except Exception as e:
            print(f"  Error: {e}")
            results.append((prompt, None, False))

        # Rate limiting delay
        if i < len(prompts) and delay > 0:
            time.sleep(delay)

    # Summary
    successful = sum(1 for _, _, success in results if success)
    print("\n" + "=" * 50)
    print(f"Batch complete: {successful}/{len(prompts)} images generated")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate images using Nano Banana",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s prompts.txt
  %(prog)s prompts.txt -o my_images/ --model pro
  %(prog)s ideas.txt --aspect 16:9 --delay 2

Prompts file format (one prompt per line):
  A sunset over mountains
  A cat playing piano
  A futuristic city at night
        """,
    )

    parser.add_argument("prompts_file", help="Path to file with one prompt per line")
    parser.add_argument(
        "-o", "--output",
        default="generated_images",
        help="Output directory (default: generated_images)",
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
        "-d", "--delay",
        type=float,
        default=1.0,
        help="Delay between requests in seconds (default: 1.0)",
    )

    args = parser.parse_args()

    # Validate 4K is only used with Pro model
    if args.size == "4K" and args.model != "pro":
        print("Error: 4K resolution requires the 'pro' model")
        print("Use: --model pro --size 4K")
        sys.exit(1)

    batch_generate(
        prompts_file=args.prompts_file,
        output_dir=args.output,
        model=args.model,
        aspect_ratio=args.aspect,
        image_size=args.size,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
