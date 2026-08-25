# Nano Banana API Reference

Complete API documentation for Google's Nano Banana image generation models.

## Models

### Nano Banana (gemini-2.5-flash-image)

- **Model ID**: `gemini-2.5-flash-image`
- **Best for**: Fast generation, quick edits, high-volume tasks
- **Max resolution**: 1024px
- **Max input images**: 3
- **Speed**: Optimized for low latency

### Nano Banana Pro (gemini-3-pro-image-preview)

- **Model ID**: `gemini-3-pro-image-preview`
- **Best for**: Professional assets, text rendering, complex compositions
- **Max resolution**: 4096px
- **Max input images**: 14 (6 objects + 5 humans for consistency)
- **Features**: Advanced "Thinking" mode for complex prompts

## Client Setup

### Gemini Developer API

```python
from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
```

### Vertex AI

```python
from google import genai

client = genai.Client(
    vertexai=True,
    project="your-project-id",
    location="us-central1"
)
```

## Core API Methods

### generate_content

Primary method for image generation and editing.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=contents,
    config=config,
)
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | str | Model ID |
| `contents` | str \| list | Prompt text and/or images |
| `config` | GenerateContentConfig | Configuration options |

### Chat Sessions

For multi-turn conversations:

```python
from google.genai import types

chat = client.chats.create(
    model="gemini-2.5-flash-image",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    ),
)

response = chat.send_message("Your prompt here")
```

## Configuration Types

### GenerateContentConfig

```python
from google.genai import types

config = types.GenerateContentConfig(
    response_modalities=["IMAGE"],  # or ["TEXT", "IMAGE"], ["TEXT"]
    image_config=types.ImageConfig(
        aspect_ratio="16:9",
        image_size="2K",
    ),
)
```

**Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `response_modalities` | list[str] | Output types: "TEXT", "IMAGE" |
| `image_config` | ImageConfig | Image-specific settings |

### ImageConfig

```python
from google.genai import types

image_config = types.ImageConfig(
    aspect_ratio="16:9",
    image_size="2K",
)
```

**Fields:**

| Field | Type | Values |
|-------|------|--------|
| `aspect_ratio` | str | "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9" |
| `image_size` | str | "1K", "2K", "4K" (4K requires Pro model) |

## Response Handling

### Extracting Images

```python
response = client.models.generate_content(...)

for part in response.parts:
    if part.inline_data:
        # Get PIL Image object
        image = part.as_image()

        # Save to file
        image.save("output.png")

        # Display
        image.show()

    if part.text:
        print(part.text)
```

### Alternative Response Access

```python
for part in response.candidates[0].content.parts:
    if part.inline_data:
        from PIL import Image
        from io import BytesIO

        image = Image.open(BytesIO(part.inline_data.data))
        image.save("output.png")
```

## Input Formats

### Text-Only Prompt

```python
contents = "A sunset over mountains"
```

### Image + Text

```python
from PIL import Image

img = Image.open("photo.jpg")
contents = [img, "Edit this image to look like a painting"]
```

### Multiple Images + Text

```python
img1 = Image.open("style.jpg")
img2 = Image.open("subject.jpg")
contents = [img1, img2, "Apply the style from the first image to the second"]
```

### File Upload (Alternative)

```python
file = client.files.upload(file="image.png")
contents = [file, "Describe this image"]
```

## Error Handling

### Safety Filters

```python
response = client.models.generate_content(...)

if response.candidates:
    candidate = response.candidates[0]

    if candidate.finish_reason:
        reason = candidate.finish_reason

        if reason == "IMAGE_SAFETY":
            print("Blocked: Safety violation")
        elif reason == "IMAGE_PROHIBITED_CONTENT":
            print("Blocked: Prohibited content")
        elif reason == "STOP":
            print("Success")

# Check prompt feedback
if response.prompt_feedback:
    if response.prompt_feedback.block_reason:
        print(f"Prompt blocked: {response.prompt_feedback.block_reason}")
```

### Common Error Codes

| Error | Description |
|-------|-------------|
| `IMAGE_SAFETY` | Content violates safety policies |
| `IMAGE_PROHIBITED_CONTENT` | Prohibited subject matter |
| `RECITATION` | Output too similar to training data |
| `MAX_TOKENS` | Response truncated |

### Exception Handling

```python
from google.api_core import exceptions

try:
    response = client.models.generate_content(...)
except exceptions.InvalidArgument as e:
    print(f"Invalid request: {e}")
except exceptions.ResourceExhausted as e:
    print(f"Rate limit exceeded: {e}")
except exceptions.PermissionDenied as e:
    print(f"Permission denied: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## Rate Limits and Quotas

### Standard Limits (Gemini Developer API)

- Requests per minute: Varies by tier
- Tokens per minute: Varies by tier
- Images per request: 3 (Flash) / 14 (Pro)
- Total file size: 50MB per request

### Batch API

For higher throughput with up to 24-hour turnaround:

```python
# Batch processing available for enterprise use
# Contact Google Cloud for batch API access
```

## Advanced Features

### Google Search Grounding (Pro)

Nano Banana Pro can access real-time data for current events:

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Create a visualization of today's weather in New York City",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)
```

### Character/Object Consistency (Pro)

Maintain appearance across multiple generations:

```python
reference_images = [
    Image.open("character_ref1.jpg"),
    Image.open("character_ref2.jpg"),
]

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        *reference_images,
        "Create a new scene with this character walking in a park"
    ],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)
```

### Thinking Mode (Pro)

For complex prompts, Pro model uses reasoning:

```python
# The model automatically engages thinking mode for complex requests
# No special configuration needed - just use detailed prompts
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="""
    Create an infographic showing the water cycle with these requirements:
    1. Show evaporation, condensation, precipitation, and collection
    2. Use a blue and green color scheme
    3. Include clear labels for each stage
    4. Add small icons representing sun, clouds, and rain
    5. Make it educational and suitable for middle school students
    """,
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(
            aspect_ratio="3:4",
            image_size="2K",
        ),
    ),
)
```

## SynthID Watermarking

All images generated by Nano Banana include invisible SynthID watermarks for AI detection. This cannot be disabled.

## Supported File Formats

### Input

- PNG
- JPEG/JPG
- GIF (first frame only)
- WebP

### Output

- PNG (default)

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | API key for Gemini Developer API |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to service account JSON (Vertex AI) |
| `GOOGLE_CLOUD_PROJECT` | GCP project ID (Vertex AI) |

## SDK Installation

```bash
# Latest SDK (recommended)
pip install google-genai pillow

# With image display support
pip install google-genai pillow

# For Vertex AI
pip install google-genai google-cloud-aiplatform
```

## Quick Reference

### Generate Image

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_API_KEY")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="Your prompt",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="1:1"),
    ),
)

for part in response.parts:
    if part.inline_data:
        part.as_image().save("output.png")
```

### Edit Image

```python
from PIL import Image

img = Image.open("input.jpg")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[img, "Your edit instruction"],
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
    ),
)

for part in response.parts:
    if part.inline_data:
        part.as_image().save("edited.png")
```

### Multi-Turn Editing

```python
chat = client.chats.create(
    model="gemini-2.5-flash-image",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"]
    ),
)

response = chat.send_message("Create a coffee shop scene")
# ... save image ...

response = chat.send_message("Add a cat on one of the chairs")
# ... save modified image ...
```
