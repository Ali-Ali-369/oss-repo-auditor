from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path

from oss_repo_auditor.cli import main


class CliTests(unittest.TestCase):
    def test_fail_under_returns_two_when_score_is_low(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")

            exit_code = main([str(root), "--fail-under", "90"], io.StringIO())

        self.assertEqual(exit_code, 2)

    def test_fail_under_returns_zero_when_score_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")

            exit_code = main([str(root), "--fail-under", "1"], io.StringIO())

        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
