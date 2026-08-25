#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai", "pillow"]
# ///
"""
Interactive multi-turn image editing session using Nano Banana.

This script maintains conversation context, allowing iterative refinement
of images through natural language instructions.

Usage:
    python multi_turn_edit.py
    python multi_turn_edit.py --model pro
    python multi_turn_edit.py --start image.png

Commands during session:
    save [filename]  - Save current image
    show             - Display current image
    reset            - Start fresh conversation
    load <file>      - Load an image for editing
    quit/exit        - End session
    (any other text) - Send as editing instruction
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


class MultiTurnSession:
    """Manages a multi-turn image editing session."""

    def __init__(self, model: str = "pro"):
        from google.genai import types

        self.client = get_client()
        self.model_id = (
            "gemini-3-pro-image-preview"
            if model == "pro"
            else "gemini-2.5-flash-image"
        )
        self.types = types
        self.current_image = None
        self.turn_count = 0
        self._init_chat()

    def _init_chat(self):
        """Initialize or reset the chat session."""
        self.chat = self.client.chats.create(
            model=self.model_id,
            config=self.types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            ),
        )
        self.turn_count = 0

    def send_message(self, message: str, image=None) -> tuple:
        """
        Send a message to the model.

        Args:
            message: Text instruction
            image: Optional PIL Image to include

        Returns:
            Tuple of (text_response, image_response)
        """
        from PIL import Image

        contents = []
        if image is not None:
            contents.append(image)
        contents.append(message)

        response = self.chat.send_message(contents)
        self.turn_count += 1

        text_response = None
        image_response = None

        for part in response.parts:
            if part.text:
                text_response = part.text
            if part.inline_data:
                image_response = part.as_image()
                self.current_image = image_response

        return text_response, image_response

    def save_image(self, filename: str = None):
        """Save the current image."""
        if self.current_image is None:
            print("No image to save")
            return None

        if filename is None:
            filename = f"edited_turn_{self.turn_count}.png"

        self.current_image.save(filename)
        print(f"Image saved to: {filename}")
        return filename

    def show_image(self):
        """Display the current image."""
        if self.current_image is None:
            print("No image to display")
            return
        self.current_image.show()

    def reset(self):
        """Reset the session."""
        self._init_chat()
        self.current_image = None
        print("Session reset - starting fresh")


def run_interactive_session(model: str = "flash", start_image: str = None):
    """Run an interactive multi-turn editing session."""
    from PIL import Image

    print("=" * 60)
    print("Nano Banana Multi-Turn Image Editor")
    print("=" * 60)
    print(f"Model: {'Nano Banana Pro' if model == 'pro' else 'Nano Banana'}")
    print()
    print("Commands:")
    print("  save [filename]  - Save current image")
    print("  show             - Display current image")
    print("  reset            - Start fresh conversation")
    print("  load <file>      - Load an image for editing")
    print("  quit/exit        - End session")
    print("  (any text)       - Send as editing instruction")
    print("=" * 60)

    session = MultiTurnSession(model=model)

    # Load starting image if provided
    loaded_image = None
    if start_image:
        if os.path.exists(start_image):
            loaded_image = Image.open(start_image)
            print(f"Loaded starting image: {start_image}")
        else:
            print(f"Warning: Starting image not found: {start_image}")

    while True:
        try:
            user_input = input(f"\n[Turn {session.turn_count + 1}] > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # Handle commands
        lower_input = user_input.lower()

        if lower_input in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        elif lower_input == "show":
            session.show_image()
            continue

        elif lower_input == "reset":
            session.reset()
            loaded_image = None
            continue

        elif lower_input.startswith("save"):
            parts = user_input.split(maxsplit=1)
            filename = parts[1] if len(parts) > 1 else None
            session.save_image(filename)
            continue

        elif lower_input.startswith("load "):
            filepath = user_input[5:].strip()
            if os.path.exists(filepath):
                loaded_image = Image.open(filepath)
                print(f"Loaded image: {filepath}")
            else:
                print(f"File not found: {filepath}")
            continue

        # Send message to model
        print("Generating...")
        try:
            text_resp, image_resp = session.send_message(
                user_input,
                image=loaded_image
            )
            loaded_image = None  # Clear after first use

            if text_resp:
                print(f"\nModel: {text_resp}")

            if image_resp:
                print("Image generated/edited")
                print("(Use 'show' to display, 'save' to save)")

            if not text_resp and not image_resp:
                print("No response received - content may have been blocked")

        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Interactive multi-turn image editing with Nano Banana",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Start interactive session
  %(prog)s --model pro          # Use Nano Banana Pro
  %(prog)s --start photo.jpg    # Start with an existing image

Session example:
  > Create a cozy coffee shop interior
  > Add a cat sleeping on a chair
  > Make it look like a watercolor painting
  > save coffee_shop_final.png
  > quit
        """,
    )

    parser.add_argument(
        "-m", "--model",
        choices=["pro", "flash"],
        default="pro",
        help="Model to use: 'pro' (high quality, default) or 'flash' (fast)",
    )
    parser.add_argument(
        "-s", "--start",
        help="Start with an existing image file",
    )

    args = parser.parse_args()

    run_interactive_session(
        model=args.model,
        start_image=args.start,
    )


if __name__ == "__main__":
    main()
