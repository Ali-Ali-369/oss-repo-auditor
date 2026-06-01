from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from oss_repo_auditor.audit import audit_repository


class AuditTests(unittest.TestCase):
    def test_scores_complete_repo_highly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "CONTRIBUTING.md").write_text("Help\n", encoding="utf-8")
            (root / "SECURITY.md").write_text("Report privately\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
            (root / "tests").mkdir()
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / ".github" / "workflows" / "tests.yml").write_text("name: tests\n", encoding="utf-8")

            report = audit_repository(root)

        self.assertEqual(report.grade, "A")

    def test_flags_secret_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("github_pat_fake_token\n", encoding="utf-8")

            report = audit_repository(root)

        secret_check = next(check for check in report.checks if check.name == "Credential markers")
        self.assertEqual(secret_check.status, "fail")


if __name__ == "__main__":
    unittest.main()
