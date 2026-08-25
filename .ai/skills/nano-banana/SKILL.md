---
name: nano-banana
description: This skill provides comprehensive image generation and editing using Google's Nano Banana AI models (Gemini 2.5 Flash Image and Gemini 3 Pro Image). Use when the user wants to generate images from text, edit existing images, apply style transfers, create product mockups, generate text-heavy graphics like posters or logos, or perform multi-turn conversational image editing. Triggers on requests involving AI image generation, photo editing, image modification, style changes, background removal, image composition, or any image manipulation task.
---

# Nano Banana Image Generation & Editing

## Overview

Nano Banana is Google's native image generation model series built into Gemini. This skill enables full-featured image generation and editing capabilities equivalent to the Nano Banana web UI, including text-to-image generation, conversational image editing, style transfer, and professional asset creation.

## Models

Two models are available:

| Model | ID | Best For | Max Resolution |
|-------|-----|----------|----------------|
| **Nano Banana** | `gemini-2.5-flash-image` | Fast generation, quick edits, high volume | 1024px |
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | Professional assets, text rendering, complex prompts | 4096px |

**Model Selection Guidelines:**
- Default to `gemini-3-pro-image-preview` (Nano Banana Pro) for best quality
- Use `gemini-2.5-flash-image` for: high-volume batch processing, quick drafts, lower cost requirements

## Setup

### Prerequisites

Scripts use PEP 723 inline metadata - dependencies install automatically when run with `uv run`. No manual installation needed.

### Authentication

Set the API key as an environment variable:

```bash
export GEMINI_API_KEY="your-api-key"
```

Or pass it directly when creating the client.

## Core Capabilities

### 1. Text-to-Image Generation

Generate images from text descriptions. Descriptive paragraphs produce better results than keyword lists.

```python
from google import genai
from google.genai import types
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="A serene Japanese garden at sunset with a wooden bridge over a koi pond, cherry blossoms falling gently",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",
        ),
    ),
)

for part in response.parts:
    if part.inline_data:
        image = part.as_image()
        image.save("generated_image.png")
        image.show()
```

### 2. Image Editing

Edit existing images by providing the image along with editing instructions.

```python
from PIL import Image

# Load the image to edit
input_image = Image.open("photo.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        input_image,
        "Remove the background and replace it with a tropical beach at sunset"
    ],
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    ),
)

for part in response.parts:
    if part.inline_data:
        edited = part.as_image()
        edited.save("edited_image.png")
```

### 3. Multi-Turn Conversational Editing

Iteratively refine images through conversation. The model maintains context across turns.

```python
from google.genai import types

# Initial generation
chat = client.chats.create(
    model="gemini-2.5-flash-image",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    ),
)

# First turn: generate initial image
response = chat.send_message("Create a cozy coffee shop interior with warm lighting")
# Save the generated image...

# Second turn: modify
response = chat.send_message("Add a cat sleeping on one of the chairs")
# Save the modified image...

# Third turn: adjust style
response = chat.send_message("Make it look like a watercolor painting")
# Save the final image...
```

### 4. Style Transfer

Apply the style from a reference image to a subject.

```python
style_reference = Image.open("van_gogh_starry_night.jpg")
subject_image = Image.open("my_photo.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        style_reference,
        subject_image,
        "Apply the artistic style from the first image to the second image"
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
    ),
)
```

### 5. Image Combination

Combine multiple images into a cohesive composition.

```python
image1 = Image.open("person.jpg")
image2 = Image.open("background.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        image1,
        image2,
        "Place the person from the first image into the scene from the second image, matching the lighting and perspective"
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"]
    ),
)
```

### 6. Text-Heavy Graphics (Nano Banana Pro)

