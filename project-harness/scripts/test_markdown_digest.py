#!/usr/bin/env python3
"""Executable Project Harness tests for markdown_digest.py."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

from markdown_digest import markdown_sha256, normalize_markdown


SCRIPT = Path(__file__).with_name("markdown_digest.py")


class NormalizeMarkdownTests(unittest.TestCase):
    def test_normalizes_line_endings_and_trailing_newlines(self) -> None:
        self.assertEqual(normalize_markdown("a\r\nb\r\n\r\n"), "a\nb\n")
        self.assertEqual(normalize_markdown("a\rb"), "a\nb\n")

    def test_empty_markdown_has_one_newline(self) -> None:
        self.assertEqual(normalize_markdown(""), "\n")

    def test_digest_uses_normalized_utf8(self) -> None:
        expected = hashlib.sha256("你好\n".encode()).hexdigest()
        self.assertEqual(markdown_sha256("你好\r\n\r\n"), expected)


class MarkdownDigestCliTests(unittest.TestCase):
    def run_cli(self, *args: str, stdin: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            input=stdin,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_expect_success_and_failure(self) -> None:
        expected = markdown_sha256("body")
        success = self.run_cli("--expect", expected, stdin="body\r\n")
        failure = self.run_cli("--expect", "0" * 64, stdin="body")
        self.assertEqual(success.returncode, 0)
        self.assertEqual(success.stdout.strip(), expected)
        self.assertEqual(failure.returncode, 1)
        self.assertEqual(failure.stdout.strip(), expected)

    def test_print_normalized(self) -> None:
        result = self.run_cli("--print-normalized", stdin="a\r\nb\n\n")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "a\nb\n")


if __name__ == "__main__":
    unittest.main()
