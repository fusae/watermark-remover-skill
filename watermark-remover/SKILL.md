---
name: watermark-remover
description: Use this skill when the user wants to remove corner watermarks from local images or image folders with a standalone CLI workflow. It supports single-image and batch directory processing, preview mask generation, parameter tuning, and first-run installation from the GitHub repository when the package is not already installed.
---

# Watermark Remover

## Overview

This skill removes corner watermarks from local images with a standalone CLI wrapper.

It does not depend on a local copy of the source repository. If `watermark-remover` is missing, the wrapper installs it from GitHub on first use.

## When To Use

- The user wants to remove watermarks from one or more local images.
- The user provides a directory and wants batch processing.
- The user wants to preview detected watermark regions before cleanup.
- The user needs parameter tuning for false positives or missed detections.

## Workflow

1. Confirm the input is a local image file or a directory of images.
2. If the request is uncertain, start with preview mode.
3. Run `scripts/run_watermark_remover.py`.
4. Report the output path and whether the run used preview mode, LaMa, or OpenCV fallback mode.

## Commands

Single image:

```bash
python3 scripts/run_watermark_remover.py /abs/path/image.jpg
```

Batch directory:

```bash
python3 scripts/run_watermark_remover.py /abs/path/photos /abs/path/output-dir
```

Preview only:

```bash
python3 scripts/run_watermark_remover.py /abs/path/photos --preview
```

Disable LaMa:

```bash
python3 scripts/run_watermark_remover.py /abs/path/photos --no-lama
```

Tune detection:

```bash
python3 scripts/run_watermark_remover.py /abs/path/photos --corner-ratio 0.2 --threshold 20 --padding 12
```

Use a custom install source:

```bash
python3 scripts/run_watermark_remover.py /abs/path/photos --install-source git+https://github.com/fusae/watermark-remover.git
```

## Parameter Guidance

- `--corner-ratio`: Increase when the watermark sits farther from the corner or is physically larger.
- `--threshold`: Lower it when the detector misses faint watermarks; raise it when it over-detects textures.
- `--padding`: Increase it when cleanup leaves watermark edges behind.
- `--preview`: Preferred first step for uncertain inputs or large batches.
- `--no-lama`: Faster, but lower quality than the default LaMa path.
- `--skip-install`: Use this when automatic network installs are not allowed.

## Constraints

- This workflow is designed for corner watermarks, not center overlays or full-image marks.
- Inputs must be local filesystem paths.
- The first run may install dependencies from GitHub and can take longer.
- Network access is required if the package is not already installed and automatic install is allowed.

## Resource

### scripts/run_watermark_remover.py

Use this wrapper instead of rebuilding CLI commands manually. It runs the installed package when available and installs from GitHub on demand when needed.
