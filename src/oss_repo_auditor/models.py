from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    detail: str
    weight: int


@dataclass(frozen=True)
class AuditReport:
    path: str
    score: int
    grade: str
    checks: tuple[CheckResult, ...]
