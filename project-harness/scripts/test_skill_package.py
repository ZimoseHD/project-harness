"""Check shipped resource links; these tests are not delivery prerequisites."""

from __future__ import annotations

import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


HARNESS = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")


def local_targets(document: Path) -> set[Path]:
    targets = set()
    for destination in LINK.findall(document.read_text(encoding="utf-8")):
        parsed = urlsplit(destination)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        targets.add((document.parent / unquote(parsed.path)).resolve())
    return targets


class SkillPackageTests(unittest.TestCase):
    def test_local_links_resolve_inside_the_distributed_skill(self) -> None:
        for document in HARNESS.rglob("*.md"):
            for target in local_targets(document):
                with self.subTest(document=document, target=target):
                    self.assertTrue(target.is_relative_to(HARNESS), target)
                    self.assertTrue(target.is_file(), target)

    def test_every_reference_is_reachable_from_the_entrypoint(self) -> None:
        pending = [HARNESS / "SKILL.md"]
        visited = set()
        while pending:
            document = pending.pop()
            if document in visited:
                continue
            visited.add(document)
            if document.suffix == ".md" and document.is_file():
                pending.extend(local_targets(document) - visited)
        references = set((HARNESS / "references").rglob("*.md"))
        self.assertEqual(references - visited, set(), "Unreachable references")


if __name__ == "__main__":
    unittest.main()
