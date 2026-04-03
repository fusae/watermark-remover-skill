# Watermark Remover Skill

Standalone skill for removing corner watermarks from local images with the `watermark-remover` CLI.

This repository only contains the skill itself. The underlying tool is installed on demand from the main project repository:

- Project repo: [fusae/watermark-remover](https://github.com/fusae/watermark-remover)
- Skill repo: [fusae/watermark-remover-skill](https://github.com/fusae/watermark-remover-skill)

## Structure

```text
watermark-remover/
  SKILL.md
  agents/openai.yaml
  scripts/run_watermark_remover.py
```

## What It Does

- Removes corner watermarks from a single local image
- Processes a local directory in batch
- Supports preview mode before cleanup
- Supports detection tuning with `corner-ratio`, `threshold`, and `padding`
- Falls back to OpenCV mode with `--no-lama`

## Usage

Single image:

```bash
python3 watermark-remover/scripts/run_watermark_remover.py /abs/path/image.jpg
```

Batch directory:

```bash
python3 watermark-remover/scripts/run_watermark_remover.py /abs/path/photos /abs/path/output-dir
```

Preview only:

```bash
python3 watermark-remover/scripts/run_watermark_remover.py /abs/path/photos --preview
```

Disable LaMa:

```bash
python3 watermark-remover/scripts/run_watermark_remover.py /abs/path/photos --no-lama
```

Custom install source:

```bash
python3 watermark-remover/scripts/run_watermark_remover.py /abs/path/photos --install-source git+https://github.com/fusae/watermark-remover.git
```

## Installation Behavior

The wrapper script checks whether `watermark-remover` is already installed.

- If installed, it runs the CLI directly.
- If not installed, it installs the package from GitHub on first use.
- If automatic installation is not allowed, use `--skip-install` to fail fast instead.

## Notes

- This skill is designed for corner watermarks, not center overlays.
- Inputs must be local filesystem paths.
- First-run installation may take longer because it installs Python dependencies.
