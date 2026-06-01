from __future__ import annotations

from pathlib import Path

from .models import AuditReport, CheckResult

SECRET_MARKERS = (
    "github_pat_",
    "ghp_",
    "sk-",
    "-----BEGIN PRIVATE KEY-----",
    "aws_secret_access_key",
)
GENERATED_DIRS = {".git", "__pycache__", ".venv", "node_modules", "dist", "build", ".mypy_cache"}


def audit_repository(path: Path) -> AuditReport:
    root = path.resolve()
    checks = (
        _required_file(root, "README", ("README.md", "README.rst", "README.txt"), 15),
        _required_file(root, "License", ("LICENSE", "LICENSE.md", "COPYING"), 15),
        _required_file(root, "Contributing guide", ("CONTRIBUTING.md", ".github/CONTRIBUTING.md"), 10),
        _required_file(root, "Security policy", ("SECURITY.md", ".github/SECURITY.md"), 10),
        _ci_check(root),
        _tests_check(root),
        _metadata_check(root),
        _secret_marker_check(root),
        _oversized_file_check(root),
    )
    possible = sum(check.weight for check in checks)
    earned = sum(check.weight for check in checks if check.status == "pass")
    score = round((earned / possible) * 100) if possible else 0
    return AuditReport(path=str(root), score=score, grade=_grade(score), checks=checks)


def _required_file(root: Path, name: str, candidates: tuple[str, ...], weight: int) -> CheckResult:
    for candidate in candidates:
        if (root / candidate).exists():
            return CheckResult(name, "pass", f"found {candidate}", weight)
    return CheckResult(name, "fail", f"missing one of: {', '.join(candidates)}", weight)


def _ci_check(root: Path) -> CheckResult:
    workflows = root / ".github" / "workflows"
    if workflows.exists() and any(path.suffix in {".yml", ".yaml"} for path in workflows.iterdir()):
        return CheckResult("CI workflow", "pass", "found GitHub Actions workflow", 10)
    return CheckResult("CI workflow", "fail", "missing .github/workflows/*.yml", 10)


def _tests_check(root: Path) -> CheckResult:
    if any((root / name).exists() for name in ("tests", "test", "__tests__")):
        return CheckResult("Tests", "pass", "found test directory", 10)
    return CheckResult("Tests", "fail", "missing test directory", 10)


def _metadata_check(root: Path) -> CheckResult:
    candidates = ("pyproject.toml", "package.json", "Cargo.toml", "go.mod", "Gemfile")
    for candidate in candidates:
        if (root / candidate).exists():
            return CheckResult("Package metadata", "pass", f"found {candidate}", 10)
    return CheckResult("Package metadata", "fail", "missing known package metadata", 10)


def _secret_marker_check(root: Path) -> CheckResult:
    suspicious: list[str] = []
    for path in _iter_text_files(root):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            continue
        if any(marker.lower() in text for marker in SECRET_MARKERS):
            suspicious.append(str(path.relative_to(root)))

    if suspicious:
        return CheckResult("Credential markers", "fail", f"review possible secrets: {', '.join(suspicious[:5])}", 15)
    return CheckResult("Credential markers", "pass", "no common token markers found", 15)


def _oversized_file_check(root: Path) -> CheckResult:
    large_files: list[str] = []
    for path in _iter_files(root):
        try:
            if path.stat().st_size > 1_000_000:
                large_files.append(str(path.relative_to(root)))
        except OSError:
            continue
    if large_files:
        return CheckResult("Large files", "fail", f"review large files: {', '.join(large_files[:5])}", 5)
    return CheckResult("Large files", "pass", "no files over 1 MB found", 5)


def _iter_text_files(root: Path):
    for path in _iter_files(root):
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".zip"}:
            continue
        yield path


def _iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in GENERATED_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def _grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
