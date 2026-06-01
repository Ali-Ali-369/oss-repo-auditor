from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from oss_repo_auditor.audit import audit_repository
from oss_repo_auditor.report import render_markdown


class ReportTests(unittest.TestCase):
    def test_markdown_contains_score_and_checks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            report = audit_repository(root)

        rendered = render_markdown(report)

        self.assertIn("# OSS Repo Audit", rendered)
        self.assertIn("- Score:", rendered)
        self.assertIn("README", rendered)


if __name__ == "__main__":
    unittest.main()
