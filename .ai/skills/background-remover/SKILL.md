---
name: background-remover
description: This skill removes backgrounds from images, creating transparent PNGs or replacing backgrounds with solid colors. Use when the user wants to remove image backgrounds, create transparent images, extract subjects from photos, make cutouts, or process product images for e-commerce. Supports single images and batch processing. Runs locally with no API calls.
---

# Background Remover

## Overview

Remove backgrounds from images using AI-powered segmentation. Runs 100% locally using the rembg library - no API calls or subscriptions required. Outputs transparent PNGs or images with custom background colors.

## Quick Start

Scripts use PEP 723 inline metadata - run with `uv run` and dependencies install automatically.

### Remove Background (Single Image)
```bash
uv run scripts/remove_bg.py photo.png -o transparent.png
```

### Batch Process Multiple Images
```bash
uv run scripts/batch_remove_bg.py photos/ -o output/
```

## Scripts

### remove_bg.py

Remove background from a single image.

```bash
# Basic usage - outputs photo_nobg.png
uv run scripts/remove_bg.py photo.png

# Specify output path
uv run scripts/remove_bg.py photo.jpg -o cutout.png

# Use portrait-optimized model
uv run scripts/remove_bg.py headshot.jpg --model birefnet-portrait

# Output only the mask
uv run scripts/remove_bg.py photo.png --mask-only

# Replace background with white instead of transparent
uv run scripts/remove_bg.py product.png --bgcolor 255,255,255

# Better edge quality (slower)
uv run scripts/remove_bg.py photo.png --alpha-matting
```

### batch_remove_bg.py

Process multiple images at once.

```bash
# Process all images in a folder
uv run scripts/batch_remove_bg.py photos/ -o transparent/

# Process specific files
uv run scripts/batch_remove_bg.py img1.png img2.jpg -o output/

# Use portrait model for headshots
uv run scripts/batch_remove_bg.py headshots/ --model birefnet-portrait -o output/
```

## Available Models

| Model | Best For | Size |
|-------|----------|------|
| `birefnet-general` | General purpose (default) | ~400MB |
| `birefnet-portrait` | Portraits and headshots | ~400MB |
| `isnet-general-use` | General purpose, fast | ~170MB |
| `isnet-anime` | Anime and illustrations | ~170MB |
| `u2net` | General purpose | ~170MB |
| `u2netp` | Fast, lightweight | ~4MB |
| `u2net_human_seg` | Human subjects | ~170MB |
| `silueta` | Lightweight | ~43MB |
| `bria-rmbg` | BRIA AI model | ~170MB |

Models auto-download to `~/.u2net/` on first use.

## Model Selection Guide

- **Portraits/headshots**: Use `--model birefnet-portrait`
- **Product photos**: Use default `birefnet-general`
- **Anime/illustrations**: Use `--model isnet-anime`
- **Fast processing**: Use `--model u2netp` or `--model silueta`
- **Human subjects**: Use `--model u2net_human_seg`

## Output Options

| Option | Description |
|--------|-------------|
| (default) | Transparent PNG |
| `--bgcolor R,G,B` | Solid color background (e.g., `255,255,255` for white) |
| `--mask-only` | Output segmentation mask only |
| `--alpha-matting` | Better edge quality, slower processing |