For logos, posters, and graphics requiring legible text, use Nano Banana Pro.

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Create a modern coffee shop logo with the text 'BREW & BLOOM' in an elegant serif font, featuring a minimalist coffee cup with a flower growing from it",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="2K",
        ),
    ),
)
```

### 7. Product Mockups

Generate realistic product mockups and packaging designs.

```python
product_image = Image.open("product.png")

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        product_image,
        "Create a professional product photography shot of this item on a marble surface with soft studio lighting and subtle shadows"
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            image_size="4K",
        ),
    ),
)
```

## Configuration Options

### Aspect Ratios

Supported aspect ratios: `"1:1"`, `"2:3"`, `"3:2"`, `"3:4"`, `"4:3"`, `"4:5"`, `"5:4"`, `"9:16"`, `"16:9"`, `"21:9"`

### Resolution (image_size)

- `"1K"` - 1024px (default for Nano Banana)
- `"2K"` - 2048px
- `"4K"` - 4096px (Nano Banana Pro only)

### Response Modalities

- `["IMAGE"]` - Image output only
- `["TEXT", "IMAGE"]` - Combined text explanation and image (useful for editing to get descriptions of changes)
- `["TEXT"]` - Text-only response (for image analysis/understanding)

## Common Editing Tasks

### Background Removal/Replacement
```python
contents=[image, "Remove the background and make it transparent"]
contents=[image, "Replace the background with a solid white color"]
contents=[image, "Change the background to a professional office setting"]
```

### Color and Lighting Adjustments
```python
contents=[image, "Adjust the lighting to golden hour warmth"]
contents=[image, "Convert to black and white with high contrast"]
contents=[image, "Make the colors more vibrant and saturated"]
contents=[image, "Change from daytime to nighttime scene"]
```

### Object Manipulation
```python
contents=[image, "Remove the person on the left side"]
contents=[image, "Add a red balloon to the child's hand"]
contents=[image, "Replace the car with a bicycle"]
contents=[image, "Extend the image to the left to show more of the room"]
```

### Style Transformations
```python
contents=[image, "Transform into a Studio Ghibli anime style"]
contents=[image, "Make it look like a 1980s photograph"]
contents=[image, "Convert to a pencil sketch"]
contents=[image, "Apply a cyberpunk neon aesthetic"]
```

### Focus and Composition
```python
contents=[image, "Add depth of field blur to the background"]
contents=[image, "Crop and reframe to focus on the subject's face"]
contents=[image, "Change the camera angle to be looking up at the subject"]
```

## Prompting Best Practices

1. **Be descriptive**: Use full sentences describing the scene rather than comma-separated keywords
2. **Specify style early**: Mention artistic style at the beginning of the prompt
3. **Include lighting**: Describe lighting conditions for more realistic results
4. **Reference context**: When editing, clearly identify what to change and what to preserve
5. **Iterate conversationally**: Use multi-turn editing for complex modifications

### Effective Prompt Examples

**Good**: "A professional photograph of a golden retriever sitting in a sunlit meadow, shallow depth of field, warm afternoon lighting, looking at the camera with a happy expression"

**Less effective**: "dog, meadow, sunny, professional photo, golden retriever, happy"

## Input Limits

| Model | Max Input Images | Max File Size |
|-------|------------------|---------------|
| Nano Banana | 3 images | 50MB total |
| Nano Banana Pro | 14 images | 50MB total |

## Safety and Watermarking

- All generated images include invisible SynthID watermarks for AI detection
- Content safety filters block harmful content automatically
- If generation fails due to safety filters, the API returns specific error codes

## Error Handling

```python
try:
    response = client.models.generate_content(...)

    # Check for blocked content
    if response.candidates and response.candidates[0].finish_reason:
        reason = response.candidates[0].finish_reason
        if reason in ["IMAGE_SAFETY", "IMAGE_PROHIBITED_CONTENT"]:
            print("Content blocked by safety filters")

except Exception as e:
    print(f"Generation failed: {e}")
```

## Scripts

This skill includes helper scripts in `scripts/`. All scripts use PEP 723 inline metadata - run them with `uv run` and dependencies install automatically.

### Generate Image
```bash
uv run scripts/generate_image.py "A sunset over mountains" -o output.png
uv run scripts/generate_image.py "A logo for a cafe" --aspect 1:1 --size 2K
```

### Edit Image
```bash
uv run scripts/edit_image.py photo.jpg "Remove the background" -o edited.png
uv run scripts/edit_image.py image.png "Make it look like a watercolor painting"
```

### Batch Generate
```bash
uv run scripts/batch_generate.py prompts.txt -o output_dir/
```

### Multi-Turn Interactive Session
```bash
uv run scripts/multi_turn_edit.py
```

Run any script with `--help` to see all available options.

## References

See `references/api_reference.md` for complete API documentation including all configuration parameters, error codes, and advanced features.
