#!/usr/bin/env python3
"""Normalize Project Harness Markdown and calculate a stable SHA-256 digest."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path


def normalize_markdown(markdown: str) -> str:
    """Use LF line endings and exactly one trailing newline."""
    return markdown.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n"


def markdown_sha256(markdown: str) -> str:
    """Return the SHA-256 of normalized UTF-8 Markdown."""
    normalized = normalize_markdown(markdown)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize UTF-8 Markdown and print or verify its SHA-256."
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        help="UTF-8 Markdown file; read standard input when omitted.",
    )
    parser.add_argument(
        "--print-normalized",
        action="store_true",
        help="Print normalized Markdown instead of its digest.",
    )
    parser.add_argument(
        "--expect",
        help="Exit with status 1 unless the digest equals this SHA-256.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    markdown = args.path.read_text(encoding="utf-8") if args.path else sys.stdin.read()
    normalized = normalize_markdown(markdown)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    if args.print_normalized:
        sys.stdout.write(normalized)
        return 0

    print(digest)
    return 0 if args.expect is None or digest == args.expect.lower() else 1


if __name__ == "__main__":
    raise SystemExit(main())
