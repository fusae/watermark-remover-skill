#!/usr/bin/env python3
"""Run watermark removal via an installed package or auto-install from GitHub."""

import argparse
import importlib.util
import shutil
import subprocess
import sys


DEFAULT_INSTALL_SOURCE = "git+https://github.com/fusae/watermark-remover.git"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Standalone wrapper for the watermark remover CLI."
    )
    parser.add_argument("input", help="Input image or directory path")
    parser.add_argument("output", nargs="?", help="Optional output path or directory")
    parser.add_argument(
        "--corner-ratio",
        type=float,
        default=0.15,
        help="Corner scan ratio passed to the project CLI",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=30,
        help="Detection sensitivity passed to the project CLI",
    )
    parser.add_argument(
        "--padding",
        type=int,
        default=10,
        help="Mask dilation padding passed to the project CLI",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate preview output only",
    )
    parser.add_argument(
        "--no-lama",
        action="store_true",
        help="Use OpenCV inpaint only",
    )
    parser.add_argument(
        "--install-source",
        default=DEFAULT_INSTALL_SOURCE,
        help="Package source used when the CLI is not installed",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Fail instead of auto-installing the package when missing",
    )
    return parser


def cli_available() -> bool:
    return shutil.which("watermark-remover") is not None


def module_available() -> bool:
    return importlib.util.find_spec("watermark_remover") is not None


def ensure_installed(install_source: str, skip_install: bool) -> None:
    if module_available() or cli_available():
        return

    if skip_install:
        raise SystemExit(
            "watermark-remover is not installed. Install it first or rerun without --skip-install."
        )

    print(f"Installing watermark-remover from {install_source} ...", flush=True)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", install_source],
        check=True,
    )

    if not (module_available() or cli_available()):
        raise SystemExit("Installation finished, but watermark-remover is still unavailable.")


def build_command(args: argparse.Namespace) -> list[str]:
    if module_available():
        command = [sys.executable, "-m", "watermark_remover.cli", args.input]
    else:
        command = ["watermark-remover", args.input]

    if args.output:
        command.append(args.output)
    if args.corner_ratio != 0.15:
        command.extend(["--corner-ratio", str(args.corner_ratio)])
    if args.threshold != 30:
        command.extend(["--threshold", str(args.threshold)])
    if args.padding != 10:
        command.extend(["--padding", str(args.padding)])
    if args.preview:
        command.append("--preview")
    if args.no_lama:
        command.append("--no-lama")
    return command


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    ensure_installed(args.install_source, args.skip_install)
    command = build_command(args)
    result = subprocess.run(command)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
